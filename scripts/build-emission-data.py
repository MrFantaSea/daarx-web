#!/usr/bin/env python3
"""Build exact height-derived step geometry using Python's standard library.

This reads retained source artifacts; it never imports or executes protocol code.
Paths are explicit CLI inputs and appear only in the private arithmetic receipt.
The public JSON is deterministic and contains no machine-specific absolute paths.
"""
from argparse import ArgumentParser
import csv
from decimal import Decimal, localcontext
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import re

YEAR_SECONDS = 31_557_600
LAST_YEAR = Fraction(25)
SAMPLE_YEARS = ("0", "0.01", "0.05", "7.77", "25")
SITE = Path(__file__).resolve().parents[1]


def digest(data):
    return hashlib.sha256(data).hexdigest()


def decimal_units(base_units, decimals):
    whole, fraction = divmod(base_units, 10 ** decimals)
    suffix = f"{fraction:0{decimals}d}".rstrip("0")
    return str(whole) + ("." + suffix if suffix else "")


def decimal_year(height, spacing):
    with localcontext() as context:
        context.prec = 45
        return str(Decimal(height * spacing) / Decimal(YEAR_SECONDS))


def constant(text, name):
    match = re.search(r"pub const " + re.escape(name) + r"\s*:[^=;]+?=\s*([0-9_]+)\s*;", text)
    if not match:
        raise ValueError("Missing literal source constant: " + name)
    return int(match[1].replace("_", ""))


def candidate_field(text, name):
    body = text.split("pub const fn candidate()", 1)[1].split("\n    }", 1)[0]
    match = re.search(r"\b" + re.escape(name) + r"\s*:\s*([^,]+),", body)
    if not match:
        raise ValueError("Missing candidate field: " + name)
    return match[1].strip()


def candidate_integer(text, name):
    value = candidate_field(text, name)
    if not re.fullmatch(r"[0-9_]+", value):
        raise ValueError("Expected integer candidate field: " + name)
    return int(value.replace("_", ""))


class Model:
    def __init__(self, unit, decimals, spacing, blocks, offset, rewards, axis, candidate, tail=None):
        self.unit, self.decimals, self.spacing = unit, decimals, spacing
        self.blocks, self.offset, self.rewards = blocks, offset, rewards
        self.axis, self.candidate, self.tail = axis, candidate, tail

    def reward(self, height):
        if height == 0:
            return 0
        epoch = (height - self.offset) // self.blocks
        return self.rewards[epoch] if epoch < len(self.rewards) else (self.tail or 0)

    def year(self, height):
        return Fraction(height * self.spacing, YEAR_SECONDS)

    def first_height(self, epoch):
        return max(1, epoch * self.blocks + self.offset)

    def sample(self, year):
        target = Fraction(year)
        height = int(target * YEAR_SECONDS / self.spacing)
        base = self.reward(height)
        return {"year": float(target), "height": height, "base_units": str(base),
                "reward": decimal_units(base, self.decimals)}


