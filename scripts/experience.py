"""Static editorial and experience layer for daarx.money. Standard library only."""
from pathlib import Path
import html
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ORIGIN = 'https://daarx.money'
DATE = 'November 5, 2026'
ISO_DATE = '2026-11-05'

def esc(x): return html.escape(str(x), quote=True)
def arrow(): return '<span aria-hidden="true">↗</span>'
def eye(x): return f'<p class="eyebrow">{x}</p>'
def btn(label, href, primary=False): return f'<a class="button{" primary" if primary else ""}" href="{href}">{label} {arrow()}</a>'
def reg(rows): return '<dl class="register">'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in rows)+'</dl>'
def heading(num,title,intro=''): return '<div class="section-heading"><p class="index">'+num+'</p><div><h2>'+title+'</h2>'+('<p class="lede">'+intro+'</p>' if intro else '')+'</div></div>'

COINS = [{'id': 'daarx',
  'name': 'DAARX',
  'unit': 'DAARX',
  'role': 'Private capital',
  'verb': 'Hold',
  'color': 'green',
  'path': '/daarx.html',
  'short': 'Private savings.',
  'title': 'DAARX',
  'intro': 'DAARX is the one to keep. It combines private ownership with a supply defined by a fixed '
           'emission schedule. That schedule eventually ends.',
  'teaser': 'Private savings. Fixed issuance. Eventually, zero new coins.',
  'story': 'DAARX uses hidden amounts and full-chain membership proofs. The aim is to let someone prove a '
           'valid spend without publishing their balance or payment history.',
  'economic_title': 'Why hold DAARX?',
  'economic': 'The holder’s bet is demand for private capital. The supply follows a known schedule and '
              'eventually stops growing. People have a reason to hold it if they want those properties in '
              'money.',
  'demand': 'Private capital + finite issuance',
  'tabs': [('Supply',
            'The supply follows the code.',
            'DAARX has an integer emission schedule that eventually reaches zero. The schedule defines how '
            'new coins enter circulation.'),
           ('Privacy',
            'A spend can be checked without publishing its history.',
            'Full-chain membership proofs target membership in the valid chain without identifying the '
            'earlier output being spent. Amount commitments keep the arithmetic verifiable while hiding '
            'the amount.'),
           ('Mining',
            'New coins come from mining.',
            'DAARX uses RandomX parent work. The shared architecture also carries child commitments for '
            'L10N, OPEN and NXXXS.')],
  'facts': [('Native coin', 'DAARX'),
            ('Economic role', 'Private capital and long-duration savings'),
            ('Supply design', 'Deterministic integer issuance; eventual zero emission'),
            ('Privacy design', 'Hidden amounts and full-chain membership'),
            ('Current block target', '111 seconds'),
            ('Mining architecture', 'RandomX parent work')],
  'wallet': 'Private wallet builds have exercised creation, reviewed transfers, encrypted backups, '
            'restoration and recovery after an interrupted send.'},
 {'id': 'l10n',
  'name': 'L10N',
  'unit': 'L10N',
  'role': 'Private cash',
  'verb': 'Move',
  'color': 'gold',
  'path': '/l10n.html',
  'short': 'Private spending.',
  'title': 'L10N',
  'intro': 'L10N is the one to spend. Private digital cash for payments between people and businesses, '
           'with an offline-payment layer in development.',
  'teaser': 'Private cash for payments between people and businesses.',
  'story': 'L10N has its own balances, transaction rules and monetary parameters. It shares the family’s '
           'mining architecture and privacy work.',
  'economic_title': 'Why would people need L10N?',
  'economic': 'To pay someone. A spending coin gets demand from people who acquire it to use it, '
              'businesses that accept it, and payments that settle in it. L10N is designed for that role.',
  'demand': 'Payments + settlement',
  'tabs': [('Payments',
            'Private digital cash.',
            'L10N is designed for spending, with native balances and transaction rules. Its purpose is '
            'payment activity between people and businesses.'),
           ('Offline',
            'The offline-payment work.',
            'The offline layer is being developed around the entire payment: loading, in-person exchange, '
            'later settlement and recovery.'),
           ('Wallet',
            'The wallet remembers an interrupted payment.',
            'Pending journals and protected custody retain the information needed to reconcile a '
            'transaction. Native transfer and recovery paths have been exercised in private builds.')],
  'facts': [('Native coin', 'L10N'),
            ('Economic role', 'Private spending and everyday settlement'),
            ('Privacy lineage', 'Shared full-chain privacy work'),
            ('Mining architecture', 'Shared parent work; independent chain rules'),
            ('Wallet foundation', 'Native transfers, custody, journals and recovery'),
            ('Offline cash', 'A separate layer in development')],
  'wallet': 'Native-transfer paths, protected custody, pending-transaction journals and off-host recovery '
            'have private implementation and testing behind them.'},
 {'id': 'open',
  'name': 'OPEN',
  'unit': 'OPEN',
  'role': 'Accountable authority',
  'verb': 'Authorize',
  'color': 'cyan',
  'path': '/open.html',
  'short': 'Public accounts.',
  'title': 'OPEN',
  'intro': 'OPEN is for activity that should be accountable. People, institutions and agents can have '
           'public accounts, defined authority and a record of what they did.',
  'teaser': 'Public accounts and accountable activity for people, institutions and agents.',
  'story': 'OPEN records who can act, the mandate they act under, and the obligations attached to the '
           'action. It includes backing, receipts and restitution in its design.',
  'economic_title': 'What gives OPEN a use?',
  'economic': 'Institutions and software agents need to pay, delegate and account for their actions. OPEN '
              'makes those relationships part of the native system. The demand case is transactions and '
              'activity that need that structure.',
  'demand': 'Transactions + accountable activity',
  'tabs': [('Accounts',
            'People, institutions and agents.',
            'OPEN distinguishes these actors and gives their authority an explicit scope. A mandate '
            'describes who can act, for whom and within which limits.'),
           ('Receipts',
            'A record of the action.',
            'Public transactions and receipts make obligations inspectable. Backing and restitution '
            'connect the action to what stands behind it.'),
           ('Uses',
            'Payments, delegation and agent work.',
            'OPEN supplies the authority side of accountable execution. Institutions can delegate '
            'activity; agents can act under mandates; providers can return evidence of the work.')],
  'facts': [('Native coin', 'OPEN'),
            ('Economic role', 'Accountable human, institutional and agent activity'),
            ('Accounts', 'Public and attributable by design'),
            ('Core objects', 'Mandates, backing, receipts and restitution'),
            ('Wallet foundation', 'Protected signing, transfers and durable outbox'),
            ('Recovery', 'Encrypted backup and restoration')],
  'wallet': 'Private work includes protected signing, supported transfers, a durable outbox and encrypted '
            'recovery, together with agent and mandate components.'},
 {'id': 'nexus',
  'name': 'Nexus / NXXXS',
  'unit': 'NXXXS',
  'role': 'Bonded assurance',
  'verb': 'Commit',
  'color': 'violet',
  'path': '/nexus.html',
  'short': 'Proof and collateral.',
  'title': 'Nexus / NXXXS',
  'intro': 'NXXXS is for paid work between systems: relaying state, proving a payment, carrying out an '
           'instruction or standing behind a service. Providers put native collateral behind their '
           'commitments.',
  'teaser': 'Paid services, proofs and native collateral.',
  'story': 'The protocol connects service requests, evidence and bonded commitments. Relayers, proof '
           'providers, solvers and venues have distinct roles in that system.',
  'economic_title': 'Where does NXXXS demand come from?',
  'economic': 'Providers need NXXXS for operating balances and collateral. Customers use it to pay for '
              'services. Service providers earn those fees. Those uses give the native coin a direct role '
              'in the service economy.',
  'demand': 'Service fees + operating balances + collateral',
  'tabs': [('Services',
            'Work that someone pays for.',
            'Relayers, proof providers, solvers and venues can charge for services in the design. '
            'Consumers pay when they use those services.'),
           ('Collateral',
            'A provider commits NXXXS.',
            'A service declares capacity and obligations, backed by native collateral. The protocol ties '
            'evidence and declared penalties to those commitments.'),
           ('Settlement',
            'The assets stay native.',
            'NXXXS coordinates evidence and service payments across independent systems. Ordinary DAARX, '
            'L10N and OPEN transactions retain their own native rules and fees.')],
  'facts': [('Working identity', 'Nexus / NXXXS · final public name and ticker to be settled'),
            ('Native-unit design', 'NXXXS'),
            ('Economic role', 'Proof, bonded services and settlement coordination'),
            ('Demand paths', 'Service fees, operating balances and collateral'),
            ('Participants', 'Relayers, providers, solvers, venues and developers'),
            ('Wallet foundation', 'Private vault, reviewed transfers and journal recovery')],
  'wallet': 'Private work includes vaults, reviewed transfers, durable journal recovery and selected '
            'operator and service components.'}]

