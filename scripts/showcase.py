"""DAARX showcase: preserve the pre-refresh visual system; update the family facts.
Standard-library build. The retained templates and diagrams pin the original art direction.
"""
from pathlib import Path
import hashlib,html,json,re
import experience as facts
from prism_art import scene,svg,utility_diagram
import charts
import atelier
R=Path(__file__).resolve().parents[1]
T=R/'scripts/templates'
COINS=facts.COINS
DATE='November 6, 2026'
def esc(s):return html.escape(str(s))
def template(name):return (T/name).read_text()
def fragment(source,cls):
    start=re.search(r'<section\b[^>]*class="[^"]*\b'+re.escape(cls)+r'\b[^\"]*"[^>]*>',source)
    if not start:raise ValueError(cls)
    depth=1
    for token in re.finditer(r'</?section\b[^>]*>',source[start.end():]):
        depth+= -1 if token.group().startswith('</') else 1
        if depth==0:return source[start.start():start.end()+token.end()]
    raise ValueError('Unclosed '+cls)
def swap(source,cls,new):return source.replace(fragment(source,cls),new,1)
def content(source):return re.search(r'<main\b[^>]*>([\s\S]*?)</main>',source).group(1)
def asset(f):return '/'+f+'?v='+hashlib.sha256((R/f).read_bytes()).hexdigest()[:12]
def btn(text,path,primary=False):return '<a class="module-button'+(' primary' if primary else '')+'" href="'+path+'"><span>'+text+'</span><span aria-hidden="true">↗</span></a>'
def nav(path):
    links=[('/','Home')]+[(c['path'],c['unit']) for c in COINS]+[('/status.html','Development'),('/testnet.html','Testnet'),('/mine.html','Hardware'),('/break-it.html','Security'),('/faq.html','Questions'),('/privacy.html','Privacy')]
    link=lambda p,n:'<a href="'+p+'"'+(' aria-current="page"' if p==path else '')+'>'+n+'</a>'
    return '<a class="skip" href="#main">Skip to content</a><nav class="nav network-nav" id="nav" aria-label="Primary"><a class="mk" href="/" aria-label="DAARX family home"><span class="mk-sigil" aria-hidden="true"></span><span class="atlas-wordmark">DAARX<span aria-hidden="true">.</span></span><span class="atlas-brand-note">THE FOUR-COIN FAMILY</span></a><div class="go"><a class="lnk" href="/#protocols">Architecture</a><a class="lnk" href="/#supply">Economics</a><a class="lnk" href="/status.html">Development</a><button class="motion-control" data-showcase-motion type="button" aria-pressed="false" aria-label="Pause visual motion">Ⅱ</button><details class="nd"><summary class="burger" aria-label="Explore all pages"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h16"/></svg></summary><div class="navmenu">'+''.join(link(*x) for x in links)+'</div></details></div></nav>'
def footer():
    return '<footer><div class="wrap wide"><p class="atlas-footer-statement">Private lives.<br><em>Accountable power.</em></p><p class="follow">Four native coins. One considered architecture.</p><nav class="fnav" aria-label="Site">'+''.join('<a href="'+c['path']+'">'+c['unit']+'</a>' for c in COINS)+''.join('<a href="'+p+'">'+t+'</a>' for p,t in [('/status.html','Development'),('/testnet.html','Testnet'),('/mine.html','Hardware'),('/break-it.html','Security'),('/faq.html','Questions'),('/flyer.html','Print'),('/privacy.html','Privacy'),('mailto:daarxmoney@proton.me','Contact')])+'</nav><p class="fine">DAARX / L10N / OPEN / NXXXS · '+DATE+'</p></div></footer>'
