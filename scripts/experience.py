"""Canonical static authoring module for daarx.money. Standard library only."""

from pathlib import Path
import html
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]

ORIGIN = 'https://daarx.money'

DATE = 'November 6, 2026'

ISO_DATE = '2026-11-06'

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

HARDWARE=[('node','Node Box','299','Node-only concept','Validation'),('compact','Mini Miner','699','Compact miner / node','6–8 kH/s estimate'),('compact','Beefy Mini','1,399','16-core compact concept','16–20 kH/s estimate'),('rig','Standard','1,899','Ryzen 9 5900XT concept','20 kH/s estimate'),('rig','Pro','2,499','Ryzen 9 9950X concept','27 kH/s estimate'),('rig','Pro ACE','2,899','Ryzen 9 9950X3D concept','27 kH/s estimate'),('rig','Pro ACE II','3,299','Dual-CCD 3D-cache study','27 kH/s estimate'),('scale','BIG_DOG','7,499','32-core Threadripper concept','40 kH/s estimate'),('scale','BIG_DOG MAX','10,999','64-core Threadripper concept','84 kH/s estimate')]

def esc(x): return html.escape(str(x), quote=True)

def arrow(): return '<span aria-hidden="true">↗</span>'

def eye(x): return f'<p class="eyebrow">{x}</p>'

def btn(label, href, primary=False): return f'<a class="button{" primary" if primary else ""}" href="{href}">{label} {arrow()}</a>'

def reg(rows): return '<dl class="register">'+''.join(f'<div><dt>{a}</dt><dd>{b}</dd></div>' for a,b in rows)+'</dl>'

def heading(num,title,intro=''): return '<div class="section-heading"><p class="index">'+num+'</p><div><h2>'+title+'</h2>'+('<p class="lede">'+intro+'</p>' if intro else '')+'</div></div>'

def footer():
    return '<footer class="site-footer"><div class="container"><div class="footer-top"><a class="brand" href="/">'+MARK+'<span>DAARX<span class="brand-dot">.</span></span></a><p>DAARX · L10N · OPEN · NXXXS</p><button class="motion-toggle" type="button" data-motion aria-pressed="false">Pause motion <span aria-hidden="true">Ⅱ</span></button></div><div class="footer-links"><nav aria-label="Coins">'+''.join(f'<a href="{c["path"]}">{c["name"]}</a>' for c in COINS)+'</nav><nav aria-label="Project"><a href="/#thesis">Economics</a><a href="/status.html">Development</a><a href="/testnet.html">Public Testnet</a><a href="/break-it.html">Security</a></nav><nav aria-label="Site"><a href="/mine.html">Hardware</a><a href="/faq.html">Questions</a><a href="/flyer.html">Print</a><a href="/privacy.html">Privacy</a><a href="mailto:daarxmoney@proton.me">Contact</a></nav></div><div class="footer-bottom"><p><a href="/status.html">Development / Public Testnet</a><span>DAARX · Desiderata Labs LLC</span></p></div></div></footer>'

def finish(title='There’s more<br><em>under the surface.</em>',text='The architecture, the economics, the work behind it. Follow the thread.',label='Inside the build',url='/status.html'):
    return '<section class="endnote"><div class="container"><h2>'+title+'</h2><div><p>'+text+'</p>'+btn(label,url,True)+'</div></div></section>'

def status_page():
    b=intro('Development','Development','Protocols, native wallets, transaction history and recovery have been exercised in private builds. Public Testnet is the next network milestone.',aside='<p class="aside-statement">'+DATE+'</p>')
    b+='<section class="section"><div class="container"><h2 class="sr-only">Release work</h2><div class="readiness-register">'
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
    b+='<section class="section" id="more"><div class="container"><h2 class="sr-only">Security work</h2><div class="product-columns"><article><h3>Cryptography.</h3><p>Membership proofs, amount commitments and signatures, including their assumptions and integration.</p></article><article><h3>Network.</h3><p>Consensus, mining commitments, transaction rules, history, forks and recovery.</p></article><article><h3>Wallets.</h3><p>Key creation, protected signing, reviewed sends, interrupted submissions, backups and restoration.</p></article></div></div></section>'
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