FAQ = [('What is DAARX?',
  'A four-coin system: DAARX for private savings, L10N for private spending, OPEN for public accounts and '
  'accountable activity, and Nexus / NXXXS for paid services backed by proof and native collateral.'),
 ('How can people make money with it?',
  'Mining rewards and service fees are the earning mechanisms in the design. Miners receive new coins '
  'under the block-reward rules. Service operators can charge for relaying, proofs, execution and other '
  'supported work. Holding a coin is a different bet: that people will want to own or use it.'),
 ('What could make the coins valuable?',
  'People wanting them for a reason. DAARX combines private ownership with an issuance schedule that ends. '
  'L10N is meant to circulate in payments. OPEN is used for accountable transactions. NXXXS is used for '
  'service payments, working balances and collateral. If those uses grow, they can create demand.'),
 ('Why four separate coins?',
  'Saving, spending, public accountability and bonded services have different requirements. Each coin has '
  'its own native balances and rules. Shared mining and infrastructure connect them.'),
 ('Why would I hold DAARX?',
  'For private capital with a deterministic issuance path that eventually stops. That is its intended '
  'long-term role in the system.'),
 ('Why would I use L10N?',
  'To make private payments. It is the spending side of the family, with an offline-payment layer being '
  'developed alongside the online chain.'),
 ('Who would use OPEN?',
  'People, institutions and agents that need public accounts, defined authority, mandates and receipts. '
  'OPEN is broader than a coin for machines.'),
 ('Who pays for NXXXS services?',
  'The design includes wallets, merchants, relayers, proof consumers, solvers, venues, institutions and '
  'API providers. Consumers pay for services they choose to use; providers maintain operating balances and '
  'commit native collateral.'),
 ('How does shared mining work?',
  'RandomX parent work satisfies the DAARX target and carries L10N, OPEN and NXXXS child commitments. The '
  'four chains retain independent native state and rules.'),
 ('What has already been built?',
  'Private work has exercised protocol proofs, transactions, authenticated history, wallet creation, '
  'reviewed transfers, encrypted backups and recovery. Shared accounts, games, collectibles and Pride Pot '
  'components are also in development.'),
 ('What is next?',
  'Public Testnet. The participant release will bring the software, network coordinates and starter '
  'instructions together. Current details are on the Development page.'),
 ('Is Nexus another coin after NXXXS?',
  'They refer to the same fourth lineage. Nexus is the working public identity; NXXXS is the native-unit '
  'design. The final public name and ticker are still to be settled.'),
 ('What is the hardware project?',
  'A research catalog of node and mining-system concepts, from compact machines to larger CPU systems, '
  'plus a self-build route. The enquiry form records which concepts people would consider.'),
 ('Who receives a hardware enquiry?',
  'Desiderata Labs LLC receives the information through Web3Forms and Proton. The Privacy page explains '
  'what is sent, how it is used and how to request access, correction or deletion.')]