def shell(path,title,description,body,cls='showcase-utility',schema=None):
    styles=['style.css','inner-shell.css','protocol-modules.css','utility-modules.css']
    if path=='/':styles+=['network.css']
    styles+=['showcase.css','prism.css','spectrum.css']
    if path!='/flyer.html':styles+=['atelier.css']
    scripts=['site.js','showcase.js','prism.js']
    if path!='/flyer.html':scripts+=['atelier.js','atlas-story.js']
    if path=='/':scripts+=['network.js']
    else:scripts+=['protocol-modules.js']
    schema=schema or {'@context':'https://schema.org','@type':'WebSite','name':'DAARX','url':'https://daarx.money','description':description}
    return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="theme-color" content="#060b09"><title>'+esc(title)+'</title><meta name="description" content="'+esc(description)+'"><link rel="canonical" href="https://daarx.money'+path+'"><link rel="icon" href="/assets/mark.svg" type="image/svg+xml">'+''.join('<link rel="stylesheet" href="'+asset(f)+'">' for f in styles)+'<meta property="og:type" content="website"><meta property="og:site_name" content="DAARX"><meta property="og:title" content="'+esc(title)+'"><meta property="og:description" content="'+esc(description)+'"><meta property="og:url" content="https://daarx.money'+path+'"><meta property="og:image" content="https://daarx.money/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+esc(title)+'"><meta name="twitter:description" content="'+esc(description)+'"><meta name="twitter:image" content="https://daarx.money/og.png"><script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</',r'<\/')+'</script>'+''.join('<script src="'+asset(f)+'" defer></script>' for f in scripts)+'</head><body class="'+cls+(' atelier' if path!='/flyer.html' else '')+' showcase">'+nav(path)+'<main id="main">'+body+'</main>'+footer()+'</body></html>'

# Monetary purpose and ethics are visible beside the design, not buried in release prose.
BRIEFS={
'daarx':[
 ('THE DISTRIBUTION','Early doesn’t mean all of it.','Issuance rises toward year 7.77 instead of starting at its maximum. At that peak, about 22.19% of the literal ceiling is scheduled to have been issued. Most of the distribution is still ahead.'),
 ('THE OWNER','A balance is personal.','Ordinary transfer amounts stay hidden. Full-chain membership proofs let the chain check a spend without identifying which earlier output it spends. One-time destination keys keep a reusable recipient address off the ledger.'),
 ('THE ALLOCATION','Mining writes the first receipt.','Miners receive the entire subsidy and transaction fees. The retained monetary policy has no premine, presale or founder reward. The issuance schedule eventually reaches zero; fees then pay for mining.')],
'l10n':[
 ('THE PURPOSE','Money for passing on.','L10N separates everyday circulation from long-duration savings. It has its own balances and monetary rules, with private amounts and the family’s full-chain privacy work.'),
 ('THE SECURITY BUDGET','Keep paying the people who secure it.','The selected FEM model adds a finite 77.7-year bonus to a permanent 1 L10N per paid block. The bonus rises toward year 7.77, then declines. Fees go to miners. Continuing issuance dilutes balances; a nominal reward floor cannot guarantee security. There is no premine, presale, founder reward or fee burn.'),
 ('THE OFFLINE LAYER','Cash has to survive a lost connection.','The offline work covers loading, local exchange, receipts, later settlement and recovery. A separate anti-fraud bond backs defined obligations. It is committed capital, not an interest-bearing deposit.')],
'open':[
 ('THE ACCOUNTS','Know who is allowed to act.','Human, Institution and Agent are distinct native account classes. Institutions use threshold authority. Agents act for a principal under mandates rather than inheriting unlimited control.'),
 ('THE LIMITS','Permission has a budget.','Per-transaction, per-epoch and lifetime spending caps follow the mandate ancestry. Delegation cannot multiply that allowance. Fees consume it too; the maximum ancestry depth is seven.'),
 ('THE BACKING','Put capital behind the action.','HALO backs admitted Agent value acts. Public accounts and committed records make the authority inspectable. The current objective-fault path concerns same-nonce equivocation; broader restitution and arbitration are separate work.')],
'nexus':[
 ('THE WORK','Pay for something that happened.','Relays, proofs, solvers, venues and settlement services are the demand paths. A customer pays a chosen provider for a supported service. An ordinary sibling-chain transfer does not incur a NXXXS toll.'),
 ('THE COMMITMENT','The provider puts something up.','Providers maintain operating balances and commit native collateral to declared capacity and obligations. Evidence is checked under the selected rules. A service fee pays the provider; a bond remains committed capital until its rules release or penalize it.'),
 ('THE ALLOCATION','A founder share with an end.','The reference schedule assigns 2% of gross subsidy to a finite founder stream for roughly seven target years. It ends before the candidate’s year-7.77 peak. Miners receive the rest; the stream is part of scheduled issuance.')]
}
DETAILS={
'daarx': [('UNIT','DIAM · 12 decimal places'),('LITERAL CEILING','5,083,000,000,000 DIAM'),('ISSUANCE PEAK','Near target year 7.77'),('BLOCK TARGET','111 seconds'),('ISSUANCE END','About 100 target years · no tail'),('FEES','Public ladder · paid to miners')],
'l10n': [('SUPPLY STRUCTURE','Uncapped · permanent positive tail'),('REFERENCE CURVE','1 baseline + finite rising/declining bonus'),('TIMING','30s blocks · bonus ends at year 77.7'),('DISTRIBUTION','All mined · fees to miners'),('FEE BURN','None in the monetary design'),('PRIVACY','Hidden amounts · full-chain membership')],
'open': [('UNIT','OPEN · 10⁹ opals'),('LITERAL CEILING','2,718,281,828,459 OPEN'),('ISSUANCE','Rise to year ~7.77 · finite slow decline'),('CURRENT SUBSIDY','About 89% miners / 11% endowment'),('DIVIDEND','Disarmed · current allocation to miners'),('FEES','Base fee burns · priority fee to miners')],
'nexus': [('LINEAGE','Nexus / NXXXS · one fourth coin'),('REFERENCE PEAK','10 NXXXS / block · near year 7.77'),('REFERENCE TAIL','0.1 NXXXS / block · permanent'),('FOUNDER STREAM','2% · finite · ends before peak'),('FEES + RENT','Base fees and rent burn; priority to miners'),('SERVICE PAYMENTS','Paid to the chosen provider')]
}