ART = '/assets/dream-gateway-v1.webp'

POLICY = {
 'daarx': dict(line='Private money.<br>Long horizons.', description='Keep your balance to yourself. Let the rules speak for the supply.',
   rule='Peak issuance · year 7.77', material='PRIVATE CAPITAL', word='Own',
   emission='A later peak. A finite supply.',
   economics='DAARX is private capital with a fixed issuance path. New issuance rises toward year 7.77, then declines through a finite schedule. Most of the supply is still ahead at the peak.',
   allocation='No premine. No presale. No founder reward. Miners receive the block subsidy and transaction fees.',
   numbers=[('7.77','target years to peak'),('111s','target block spacing'),('~100','target years of issuance')],
   monetary='The literal ceiling is 5.083 trillion DIAM, with 12 decimal places. The frozen integer table defines issuance. Per-block rounding leaves a tiny amount below that ceiling. After the finite schedule, miner income comes from transaction fees.',
   detail='Hidden ordinary transfer amounts. Full-chain membership proofs. A public fee ladder that avoids charging a percentage of a hidden payment.',
   study='A valid spend, without opening the balance sheet.', nodes=['One-time destination','Hidden amount','Membership proof','Valid spend']),
 'l10n': dict(line='Money moves.<br>The details don’t.', description='Private cash for the everyday exchange between people.',
   rule='Permanent miner funding', material='PRIVATE CASH', word='Move',
   emission='Security keeps getting paid.',
   economics='L10N is money for circulation. The selected FEM model combines a permanent 1 L10N per paid block with a finite distribution bonus. This keeps a nominal miner incentive after the bonus ends; its purchasing power and actual security depend on participation, costs and demand.',
   allocation='All mined. No premine, presale or founder reward. Transaction fees stay with miners; the design does not burn them.',
   numbers=[('∞','positive tail design'),('12','candidate decimal places'),('CTS','shared privacy lineage')],
   monetary='The selected FEM-20261106-v1 model pays a 1 L10N baseline from the first paid block, plus a bonus rising toward year 7.77 and declining within a finite 77.7-target-year window. The bonus budget is 99,892,796.491812251840 L10N; the baseline continues forever, so supply is uncapped. The block target remains 30 seconds. Consensus integration and release qualification remain pending.',
   detail='Spending patterns deserve privacy. The offline-cash work adds receipts, a separate anti-fraud bond and later settlement to the online money.',
   study='Private spending. Verifiable obligations.', nodes=['Private payer','Sealed amount','Payment proof','Private payee']),
 'open': dict(line='Give permission.<br>Keep the limits.', description='Public accounts and bounded authority for people, institutions and agents.',
   rule='Mandates · HALO · receipts', material='ACCOUNTABLE AUTHORITY', word='Authorize',
   emission='A visible allocation.',
   economics='OPEN gives delegated activity its own economic structure. Principals fund agents, mandates limit what they can spend, and HALO puts capital behind Agent value acts.',
   allocation='The current subsidy sends 11% to the endowment and the remainder to miners. The designed dividend is disarmed; its share currently goes to miners.',
   numbers=[('7','maximum mandate depth'),('11%','endowment subsidy share'),('HALO','native Agent backing')],
   monetary='The selected FEM model rises toward year 7.77, then declines slowly with no permanent tail. Lifetime gross issuance remains exactly 2,718,281,828,456.627160420 OPEN, below the unchanged 2,718,281,828,459 ceiling. Rewards end after height 992,817,450. The block target remains 27 seconds. Base fees burn; priority fees go to miners. Monetary amendment, consensus integration and release qualification remain pending; dividend activation is separate.',
   detail='Per-transaction, per-epoch and lifetime caps apply through the mandate ancestry. Delegating a mandate does not multiply its budget.',
   study='Inspect the authority behind the action.', nodes=['Principal','Mandate + limits','Agent + HALO','Receipt']),
 'nexus': dict(line='Useful work.<br>Something behind it.', description='Proof, relay and settlement services with native collateral behind the commitment.',
   rule='Services · evidence · bonds', material='BONDED ASSURANCE', word='Prove',
   emission='A ramp. A tail. Paid work.',
   economics='NXXXS gives service providers operating balances and collateral, and gives customers a way to pay for useful work. Relayers, proof providers, solvers and venues have distinct roles.',
   allocation='The reference candidate assigns 2% of subsidy to a finite founder stream during roughly seven target years. The stream ends before peak issuance. Miners receive the remaining subsidy.',
   numbers=[('7.77','target years to peak'),('0.1','candidate tail / block'),('2%','finite founder share')],
   monetary='The candidate ramps toward 10 NXXXS per block around year 7.77, then declines to a permanent 0.1 reward. Base fees and rent burn. Priority fees go to miners; service payments go to the chosen provider. Final public identity and parameters remain part of release preparation.',
   detail='A bond is committed capital. A service fee is payment to a provider. A burn removes supply. The protocol accounts for those effects separately.',
   study='A request, evidence and a paid provider.', nodes=['Request','Bonded provider','Work + evidence','Service payment']),
}