STATUS=[('01','Proofs, transactions and consensus','Exercised privately','tested','The accepted private source has completed its current proof, wire and consensus cases. Wallet, history and recovery evidence sits alongside that work.'),('02','Current build and integration work','Active','active','The current components are moving through build checks and four-chain integration, with the release configuration taking shape.'),('03','Public source and network setup','In preparation','active','The public source, network identities and authority configuration are being brought together for the participant release.'),('04','Reproducible packages and recovery','In preparation','active','The release work covers reproducible public builds, signatures, supported installation and a way back after interruption.'),('05','The participant toolkit','Next','pending','Network coordinates, test-coin access, observation tools and starter instructions will accompany public entry.')]

MARK='<svg viewBox="0 0 36 36" aria-hidden="true"><path d="M4 8h11l6 6h11M4 18h28M4 28h11l6-6h11"/></svg>'

def header(current):
    nav=[('/#thesis','Economics'),('/#ecosystem','Four coins'),('/status.html','Development'),('/testnet.html','Testnet')]
    def item(path,label): return f'<a href="{path}"'+(' aria-current="page"' if path==current else '')+'>'+label+'</a>'
    return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="/" aria-label="DAARX home">'+MARK+'<span>DAARX<span class="brand-dot">.</span></span></a><nav class="desktop-nav" aria-label="Primary">'+''.join(item(*x) for x in nav)+'</nav><details class="site-menu"><summary>Explore <span aria-hidden="true">＋</span></summary><nav aria-label="All pages">'+''.join(item(c['path'],c['name']) for c in COINS)+''.join(item(*x) for x in [('/status.html','Development'),('/testnet.html','Public Testnet'),('/break-it.html','Security'),('/mine.html','Hardware'),('/faq.html','Questions'),('/privacy.html','Privacy')])+'</nav></details></div></header>'

def footer():
    return '<footer class="site-footer"><div class="container"><div class="footer-top"><a class="brand" href="/">'+MARK+'<span>DAARX<span class="brand-dot">.</span></span></a><p>DAARX · L10N · OPEN · NXXXS</p><button class="motion-toggle" type="button" data-motion aria-pressed="false">Pause motion <span aria-hidden="true">Ⅱ</span></button></div><div class="footer-links"><nav aria-label="Coins">'+''.join(f'<a href="{c["path"]}">{c["name"]}</a>' for c in COINS)+'</nav><nav aria-label="Project"><a href="/#thesis">Economics</a><a href="/status.html">Development</a><a href="/testnet.html">Public Testnet</a><a href="/break-it.html">Security</a></nav><nav aria-label="Site"><a href="/mine.html">Hardware</a><a href="/faq.html">Questions</a><a href="/flyer.html">Print</a><a href="/privacy.html">Privacy</a><a href="mailto:daarxmoney@proton.me">Contact</a></nav></div><div class="footer-bottom"><p><a href="/status.html">Development / Public Testnet</a><span>DAARX · Desiderata Labs LLC</span></p></div></div></footer>'

def shell(path,title,description,body,schema=None,cls=''):
    schema=schema or {'@context':'https://schema.org','@type':'WebSite','name':'DAARX','url':ORIGIN,'description':'Four native coins. Private capital, private cash, accountable authority and bonded assurance.'}
    head='<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#08090b"><title>'+esc(title)+'</title><meta name="description" content="'+esc(description)+'"><link rel="canonical" href="'+ORIGIN+path+'"><link rel="icon" href="/assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/type.css"><link rel="stylesheet" href="/site.css"><meta property="og:type" content="website"><meta property="og:site_name" content="DAARX"><meta property="og:title" content="'+esc(title)+'"><meta property="og:description" content="'+esc(description)+'"><meta property="og:url" content="'+ORIGIN+path+'"><meta property="og:image" content="'+ORIGIN+'/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+esc(title)+'"><meta name="twitter:description" content="'+esc(description)+'"><meta name="twitter:image" content="'+ORIGIN+'/og.png"><script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</',r'<\/')+'</script><script src="/site.js" defer></script></head>'
    return head+'<body class="mystique '+cls+'">'+header(path)+'<main id="main">'+body+'</main>'+footer()+'</body></html>'

