"""Exact schedule steps with native-unit axes shared by plots and readouts."""
from pathlib import Path
from decimal import Decimal
import html,json,hashlib
ROOT=Path(__file__).resolve().parents[1]
def versioned(path):
    return path+'?v='+hashlib.sha256((ROOT/path.lstrip('/')).read_bytes()).hexdigest()[:12]
X0,X1,Y0,Y1=56,960,20,190
COLORS={'daarx':'#8bffc0','l10n':'#ffdb90','open':'#94efff','nexus':'#d6b4ff'}
def esc(x):return html.escape(str(x),quote=True)
def compact(x):
    d=Decimal(str(x));return format(d,'f').rstrip('0').rstrip('.') if '.' in format(d,'f') else format(d,'f')
def number(x):
    d=Decimal(str(x));places=12 if 0<d<Decimal('.000001') else 6 if abs(d)<1 else 3
    return f'{d:,.{places}f}'.rstrip('0').rstrip('.') if places else f'{d:,}'
def schedules(root):return json.loads((root/'data/emission-steps.json').read_text())['coins']
def coordinates(year,reward,upper):
    return Decimal(X0)+Decimal(str(year))/25*(X1-X0),Decimal(Y1)-Decimal(str(reward))/Decimal(str(upper))*(Y1-Y0)
def coord(x):return format(x.quantize(Decimal('.0000000001')),'f').rstrip('0').rstrip('.')
def build_assets(root):
    out=root/'assets/charts';out.mkdir(exist_ok=True)
    for ident,c in schedules(root).items():
        upper=c['axis_max'];parts=[]
        for i,(year,reward) in enumerate(c['vertices']):
            x,y=coordinates(year,reward,upper);parts.append(('M' if i==0 else 'L')+coord(x)+' '+coord(y))
        meta={k:c.get(k)for k in ['unit','axis_max','peak','tail','samples','model_id','permanent_baseline','finite_component_end_height']};meta.update(coin=ident,years=25,source_vertices=len(parts),plot={'x0':X0,'x1':X1,'y0':Y0,'y1':Y1})
        grid='<path d="M56 20H960M56 105H960M56 190H960M56 20V190M236.8 20V190M417.6 20V190M598.4 20V190M779.2 20V190M960 20V190" fill="none" stroke="#aecfbb" stroke-opacity=".28" stroke-width="1"/>'
        svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 220" preserveAspectRatio="none"><metadata id="schedule-metadata">'+html.escape(json.dumps(meta,separators=(',',':')))+ '</metadata>'+grid+'<path id="schedule-path" data-coin="'+ident+'" data-ymax="'+str(upper)+'" d="'+''.join(parts)+'" fill="none" stroke="'+COLORS[ident]+'" stroke-width="2.5" vector-effect="non-scaling-stroke" stroke-linejoin="miter"/></svg>'
        (out/(ident+'-issuance.svg')).write_text(svg+'\n')
def plot(ident,c,coin,marker='schedule',year=7.77,reward=None):
    upper=c['axis_max'];unit=c['unit'];value=c['samples']['7.77']['reward'] if reward is None else reward
    x,y=coordinates(year,value,upper)
    attrs=' data-schedule-plot="'+ident+'" data-ymax="'+str(upper)+'" data-unit="'+unit+'"'
    marker_attrs=('data-schedule-marker="'+ident+'"' if marker=='schedule' else 'class="supply-marker"')
    chart='<div class="schedule-plot"'+attrs+'><img class="schedule-image" src="'+versioned('/assets/charts/'+ident+'-issuance.svg')+'" width="1000" height="220" loading="lazy" decoding="async" alt="'+coin+' scheduled block reward during the first 25 target years, in '+unit+' per block, with exact reward-change steps and a linear native-unit scale."><svg class="emission-chart schedule-overlay" viewBox="0 0 1000 220" preserveAspectRatio="none" aria-hidden="true"><line data-schedule-cursor="'+ident+'" x1="'+coord(x)+'" x2="'+coord(x)+'" y1="20" y2="190"/><circle '+marker_attrs+' cx="'+coord(x)+'" cy="'+coord(y)+'" r="4"/></svg><div class="schedule-axis-y" aria-hidden="true">'+''.join('<span class="schedule-y" data-value="'+str(v)+'" style="top:'+str(pos/220*100)+'%">'+number(v)+'</span>'for v,pos in [(upper,Y0),(Decimal(str(upper))/2,105),(0,Y1)])+'</div><div class="schedule-axis-x" aria-hidden="true">'+''.join('<span style="left:calc(74px + (100% - 74px) * '+str((56+y/25*904)/1000)+')">'+str(y)+'</span>'for y in [0,5,10,15,20,25])+'</div></div>'
    return chart