for coin in COINS:
    coin.update(POLICY[coin['id']])
    coin['economic']=coin['economics']
    coin['intro']=coin['description']
    coin['story']=coin['detail']

FAQ = FAQ[:4] + [('What does peak issuance mean?', 'The highest scheduled rate of new gross issuance. In the selected FEM model all four curves peak near 7.77 target years, then decline. DAARX and NXXXS are unchanged; L10N and OPEN replace their former launch maxima. Heights and existing epochs govern rewards, so target years are approximate timing, not calendar appointments.'),('Who receives newly issued coins?', 'DAARX and L10N have no premine, presale or founder reward in the retained monetary policy. OPEN currently allocates 11% to an endowment and the rest to miners, with its dividend disarmed. NXXXS’s reference candidate has a finite 2% founder stream ending before peak; miners receive the remaining subsidy.')] + FAQ[4:]

def art(cls='', decorative=True):
    return '<div class="dream-art '+cls+'" aria-hidden="true"><picture><source media="(max-width: 600px)" srcset="/assets/dream-gateway-mobile-v1.webp"><img src="'+ART+'" width="1672" height="941" alt="" fetchpriority="high"></picture><canvas data-dream-canvas></canvas><div class="art-vignette"></div></div>'

def symbol(c):
    return '<div class="dream-object '+c['id']+'" data-art-object aria-hidden="true"><img src="/assets/dream-'+c['id']+'-v1.webp" width="640" height="640" alt="" loading="lazy" decoding="async"><i></i></div>'

def header(current):
    nav=[('/#ecosystem','The four coins'),('/#thesis','Issuance'),('/status.html','Development'),('/testnet.html','Testnet')]
    def link(p,n): return '<a href="'+p+'"'+(' aria-current="page"' if p==current else '')+'>'+n+'</a>'
    return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="/" aria-label="DAARX home">'+MARK+'<span>DAARX<span class="brand-dot">.</span></span></a><nav class="desktop-nav" aria-label="Primary">'+''.join(link(*x) for x in nav)+'</nav><div class="header-controls"><button class="motion-toggle header-motion" type="button" data-motion aria-pressed="false" title="Pause or resume visual motion">Pause motion Ⅱ</button><details class="site-menu"><summary>Explore <span aria-hidden="true">＋</span></summary><nav aria-label="All pages">'+''.join(link(c['path'],c['name']) for c in COINS)+''.join(link(*x) for x in [('/status.html','Development'),('/testnet.html','Public Testnet'),('/break-it.html','Security'),('/mine.html','Hardware'),('/faq.html','Questions'),('/privacy.html','Privacy')])+'</nav></details></div></div></header>'

def intro(kicker,title,text,c='green',aside=''):
    return '<section class="page-hero '+c+'"><div class="container"><a class="back-link" href="/">DAARX / '+kicker+'</a><div class="page-hero-grid"><div>'+eye(kicker)+'<h1>'+title+'</h1><p class="hero-copy">'+text+'</p></div><div class="hero-aside">'+aside+'</div></div></div><div class="horizon-line" aria-hidden="true"></div></section>'