def glyph(c): return f'<div class="coin-glyph {c["id"]}" aria-hidden="true"><i></i><i></i><i></i></div>'
def intro(kicker,title,text,c='green',aside=''):
    return f'<section class="page-hero {c}"><div class="container"><a class="back-link" href="/">DAARX / {kicker}</a><div class="page-hero-grid"><div>{eye(kicker)}<h1>{title}</h1><p class="hero-copy">{text}</p></div><div class="hero-aside">{aside}</div></div></div></section>'
def finish(title='There’s more<br><em>under the surface.</em>',text='The architecture, the economics, the work behind it. Follow the thread.',label='Inside the build',url='/status.html'):
    return '<section class="endnote"><div class="container"><h2>'+title+'</h2><div><p>'+text+'</p>'+btn(label,url,True)+'</div></div></section>'

def lens():
    return '<div class="spectrum-lens" data-lens="system"><canvas data-spectrum aria-hidden="true"></canvas><div class="lens-rings" aria-hidden="true"><i></i><i></i><i></i></div><div class="lens-center" aria-hidden="true"><span>◈</span><small>DAARX</small></div>'+''.join(f'<a class="orbit-label orbit-{x}" href="{c["path"]}">{c["unit"]}</a>' for x,c in zip('abcd',COINS))+'</div>'

def home():
    b='<section class="home-hero" id="top"><div class="container hero-grid"><div class="hero-word">'+eye('DAARX / L10N / OPEN / NXXXS')+'<h1>Money that minds<br><em>its own business.</em></h1><p class="hero-copy">Four coins. Private savings, private spending, public accounts and paid work backed by collateral.</p><div class="actions">'+btn('The four coins','#ecosystem',True)+btn('How the economics work','#thesis')+'</div></div>'+lens()+'</div><div class="hero-coda container"><span>DAARX · L10N · OPEN · NEXUS / NXXXS</span><a href="#ecosystem">The system <span aria-hidden="true">↓</span></a></div></section>'
    b+='<section class="section thesis-section" id="thesis"><div class="container"><div class="thesis-opening">'+eye('THE ECONOMICS')+'<h2>What would make<br><em>these coins valuable?</em></h2></div><div class="thesis-body"><p>People using them.</p><p>DAARX gives people a reason to hold private capital. L10N is for money changing hands. OPEN handles activity that needs public accounts and defined authority. NXXXS lets people charge for services and put collateral behind the work.</p><p>Mining rewards and paid services are ways to earn coins in the design. The holder’s bet is that enough people will want to own or use them.</p></div><div class="demand-grid">'+''.join(f'<a class="demand-item {c["color"]}" href="{c["path"]}#economics"><span>{c["unit"]}</span><strong>{c["role"]}</strong><p>{c["demand"]}</p>{arrow()}</a>' for c in COINS)+'</div></div></section>'
    b+='<section class="section ecosystem" id="ecosystem"><div class="container"><span id="protocols" class="anchor-alias"></span>'+heading('01','The four coins.')+'<div class="coin-explorer" data-tabs><div class="coin-rail" role="tablist" aria-label="Explore the four coins">'
    for i,c in enumerate(COINS):b+=f'<button class="coin-row {c["color"]}" id="coin-tab-{c["id"]}" type="button" role="tab" aria-selected="{"true" if i==0 else "false"}" aria-controls="coin-panel-{c["id"]}"><span class="coin-number">0{i+1}</span><span><strong>{c["name"]}</strong><small>{c["role"]}</small></span><span class="row-arrow" aria-hidden="true">↗</span></button>'
    b+='</div><div class="coin-panels">'
    for c in COINS:b+=f'<div class="coin-panel {c["color"]}" id="coin-panel-{c["id"]}" role="tabpanel" aria-labelledby="coin-tab-{c["id"]}">{glyph(c)}{eye(c["name"])}<h3>{c["short"]}</h3><p>{c["teaser"]}</p><p class="small-copy">{c["story"]}</p>{btn("About "+c["name"],c["path"])}</div>'
    b+='</div></div></div></section>'
    b+='<section class="section architecture"><div class="container">'+heading('02','Shared mining.<br>Separate native coins.')+'<div class="architecture-grid"><div class="chain-diagram" role="img" aria-label="RandomX parent work satisfies the DAARX target and carries L10N, OPEN and NXXXS child commitments."><div class="parent-work"><span>PARENT WORK</span><strong>RandomX</strong><small>DAARX target + three child commitments</small></div><div class="chain-branches">'+''.join(f'<div class="{c["color"]}"><span class="chain-dot" aria-hidden="true"></span><strong>{c["unit"]}</strong><small>Native state + rules</small></div>' for c in COINS)+'</div></div><div class="architecture-copy"><h3>Each coin keeps its own rules.</h3><p>Mining work connects the four chains. Their balances, transaction rules and monetary roles stay distinct.</p><p>NXXXS adds service payments, proofs and bonded commitments. Service providers get paid for work customers use. NXXXS supplies the payment and collateral mechanisms.</p>'+btn('NXXXS services','/nexus.html')+'</div></div></div></section>'
    b+='<section class="section participation-section"><div class="container">'+heading('03','Where people fit.')+'<div class="product-columns"><article><span class="small-index">MINING</span><h3>Earn newly issued coins.</h3><p>The block-reward rules define mining rewards. Shared work connects participation across the four-chain architecture.</p></article><article><span class="small-index">SERVICES</span><h3>Charge for useful work.</h3><p>Relaying, proofs, settlement coordination and accountable execution are service roles in the design. Providers can charge fees and commit collateral.</p></article><article><span class="small-index">OWNERSHIP</span><h3>Choose what you want to hold.</h3><p>The reasons differ by coin: private capital, spending balances, accountable activity or the operating needs of a service network.</p></article></div></div></section>'
    b+='<section class="section launch-section" id="status"><div class="container launch-grid"><div>'+eye('DEVELOPMENT')+'<h2>Public Testnet<br><em>is next.</em></h2><p>Private builds have exercised transactions, proofs, wallets, encrypted backups and recovery. The release work now brings the source, network configuration and participant packages together.</p>'+btn('Development details','/status.html',True)+'</div><div class="chapter-art" aria-hidden="true"><span>Ⅰ</span><i></i><i></i><small>DAARX / L10N / OPEN / NXXXS</small></div></div></section>'
    return shell('/','DAARX — Money that minds its own business.','DAARX, L10N, OPEN and NXXXS. Four native coins for private savings, private payments, public accounts and services backed by collateral.',b,cls='home')