NEXUS_SVG='''<svg viewBox="0 0 760 610" fill="none" aria-hidden="true"><defs><radialGradient id="nxx-glow"><stop stop-color="#c298ff" stop-opacity=".35"/><stop offset="1" stop-color="#c298ff" stop-opacity="0"/></radialGradient><linearGradient id="nxx-line"><stop stop-color="#4ae08c"/><stop offset=".5" stop-color="#c298ff"/><stop offset="1" stop-color="#63b9d6"/></linearGradient></defs><circle cx="380" cy="290" r="280" fill="url(#nxx-glow)"/><g stroke="#c298ff" stroke-opacity=".2"><path d="M0 160H760M0 290H760M0 420H760M125 0V610M380 0V610M635 0V610"/><circle cx="380" cy="290" r="210"/><circle cx="380" cy="290" r="165"/></g><path d="M150 290L380 140L610 290L380 440Z" stroke="url(#nxx-line)" stroke-width="4"/><path d="M150 290H610M380 140V440" stroke="#c298ff" stroke-opacity=".35" stroke-dasharray="6 8"/><g fill="#121221" stroke="#d0aaff" stroke-width="2"><circle cx="150" cy="290" r="42"/><circle cx="380" cy="140" r="42"/><circle cx="610" cy="290" r="42"/><circle cx="380" cy="440" r="42"/></g><g fill="#eee4ff" font-family="monospace" font-size="12" text-anchor="middle"><text x="150" y="295">REQUEST</text><text x="380" y="145">BOND</text><text x="610" y="295">PROOF</text><text x="380" y="445">PAYMENT</text></g><circle cx="380" cy="290" r="65" fill="#201930" stroke="#c298ff" stroke-width="2"/><path d="M350 290l20 20 40-42" stroke="#d8baff" stroke-width="5"/><g fill="#b9a5ce" font-family="monospace" font-size="11" letter-spacing="1"><text x="270" y="565">COMMITTED CAPITAL / VERIFIED WORK</text></g></svg>'''

def coin_curve(c):
    return charts.coin_curve(c,R)