def issuance_study():
    """All chart entrypoints use the same exact-step native-unit renderer."""
    from charts import issuance_study as render_issuance
    return render_issuance(COINS,ROOT)

def mining_scene():
    return '<section class="section mining-section"><div class="container"><div class="mining-copy">'+eye('ONE WORK RESULT / FOUR NATIVE CHAINS')+'<h2>Same work.<br><em>Different worlds.</em></h2><p>RandomX parent work carries the child commitments. Each chain checks its own target and rules.</p><button type="button" class="button primary" data-work-pulse>Trace the work <span aria-hidden="true">↗</span></button></div><div class="work-study" data-work-study><div class="work-source"><span>RandomX</span><small>PARENT WORK</small></div><svg viewBox="0 0 700 430" aria-hidden="true"><defs><linearGradient id="work-spectrum"><stop stop-color="#176747"/><stop offset=".5" stop-color="#126372"/><stop offset="1" stop-color="#6941a7"/></linearGradient></defs><g class="work-lines">'+''.join('<path d="M350 50 C350 180 '+str(x)+' 200 '+str(x)+' 335"/>' for x in [75,258,441,624])+'</g><g class="work-pulses">'+''.join('<circle r="5" cx="'+str(x)+'" cy="335"/>' for x in [75,258,441,624])+'</g></svg><div class="work-chains">'+''.join('<a class="'+c['color']+'" href="'+c['path']+'"><i aria-hidden="true"></i><strong>'+c['unit']+'</strong><span>Own state. Own rules.</span></a>' for c in COINS)+'</div><p data-work-message aria-live="polite">Independent money. Shared mining architecture.</p></div></div></section>'

def home():
    b='<section class="home-hero" id="top">'+art('hero-art')+'<div class="hero-grain" aria-hidden="true"></div><div class="container hero-grid"><div class="hero-word">'+eye('DAARX / L10N / OPEN / NXXXS')+'<h1>Money that<br>minds its own<br><em>business.</em></h1><p class="hero-copy">Private capital. Private cash.<br>Accountable authority. Paid services.</p><div class="actions">'+btn('Four coins','#ecosystem',True)+btn('Issuance','#thesis')+'</div></div><div class="portal-object" aria-hidden="true"><div class="dream-object daarx" data-art-object><img data-portal-art src="/assets/dream-daarx-v1.webp" width="627" height="580" alt="" decoding="async"></div></div><div class="portal-caption"><span class="portal-coordinate">04 / NATIVE COINS</span><span class="portal-word" data-realm-word>Own</span><p data-realm-caption aria-live="polite">Private capital · Peak issuance near year 7.77</p></div></div><div class="hero-coda container"><div class="realm-choices" role="group" aria-label="Choose a coin">'+''.join('<button type="button" class="'+c['color']+'" data-realm-choice="'+c['id']+'" aria-pressed="'+('true' if i==0 else 'false')+'"><i aria-hidden="true"></i>'+c['unit']+'</button>' for i,c in enumerate(COINS))+'</div><a href="#ecosystem">Scroll to explore <span aria-hidden="true">↓</span></a></div></section>'
    b+='<section class="section ecosystem" id="ecosystem"><div class="container"><span id="protocols" class="anchor-alias"></span><div class="section-heading"><p class="index">01 / THE FAMILY</p><h2>Four kinds<br><em>of money.</em></h2><p>Different rules. Different reasons to exist.<br>Choose one. Follow it through.</p></div><div class="coin-explorer" data-tabs><div class="coin-rail" role="tablist" aria-orientation="vertical" aria-label="Explore the four coins">'
    for i,c in enumerate(COINS):
        b+='<button class="coin-row '+c['color']+'" id="coin-tab-'+c['id']+'" type="button" role="tab" aria-selected="'+('true' if i==0 else 'false')+'" aria-controls="coin-panel-'+c['id']+'"><span class="coin-number">0'+str(i+1)+'</span><span><strong>'+c['unit']+'</strong><small>'+c['role']+'</small></span><span class="row-arrow" aria-hidden="true">↗</span></button>'
    b+='</div><div class="coin-panels">'
    for c in COINS:
        b+='<div class="coin-panel '+c['color']+'" id="coin-panel-'+c['id']+'" role="tabpanel" aria-labelledby="coin-tab-'+c['id']+'"><div class="realm-object">'+symbol(c)+'</div><div class="realm-description">'+eye(c['material'])+'<h3>'+c['line']+'</h3><p>'+c['description']+'</p><p class="realm-rule">'+c['rule']+'</p>'+btn('Inside '+c['unit'],c['path'])+'</div></div>'
    b+='</div></div></div></section>'
    b+=issuance_study()+mining_scene()
    b+='<section class="section ways-section"><div class="container"><div class="ways-opening">'+eye('PARTICIPATION')+'<h2>The ways in.</h2><p>Mining rewards. Customer payments. Useful work.</p></div><div class="ways-list">'+''.join('<a href="'+href+'"><span>0'+str(i+1)+'</span><div><h3>'+title+'</h3><p>'+copy+'</p></div><span aria-hidden="true">↗</span></a>' for i,(title,copy,href) in enumerate([('Mine.','Explore mining participation in the coming Testnet. Hardware research has its own catalog.','/testnet.html'),('Build and operate.','Relay, prove, coordinate settlement. Get paid for a service someone uses.','/nexus.html'),('Hold and use.','Choose private capital, spending money or balances for accountable activity.','/daarx.html')]))+'</div></div></section>'
    b+='<section class="section launch-section" id="status"><div class="container launch-grid"><div>'+eye('THE NEXT NETWORK MILESTONE')+'<h2>Public Testnet.<br><em>Getting closer.</em></h2><p>Transactions, proofs, wallets and recovery have private implementation behind them. The next release brings the four-coin system to independent participants.</p>'+btn('Inside development','/status.html',True)+'</div><div class="launch-emblem" aria-hidden="true">'+symbol(COINS[3])+'</div></div></section>'
    return shell('/','DAARX — Money that minds its own business.','Four native coins. Private capital, private cash, accountable authority and paid work backed by collateral.',b,cls='home')