def issuance_study(coins,root):
    data=schedules(root);cards=[];readouts=[]
    for coin in coins:
        ident=coin['id'];c=data[ident];unit=c['unit'];candidate=' · reference candidate' if c['candidate'] else ''
        tail=c.get('tail');annotation={'daarx':'Finite issuance continues beyond this 25-year view, ending around year 100.','open':'Reward rises toward year 7.77, then declines beyond this view; finite issuance with no permanent tail.'}.get(ident,'')
        if ident == 'l10n':
            annotation='1 L10N / block baseline from height 1; a finite bonus rises toward year 7.77 and ends at target year 77.7.'
        elif tail:
            annotation='Permanent tail: '+number(tail['reward'])+' '+unit+' / block from target year '+f"{tail['year']:.4f}"+'.'
        cards.append('<article class="schedule-card '+coin['color']+'"><h3><a href="'+coin['path']+'#issuance">'+coin['unit']+' <span aria-hidden="true">↗</span></a><small>'+unit+' / block'+candidate+'</small></h3>'+plot(ident,c,coin['unit'])+'<p class="schedule-context">'+annotation+'</p></article>')
        value=c['samples']['7.77']['reward']
        readouts.append('<div class="'+coin['color']+'"><a class="reward-link" id="reward-name-'+ident+'" href="'+coin['path']+'#issuance">'+coin['unit']+' ↗</a><output for="time-range" aria-live="off" aria-labelledby="reward-name-'+ident+' reward-unit-'+ident+'" data-reward="'+ident+'">'+number(value)+'</output><small id="reward-unit-'+ident+'">'+unit+' / block</small></div>')
    return '<section class="network-section issuance-section" id="supply"><div class="network-shell"><div class="emission-heading"><div><p class="eyebrow">THE MONETARY DESIGN</p><h2>The shape<br><em>of issuance.</em></h2></div><p>Four native-unit scales. The same 25-year window.<br>Choose a year; the markers and rewards follow the exact schedule.</p></div><div class="emission-instrument" data-emission data-src="'+versioned('/data/emission-study.json')+'"><div class="instrument-top"><span>SCHEDULED ISSUANCE / NEW COINS PER BLOCK</span><span>FIRST 25 TARGET YEARS · LINEAR AXES</span></div><div class="schedule-grid">'+''.join(cards)+'</div><div class="time-control"><div class="time-label"><label for="time-range">Explore a target year</label><output id="time-output" for="time-range" aria-live="off">7.77</output></div><input id="time-range" type="range" min="0.01" max="25" value="7.77" step="0.01" aria-valuetext="7.77 target years" disabled><span>25 years →</span></div><div class="reward-readouts">'+''.join(readouts)+'</div><p class="sr-only" data-schedule-announcement role="status" aria-live="polite" aria-atomic="true"></p><p class="instrument-note">Gross new issuance per block, before allocation and excluding transaction fees. This is not total supply or price. Each chart labels its own native-unit y-axis. One target year is 31,557,600 seconds at the stated block target. FEM-20261106-v1 selected model; consensus integration and activation pending. <a href="/data/emission-steps.json">Exact schedule data ↗</a></p><noscript><p class="instrument-note">Showing the year 7.77 snapshot.</p></noscript></div></div></section>'
def coin_curve(coin,root):
    c=schedules(root)[coin['id']];marks=[]
    for year in ['0.01','7.77','25']:
        m=c['samples'][year];x,y=coordinates(year,m['reward'],c['axis_max']);marks.append({'year':float(year),'value':m['reward'],'x':float(x),'y':float(y)})
    return '<div class="coin-supply-curve" data-coin-curve data-ymax="'+str(c['axis_max'])+'" data-unit="'+c['unit']+'" data-curve-points="'+esc(json.dumps(marks))+'"><p>GROSS ISSUANCE / FIRST 25 TARGET YEARS / '+c['unit']+' PER BLOCK</p>'+plot(coin['id'],c,coin['unit'],'supply')+'<div class="supply-readout"><div><output data-curve-reward aria-live="polite">'+number(marks[1]['value'])+'</output><small> '+c['unit']+' / block</small></div><div class="supply-years" role="group" aria-label="Explore '+coin['unit']+' block rewards">'+''.join('<button type="button" data-curve-step="'+str(i)+'" aria-pressed="'+str(i==1).lower()+'">Year '+str(m['year']).removesuffix('.0')+'</button>'for i,m in enumerate(marks))+'</div></div></div>'