def coin_page(c):
    aside=f'<div class="coin-hero-symbol {c["color"]}">{glyph(c)}<span>{c["unit"]}</span></div>'
    b=intro(c['role'],c['title'],c['intro'],c['color'],aside)
    b+='<section class="section" id="economics"><div class="container two-column"><div>'+eye('ECONOMICS')+'<h2>'+c['economic_title']+'</h2></div><div><p class="large-paragraph">'+c['economic']+'</p></div></div></section>'
    b+='<section class="section dim-section" id="architecture"><div class="container">'+heading('01','How it works.')+'<div class="inspection" data-tabs><div class="inspection-tabs" role="tablist" aria-label="'+esc(c['name'])+' inspection">'
    for i,(name,title,text) in enumerate(c['tabs']):b+=f'<button type="button" role="tab" id="inspect-{c["id"]}-{i}" aria-controls="inspect-panel-{c["id"]}-{i}" aria-selected="{"true" if i==0 else "false"}"><span>0{i+1}</span>{name}</button>'
    b+='</div><div class="inspection-panels">'
    for i,(name,title,text) in enumerate(c['tabs']):b+=f'<div role="tabpanel" id="inspect-panel-{c["id"]}-{i}" aria-labelledby="inspect-{c["id"]}-{i}"><h3>{title}</h3><p>{text}</p></div>'
    b+='</div></div></div></section>'
    b+='<section class="section"><div class="container two-column"><div>'+eye('DETAILS')+'<h2>'+c['unit']+'</h2></div>'+reg(c['facts'])+'</div></section>'
    b+='<section class="section dim-section"><div class="container two-column"><div>'+eye('WALLET')+'<h2>Transactions<br>and recovery.</h2></div><div><p class="large-paragraph">'+c['wallet']+'</p>'+btn('Development','/status.html')+'</div></div></section>'
    b+='<section class="sibling-section"><div class="container">'+eye('THE OTHER COINS')+'<div class="sibling-grid">'+''.join(f'<a class="sibling-link {x["color"]}" href="{x["path"]}"><span>{x["role"]}</span><strong>{x["name"]}</strong>{arrow()}</a>' for x in COINS if x['id']!=c['id'])+'</div></div></section>'
    return shell(c['path'],c['name']+' — '+c['role']+' | DAARX',c['teaser'],b,cls=c['color'])

def status_page():
    b=intro('Development','Development','Protocols, native wallets, transaction history and recovery have been exercised in private builds. Public Testnet is the next network milestone.',aside='<p class="aside-statement">'+DATE+'</p>')
    b+='<section class="section"><div class="container"><div class="readiness-register">'
    for num,title,state,cls,text in STATUS:b+=f'<article class="readiness-row"><span class="index">{num}</span><div><h3>{title}</h3><p>{text}</p></div><span class="step-state {cls}">{state}</span></article>'
    b+='</div></div></section>'
    b+='<section class="section dim-section"><div class="container">'+heading('01','Applications.')+'<div class="product-columns"><article><h3>Wallets.</h3><p>Creation, protected signing, reviewed transfers, pending journals, encrypted backup and restoration.</p></article><article><h3>Games and accounts.</h3><p>Shared accounts, Rally, Sunhop, Color Pop, collectibles and Pride Pot components. Game balances are separate from native coins.</p></article><article><h3>Offline payments.</h3><p>L10N’s separate offline track covers loading, exchange, later settlement and recovery.</p></article></div></div></section>'
    b+='<section class="section"><div class="container notes-list"><details><summary>Public Testnet release '+arrow()+'</summary><p>Public participation is in preparation. The release will include supported packages, public network configuration, verification and starter instructions. Testnet coins are for testing and have no monetary value.</p></details><details><summary>Verification and review '+arrow()+'</summary><p>Private results apply to the source and configurations exercised. Current release review, public build reproducibility and four-chain operation remain part of the release work. An independent professional audit has not been completed.</p></details><details><summary>Nexus / NXXXS identity '+arrow()+'</summary><p>Nexus and NXXXS refer to one fourth lineage. Final public naming, ticker and unresolved economic choices are still to be settled. The site describes the system and economic design rather than a current coin offering.</p></details></div></section>'
    return shell('/status.html','Development — DAARX','Current protocol, wallet, application and public Testnet development.',b)