def protocol_study(c):
    descriptions={
      'daarx':['A recipient-specific output key.','Commitments keep the transfer arithmetic checkable.','Prove valid membership without identifying the earlier output.','Authorization and spent tags check spending rights and reject reuse.'],
      'l10n':['Ownership is proved without publishing a sender account.','Ordinary transfer amounts remain hidden.','Native transaction rules validate the spend.','Recipient keys recover the output.'],
      'open':['The principal authorizes the root mandate.','Per-transaction, epoch and lifetime caps bound the debit.','Native HALO backs admitted Agent value acts.','A committed record makes the action inspectable.'],
      'nexus':['The customer specifies a supported service.','The provider commits native capital and capacity.','Evidence is evaluated under the selected client rules.','Service fees go to the selected provider.'],
    }
    return '<section class="section protocol-study '+c['color']+'"><div class="container"><div class="study-opening">'+eye('PROTOCOL STUDY')+'<h2>'+c['study']+'</h2><p>'+{'daarx':'Open the layers of a private spend. Each part has a specific job.', 'l10n':'Follow the online payment path, one layer at a time.', 'open':'Follow a principal’s authority through a mandate to an Agent’s backed action.', 'nexus':'Follow a service request from committed capital to evidence and payment.'}[c['id']]+'</p></div><div class="proof-scene" data-proof-scene><div class="proof-orbit" aria-hidden="true">'+symbol(c)+'</div><div class="proof-nodes" id="proof-details-'+c['id']+'">'+''.join('<div><span>0'+str(i+1)+'</span><strong>'+n+'</strong><p data-proof-description>'+descriptions[c['id']][i]+'</p></div>' for i,n in enumerate(c['nodes']))+'</div><button type="button" class="button" data-inspect aria-pressed="false" aria-expanded="false" aria-controls="proof-details-'+c['id']+'">Inspect the structure <span aria-hidden="true">＋</span></button><p class="proof-caption">'+('Illustration of authority and limits.' if c['id']=='open' else 'Illustration of a service flow; payments go to the provider.' if c['id']=='nexus' else 'Illustration: payment amounts stay sealed; validity is checked.')+'</p></div></div></section>'

