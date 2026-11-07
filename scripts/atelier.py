"""Editorial framing for the DAARX protocol atlas. No monetary inputs live here."""
import html
import re
from atelier_art import engine

def e(value):
    return html.escape(str(value), quote=True)

def hero(coins, button):
    roles = ['Private capital', 'Private cash', 'Bounded authority', 'Bonded services']
    links = ''.join('<a class="atlas-route '+c['color']+'" href="'+c['path']+'"><span class="atlas-route-index">0'+str(i+1)+'</span><strong>'+c['unit']+'</strong><span>'+roles[i]+'</span><b aria-hidden="true">↗</b></a>' for i,c in enumerate(coins))
    return '''<section class="atlas-hero" id="top" aria-labelledby="hero-title">
      <div class="atlas-backdrop" aria-hidden="true"><img src="/assets/daarx-privacy-grid-v1.webp" width="1672" height="941" alt="" fetchpriority="high"></div>
      <div class="atlas-hero-shell network-shell">
        <div class="atlas-hero-copy"><p class="atlas-kicker"><span aria-hidden="true"></span> DAARX / THE FOUR-COIN FAMILY</p>
          <h1 id="hero-title">Money that<br>minds its own<br><em>business.</em></h1>
          <p class="atlas-intro">Private lives. Accountable power.<br>Four native coins for a world of people, institutions and autonomous agents.</p>
          <div class="atlas-actions">'''+button('Enter the architecture','#protocols',True)+button('Explore the issuance','#supply')+'''</div>
          <a class="atlas-hero-note" href="/status.html"><span aria-hidden="true">◈</span> In development · building toward Public Testnet <span aria-hidden="true">↗</span></a>
        </div>'''+engine()+'''</div>
      <div class="atlas-hero-foot network-shell">'''+links+'''</div>
    </section>'''

def chapters():
    entries = [('protocols','The family'),('possibilities','In practice'),('fairness','The principles'),('supply','The issuance'),('status','The next chapter')]
    return '<nav class="atlas-chapters" aria-label="Explore the showcase"><div class="network-shell">'+''.join('<a href="#'+ident+'"><span>0'+str(i+1)+'</span>'+label+'</a>' for i,(ident,label) in enumerate(entries))+'</div><span class="atlas-reading-progress" data-reading-progress aria-hidden="true"></span></nav>'

def manifesto():
    return '''<section class="atlas-manifesto network-section" aria-labelledby="atlas-manifesto-title"><div class="network-shell">
      <p class="section-index">THE IDEA / A DIFFERENT STARTING POINT</p>
      <h2 id="atlas-manifesto-title">Your life is private.<br><em>Power should have limits.</em></h2>
      <div class="atlas-manifesto-bottom"><span class="atlas-mark" aria-hidden="true">◈</span><p>Money is more than a balance. It carries freedom, permission and responsibility. This family gives each a place: private ownership, everyday exchange, accountable authority and services backed by evidence.</p><a class="text-link" href="#fairness">The principles behind the design <span aria-hidden="true">↗</span></a></div>
    </div></section>'''

