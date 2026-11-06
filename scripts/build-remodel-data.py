#!/usr/bin/env python3
"""Build FEM-v1 public charts from an explicitly supplied private model directory.

Only public numerical schedule data and allowlisted evidence hashes are exported.
No private receipt or page is written. Run with PYTHONDONTWRITEBYTECODE=1.
"""
import argparse
import bisect
import copy
import csv
import gzip
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import sys

sys.dont_write_bytecode = True
SITE = Path(__file__).resolve().parents[1]
MODEL_SHA = 'bb9af4dc679b35b7b190876e6ae2a0a641ee1bf6811a8ad8472496db1c1ec3a0'
PARAMETERS_SHA = '74f7f8681077a36be4572351116ddd06ff76655a988c5ef4a93b908e04c1f61e'


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--model-dir', required=True, type=Path)
    args = parser.parse_args()
    directory = args.model_dir.resolve()
    assert sha(directory/'model.py') == MODEL_SHA, 'Unselected model'
    assert sha(directory/'parameters.json') == PARAMETERS_SHA, 'Unselected parameters'
    spec = importlib.util.spec_from_file_location('fem_reference', directory/'model.py')
    model = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = model
    spec.loader.exec_module(model)
    # Adoption can change the old source checkout: use the selected, pinned
    # full epoch exports instead of suppressing model.load()'s drift checks.
    binding = json.loads((directory/'parameters.json').read_text())
    texts = {}
    for source in binding['sources']:
        if source['file'].startswith(('daarx/', 'crates/nxxxs-core/')):
            path = Path(source['path'])
            assert sha(path) == source['sha256'], 'Unchanged source drift'
            texts[source['file']] = path.read_text()
    dp = texts['daarx/src/params.rs']
    dt = texts['daarx/src/emission_table.rs']
    blocks = model.const(dp, 'BLOCKS_PER_EPOCH')
    allocations = [int(v) for v in re.findall(r'\b\d+\b',dt.split('= [',1)[1].split('];',1)[0])]
    rewards = [v//blocks for v in allocations]
    daarx = model.Schedule('DAARX',12,111,[(blocks-1,(blocks-1)*rewards[0])]+[(blocks,blocks*r) for r in rewards[1:]])
    np = texts['crates/nxxxs-core/src/params.rs']
    ramp = model.const(np,'RAMP_EPOCHS')
    rewards = [model.const(np,'PEAK_REWARD')*(i+1)//ramp for i in range(ramp)]
    tail = model.const(np,'TAIL_REWARD')
    while rewards[-1] > tail:
        rewards.append(max(tail,rewards[-1]*model.const(np,'DECLINE_NUMERATOR')//model.const(np,'DECLINE_DENOMINATOR')))
    nexus = model.Schedule('NXXXS',9,30,[(2880,2880*r) for r in rewards[:-1]],tail=tail)
    selected = {'daarx':daarx,'nexus':nexus}
    export_hashes = {'l10n':'be08f2b8097490cd3d4da963bf6daa2c8bbaca1d8bccbf51004689583cf49588',
                     'open':'3b539b9e5ec2c647c1e7b939c6685d67810bd21d22c52717fa139c892d0a029d'}
    for ident,expected_sha in export_hashes.items():
        path = directory/(ident+'-candidate-epochs.csv.gz')
        assert sha(path) == expected_sha, 'Selected epoch export drift'
        segments = []
        baseline = 10**12 if ident == 'l10n' else 0
        total = end = 0
        with gzip.open(path,'rt') as stream:
            for i,row in enumerate(csv.DictReader(stream),1):
                count = int(row['paid_blocks'])
                amount = int(row['finite_allocation_base_units'])
                q,r = divmod(amount,count)
                assert int(row['epoch_1based']) == i
                assert int(row['first_height']) == end+1
                assert int(row['finite_reward_floor_base_units']) == q
                assert int(row['prefix_blocks_with_one_extra_atom']) == r
                assert int(row['permanent_baseline_base_units']) == baseline
                total += amount; end += count
                assert int(row['finite_cumulative_base_units']) == total
                segments.append((count,amount))
        selected[ident] = model.Schedule(ident.upper(),12 if ident=='l10n' else 9,
                                         30 if ident=='l10n' else 27,segments,baseline=baseline)
    selected = {k:selected[k] for k in ('daarx','l10n','open','nexus')}
    steps = json.loads((SITE/'data/emission-steps.json').read_text())
    study = json.loads((SITE/'data/emission-study.json').read_text())
    previous_sources = {s['file']: s['sha256'] for s in steps['sources']}
    for source in binding['sources']:
        assert previous_sources[source['file']] == source['sha256'], 'Retained binding drift'
    evidence = [{'file': s['file'], 'sha256': s['sha256']} for s in binding['sources']]
    evidence += [{'file': k+'-candidate-epochs.csv.gz', 'sha256': v} for k,v in export_hashes.items()]
    evidence += [{'file': 'model.py', 'sha256': MODEL_SHA},
                 {'file': 'parameters.json', 'sha256': PARAMETERS_SHA}]
    steps['sources'] = evidence
    steps['model_id'] = study['model_id'] = 'FEM-20261106-v1'
    status = 'Selected economic reference model; consensus integration and activation pending.'
    steps['model_status'] = study['model_status'] = status
    study['meaning'] = ('Scheduled gross block reward at floor-height for each target year '
                        '(31,557,600 seconds/year). Native units per block; exact reward-change '
                        'steps include within-epoch quotient/remainder transitions. Genesis pays zero. '+status)
    summary = {}
    for ident, m in selected.items():
        c = copy.deepcopy(steps['coins'][ident])
        scale = 10**m.decimals
        units = lambda value: model.units(value, m.decimals)
        year = lambda height: Fraction(height*m.spacing, model.YEAR)
        sample = lambda t: {'year': float(Fraction(t)), 'height': m.height(t),
                            'base_units': str(m.reward(m.height(t))), 'reward': units(m.reward(m.height(t)))}
        peak = m.peak()
        if ident in ('daarx', 'nexus'):
            for i, actual in enumerate(study['coins'][ident]['rewards']):
                # JSON numbers carry browser precision; compare canonical numeric conversion.
                assert float(actual) == float(Fraction(m.reward(m.height(Fraction(i,100))), scale))
            for t, reward in c['vertices']:
                assert 0 <= Decimal(reward) <= Decimal(peak['reward'])
            assert c['peak']['base_units'] == peak['base_units']
        limit = m.height(25)
        heights = {1}
        for i, (count, amount) in enumerate(m.segments):
            start = m.ends[i]+1
            if start > limit:
                break
            heights.add(start)
            _, remainder = divmod(amount, count)
            if remainder and start+remainder <= limit:
                heights.add(start+remainder)
        if m.ends[-1]+1 <= limit:
            heights.add(m.ends[-1]+1)
        events = [h for h in sorted(heights) if m.reward(h-1) != m.reward(h)]
        vertices = [(Fraction(0), 0, 0)]
        for h in events:
            vertices.extend([(year(h),0,m.reward(h-1)), (year(h),1,m.reward(h))])
        c['samples'] = {t: sample(t) for t in ('0','0.01','0.05','7.77','25')}
        for t,s in c['samples'].items():
            if t != '0':
                vertices.append((Fraction(t),2,int(s['base_units'])))
        vertices.sort(key=lambda v: (v[0],v[1]))
        c['vertices'] = [[float(t), units(r)] for t,_,r in vertices]
        peak = m.peak()
        h, end = peak['first_height'], peak['last_height']
        c['peak'] = {'reward': peak['reward'], 'base_units': peak['base_units'],
                     'epoch': bisect.bisect_right(m.ends,h-1)-1, 'height': h,
                     'year': float(year(h)), 'year_decimal': str(Decimal(h*m.spacing)/model.YEAR),
                     'end_height': end, 'end_year': float(year(end))}
        c['first_positive_height'] = next(h for h in events if m.reward(h)>0)
        c['epoch_height_offset'] = 0 if ident == 'daarx' else 1
        c['axis_max'] = {'daarx':1000000,'l10n':20,'open':80000,'nexus':10}[ident]
        c['candidate'] = ident != 'daarx'
        c['tail'] = None
        tail = m.baseline or m.tail
        if tail:
            # Find the first height of the final constant run, including zero
            # bonus segments and partial remainder epochs before schedule end.
            tail_height = m.ends[-1]+1
            for i in range(len(m.segments)-1,-1,-1):
                count, amount = m.segments[i]
                q,r = divmod(amount,count)
                if q+m.baseline != tail:
                    break
                tail_height = m.ends[i]+r+1
                if r:
                    break
            assert m.reward(tail_height) == tail
            assert m.reward(tail_height-1) != tail
            c['tail'] = {'reward':units(tail),'base_units':str(tail),
                         'epoch':bisect.bisect_right(m.ends,tail_height-1)-1,
                         'height':tail_height,'year':float(year(tail_height)),
                         'year_decimal':str(Decimal(tail_height*m.spacing)/model.YEAR)}
        c['finite_component_end_height'] = m.ends[-1]
        c['permanent_baseline'] = units(m.baseline)
        c['model_id'] = 'FEM-20261106-v1'
        # Validate the entire displayed grid using a separate direct segment lookup,
        # rather than the reference's cumulative-total difference implementation.
        rewards = []
        base_units = []
        times = [v[0] for v in vertices]
        for i in range(2501):
            t = Fraction(i,100)
            h = m.height(t)
            j = bisect.bisect_right(m.ends,h-1)-1 if h else -1
            if not h:
                expected = 0
            elif j >= len(m.segments):
                expected = m.baseline+m.tail
            else:
                count,amount = m.segments[j]
                q,r = divmod(amount,count)
                expected = m.baseline+q+int(h-m.ends[j]<=r)
            actual = m.reward(h)
            assert actual == expected
            k = bisect.bisect_right(times,t)-1
            assert vertices[k][2] == expected, (ident,i,'geometry mismatch')
            rewards.append(float(Fraction(actual,scale)))
            base_units.append(str(actual))
            assert rewards[-1] == float(Decimal(units(expected)))
        assert max(v[2] for v in vertices) == int(peak['base_units'])
        assert Decimal(peak['reward']) <= c['axis_max']
        steps['coins'][ident] = c
        study['coins'][ident] = {'rewards':rewards, 'peak':float(peak['reward']), 'reward_base_units':base_units}
        summary[ident] = {'events':len(events),'vertices':len(vertices),'readouts_verified':2501,
                          'peak':peak['reward'],'tail':c['tail']}
    assert selected['l10n'].prefix[-1] == int(binding['l10n_bonus_budget_base_units'])
    assert selected['open'].prefix[-1] == int(binding['open_lifetime_budget_base_units'])
    for name,data in [('emission-steps.json',steps),('emission-study.json',study)]:
        payload = json.dumps(data,separators=(',',':'),ensure_ascii=False)+'\n'
        assert not re.search(r'/(?:home|tmp|Users)/',payload)
        (SITE/'data'/name).write_text(payload)
    spec = importlib.util.spec_from_file_location('site_charts',SITE/'scripts/charts.py')
    charts = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(charts)
    charts.build_assets(SITE)
    print(json.dumps({'status':'PASS','model_id':'FEM-20261106-v1','coins':summary,
                      'readouts_verified':10004,'unchanged_source_files_verified':len(texts),'selected_exports_verified':len(export_hashes)}))


if __name__ == '__main__':
    with localcontext() as context:
        context.prec = 45
        main()