def coin_page(c):
    b=intro(c['material'],c['unit'],c['description'],c['color'],'<div class="coin-hero-symbol">'+symbol(c)+'</div>')
    b+='<section class="section coin-thesis" id="economics"><div class="container two-column"><div>'+eye('WHY THIS MONEY EXISTS')+'<h2>'+c['line']+'</h2></div><div><p class="large-paragraph">'+c['economics']+'</p></div></div></section>'
    b+='<section class="section coin-issuance '+c['color']+'" id="issuance"><div class="container"><div class="policy-title">'+eye('ISSUANCE + ALLOCATION')+'<h2>'+c['emission']+'</h2></div><div class="policy-numbers">'+''.join('<div><strong>'+x+'</strong><span>'+y+'</span></div>' for x,y in c['numbers'])+'</div><div class="policy-copy"><p>'+c['monetary']+'</p><p>'+c['allocation']+'</p></div>'+btn('Compare the four curves','/#thesis')+'</div></section>'
    b+=protocol_study(c)
    b+='<section class="section dim-section" id="wallet"><div class="container two-column"><div>'+eye('USING '+c['unit'])+'<h2>Wallet and<br>recovery.</h2></div><div><p class="large-paragraph">'+c['wallet']+'</p><div class="actions">'+btn('Public Testnet','/testnet.html',True)+btn('Development','/status.html')+'</div></div></div></section><section class="sibling-section"><div class="container">'+eye('THE OTHER COINS')+'<div class="sibling-grid">'+''.join('<a class="sibling-link '+x['color']+'" href="'+x['path']+'"><span>'+x['role']+'</span><strong>'+x['unit']+'</strong>'+arrow()+'</a>' for x in COINS if x['id']!=c['id'])+'</div></div></section>'
    return shell(c['path'],c['name']+' — '+c['role']+' | DAARX',c['description'],b,cls=c['color']+' coin-page '+c['id']+'-page')

def shell(path,title,description,body,schema=None,cls=''):
    def asset(name): return '/'+name+'?v='+hashlib.sha256((ROOT/name).read_bytes()).hexdigest()[:12]
    schema=schema or {'@context':'https://schema.org','@type':'WebSite','name':'DAARX','url':ORIGIN,'description':'Four native coins. Private capital, private cash, accountable authority and bonded assurance.'}
    head='<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="theme-color" content="#f0f5ed"><title>'+esc(title)+'</title><meta name="description" content="'+esc(description)+'"><link rel="canonical" href="'+ORIGIN+path+'"><link rel="icon" href="/assets/mark.svg" type="image/svg+xml"><link rel="stylesheet" href="/assets/type.css"><link rel="stylesheet" href="'+asset('dream.css')+'"><meta property="og:type" content="website"><meta property="og:site_name" content="DAARX"><meta property="og:title" content="'+esc(title)+'"><meta property="og:description" content="'+esc(description)+'"><meta property="og:url" content="'+ORIGIN+path+'"><meta property="og:image" content="'+ORIGIN+'/og.png"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630"><meta name="twitter:card" content="summary_large_image"><meta name="twitter:title" content="'+esc(title)+'"><meta name="twitter:description" content="'+esc(description)+'"><meta name="twitter:image" content="'+ORIGIN+'/og.png"><script type="application/ld+json">'+json.dumps(schema,ensure_ascii=False).replace('</',r'<\/')+'</script><script src="'+asset('site.js')+'" defer></script><script src="'+asset('dream.js')+'" defer></script></head>'
    return head+'<body class="mystique '+cls+' dream">'+header(path)+'<main id="main">'+body+'</main>'+footer()+'</body></html>'

def build():
    """Compatibility: all page output now belongs to the original-theme showcase."""
    from showcase import build as build_showcase
    build_showcase()

