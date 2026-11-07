# daarx.money

Static website for the four-coin system: DAARX, L10N, OPEN and Nexus / NXXXS.
The current public stage is Testnet preparation. Nexus / NXXXS is a working
public identity; the site does not announce an open network or a coin sale.

Pages are generated with the Python standard library:

```sh
python3 scripts/build-pages.py
```

The generator keeps the existing hardware-interest form endpoint and hidden
payload. Hardware interest remains separate from Testnet participation.
Update the dated copy and `data/release-status.json` through the generator.

Run the locked quality checks before publication:

```sh
npm ci --ignore-scripts
npm test
```

The site has no build-time framework, external font request or runtime account
service. `site.js` provides keyboard-accessible tabs, FAQ filtering, the existing
interest-form interaction and a procedural spectral visual. The visual honors
reduced-motion preferences and has a page-local pause control.

The public monetary study follows the selected FEM-20261106-v1 reference.
To regenerate exact chart data from an independently retained, hash-pinned FEM
package, run `PYTHONDONTWRITEBYTECODE=1 python3 scripts/build-remodel-data.py
--model-dir /path/to/selected-model`, then regenerate pages as above. The model
package is an explicit input; private evidence paths and receipts are excluded
from public output. The older build-emission-data.py reconstructs the historical
pre-remodel schedule and must not overwrite the selected public study.

The protocol-atlas presentation is authored in `scripts/atelier.py`, with a
local deterministic sculpture in `scripts/atelier_art.py`. `atelier.css`,
`atelier.js` and `atlas-story.js` supply responsive presentation and progressive
interactions. No service credentials, third-party scripts or new dependencies
are needed. Visual changes leave the selected monetary JSON and exact chart
geometry independent of presentation.