def main():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--family-source", required=True, type=Path,
                        help="Retained source root containing daarx, l10n-core and open-core")
    parser.add_argument("--nxxxs-source", required=True, type=Path)
    parser.add_argument("--nxxxs-parameters", required=True, type=Path)
    parser.add_argument("--as-of", default="2026-11-06")
    args = parser.parse_args()
    public_sources, private_sources = [], []

    def read(root, relative, label):
        path = (root / relative).resolve()
        data = path.read_bytes()
        public = {"label": label, "file": relative, "sha256": digest(data), "bytes": len(data)}
        public_sources.append(public)
        private_sources.append({**public, "path": str(path)})
        return data.decode("utf-8")

    family, nexus = args.family_source.resolve(), args.nxxxs_source.resolve()
    dp = read(family, "daarx/src/params.rs", "DAARX retained parameters")
    dt = read(family, "daarx/src/emission_table.rs", "DAARX frozen integer epoch allocations")
    read(family, "daarx/src/emission.rs", "DAARX height-to-reward convention")
    allocations = [int(value) for value in re.findall(r"\b\d+\b", dt.split("= [", 1)[1].split("];", 1)[0])]
    assert len(allocations) == 36_589
    assert sum(allocations) == 5_083_000_000_000_000_000_000_000
    db = constant(dp, "BLOCKS_PER_EPOCH")
    daarx = Model("DIAM", constant(dp, "DECIMALS"), constant(dp, "BLOCK_TIME_SECONDS"),
                  db, 0, [value // db for value in allocations], 1_000_000, False)

    lp = read(family, "l10n-core/src/params.rs", "L10N numeric reference candidate")
    lc = read(family, "l10n-core/src/chain_params.rs", "L10N candidate report spacing")
    read(family, "l10n-core/src/schedule.rs", "L10N integer declining-to-tail recurrence")
    read(family, "l10n-core/src/genesis.rs", "L10N zero-emission genesis override")
    assert candidate_field(lp, "initial_block_reward") == "50 * ONE_L10N"
    assert candidate_field(lp, "tail_block_reward") == "ONE_L10N"
    one_lion = constant(lp, "ONE_L10N")
    lion_num, lion_den = candidate_integer(lp, "decay_num"), candidate_integer(lp, "decay_den")
    lion_rewards = [50 * one_lion]
    while lion_rewards[-1] > one_lion:
        lion_rewards.append(max(one_lion, lion_rewards[-1] * lion_num // lion_den))
    lion_blocks = candidate_integer(lp, "blocks_per_epoch")
    assert constant(lc, "BLOCK_TIME_SECONDS") == candidate_integer(lp, "block_time_seconds")
    assert len(lion_rewards) - 1 == 3008
    assert sum(lion_rewards[:-1]) * lion_blocks == 108_555_885_491_812_251_840
    lion = Model("L10N", constant(lp, "DECIMALS"), constant(lc, "BLOCK_TIME_SECONDS"),
                 lion_blocks, 0, lion_rewards, 50, True, one_lion)

    op = read(family, "open-core/src/params.rs", "OPEN retained timing parameters")
    ot = read(family, "open-core/src/emission_table_100y.csv", "OPEN frozen integer epoch allocations")
    read(family, "open-core/src/emission.rs", "OPEN one-based emission epoch convention")
    rows = list(csv.DictReader(ot.splitlines()))
    assert len(rows) == 43_003
    running, open_allocations = 0, []
    for index, row in enumerate(rows, 1):
        assert int(row["epoch"]) == index
        allocation = int(row["emission_opals"])
        running += allocation
        assert int(row["cumulative_opals"]) == running
        open_allocations.append(allocation)
    ob = constant(op, "EPOCH_BLOCKS")
    opened = Model("OPEN", 9, constant(op, "BLOCK_TIME_SECONDS"), ob, 1,
                   [value // ob for value in open_allocations], 90_000, False)

    np = read(nexus, "crates/nxxxs-core/src/params.rs", "NXXXS reference candidate constants")
    read(nexus, "crates/nxxxs-core/src/emission.rs", "NXXXS gross emission and finite founder allocation")
    npt = read(args.nxxxs_parameters.resolve().parent, args.nxxxs_parameters.name,
               "NXXXS v1.4 candidate parameter record")
    parameters = json.loads(npt)
    ramp, peak = constant(np, "RAMP_EPOCHS"), constant(np, "PEAK_REWARD")
    nn, nd = constant(np, "DECLINE_NUMERATOR"), constant(np, "DECLINE_DENOMINATOR")
    ntail, nb = constant(np, "TAIL_REWARD"), constant(np, "BLOCKS_PER_EPOCH")
    nexus_rewards = [peak * (epoch + 1) // ramp for epoch in range(ramp)]
    while nexus_rewards[-1] > ntail:
        nexus_rewards.append(max(ntail, nexus_rewards[-1] * nn // nd))
    pre_tail = len(nexus_rewards) - 1
    assert pre_tail == constant(np, "PRE_TAIL_EPOCHS")
    assert pre_tail * nb + 1 == constant(np, "TAIL_START_HEIGHT")
    assert sum(nexus_rewards[:-1]) * nb == constant(np, "PRE_TAIL_SUPPLY")
    nscale = constant(np, "BASE_UNITS_PER_NXXXS")
    assert nscale == 10 ** 9
    nx = Model("NXXXS", 9, parameters["consensus"]["block_target_seconds"], nb, 1,
               nexus_rewards, 10, True, ntail)
    canonical = "DAARX-NXXXS/emission/v1\nepoch,reward_base_units\n"
    canonical += "".join(f"{epoch},{reward}\n" for epoch, reward in enumerate(nexus_rewards[:-1]))
    canonical += f"tail,{ntail}\n"
    assert digest(canonical.encode()) == parameters["emission"]["schedule_canonical_sha256"]
    founder_start = constant(np, "FOUNDER_STREAM_START_HEIGHT")
    founder_end = constant(np, "FOUNDER_STREAM_END_HEIGHT")
    founder_epochs = constant(np, "FOUNDER_STREAM_EPOCHS")
    founder_bp, bp_den = constant(np, "FOUNDER_STREAM_BASIS_POINTS"), constant(np, "BASIS_POINTS_DENOMINATOR")
    founder_total = sum(reward * founder_bp // bp_den for reward in nexus_rewards[:founder_epochs]) * nb
    assert founder_start == 1 and founder_end == founder_epochs * nb
    assert founder_total == constant(np, "FOUNDER_STREAM_TOTAL")

    models = {"daarx": daarx, "l10n": lion, "open": opened, "nexus": nx}
    previous_path = SITE / "data/emission-study.json"
    previous_bytes = previous_path.read_bytes()
    previous = json.loads(previous_bytes)
    output = {"schema": "daarx-exact-emission-steps-v1", "as_of": args.as_of,
              "year_seconds": YEAR_SECONDS, "years": 25,
              "quantity": "gross scheduled newly issued coins per block",
              "vertex_semantics": "Both left-limit and right-limit values appear at every reward change. Year zero is zero-emission genesis. Years are reporting coordinates derived from height and target spacing; issuance is height-based.",
              "sources": public_sources, "coins": {}}
    audit = {"schema": "daarx-curve-arithmetic-audit-v1", "as_of": args.as_of,
             "method": "Standard-library integer reconstruction and rational step coordinates; no protocol code execution or protocol tests.",
             "sources": private_sources, "readout_file": {"path": str(previous_path), "sha256": digest(previous_bytes)},
             "coins": {}, "all_samples_match": True}
    total_vertices = 0
    for ident, model in models.items():
        max_height = int(LAST_YEAR * YEAR_SECONDS / model.spacing)
        events = []
        event_heights = {1}
        for epoch in range(1, (max_height - model.offset) // model.blocks + 1):
            event_heights.add(epoch * model.blocks + model.offset)
        vertices = [(Fraction(0), 0, 0)]
        for height in sorted(event_heights):
            old, new = model.reward(height - 1), model.reward(height)
            if height != 1 and old == new:
                continue
            year = model.year(height)
            if year <= LAST_YEAR:
                vertices.extend(((year, 0, old), (year, 1, new)))
                events.append([height, str(old), str(new)])
        samples = {year: model.sample(year) for year in SAMPLE_YEARS}
        for year, sample in samples.items():
            if year != "0":
                vertices.append((Fraction(year), 2, int(sample["base_units"])))
        vertices.sort(key=lambda point: (point[0], point[1]))
        display_vertices = [[float(year), decimal_units(value, model.decimals)] for year, _, value in vertices]
        peak_reward = max(model.rewards)
        peak_epoch = model.rewards.index(peak_reward)
        peak_end_epoch = max(index for index, reward in enumerate(model.rewards) if reward == peak_reward)
        peak_height = model.first_height(peak_epoch)
        peak_end = (peak_end_epoch + 1) * model.blocks + model.offset - 1
        first_positive = model.first_height(next(index for index, reward in enumerate(model.rewards) if reward))
        point = {"unit": model.unit, "display_decimals": model.decimals, "axis_max": model.axis,
                 "candidate": model.candidate, "spacing_seconds": model.spacing, "epoch_blocks": model.blocks,
                 "epoch_height_offset": model.offset, "genesis_reward": "0",
                 "first_positive_height": first_positive, "vertices": display_vertices, "samples": samples,
                 "peak": {"reward": decimal_units(peak_reward, model.decimals), "base_units": str(peak_reward),
                          "epoch": peak_epoch, "height": peak_height, "year": float(model.year(peak_height)),
                          "year_decimal": decimal_year(peak_height, model.spacing), "end_height": peak_end,
                          "end_year": float(model.year(peak_end))}, "tail": None}
        if model.tail:
            tail_epoch = model.rewards.index(model.tail)
            tail_height = tail_epoch * model.blocks + model.offset
            point["tail"] = {"reward": decimal_units(model.tail, model.decimals), "base_units": str(model.tail),
                             "epoch": tail_epoch, "height": tail_height, "year": float(model.year(tail_height)),
                             "year_decimal": decimal_year(tail_height, model.spacing)}
        if ident == "nexus":
            point["founder"] = {"basis_points": founder_bp, "first_height": founder_start,
                                "last_height": founder_end, "end_year": float(model.year(founder_end)),
                                "end_year_decimal": decimal_year(founder_end, model.spacing),
                                "total_base_units": str(founder_total), "total_reward_units": decimal_units(founder_total, 9),
                                "deducted_from_gross": True, "ends_before_peak": founder_end < peak_height}
        comparisons = []
        for index, actual in enumerate(previous["coins"][ident]["rewards"]):
            year = Fraction(index, 100)
            sample = model.sample(str(Decimal(index) / 100))
            matches = Decimal(actual) == Decimal(sample["reward"])
            comparisons.append([index, sample["height"], sample["base_units"], actual, matches])
            audit["all_samples_match"] &= matches
        assert len(comparisons) == 2501
        coin_audit = {"vertex_count": len(vertices), "changed_reward_events": len(events),
                      "event_columns": ["height", "left_limit_base_units", "right_limit_base_units"],
                      "events": events, "sample_columns": ["centiyear_index", "height", "expected_base_units", "observed_display_reward", "matches"],
                      "full_readout_sample_comparison": comparisons,
                      "mismatches": [row for row in comparisons if not row[-1]],
                      "true_genesis_zero": point["vertices"][0] == [0.0, "0"],
                      "all_events_both_sides": len(vertices) == 1 + len(events) * 2 + len(SAMPLE_YEARS) - 1,
                      "nondecreasing_time": all(a[0] <= b[0] for a, b in zip(vertices, vertices[1:])),
                      "clipped_last_year": display_vertices[-1][0] == 25.0,
                      "first_positive_height": first_positive}
        assert coin_audit["all_events_both_sides"] and coin_audit["nondecreasing_time"] and coin_audit["clipped_last_year"]
        assert point["peak"]["reward"] == decimal_units(peak_reward, model.decimals)
        output["coins"][ident], audit["coins"][ident] = point, coin_audit
        total_vertices += len(vertices)
    assert audit["all_samples_match"], "Readout JSON differs from height-derived source math; see actual mismatches before publication"
    public_bytes = (json.dumps(output, ensure_ascii=False, separators=(",", ":")) + "\n").encode()
    assert not re.search(rb"/(?:home|tmp|Users)/", public_bytes)
    destination = SITE / "data/emission-steps.json"
    audit.update({"total_vertices": total_vertices, "compared_readout_samples": 10004,
                  "public_output": {"path": str(destination), "sha256": digest(public_bytes), "bytes": len(public_bytes)},
                  "generator": {"path": str(Path(__file__).resolve()), "sha256": digest(Path(__file__).read_bytes())}})
    destination.write_bytes(public_bytes)
    audit_path = SITE.parent / "curve-arithmetic-audit.json"
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, separators=(",", ":")) + "\n")
    print(json.dumps({"status": "PASS", "coins": list(models), "vertices": total_vertices,
                      "samples_compared": 10004, "all_samples_match": True,
                      "public_bytes": len(public_bytes), "public_sha256": digest(public_bytes),
                      "audit_sha256": digest(audit_path.read_bytes())}))


if __name__ == "__main__":
    main()
