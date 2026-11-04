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