def scenario():
    return '''<section class="network-section atlas-scenario" id="possibilities" aria-labelledby="atlas-scenario-title"><div class="network-shell">
      <div class="atlas-scenario-heading"><div><p class="section-index">02 / THE ARCHITECTURE IN PRACTICE</p><h2 id="atlas-scenario-title">Follow the money.<br><em>Understand the rules.</em></h2></div><p>Different situations deserve different protections. Explore the intended path from a person’s decision to a verifiable result.</p></div>
      <div class="atlas-scenario-tabs" role="group" aria-label="Choose an illustrative protocol flow">
        <button type="button" data-atlas-scenario="private" aria-pressed="true" aria-controls="atlas-scenario-panel"><span>01</span> Pay privately <b>DAARX / L10N</b></button>
        <button type="button" data-atlas-scenario="authority" aria-pressed="false" aria-controls="atlas-scenario-panel"><span>02</span> Delegate safely <b>OPEN</b></button>
        <button type="button" data-atlas-scenario="service" aria-pressed="false" aria-controls="atlas-scenario-panel"><span>03</span> Choose useful work <b>NXXXS</b></button>
      </div>
      <div class="atlas-scenario-panel" id="atlas-scenario-panel" data-atlas-scenario-active="private">
        <div class="atlas-scenario-art" aria-hidden="true">
          <svg viewBox="0 0 760 400" fill="none"><defs><linearGradient id="atlas-flow-gradient"><stop stop-color="#8bffc0"/><stop offset=".48" stop-color="#94efff"/><stop offset="1" stop-color="#d6b4ff"/></linearGradient><pattern id="atlas-flow-grid" width="28" height="28" patternUnits="userSpaceOnUse"><path d="M28 0H0V28" stroke="#a6d9c2" stroke-opacity=".09"/></pattern></defs>
          <rect width="760" height="400" fill="url(#atlas-flow-grid)"/><path d="M54 200H706M380 54V346" stroke="#a6d9c2" stroke-opacity=".1"/>
          <path class="atlas-flow-track" d="M106 200C205 200 217 115 302 115S425 285 505 285 587 200 654 200" stroke="url(#atlas-flow-gradient)" stroke-width="2"/>
          <path class="atlas-flow-trace" d="M106 200C205 200 217 115 302 115S425 285 505 285 587 200 654 200" stroke="url(#atlas-flow-gradient)" stroke-width="4" stroke-dasharray="6 18"/>
          <g class="atlas-flow-person" transform="translate(106 200)"><circle r="42" fill="#0b1c18" stroke="#8bffc0"/><circle cy="-10" r="10" stroke="#8bffc0" stroke-width="2"/><path d="M-18 20C-18 0 18 0 18 20" stroke="#8bffc0" stroke-width="2"/></g>
          <g transform="translate(302 115)"><path d="M0-43 43 0 0 43-43 0Z" fill="#0b1c18" stroke="#94efff"/><path class="atlas-flow-seal" d="M-15-5V17H15V-5ZM-9-5V-13A9 9 0 0 1 9-13V-5" stroke="#94efff" stroke-width="2"/></g>
          <g transform="translate(505 285)"><path d="M0-43 43 0 0 43-43 0Z" fill="#0b1c18" stroke="#ffdb90"/><path d="M-16 0-4 12 18-14" stroke="#ffdb90" stroke-width="3"/></g>
          <g transform="translate(654 200)"><circle r="42" fill="#0b1c18" stroke="#d6b4ff"/><path d="M-16-12H16V12H-16ZM-8-20V-12M8-20V-12M-8 12V20M8 12V20" stroke="#d6b4ff" stroke-width="2"/></g>
          <g font-family="monospace" font-size="12" fill="#d6e6dc" text-anchor="middle"><text x="106" y="272" data-atlas-flow-label="0">YOUR DECISION</text><text x="302" y="48" data-atlas-flow-label="1">SEALED AMOUNT</text><text x="505" y="358" data-atlas-flow-label="2">VALIDITY PROOF</text><text x="654" y="272" data-atlas-flow-label="3">PRIVATE PAYEE</text></g>
          </svg><p class="atlas-scenario-art-note">ILLUSTRATIVE PROTOCOL PATH / NOT LIVE TRANSACTION DATA</p>
        </div>
        <div class="atlas-scenario-copy" aria-live="polite" aria-atomic="true"><p class="panel-code" data-atlas-scenario-code>PRIVATE VALUE / DAARX + L10N</p><h3 data-atlas-scenario-heading>Prove the payment.<br>Keep the amount private.</h3><p data-atlas-scenario-description>A valid spend should not require a public financial biography. Hidden amounts and full-chain membership proofs are designed to let the chain check validity without naming the earlier output.</p><ol class="atlas-scenario-steps"><li data-atlas-flow-step="0">You authorize a private spend.</li><li data-atlas-flow-step="1">A proof establishes validity while the amount stays sealed.</li><li data-atlas-flow-step="2">The recipient receives value on its native chain.</li></ol><a class="text-link" data-atlas-scenario-link href="/daarx.html">Inside private capital <span aria-hidden="true">↗</span></a></div>
      </div><p class="atlas-scenario-boundary">Architectural illustrations. The complete public system is still being qualified; explore <a href="/status.html">development and release work</a>.</p>
    </div></section>'''

def simplify_section(markup, ident):
    """Keep long-form facts available while giving the homepage a readable rhythm."""
    if ident == 'principles':
        markup = markup.replace('Who gets<br><em>the money.</em>', 'The allocation.<br><em>In plain sight.</em>')
    if ident == 'economics':
        markup = re.sub(r'<article class="architecture-card"><p class="architecture-number">(.*?)</p><div><h3>(.*?)</h3>(.*?)</div></article>', lambda m: '<details class="atlas-note"><summary><span>'+m[1]+'</span>'+m[2]+'<b aria-hidden="true">＋</b></summary><div>'+m[3]+'</div></details>', markup)
    return markup

def home_sections(coins, button, thesis, switch, ethics, fairness, rationale, supply, ending):
    return (hero(coins,button)+chapters()+manifesto()+switch+scenario()+thesis+
            fairness+simplify_section(ethics,'principles')+supply+simplify_section(rationale,'economics')+ending)

def page_navigation(coin):
    return '<nav class="atlas-page-nav" aria-label="Explore '+e(coin['unit'])+'"><a href="#architecture">01 / The idea</a><a href="#issuance">02 / Monetary rules</a><a href="#proofs">03 / The architecture</a><a href="/#protocols">↖ The whole family</a></nav>'