def coin_page(c):
    ident=c['id'];i=next(i for i,x in enumerate(COINS) if x['id']==ident)
    original_visual=template(ident+'-hero.fragment') if ident!='nexus' else NEXUS_SVG
    hero_diagram=re.sub(r'(id="|url\(#)([A-Za-z][A-Za-z0-9_-]*)',lambda m:m[1]+'hero-'+m[2],original_visual)
    visual=scene(ident).replace('<canvas data-prism-canvas aria-hidden="true"></canvas>','<canvas data-prism-canvas aria-hidden="true"></canvas><div class="prism-original" aria-hidden="true">'+hero_diagram+'</div>')
    heading={'daarx':'The one to <em>keep.</em>','l10n':'The one to <em>spend.</em>','open':'Authority with <em>limits.</em>','nexus':'Work with <em>proof.</em>'}[ident]
    rows=DETAILS[ident]
    hero='<section class="protocol-hero" aria-labelledby="hero-title"><div class="protocol-frame" aria-hidden="true"><span class="tl"></span><span class="tr"></span><span class="bl"></span><span class="br"></span></div><div class="protocol-shell protocol-hero-layout"><div class="protocol-hero-copy"><p class="protocol-flag">THE FOUR-COIN FAMILY</p><h1 id="hero-title">'+c['unit']+'</h1><span class="protocol-ordinal">0'+str(i+1)+' / '+c['material']+'</span><h2>'+heading+'</h2><p class="protocol-lede">'+c['description']+'</p><div class="protocol-actions">'+btn('The idea','#architecture',True)+btn('The monetary rules','#issuance')+'</div></div><div class="protocol-hero-visual">'+visual+'</div></div></section>'
    brief='<section class="module-section brief-section" id="architecture"><div class="protocol-shell brief-grid"><header class="module-section-intro"><p class="module-index">01 / PURPOSE + PRINCIPLES</p><h2>'+c['line']+'</h2><p>'+c['economics']+'</p></header><div class="brief-stack">'+''.join('<article class="brief-item"><p class="brief-number">0'+str(n+1)+'</p><div><p class="panel-code">'+code+'</p><h3>'+title+'</h3><p>'+text+'</p></div></article>' for n,(code,title,text) in enumerate(BRIEFS[ident]))+'</div></div></section>'
    supply='<section class="module-section spec-section" id="issuance"><div class="protocol-shell"><header class="module-section-intro split"><div><p class="module-index">02 / ISSUANCE + ALLOCATION</p><h2>'+c['emission']+'</h2></div><p>'+c['allocation']+'</p></header>'+coin_curve(c)+'<div class="spec-console"><div class="spec-bar"><strong>'+c['unit']+'::MONETARY_RULES</strong><span>'+('SELECTED FEM MODEL' if ident in ['l10n','open'] else 'REFERENCE CANDIDATE' if ident=='nexus' else 'RETAINED DESIGN')+'</span></div><dl class="spec-rows">'+''.join('<div><dt>'+a+'</dt><dd>'+b+'</dd></div>' for a,b in rows)+'</dl></div><p class="monetary-detail">'+c['monetary']+'</p><div class="protocol-actions">'+btn('Compare the four curves','/#supply')+'</div></div></section>'
    proof=facts.protocol_study(c).replace('class="section protocol-study','class="module-section protocol-study').replace('class="container"','class="protocol-shell"')
    proof=proof.replace('<section ', '<section id="proofs" ',1)
    proof=proof.replace('</section>','<div class="protocol-shell"><details class="protocol-schematic"><summary>Trace the '+c['unit']+' structure <span aria-hidden="true">＋</span></summary>'+original_visual+'</details></div></section>')
    final='<section class="module-section module-final" id="wallet"><div class="protocol-shell module-final-grid"><div class="module-final-copy"><p class="module-index">03 / WALLET + RECOVERY</p><h2>Wallets.<br><em>Recovery.</em></h2><p>'+c['wallet']+'</p><div class="protocol-actions">'+btn('Follow development','/status.html',True)+btn('Public Testnet','/testnet.html')+'</div></div><nav class="family-routes" aria-label="Other coins">'+''.join('<a class="family-route '+x['id']+'" href="'+x['path']+'"><span class="route-node" aria-hidden="true"></span><span><b>'+x['unit']+'</b><small>'+x['role']+'</small></span><span aria-hidden="true">↗</span></a>' for x in COINS if x!=c)+'</nav></div></section>'
    return shell(c['path'],c['name']+' — '+c['role']+' | DAARX',c['description'],hero+atelier.page_navigation(c)+brief+supply+proof+final,'protocol-page p-'+ident)