def testnet_page():
    b=intro('Public Testnet','Public Testnet','The participant release brings the software, network coordinates and starter instructions together. The next stage is people running the system on their own machines.')
    b+='<section class="section"><div class="container">'+heading('01','Taking part.')+'<div class="product-columns"><article><h3>Run a node or miner.</h3><p>Follow the chain, validate transactions and use the supported mining paths. The release will state supported platforms and configurations.</p></article><article><h3>Use a test wallet.</h3><p>Create a dedicated wallet, receive test coins, make transfers and work through backup and recovery.</p></article><article><h3>Build and test.</h3><p>Work with the interfaces, investigate behavior and report reproducible findings.</p></article></div></div></section>'
    b+='<section class="section dim-section"><div class="container two-column"><div>'+eye('THE PARTICIPANT RELEASE')+'<h2>What comes<br>with the software.</h2></div>'+reg([('Packages','Supported source and builds, hashes and signatures'),('Network','Configuration, bootstrap peers and observation tools'),('Wallet','Test-coin access, installation and recovery'),('Support','Known issues, release notes and reporting route')])+'</div></section><section class="section"><div class="container"><p>Entry details will be posted here with the release.</p>'+btn('Current development','/status.html',True)+'</div></section>'
    return shell('/testnet.html','Public Testnet — DAARX','The software and information included in the DAARX participant release.',b)

def security_page():
    b=intro('Security','Security','The work covers the cryptography, consensus, software, wallets and the behavior of the system across machines.')
    b+='<section class="section" id="more"><div class="container"><div class="product-columns"><article><h3>Cryptography.</h3><p>Membership proofs, amount commitments and signatures, including their assumptions and integration.</p></article><article><h3>Network.</h3><p>Consensus, mining commitments, transaction rules, history, forks and recovery.</p></article><article><h3>Wallets.</h3><p>Key creation, protected signing, reviewed sends, interrupted submissions, backups and restoration.</p></article></div></div></section>'
    b+='<section class="section dim-section" id="security-network"><div class="container two-column"><div><h2>Builds and review.</h2></div><div><p>Reproducible packages and current integration checks connect the source to what people install. Public Testnet adds independent machines and observations.</p>'+btn('Development details','/status.html')+'</div></div></section>'
    b+='<section class="section" id="security-bounty"><div class="container two-column"><div><h2>Research enquiries.</h2><p><a href="mailto:daarxmoney@proton.me">daarxmoney@proton.me</a></p></div><div class="notes-list" id="security-report"><details><summary>Review status '+arrow()+'</summary><p>Internal testing and release qualification are active. Independent professional audit remains a separate step.</p></details><details><summary>Public research programme '+arrow()+'</summary><p>Scope, reporting instructions, safe-harbor terms, response expectations and confirmed award funding will be published when the programme opens.</p></details><details><summary>Contact details '+arrow()+'</summary><p>The address is for general enquiries. A dedicated vulnerability intake and encryption instructions will be published with the programme. Keep seeds, keys and credentials out of messages.</p></details></div></div></section>'
    return shell('/break-it.html','Security — DAARX','Cryptography, network, wallet and release-security work for the DAARX system.',b)

def faq_page():
    b=intro('Questions','Questions','The four coins, the money, mining and services.')
    b+='<section class="section" id="questions"><div class="container faq-layout"><div class="faq-sidebar"><label for="faq-query">Search</label><input type="search" id="faq-query" placeholder="Mining, money, wallets…" autocomplete="off" aria-describedby="faq-results"><output id="faq-results" for="faq-query" aria-live="polite">'+str(len(FAQ))+' answers</output><p>Other questions?</p><a class="text-link" href="mailto:daarxmoney@proton.me">Email '+arrow()+'</a></div><div class="faq-list">'
    for i,(q,a) in enumerate(FAQ):b+=f'<details class="qa"{" open" if i==0 else ""}><summary>{esc(q)}<span aria-hidden="true">＋</span></summary><div><p>{esc(a)}</p></div></details>'
    b+='<p class="no-results" hidden>Try another word, or clear the search.</p></div></div></section>'
    schema={'@context':'https://schema.org','@type':'FAQPage','mainEntity':[{'@type':'Question','name':q,'acceptedAnswer':{'@type':'Answer','text':a}} for q,a in FAQ]}
    return shell('/faq.html','Questions — DAARX','Questions about the four coins, economic demand, mining rewards, service fees and development.',b,schema)

