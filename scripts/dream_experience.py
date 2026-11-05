"""DAARX's interactive visual edition. Retains the site's native form and utilities."""
import json
import experience as E

ROOT = E.ROOT
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
   economics='L10N is money for circulation. Its monetary design keeps a permanent positive mining reward, with fees also going to miners. A continuing security budget is part of the money itself.',
   allocation='All mined. No premine, presale or founder reward. Transaction fees stay with miners; the design does not burn them.',
   numbers=[('∞','positive tail design'),('12','candidate decimal places'),('CTS','shared privacy lineage')],
   monetary='The structure is a declining reward followed by a fixed, nonzero tail. The current reference curve uses 50 L10N per block, declining to 1. Those numeric parameters and the exact blocktime remain candidates while the economic model is reconciled.',
   detail='Spending patterns deserve privacy. The offline-cash work adds receipts, a separate anti-fraud bond and later settlement to the online money.',
   study='Private spending. Verifiable obligations.', nodes=['Private payer','Sealed amount','Payment proof','Private payee']),
 'open': dict(line='Give permission.<br>Keep the limits.', description='Public accounts and bounded authority for people, institutions and agents.',
   rule='Mandates · HALO · receipts', material='ACCOUNTABLE AUTHORITY', word='Authorize',
   emission='A visible allocation.',
   economics='OPEN gives delegated activity its own economic structure. Principals fund agents, mandates limit what they can spend, and HALO puts capital behind Agent value acts.',
   allocation='The current subsidy sends 11% to the endowment and the remainder to miners. The designed dividend is disarmed; its share currently goes to miners.',
   numbers=[('7','maximum mandate depth'),('11%','endowment subsidy share'),('HALO','native Agent backing')],
   monetary='OPEN starts at its highest issuance rate and declines. Its ceiling is 2,718,281,828,459 OPEN, with actual minted supply remaining below it. Base transaction fees burn; priority fees go to miners. Dividend activation is a separate protocol change.',
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
for c in E.COINS:
    c.update(POLICY[c['id']])
    c['economic'] = c['economics']
    c['intro'] = c['description']
    c['story'] = c['detail']


def art(cls='', decorative=True):
    return '<div class="dream-art '+cls+'"'+(' aria-hidden="true"' if decorative else '')+'><picture><source media="(max-width: 600px)" srcset="/assets/dream-gateway-mobile-v1.webp"><img src="'+ART+'" width="1672" height="941" alt="" fetchpriority="high"></picture><canvas data-dream-canvas></canvas><div class="art-vignette"></div></div>'


def symbol(c):
    return '<div class="dream-object '+c['id']+'" data-art-object aria-hidden="true"><img src="/assets/dream-'+c['id']+'-v1.webp" width="640" height="640" alt="" loading="lazy" decoding="async"><i></i></div>'


def header(current):
    nav=[('/#ecosystem','The four coins'),('/#thesis','Issuance'),('/status.html','Development')]
    def link(p,n): return '<a href="'+p+'"'+(' aria-current="page"' if p==current else '')+'>'+n+'</a>'
    return '<a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="/" aria-label="DAARX home">'+E.MARK+'<span>DAARX<span class="brand-dot">.</span></span></a><nav class="desktop-nav" aria-label="Primary">'+''.join(link(*x) for x in nav)+'</nav><div class="header-controls"><button class="motion-toggle header-motion" type="button" data-motion aria-pressed="false" title="Pause or resume visual motion">Pause motion Ⅱ</button><details class="site-menu"><summary>Explore <span aria-hidden="true">＋</span></summary><nav aria-label="All pages">'+''.join(link(c['path'],c['name']) for c in E.COINS)+''.join(link(*x) for x in [('/status.html','Development'),('/testnet.html','Public Testnet'),('/break-it.html','Security'),('/mine.html','Hardware'),('/faq.html','Questions'),('/privacy.html','Privacy')])+'</nav></details></div></div></header>'


OLD_SHELL=E.shell
def shell(path,title,description,body,schema=None,cls=''):
    source=OLD_SHELL(path,title,description,body,schema,cls+' dream')
    source=source.replace('<link rel="stylesheet" href="/site.css">','<link rel="stylesheet" href="/dream.css">')
    source=source.replace('<script src="/site.js" defer></script>','<script src="/site.js" defer></script><script src="/dream.js" defer></script>')
    return source


def intro(kicker,title,text,c='green',aside=''):
    return '<section class="page-hero '+c+'">'+art('inner-art')+'<div class="container"><a class="back-link" href="/">DAARX / '+kicker+'</a><div class="page-hero-grid"><div>'+E.eye(kicker)+'<h1>'+title+'</h1><p class="hero-copy">'+text+'</p></div><div class="hero-aside">'+aside+'</div></div></div><div class="horizon-line" aria-hidden="true"></div></section>'


def issuance_study():
    data=json.loads((ROOT/'data/emission-study.json').read_text())
    colors=['#9af6b4','#f5ce7b','#8aeeed','#c0a0ff']
    paths=[]
    patterns=['','8 5','2 5','12 4 2 4']
    for idx,c in enumerate(E.COINS):
        values=data['coins'][c['id']]['rewards'][::10]; peak=data['coins'][c['id']]['peak']
        pts=' '.join(f'{56+i/(len(values)-1)*1088:.2f},{304-float(v)/peak*246:.2f}' for i,v in enumerate(values))
        paths.append('<polyline data-curve="'+c['id']+'" points="'+pts+'" stroke="'+colors[idx]+'" stroke-dasharray="'+patterns[idx]+'"/>')
    grid=''.join('<line x1="56" y1="'+str(y)+'" x2="1144" y2="'+str(y)+'"/>' for y in [58,181,304])+''.join('<line x1="'+str(56+x/25*1088)+'" y1="40" x2="'+str(56+x/25*1088)+'" y2="304"/>' for x in [0,5,10,15,20,25])
    labels=''.join('<text x="'+str(56+x/25*1088)+'" y="340" text-anchor="middle">'+str(x)+'</text>' for x in [0,5,10,15,20,25])
    chart='<svg class="emission-chart" viewBox="0 0 1200 360" role="img" aria-label="Block rewards over 25 target years, each normalized to its own peak. DAARX and NXXXS rise then fall; L10N and OPEN decline from the start."><g class="chart-grid">'+grid+'</g><g class="chart-curves">'+''.join(paths)+'</g><g class="chart-labels">'+labels+'<text x="28" y="63">100%</text><text x="35" y="309">0</text></g><line class="time-cursor" x1="394" y1="38" x2="394" y2="305"/></svg>'
    return '<section class="section issuance-section" id="thesis"><div class="container"><div class="emission-heading"><div>'+E.eye('THE MONETARY DESIGN')+'<h2>Time changes<br><em>the distribution.</em></h2></div><p>Two delayed peaks. Two curves that begin high.<br>Four different ways to bring money into the world.</p></div><div class="emission-instrument" data-emission><div class="instrument-top"><span>ISSUANCE / 01</span><span>BLOCK REWARD · SHARE OF EACH COIN’S OWN PEAK</span></div>'+chart+'<div class="time-control"><div class="time-label"><label for="time-range">Explore a target year</label><output id="time-output" for="time-range">7.77</output></div><input id="time-range" type="range" min="0.01" max="25" value="7.77" step="0.01"><span>25 years →</span></div><div class="reward-readouts">'+''.join('<div class="'+c['color']+'"><span><svg viewBox="0 0 30 8" aria-hidden="true"><path d="M0 4H30" stroke="currentColor" stroke-width="2" stroke-dasharray="'+patterns[i]+'"/></svg>'+c['unit']+'</span><output data-reward="'+c['id']+'">—</output><small>'+('DIAM' if c['id']=='daarx' else c['unit'])+' / block</small></div>' for i,c in enumerate(E.COINS))+'</div><p class="instrument-note">Height-based schedule study. Curves use each coin’s own scale. L10N and NXXXS use reference candidate parameters. <a href="/daarx.html#issuance">Read the monetary rules ↗</a></p><script type="application/json" id="emission-data">'+json.dumps(data,separators=(',',':'))+'</script></div></div></section>'


def mining_scene():
    return '<section class="section mining-section"><div class="container"><div class="mining-copy">'+E.eye('ONE WORK RESULT / FOUR NATIVE CHAINS')+'<h2>Same work.<br><em>Different worlds.</em></h2><p>RandomX parent work carries the child commitments. Each chain checks its own target and rules.</p><button type="button" class="button primary" data-work-pulse>Trace the work <span aria-hidden="true">↗</span></button></div><div class="work-study" data-work-study><div class="work-source"><span>RandomX</span><small>PARENT WORK</small></div><svg viewBox="0 0 700 430" aria-hidden="true"><defs><linearGradient id="work-spectrum"><stop stop-color="#9af6b4"/><stop offset=".5" stop-color="#8aeeed"/><stop offset="1" stop-color="#c0a0ff"/></linearGradient></defs><g class="work-lines">'+''.join('<path d="M350 50 C350 180 '+str(x)+' 200 '+str(x)+' 335"/>' for x in [75,258,441,624])+'</g><g class="work-pulses">'+''.join('<circle r="5" cx="'+str(x)+'" cy="335"/>' for x in [75,258,441,624])+'</g></svg><div class="work-chains">'+''.join('<a class="'+c['color']+'" href="'+c['path']+'"><i aria-hidden="true"></i><strong>'+c['unit']+'</strong><span>Own state. Own rules.</span></a>' for c in E.COINS)+'</div><p data-work-message aria-live="polite">Independent money. Shared mining architecture.</p></div></div></section>'


def home():
    b='<section class="home-hero" id="top">'+art('hero-art')+'<div class="hero-grain" aria-hidden="true"></div><div class="container hero-grid"><div class="hero-word">'+E.eye('DAARX / L10N / OPEN / NXXXS')+'<h1>Money that minds<br><em>its own business.</em></h1><p class="hero-copy">Private capital. Private cash.<br>Accountable authority. Work with something behind it.</p><div class="actions">'+E.btn('Enter the four coins','#ecosystem',True)+E.btn('Follow the issuance','#thesis')+'</div></div><div class="portal-object" aria-hidden="true"><div class="dream-object daarx" data-art-object><img data-portal-art src="/assets/dream-daarx-v1.webp" width="627" height="580" alt="" decoding="async"></div></div><div class="portal-caption"><span class="portal-coordinate">04 / NATIVE COINS</span><span class="portal-word" data-realm-word>Own</span><p data-realm-caption aria-live="polite">Private capital · Peak issuance near year 7.77</p></div></div><div class="hero-coda container"><div class="realm-choices" role="group" aria-label="Change the visual current">'+''.join('<button type="button" class="'+c['color']+'" data-realm-choice="'+c['id']+'" aria-pressed="'+('true' if i==0 else 'false')+'"><i aria-hidden="true"></i>'+c['unit']+'</button>' for i,c in enumerate(E.COINS))+'</div><a href="#ecosystem">Scroll to explore <span aria-hidden="true">↓</span></a></div></section>'
    b+='<section class="section ecosystem" id="ecosystem"><div class="container"><span id="protocols" class="anchor-alias"></span><div class="section-heading"><p class="index">01 / THE FAMILY</p><h2>Four kinds<br><em>of money.</em></h2><p>Different rules. Different reasons to exist.<br>Choose one. Follow it through.</p></div><div class="coin-explorer" data-tabs><div class="coin-rail" role="tablist" aria-label="Explore the four coins">'
    for i,c in enumerate(E.COINS):
        b+='<button class="coin-row '+c['color']+'" id="coin-tab-'+c['id']+'" type="button" role="tab" aria-selected="'+('true' if i==0 else 'false')+'" aria-controls="coin-panel-'+c['id']+'"><span class="coin-number">0'+str(i+1)+'</span><span><strong>'+c['unit']+'</strong><small>'+c['role']+'</small></span><span class="row-arrow" aria-hidden="true">↗</span></button>'
    b+='</div><div class="coin-panels">'
    for c in E.COINS:
        b+='<div class="coin-panel '+c['color']+'" id="coin-panel-'+c['id']+'" role="tabpanel" aria-labelledby="coin-tab-'+c['id']+'"><div class="realm-object">'+symbol(c)+'</div><div class="realm-description">'+E.eye(c['material'])+'<h3>'+c['line']+'</h3><p>'+c['description']+'</p><p class="realm-rule">'+c['rule']+'</p>'+E.btn('Inside '+c['unit'],c['path'])+'</div></div>'
    b+='</div></div></div></section>'
    b+=issuance_study()+mining_scene()
    b+='<section class="section ways-section"><div class="container"><div class="ways-opening">'+E.eye('PARTICIPATION')+'<h2>The ways in.</h2><p>Mining rewards. Customer payments. Useful work.</p></div><div class="ways-list">'+''.join('<a href="'+href+'"><span>0'+str(i+1)+'</span><div><h3>'+title+'</h3><p>'+copy+'</p></div><span aria-hidden="true">↗</span></a>' for i,(title,copy,href) in enumerate([('Mine.','Earn scheduled block rewards and the applicable miner fees.','/mine.html'),('Build and operate.','Relay, prove, coordinate settlement. Get paid for a service someone uses.','/nexus.html'),('Hold and use.','Choose private capital, spending money or balances for accountable activity.','/daarx.html')]))+'</div></div></section>'
    b+='<section class="section launch-section" id="status"><div class="container launch-grid"><div>'+E.eye('THE NEXT NETWORK MILESTONE')+'<h2>Public Testnet.<br><em>Getting closer.</em></h2><p>Transactions, proofs, wallets and recovery have private implementation behind them. The next release brings the four-coin system to independent participants.</p>'+E.btn('Inside development','/status.html',True)+'</div><div class="launch-emblem" aria-hidden="true">'+symbol(E.COINS[3])+'</div></div></section>'
    return shell('/','DAARX — Money that minds its own business.','Four native coins. Private capital, private cash, accountable authority and paid work backed by collateral.',b,cls='home')


def protocol_study(c):
    descriptions={
      'daarx':['A recipient-specific output key.','Commitments keep the transfer arithmetic checkable.','Prove valid membership without identifying the earlier output.','Authorization and spent tags check spending rights and reject reuse.'],
      'l10n':['Ownership is proved without publishing a sender account.','Ordinary transfer amounts remain hidden.','Native transaction rules validate the spend.','Recipient keys recover the output.'],
      'open':['The principal authorizes the root mandate.','Per-transaction, epoch and lifetime caps bound the debit.','Native HALO backs admitted Agent value acts.','A committed record makes the action inspectable.'],
      'nexus':['The customer specifies a supported service.','The provider commits native capital and capacity.','Evidence is evaluated under the selected client rules.','Service fees go to the selected provider.'],
    }
    return '<section class="section protocol-study '+c['color']+'"><div class="container"><div class="study-opening">'+E.eye('PROTOCOL STUDY')+'<h2>'+c['study']+'</h2><p>'+c['detail']+'</p></div><div class="proof-scene" data-proof-scene><div class="proof-orbit" aria-hidden="true">'+symbol(c)+'</div><div class="proof-nodes">'+''.join('<div><span>0'+str(i+1)+'</span><strong>'+n+'</strong><p data-proof-description hidden>'+descriptions[c['id']][i]+'</p></div>' for i,n in enumerate(c['nodes']))+'</div><button type="button" class="button" data-inspect aria-pressed="false">Inspect the structure <span aria-hidden="true">＋</span></button><p class="proof-caption">'+('Illustration of authority and limits.' if c['id']=='open' else 'Illustration of a service flow; payments go to the provider.' if c['id']=='nexus' else 'Illustration: payment amounts stay sealed; validity is checked.')+'</p></div></div></section>'


def coin_page(c):
    b=intro(c['material'],c['unit'],c['description'],c['color'],'<div class="coin-hero-symbol">'+symbol(c)+'</div>')
    b+='<section class="section coin-thesis" id="economics"><div class="container two-column"><div>'+E.eye('WHY THIS MONEY EXISTS')+'<h2>'+c['line']+'</h2></div><div><p class="large-paragraph">'+c['economics']+'</p><p>'+c['detail']+'</p></div></div></section>'
    b+='<section class="section coin-issuance '+c['color']+'" id="issuance"><div class="container"><div class="policy-title">'+E.eye('ISSUANCE + ALLOCATION')+'<h2>'+c['emission']+'</h2></div><div class="policy-numbers">'+''.join('<div><strong>'+x+'</strong><span>'+y+'</span></div>' for x,y in c['numbers'])+'</div><div class="policy-copy"><p>'+c['monetary']+'</p><p>'+c['allocation']+'</p></div>'+E.btn('Compare the four curves','/#thesis')+'</div></section>'
    b+=protocol_study(c)
    b+='<section class="section dim-section"><div class="container">'+E.heading('03 / DETAILS','Look closer.')+'<div class="inspection" data-tabs><div class="inspection-tabs" role="tablist" aria-label="'+E.esc(c['name'])+' inspection">'
    tabs=[('Money',c['emission'],c['monetary']),('Rules',c['study'],c['detail']),('Wallet','Transactions and recovery.',c['wallet'])]
    for i,(name,title,text) in enumerate(tabs):b+='<button type="button" role="tab" id="inspect-'+c['id']+'-'+str(i)+'" aria-controls="inspect-panel-'+c['id']+'-'+str(i)+'" aria-selected="'+('true' if i==0 else 'false')+'"><span>0'+str(i+1)+'</span>'+name+'</button>'
    b+='</div><div class="inspection-panels">'
    for i,(name,title,text) in enumerate(tabs):b+='<div role="tabpanel" id="inspect-panel-'+c['id']+'-'+str(i)+'" aria-labelledby="inspect-'+c['id']+'-'+str(i)+'"><h3>'+title+'</h3><p>'+text+'</p></div>'
    b+='</div></div></div></section><section class="sibling-section"><div class="container">'+E.eye('FOLLOW ANOTHER CURRENT')+'<div class="sibling-grid">'+''.join('<a class="sibling-link '+x['color']+'" href="'+x['path']+'"><span>'+x['role']+'</span><strong>'+x['unit']+'</strong>'+E.arrow()+'</a>' for x in E.COINS if x['id']!=c['id'])+'</div></div></section>'
    return shell(c['path'],c['name']+' — '+c['role']+' | DAARX',c['description'],b,cls=c['color']+' coin-page '+c['id']+'-page')


def build():
    E.header=header; E.shell=shell; E.intro=intro; E.home=home; E.coin_page=coin_page
    E.FAQ.insert(4,('What does peak issuance mean?','The highest scheduled rate at which new coins enter circulation. DAARX and the NXXXS reference candidate peak near 7.77 target years. OPEN begins at its highest rate. L10N’s current provisional curve declines from its initial reward into a permanent tail.'))
    E.FAQ.insert(5,('Who receives newly issued coins?','DAARX and L10N have no premine, presale or founder reward in the retained monetary policy. OPEN currently allocates 11% to an endowment and the rest to miners, with its dividend disarmed. NXXXS’s reference candidate has a finite 2% founder stream ending before peak; miners receive the remaining subsidy.'))
    E.build()


if __name__=='__main__':build()