def home():
    original=content(template('index.template'))
    hero=fragment(original,'network-hero')
    hero=re.sub(r'<p class="system-flag">[\s\S]*?</p>','<p class="system-flag"><span class="status-pulse" aria-hidden="true"></span> DAARX / L10N / OPEN / NXXXS</p>',hero)
    hero=re.sub(r'<h1 id="hero-title">[\s\S]*?</h1>','<h1 id="hero-title"><span>Money </span><span>designed for </span><span class="signal-word">privacy.</span></h1>',hero)
    hero=re.sub(r'<p class="hero-lede">[\s\S]*?</p>','<p class="hero-lede">Keep it private. Let it circulate. Decide who can act, and what stands behind the work.</p>',hero)
    hero=re.sub(r'<p class="hero-truth">[\s\S]*?</p>','',hero)
    hero=hero.replace('BUILD STATE / PRE-TESTNET','FOUR COINS / FOUR SETS OF RULES')
    hero=hero.replace('Inspect the systems','Explore the family').replace('View system status','Follow the supply').replace('href="#status"','href="#supply"')
    hero=re.sub(r'<div class="hero-readout">[\s\S]*?</dl>[\s\S]*?</div>','<div class="hero-readout"><p class="readout-title"><span>FOUR NATIVE COINS</span><span>ONE FAMILY</span></p><dl>'+''.join('<div><dt class="'+cl+'">'+c['unit']+'</dt><dd>'+role+'</dd></div>' for c,cl,role in zip(COINS,['d','l','o','n'],['PRIVATE CAPITAL','PRIVATE CASH','BOUNDED AUTHORITY','BONDED SERVICES']))+'</dl></div>',hero)
    hero=re.sub(r'<div class="hero-readout">[\s\S]*?</dl>[\s\S]*?</div>','<div class="hero-showcase">'+scene('family')+'</div>',hero)
    thesis=fragment(original,'thesis-section')
    thesis=thesis.replace('OPEN explores public accounting for machines.','OPEN makes authority public and bounded. NXXXS connects paid services to evidence and collateral.')
    thesis=thesis.replace('PRIVACY TARGET','PRIVATE LEDGER').replace('RELATIONSHIPS ARE THE PRIVACY TARGET','AMOUNTS AND MEMBERSHIP STAY SEALED').replace('MODEL / PRIVACY DESIGN TARGET','MODEL / PRIVATE VALUE')
    thesis=thesis.replace('DAARX and L10N target hidden amounts and full-chain membership proofs. This is an anonymity-set design, not a guarantee of end-to-end anonymity.','DAARX and L10N use hidden amounts and full-chain membership proofs. The chain checks the spend without publishing the amount or naming the earlier output.')
    switch=fragment(original,'protocols-section').replace('Three lanes.','Four coins.').replace('PROTOCOL SWITCHYARD','THE FAMILY')
    switch=switch.replace('Select a route to inspect its purpose, current state, and limits. The visual is a map of the design—not live network telemetry.','Saving and spending. Delegation and services. Choose a coin to see the rules behind its role.')
    switch=switch.replace('Three luminous signal conduits converge through a black-glass network switchyard.','Luminous signal conduits meet in a black-glass switchyard, overlaid with the four coin routes.')
    switch=switch.replace('<circle class="route-core"','<path class="route route-nexus" d="M1000 430C760 430 680 350 500 260"/><circle class="route-core"')
    switch=switch.replace('<figcaption>Conceptual protocol switchyard. Not a live topology or network-status display.</figcaption>','<div class="switchyard-label switchyard-label-n"><span>04</span> NXXXS / BONDED SERVICES</div><figcaption>Four independent chains. Shared mining architecture.</figcaption>')
    tabs=''.join('<button id="tab-'+c['id']+'" type="button" role="tab" aria-selected="'+('true' if i==0 else 'false')+'" aria-controls="panel-'+c['id']+'" data-protocol="'+c['id']+'" tabindex="'+('0' if i==0 else '-1')+'"><span>0'+str(i+1)+'</span><b>'+c['unit']+'</b><small>'+['KEEP','SPEND','AUTHORIZE','PROVE'][i]+'</small></button>' for i,c in enumerate(COINS))
    switch=re.sub(r'(<div class="protocol-tabs"[^>]*>)[\s\S]*?</div>',lambda m:m[1]+tabs+'</div>',switch,count=1)
    panels=''
    for i,c in enumerate(COINS):
        panels+='<div class="protocol-panel protocol-'+c['id']+(' is-active' if i==0 else '')+'" id="panel-'+c['id']+'" role="tabpanel" aria-labelledby="tab-'+c['id']+'"><div class="protocol-state"><span>'+c['material']+'</span><strong>'+c['rule']+'</strong></div><h3>'+c['unit']+' <span>/ '+['the one to keep','the one to spend','authority with limits','work with proof'][i]+'</span></h3><p>'+c['description']+'</p><dl class="protocol-facts">'+''.join('<div><dt>'+a+'</dt><dd>'+b+'</dd></div>' for a,b in DETAILS[c['id']][:3])+'</dl><a class="text-link" href="'+c['path']+'">Inside '+c['unit']+' <span aria-hidden="true">↗</span></a></div>'
    first=switch.index('<div class="protocol-panel');switch=switch[:first]+panels+'</div></div></div></section>'
    ethics='<section class="network-section architecture-section" id="principles"><div class="network-shell architecture-grid"><header class="section-intro"><p class="section-index">03 / THE PRINCIPLES</p><h2>Who gets<br><em>the money.</em></h2><p>The distribution matters as much as the supply. Each coin makes a different choice. You should be able to see it.</p></header><div class="architecture-stack">'+''.join('<article class="architecture-card"><p class="architecture-number">0'+str(i+1)+'</p><div><p class="panel-code '+cl+'">'+c['unit']+'</p><h3>'+title+'</h3><p>'+text+'</p></div></article>' for i,(c,cl,title,text) in enumerate(zip(COINS,['d','l','o','n'],['Mined, from beginning to end.','A security budget that continues.','A public endowment allocation.','A finite founder stream.'],['No premine, presale or founder reward. Issuance rises into a delayed peak, then winds down to zero.','All issuance and fees go to miners. A 1 L10N baseline continues after the finite 77.7-year bonus. This supports miner incentives, while actual security depends on costs, reward value and participation.','The current subsidy allocates 11% to the endowment and the rest to miners. The designed dividend is disarmed.','The reference candidate assigns 2% of subsidy to the founder stream for roughly seven target years. It ends before peak issuance.'])))+'</div></div></section>'
    rationale='<section class="network-section architecture-section" id="economics"><div class="network-shell architecture-grid"><header class="section-intro"><p class="section-index">ECONOMICS / FEM-20261106-v1</p><h2>Opportunity<br><em>over time.</em></h2><p>The selected model moves L10N and OPEN away from a launch maximum toward year 7.77. DAARX and NXXXS retain their curves. Consensus integration and release qualification remain pending.</p></header><div class="architecture-stack"><article class="architecture-card"><p class="architecture-number">01</p><div><h3>Give participation time to grow.</h3><p>Lower early issuance leaves more distribution for later participants. L10N’s first-year share of its first 25 target years falls from 33.20% to 1.69%; OPEN’s falls from 6.01% to 0.39%. These are gross issuance shares within each version’s 25-year window, not lifetime or ownership percentages. Both cumulative schedules stay at or below their predecessors.</p></div></article><article class="architecture-card"><p class="architecture-number">02</p><div><h3>Different money, different commitments.</h3><p>L10N keeps a permanent 1-coin baseline plus a finite 77.7-year bonus; its supply remains uncapped. OPEN preserves its exact lifetime gross budget of 2,718,281,828,456.627160420 coins with no permanent tail. DAARX issuance ends; NXXXS retains its permanent 0.1 tail. A continuing reward dilutes balances; finite issuance makes future miner income more dependent on fees.</p></div></article><article class="architecture-card"><p class="architecture-number">03</p><div><h3>Judge access as well as the curve.</h3><p>7.77 is symbolic, not proof of fairness. Hardware, electricity, software availability and mining concentration affect who receives coins. Lower launch rewards also reduce early miner income. A nominal floor cannot guarantee security or returns. L10N distributes more than half its finite bonus by peak; DAARX’s later-majority claim does not apply to every curve.</p><p>OPEN’s endowment and NXXXS’s finite founder stream concentrate some issuance with named recipients. Transparent percentages make those tradeoffs inspectable; they do not establish equal opportunity.</p><a class="text-link" href="/faq.html#questions">Explore distribution and allocation questions <span aria-hidden="true">↗</span></a></div></article></div></div></section>'
    fairness_points=[
        ('Privacy for people. Accountability for authority.', 'DAARX and L10N protect ordinary payment amounts and spend membership. OPEN makes delegated authority explicit through distinct Human, Institution and Agent accounts. The design gives people private financial lives while making permissions and obligations inspectable.'),
        ('Give permission without giving everything.', 'OPEN mandates put per-transaction, epoch and lifetime limits on Agent spending. Fees consume the allowance, and each ancestor’s budget applies: delegation cannot multiply spending power. Institutions can use threshold authority. This gives people and organizations a concrete way to authorize useful automation while retaining limits.'),
        ('Pay for the service you choose.', 'Four native roles separate private savings, everyday cash, accountable authority and bonded services. NXXXS service payments go to the selected provider. Ordinary DAARX, L10N and OPEN transfers require no NXXXS purchase or automatic NXXXS fee share. Useful infrastructure earns through chosen work rather than a compulsory toll on sibling activity.'),
        ('Make participation and allocation visible.', 'Delayed issuance gives participation time to develop beyond launch. DAARX and L10N allocate issuance to miners without a premine, presale or founder reward. OPEN discloses its 11% endowment share; NXXXS discloses its finite 2% founder stream. L10N’s continuing baseline supports miner incentives. These rules let participants inspect who is paid and compare the commitments; practical mining access remains part of the fairness test.'),
        ('Share work. Keep the rules independent.', 'RandomX parent work carries child commitments, while each chain checks its own target and native validity rules. Shared mining connects the family without merging its balances or monetary policies. The purpose is coordinated infrastructure with distinct responsibilities and validation boundaries.')
    ]
    fairness='<section class="network-section architecture-section" id="fairness"><div class="network-shell architecture-grid"><header class="section-intro"><p class="section-index">ARCHITECTURE / PEOPLE + INSTITUTIONS + AI</p><h2>Fairness<br><em>by design.</em></h2><p>A stronger foundation puts control in the right hands: private lives, bounded permissions, chosen services and visible economic rules. These are the concrete commitments behind the four-coin architecture.</p><p>This is the design purpose. Private component and composition tests support parts of it; public deployment and qualification of the complete system remain ahead.</p><p class="fine">Principle sources: <a href="https://csrc.nist.gov/Glossary/term/least_privilege">NIST on least privilege</a>; <a href="https://www.getmonero.org/resources/moneropedia/tail-emission.html">Monero on continuing miner incentives</a>. These explain the principles, not validation or endorsement of DAARX.</p></header><div class="architecture-stack">'+''.join('<article class="architecture-card"><p class="architecture-number">0'+str(i+1)+'</p><div><h3>'+title+'</h3><p>'+text+'</p></div></article>' for i,(title,text) in enumerate(fairness_points))+'</div></div></section>'
    supply=charts.issuance_study(COINS,R)
    ending='<section class="network-section showcase-entry"><div class="network-shell"><header class="section-intro"><p class="section-index">05 / TAKE PART</p><h2>More than<br><em>a balance.</em></h2></header><div class="entry-paths"><a href="/testnet.html"><span>01 / MINE</span><h3>Bring computing power.</h3><p>Scheduled block rewards and transaction fees pay for chain security. RandomX parent work carries the three child commitments.</p><b aria-hidden="true">↗</b></a><a href="/nexus.html"><span>02 / OPERATE</span><h3>Do work someone needs.</h3><p>Relay, prove, solve, coordinate settlement. Service providers earn fees from customers who choose their work.</p><b aria-hidden="true">↗</b></a><a href="/daarx.html"><span>03 / OWN + USE</span><h3>Choose the rules you hold.</h3><p>Private savings, spending balances, Agent backing and service collateral give the coins different reasons to be held and used.</p><b aria-hidden="true">↗</b></a></div></div></section><section class="network-section status-section" id="status"><div class="network-shell showcase-development"><header class="section-intro"><p class="section-index">06 / THE BUILD</p><h2>Next stop.<br><em>Public Testnet.</em></h2><p>Private proofs, transfers, wallets and recovery are in place. Reproducible release work and four-chain integration lead into public participation.</p></header><div class="protocol-actions">'+btn('Inside development','/status.html',True)+btn('The participant path','/testnet.html')+'</div></div></section>'
    strip='<section class="signal-strip" aria-label="The four coin roles"><div class="signal-strip-track">'+''.join('<span><b class="'+cl+'">'+c['unit']+'</b> / '+c['role'].upper()+'</span>' for c,cl in zip(COINS,['d','l','o','n']))+'</div></section>'
    return shell('/','DAARX — Money designed for privacy.','Four coins: private capital, private cash, bounded authority and bonded services. Explore the monetary design and the people it pays.',atelier.home_sections(COINS,btn,thesis,switch,ethics,fairness,rationale,supply,ending),'network-home')