def privacy_page():
    b=intro('Privacy','Privacy','A short account of what the site collects and where it goes. Reviewed '+DATE+'.')
    rows=[('Who operates the site','Desiderata Labs LLC operates the DAARX information site and hardware-interest form. DAARX is its registered alternate name. Protocol governance and commercial services are separate.'),('Browsing','Pages, fonts and visual effects are served with the site. There are no advertising trackers, analytics scripts, site accounts or marketing cookies. The motion control changes only the current page. GitHub Pages may process ordinary network, device, delivery, security and server-log metadata.'),('Your enquiry','The hardware form sends an email address; optional name; hardware, access-model, membership, accessory and merchandise choices; optional notes; privacy acknowledgment; and delivery metadata. Web3Forms relays the submission and Proton receives the message for Desiderata Labs LLC.'),('Purpose','We use enquiries to understand interest, answer questions, prevent abuse and follow up about a relevant offer or material update. We do not sell personal information or make automated eligibility decisions. A hardware enquiry records interest rather than creating an order or account.'),('Retention','An active interest record is kept only as long as needed, up to 24 months after your last interaction unless a shorter period applies. Provider logs, backups and copies follow provider retention. We delete records we control within 30 days of a verified request unless legal preservation is required.'),('Your choices','Enquiries are optional and free. Ask to access, correct or delete a record, or withdraw from follow-up, at daarxmoney@proton.me. We may verify control of the email address first.'),('Care with information','The form is for adults. Keep payment data, identity documents, wallet seeds and credentials out of the notes. Access is limited to the people and providers needed to operate the enquiry and follow up. Internet transmission and email have ordinary security limits.'),('Changes','This notice covers the current static site and enquiry relay. New account, commerce, support or analytics features require an updated notice before that processing begins.')]
    b+='<section class="section" id="data-register"><div class="container privacy-register">'+''.join(f'<article><h2>{x}</h2><p>{y}</p></article>' for x,y in rows)+btn('Ask about your data','mailto:daarxmoney@proton.me')+'</div></section>'
    return shell('/privacy.html','Privacy — DAARX','How the DAARX site and optional hardware enquiry handle information. Operator, providers, purpose, retention and your choices.',b)

HARDWARE=[('node','Node Box','299','Node-only concept','Validation'),('compact','Mini Miner','699','Compact miner / node','6–8 kH/s estimate'),('compact','Beefy Mini','1,399','16-core compact concept','16–20 kH/s estimate'),('rig','Standard','1,899','Ryzen 9 5900XT concept','20 kH/s estimate'),('rig','Pro','2,499','Ryzen 9 9950X concept','27 kH/s estimate'),('rig','Pro ACE','2,899','Ryzen 9 9950X3D concept','27 kH/s estimate'),('rig','Pro ACE II','3,299','Dual-CCD 3D-cache study','27 kH/s estimate'),('scale','BIG_DOG','7,499','32-core Threadripper concept','40 kH/s estimate'),('scale','BIG_DOG MAX','10,999','64-core Threadripper concept','84 kH/s estimate')]

def hardware_page(form):
    b=intro('Hardware research','Hardware','Node and mining-system concepts, from compact machines to larger CPU systems.',aside='<div class="hardware-sculpture" aria-hidden="true"><i></i><i></i><i></i></div>')
    b+='<section class="section" id="concepts"><div class="container">'+heading('01','Pick your scale.','Planning estimates for the hardware research catalog.')+'<div class="hardware-tabs" data-tabs><div class="inspection-tabs" role="tablist" aria-label="Hardware concept scale">'
    for i,(key,label) in enumerate([('node','Node'),('compact','Compact'),('rig','Rig'),('scale','BIG_DOG')]):b+=f'<button type="button" role="tab" id="tab-{key}" aria-controls="panel-{key}" aria-selected="{"true" if i==0 else "false"}">{label}</button>'
    b+='</div>'
    for key in ['node','compact','rig','scale']:
        b+=f'<div role="tabpanel" id="panel-{key}" aria-labelledby="tab-{key}" class="hardware-panel">'
        for kind,name,price,description,estimate in HARDWARE:
            if kind!=key:continue
            choice=(name+' (32-core)' if name=='BIG_DOG' else name+' (64-core)' if name=='BIG_DOG MAX' else name)+' — est. $'+price
            b+=f'<a class="hardware-row" href="#reserve" data-sku="{esc(choice)}"><div><h3>{name}</h3><p>{description}</p></div><span>{estimate}</span><strong>est. ${price}</strong><span aria-hidden="true">↗</span></a>'
        b+='</div>'
    b+='</div><details class="catalog-note"><summary>About the concept figures '+arrow()+'</summary><p>Prices, configurations and performance figures are unverified research estimates. Final parts, benchmarks, power, noise, availability and commercial terms will accompany an actual offer. Node Box is a validation concept. The ACE studies do not have a verified mining advantage over Pro.</p></details></div></section>'
    b+='<section class="section dim-section" id="self-build"><div class="container two-column"><div>'+eye('02 / THE SELF-BUILD ROUTE')+'<h2>Build your own.</h2><p>A free software image and a vetted parts list are part of the plan. The first participant release will define supported configurations and installation.</p></div>'+reg([('CPU study','Ryzen 9 5900XT · 16 cores'),('Board / memory','B550 ATX / 16 GB dual-channel DDR4'),('Power-supply class','650W Gold-class concept'),('Display / storage','Intel Arc A310 / NVMe SSD'),('Cooling study','Air cooling for continuous operation')])+'</div></section>'
    b+='<section class="section"><div class="container">'+heading('03','Other hardware and service concepts.')+'<div class="product-columns"><article><h3>Access models.</h3><p>Purchase, hosted ownership and rental are among the access models being explored.</p></article><article><h3>Services.</h3><p>Managed support, hosting and community services are also being explored.</p></article><article><h3>Accessories.</h3><p>Status displays, backup plates, release media, merchandise and a Proof-of-Squish three-pack.</p></article></div><div class="accessory-links">'+''.join(f'<a href="#reserve" data-acc="{key}">{label} {arrow()}</a>' for key,label in [('acc_display','Status display'),('acc_coldstorage','Backup plate'),('acc_usb','Release USB'),('acc_merch','Merch'),('acc_squish','Squish three-pack')])+'</div></div></section>'
    b+='<section class="section dim-section" id="reserve"><div class="container two-column"><div>'+eye('04 / HARDWARE ENQUIRIES')+'<h2>Hardware enquiries.</h2><p>Tell us which concepts you would consider. Your enquiry helps shape the hardware research.</p><p class="small-copy">Optional, non-binding hardware interest. Operated by Desiderata Labs LLC. <a href="/privacy.html">How your information is handled</a>.</p></div><div class="form-wrap">'+form+'<p id="f-status" role="status" aria-live="polite" tabindex="-1"></p></div></div></section>'
    return shell('/mine.html','Hardware — DAARX','Compact nodes, larger mining systems and a self-build route. Explore the DAARX hardware research catalog.',b)

