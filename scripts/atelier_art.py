"""Deterministic, dependency-free Atlas sculpture. No network or build side effects."""
from math import sin, cos, pi, sqrt
from html import escape

COINS = (
    ('daarx', 'DAARX', '#79f5b0', 'Private ownership', 'Private payment amounts, one-time destination keys and full-chain membership proofs protect the person behind a balance.'),
    ('l10n', 'L10N', '#f3cc79', 'Everyday circulation', 'Private everyday money with its own balances and monetary rules. Offline exchange and later settlement are part of the engineering work.'),
    ('open', 'OPEN', '#77e5f5', 'Bounded authority', 'Distinct Human, Institution and Agent accounts. Mandates bound delegated spending; delegation cannot multiply the allowance.'),
    ('nexus', 'NXXXS', '#c8a4ff', 'Evidence-backed services', 'The Nexus / NXXXS lineage connects chosen services to evidence and collateral. Ordinary sibling-chain transfers carry no automatic NXXXS toll.'),
)


def _point(t, v, strand):
    # A rounded diamond backbone with four helical, fluted ribbons.
    c, s = cos(t), sin(t)
    r = 254 / (abs(c) ** 1.30 + abs(s) ** 1.30) ** (1 / 1.30)
    phase = 3 * t + strand * pi / 2
    radial = r + 43 * cos(phase) + v * 19
    x, y, z = radial * c * 1.18, radial * s, 64 * sin(phase) + v * 16 * cos(phase)
    # Tilt before perspective; actual depth drives both scale and painter order.
    yy, zz = y * .88 - z * .475, y * .475 + z * .88
    scale = 980 / (980 - zz)
    return (480 + (x + zz * .13) * scale, 350 + yy * scale, zz)


def _svg():
    pieces = []
    count = 96
    for k, (key, _, color, _, _) in enumerate(COINS):
        rgb = tuple(int(color[i:i+2], 16) for i in (1, 3, 5))
        for i in range(count):
            t = i * 2 * pi / count
            for j in range(3):
                v = -1 + j * 2 / 3
                pts = [_point(t, v, k), _point(t + 2*pi/count, v, k),
                       _point(t + 2*pi/count, v+2/3, k), _point(t, v+2/3, k)]
                depth = sum(p[2] for p in pts) / 4
                light = .30 + .52 * (j / 2) + .17 * sin(t * 3 + k*pi/2)
                fill = '#'+''.join(f'{max(0,min(255,int(c*light))):02x}' for c in rgb)
                # Quadratic longitudinal boundaries preserve smooth silhouettes at
                # half the segment count; midpoint interpolation follows the 3D curve.
                a, b, c, d = pts
                m = _point(t + pi/count, v, k)
                n = _point(t + pi/count, v+2/3, k)
                q = (2*m[0]-(a[0]+b[0])/2, 2*m[1]-(a[1]+b[1])/2)
                r = (2*n[0]-(c[0]+d[0])/2, 2*n[1]-(c[1]+d[1])/2)
                path = (f'M{a[0]:.2f},{a[1]:.2f}Q{q[0]:.2f},{q[1]:.2f} {b[0]:.2f},{b[1]:.2f}'
                        f'L{c[0]:.2f},{c[1]:.2f}Q{r[0]:.2f},{r[1]:.2f} {d[0]:.2f},{d[1]:.2f}Z')
                pieces.append((depth, f'<path data-atlas-strand="{key}" d="{path}" fill="{fill}" stroke="{color}" stroke-opacity="{.23 if j==2 else .07}" stroke-width=".5"/>'))
        # Edge wires, independently sorted for physically consistent occlusion.
        for i in range(count):
            t = i * 2*pi/count
            a, b = _point(t, 1, k), _point(t+2*pi/count, 1, k)
            m = _point(t+pi/count, 1, k)
            q = (2*m[0]-(a[0]+b[0])/2, 2*m[1]-(a[1]+b[1])/2)
            pieces.append(((a[2]+b[2])/2+.2, f'<path data-atlas-strand="{key}" d="M{a[0]:.2f},{a[1]:.2f}Q{q[0]:.2f},{q[1]:.2f} {b[0]:.2f},{b[1]:.2f}" stroke="{color}" stroke-width="1.15" fill="none"/>'))
    stars = ''.join(f'<path d="M{x-2} {y}h4m-2-2v4" opacity="{.18+(i%3)*.1}"/>' for i,(x,y) in enumerate([(113,181),(786,122),(840,412),(109,531),(710,611),(289,77),(870,245),(221,635),(61,331),(662,56),(817,566)]))
    return ('<svg class="atlas-engine-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 720" fill="none" aria-hidden="true" focusable="false" style="display:block;width:100%;height:auto">'
            '<defs><linearGradient id="atlas-diamond" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#79f5b0"/><stop offset=".5" stop-color="#77e5f5"/><stop offset="1" stop-color="#c8a4ff"/></linearGradient></defs>'
            '<g stroke="#b5cfca" stroke-width=".7">'+stars+'</g>'
            '<g stroke="#526762" stroke-width=".6" opacity=".6"><path d="M35 83V35h48M877 35h48v48M35 637v48h48M877 685h48v-48M35 350h38M887 350h38"/><path d="M480 57v27M480 637v27"/></g>'
            '<g class="atlas-engine-sculpture">'+''.join(p[1] for p in sorted(pieces,key=lambda p:p[0]))+'</g>'
            '<g stroke="url(#atlas-diamond)" stroke-width=".8"><path d="M480 253l69 88-69 103-69-103Z"/><path d="M480 253l24 88-24 103-24-103ZM411 341h138" opacity=".38"/></g>'
            '<g stroke="#a3bdb2" stroke-width=".6" opacity=".65"><path d="M164 205H77v-41M740 512h125v35M554 291l78-90h101"/></g>'
            '<g fill="#b4c8bf" font-family="monospace" font-size="10" letter-spacing="2"><text x="78" y="149">01 / PRIVATE VALUE</text><text x="737" y="190" text-anchor="end">FACET / SHARED WORK</text><text x="865" y="565" text-anchor="end">04 / INDEPENDENT RULES</text><text x="480" y="684" text-anchor="middle">FOUR STRANDS · ONE COMPOSITION</text></g></svg>')


def engine():
    """Return the complete progressively enhanced, accessible hero figure."""
    buttons = ''.join(f'<button type="button" data-atlas-coin="{key}" aria-pressed="{str(i == 0).lower()}" style="--atlas-coin:{color}">{name}</button>' for i,(key,name,color,_,_) in enumerate(COINS))
    return ('<figure class="atlas-engine" data-atlas-selected="daarx" data-atlas-active="false" data-atlas-frames="0">'
            '<div class="atlas-engine-stage">'+_svg()+'<canvas data-atlas-canvas aria-hidden="true"></canvas>'
            '<span class="atlas-engine-label">ATLAS / A STUDY IN FOUR PROTOCOLS</span></div>'
            '<div class="atlas-engine-controls" role="group" aria-label="Explore the four coin roles">'+buttons+'</div>'
            '<figcaption class="atlas-engine-caption" aria-live="polite" aria-atomic="true"><strong data-atlas-title>DAARX / Private ownership</strong>'
            '<p data-atlas-description>'+escape(COINS[0][4])+'</p></figcaption></figure>')