def utility_page(name,source):
    body=content(source)
    hero=fragment(body,'page-hero')
    # Keep current factual utility prose, in the original site's typography and shell.
    kind={'status.html':'development','testnet.html':'testnet','break-it.html':'security','mine.html':'hardware','faq.html':'questions','privacy.html':'privacy'}[name]
    utility_scene=scene(kind).replace('<canvas data-prism-canvas aria-hidden="true"></canvas>','<canvas data-prism-canvas aria-hidden="true"></canvas><div class="prism-map" aria-hidden="true">'+utility_diagram(kind)+'</div>')
    enhanced=hero.replace('page-hero','utility-hero')
    enhanced=re.sub(r'<div class="hero-aside">[\s\S]*?</div></div></div><div class="horizon-line"',lambda m:'<div class="hero-aside">'+utility_scene+'</div></div></div><div class="horizon-line"',enhanced)
    action,anchor={'status.html':('Follow the release work','#release-work'),'testnet.html':('Taking part','#participant-path'),'break-it.html':('Explore the layers','#more'),'mine.html':('Explore configurations','#concepts'),'faq.html':('Search the questions','#questions'),'privacy.html':('Read the data register','#data-register')}[name]
    enhanced=enhanced.replace('</p></div><div class="hero-aside">','</p><div class="protocol-actions">'+btn(action,anchor,True)+'</div></div><div class="hero-aside">',1)
    body=body.replace(hero,enhanced)
    if name in ('status.html','testnet.html'):
        body=body.replace('<section class="section">','<section class="section" id="'+anchor[1:]+'">',1)
    title=re.search(r'<title>(.*?)</title>',source).group(1)
    desc=re.search(r'<meta name="description" content="([^"]*)',source).group(1)
    schema=None
    if name=='faq.html':schema=json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>',source,re.S).group(1))
    return shell('/'+name,html.unescape(title),html.unescape(desc),body,'showcase-utility p-'+('mine' if name=='mine.html' else 'break' if name=='break-it.html' else 'daarx'),schema)

def build():
    # The data module remains the sole researched fact collection and print author.
    charts.build_assets(R)
    form=template('hardware-form.fragment')
    pages={'index.html':home()}
    pages.update({c['path'][1:]:coin_page(c) for c in COINS})
    functions={'status.html':facts.status_page,'testnet.html':facts.testnet_page,'break-it.html':facts.security_page,'faq.html':facts.faq_page,'privacy.html':facts.privacy_page,'mine.html':lambda:facts.hardware_page(form)}
    for name,fn in functions.items():pages[name]=utility_page(name,fn())
    qr=re.search(r'<svg[^>]*class="segno"[\s\S]*?</svg>',(R/'flyer.html').read_text()).group()
    pages['flyer.html']=facts.flyer_page(qr).replace('<main class="print-sheet">','<main class="print-sheet"><div class="print-sigil" aria-hidden="true">'+svg('family',True)+'</div>')
    for name,s in pages.items():facts.write_page(name,"\n".join(line.rstrip() for line in s.splitlines()))
    print('Generated12 showcase pages from original design and researched four-coin facts.')
if __name__=='__main__':build()