def flyer_page(qr):
    return '<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex"><title>DAARX — Money that minds its own business.</title><link rel="stylesheet" href="/assets/type.css"><link rel="stylesheet" href="/print.css"><script src="/print.js" defer></script></head><body><header class="print-toolbar"><a href="/">← DAARX</a><span>Paper <button type="button" data-paper="letter" aria-pressed="true">Letter</button><button type="button" data-paper="a4" aria-pressed="false">A4</button></span><button type="button" data-print>Print ↗</button></header><main class="print-sheet"><p class="print-eyebrow">DAARX / L10N / OPEN / NXXXS</p><h1>Money that minds<br>its own business.</h1><div class="print-coins">'+''.join(f'<section><h2>{c["name"]}</h2><p>{c["role"]}</p><p>{c["teaser"]}</p></section>' for c in COINS)+'</div><p>Mining rewards. Service fees. Private capital. Payments. Four native coins with different economic roles and shared infrastructure.</p><div class="print-bottom"><div class="qr">'+qr+'</div><div><strong>daarx.money</strong><p>The four coins, economics and development.</p><small>'+DATE+'</small></div></div></main></body></html>'

def write_page(name,source):
    source=re.sub(r'&(?![A-Za-z][A-Za-z0-9]+;|#[0-9]+;|#x[0-9A-Fa-f]+;)', '&amp;', source)
    (ROOT/name).write_text(source.replace('><','>\n<')+'\n')

def build():
    form=re.search(r'<form\b[^>]*class="pre"[\s\S]*?</form>',(ROOT/'mine.html').read_text())
    qr=re.search(r'<svg[^>]*class="segno"[\s\S]*?</svg>',(ROOT/'flyer.html').read_text())
    if not form or not qr:raise ValueError('Retained form or QR is missing')
    form_html=form.group(0)
    form_html=re.sub(r'I understand that this is non-binding interest,[\s\S]*?privacy notice</a>\s*\.', 'I’ve read the <a href="/privacy.html">privacy notice</a> and agree to be contacted about this hardware enquiry.', form_html)
    form_html=form_html.replace('Which estimated concept interests you?', 'Which build interests you?').replace('Which possible access model interests you? (optional)', 'Access model (optional)').replace('Interest in a possible membership? (optional)', 'Services (optional)').replace('Interest in possible accessories or merch? (optional)', 'Accessories and merch (optional)')
    pages={'index.html':home(),'status.html':status_page(),'testnet.html':testnet_page(),'break-it.html':security_page(),'faq.html':faq_page(),'privacy.html':privacy_page(),'mine.html':hardware_page(form_html),'flyer.html':flyer_page(qr.group(0))}
    for c in COINS:pages[c['path'][1:]]=coin_page(c)
    for name,body in pages.items():write_page(name,body)
    urls=['/']+['/'+p for p in pages if p not in ['index.html','flyer.html']]
    (ROOT/'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{ORIGIN}{u}</loc><lastmod>{ISO_DATE}</lastmod></url>\n' for u in urls)+'</urlset>\n')
    data={'as_of':ISO_DATE,'stage':'Public Testnet preparation','public_participation_open':False,'native_coin_count':4,'coins':[{'name':c['name'],'unit':c['unit'],'role':c['role'],'working_identity':c['id']=='nexus','economic_thesis':c['demand']} for c in COINS],'work':[{'area':t,'state':s,'description':text} for n,t,s,cl,text in STATUS],'independent_professional_audit_complete':False,'hardware_sales_open':False,'test_coins_have_monetary_value':False}
    (ROOT/'data/release-status.json').write_text(json.dumps(data,indent=2,ensure_ascii=False)+'\n')
    print(f'Generated {len(pages)} pages, {len(FAQ)} questions and {len(urls)} sitemap entries; existing form retained.')