# Questions remain a fixed collection, composed once rather than inserted at build time.
FAQ_UPDATES={
 'How can people make money with it?':'Miners earn scheduled block rewards and the applicable transaction fees. Service operators can charge for supported relay, proof, execution and settlement work. NXXXS service fees go to the selected provider; OPEN supplies bounded authority for Agent activity.',
 'What could make the coins valuable?':'Useful balances and paid activity. DAARX is private capital with finite issuance. L10N is private spending money with a continuing mining reward. OPEN funds accountable payments and HALO backing. NXXXS pays for services and supplies provider working balances, resource fees and collateral.',
 'Why four separate coins?':'They follow different monetary and accountability rules. DAARX has finite issuance; L10N keeps funding miners through a permanent tail; OPEN supports visible authority and backing; NXXXS coordinates paid services and evidence. Shared mining connects the chains while their supplies and native rules stay distinct.',
 'Why would I hold DAARX?':'For private ownership and a distribution that unfolds over time. DAARX’s issuance peaks around year 7.77, when roughly 22.19% of the literal cap is scheduled to have been issued. The retained monetary policy has no premine, presale or founder reward.'
}
FAQ=[(question,FAQ_UPDATES.get(question,answer)) for question,answer in FAQ]

# These answers use the existing searchable, native-details FAQ and shared JSON-LD.
FAQ += [
 ('Why distribute coins gradually?', 'A slower start leaves more issuance available as participation and software access develop. In the selected model, L10N first-year issuance falls from about 41.89 million to 2.13 million; OPEN falls from about 98.19 billion to 5.64 billion. This reduces the advantage of arriving at launch, but mining access, equipment, electricity costs and concentration still determine who receives coins. Lower early rewards also make launch security an important tradeoff.'),
 ('Does year 7.77 prove fairness?', 'No. The 7.77 and 77.7 motifs are symbolic design choices. Fairness depends on practical access, participation and transparent allocations. A delayed peak does not promise equal ownership, demand, price or returns. L10N has already distributed more than half its finite bonus by peak; the claim that most supply remains after peak applies to DAARX, not automatically to every coin.'),
 ('Does L10N have a supply cap or guaranteed security?', 'L10N remains uncapped. Its selected model adds a finite 77.7-target-year bonus to a permanent 1 L10N baseline per paid block. A nominal floor supports continuing miner incentives, but cannot guarantee sufficient security: reward purchasing power, mining costs, fees and participation matter. Continuing issuance also dilutes existing balances.'),
 ('Does the OPEN remodel create more coins?', 'No. It redistributes the same lifetime gross budget of 2,718,281,828,456.627160420 OPEN over time, with no permanent tail. Cumulative issuance never exceeds the former schedule. The 11% endowment allocation and miner remainder are retained with the dividend disarmed; early endowment receipts fall, and per-block rounding means its exact lifetime receipts differ slightly.'),
 ('What makes an allocation ethical?', 'Disclosure lets people judge the tradeoffs. DAARX and L10N have no premine, presale or founder reward. OPEN directs 11% of subsidy to an endowment, concentrating resources there while reducing the miner share. NXXXS retains its finite 2% founder stream, ending before peak. These are visible policy choices, not proof of fair ownership; who can actually mine matters too.'),
 ('Are the FEM curves already active on a public network?', 'FEM-20261106-v1 is the selected economic reference. Consensus integration, qualification and release remain pending. This explanation does not establish activation, public-network readiness or a mainnet launch.')
]

FAQ += [('Why is this architecture suited to a future of people, institutions and AI?', 'People need private savings and payments. Institutions need shared authority and clear records. AI agents need permission to act within enforceable limits. The four native roles give those needs distinct rules: DAARX for private capital, L10N for private spending, OPEN for accountable authority and NXXXS for chosen bonded services. OPEN delegation consumes ancestor budgets, including fees, so passing authority onward does not create more spending power. Providers earn when customers select their services; ordinary sibling-chain transfers incur no automatic NXXXS toll. Shared mining connects the chains while each validates its own rules. This is a concrete design for useful automation under human and institutional control. Private tests support specific components; complete public deployment remains ahead.')]

if __name__ == '__main__':
    build()
