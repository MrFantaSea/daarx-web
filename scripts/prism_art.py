"""Deterministic native-vector companions to the original DAARX graphics."""
from math import sin,cos,pi

SCENES={
'family':('THE FAMILY',[
 ('Four native coins','Saving, spending, authority and services. Each coin has its own balances and monetary rules.','Coins'),
 ('One work result','RandomX parent work carries the L10N, OPEN and NXXXS child commitments.','Mining'),
 ('Independent rules','Each chain checks its own target and native state. Shared work connects them.','Rules')]),
'daarx':('PRIVATE CAPITAL',[
 ('A balance is personal','Hidden amounts and full-chain membership proofs keep ordinary payment details off the public balance sheet.','Privacy'),
 ('A distribution that takes time','Issuance peaks near target year 7.77. About 22.19% of the literal ceiling is scheduled by then.','The peak'),
 ('Eventually, zero new coins','The finite integer schedule winds down after about 100 target years. Transaction fees then pay miners.','The horizon')]),
'l10n':('PRIVATE CASH',[
 ('Money for passing on','Private amounts and native spending rules serve everyday circulation.','Circulate'),
 ('Security keeps getting paid','The monetary design keeps a permanent positive mining tail. Issuance and fees go to miners.','Secure'),
 ('Beyond the connection','The offline layer is being developed around local exchange, receipts, later settlement and recovery.','Settle')]),
'open':('BOUNDED AUTHORITY',[
 ('Someone gives the permission','Human, Institution and Agent are distinct native account classes. Institutions use threshold authority.','Principal'),
 ('Permission has a budget','Per-transaction, epoch and lifetime caps follow the mandate ancestry. Delegation cannot multiply the allowance.','Mandate'),
 ('Capital behind the action','HALO backs admitted Agent value acts. Public accounts and committed records make authority inspectable.','Agent')]),
'nexus':('BONDED SERVICES',[
 ('A customer asks for work','Relays, proofs, solvers and settlement services give the native coin a job to do.','Request'),
 ('A provider commits capital','Native collateral backs declared capacity and obligations. A bond is committed capital.','Commit'),
 ('Evidence, then payment','Supported service rules connect the work to evidence. Service fees go to the chosen provider.','Prove')]),
'development':('THE BUILD',[
 ('The source behind the system','Private protocol, transaction, history, wallet and recovery work feeds the participant release.','Source'),
 ('From code to packages','Current release work connects source, reproducible builds, verification and installation.','Build'),
 ('Independent machines','Public Testnet preparation brings the four-coin system to people running it themselves.','Join')]),
 'testnet':('PUBLIC TESTNET',[
 ('Follow the chains','The participant release will include supported node and mining paths with network coordinates.','Run'),
 ('Put the rules to work','Dedicated test wallets and test-coin access support transfers across the system.','Transact'),
 ('Make a way back','Backup, interrupted sends and restoration belong in the participant journey.','Recover')]),
'security':('SECURITY',[
 ('Validity has a structure','Membership proofs, amount commitments and signatures connect privacy to verifiable rules.','Prove'),
 ('The rules meet the network','Consensus, mining commitments, transaction history and forks must agree across machines.','Check'),
 ('Ownership survives interruption','Protected signing, reviewed sends, pending journals and encrypted backups support recovery.','Recover')]),
'hardware':('HARDWARE RESEARCH',[
 ('A place on the network','The node concept begins with following and validating the chains.','Node'),
 ('A smaller footprint','Compact CPU-system concepts explore the space between a node and a larger mining build.','Compact'),
 ('More room for work','The larger research configurations explore CPU capacity, cooling and system scale.','Scale')]),
'questions':('QUESTIONS',[
 ('Why four?','Different monetary and accountability rules give each coin a different purpose.','Coins'),
 ('Who earns the issuance?','Miners earn scheduled block rewards and the applicable transaction fees. Allocation differs by coin.','Mining'),
 ('What gets paid for?','Supported relay, proof, execution and settlement work connects customers to service providers.','Services')]),
'privacy':('SITE PRIVACY',[
 ('Just visiting','The static site has no advertising trackers, analytics scripts or marketing cookies. Hosting processes ordinary delivery metadata.','Browse'),
 ('An optional enquiry','The hardware form passes your enquiry through Web3Forms to Proton for Desiderata Labs LLC.','Enquire'),
 ('Your record, your choice','You can request access, correction or deletion and withdraw from follow-up. The Privacy page gives the details.','Choose')])
}

def shape(kind,t,u):
    a=2*pi*t;b=2*pi*u
    if kind=='l10n':return (1.25*sin(a),.72*sin(2*a),.4*cos(a+b))
    if kind=='open':return ((.55+.42*u)*cos(a),(.65+.32*u)*sin(a),.4*sin(3*a)+.25*cos(b))
    if kind=='nexus':
        q=(t*4)%1;side=int(t*4)%4;verts=[(-1,0,0),(0,-1,.4),(1,0,0),(0,1,-.4),(-1,0,0)];v=verts[side];w=verts[side+1];return tuple((v[i]*(1-q)+w[i]*q)*(1-.4*u) for i in range(3))
    if kind=='hardware':return (cos(a)*(.45+.55*u),sin(a)*(.45+.55*u),.42*sin(4*a+b))
    if kind=='testnet':return ((.5+.45*cos(3*a+b))*cos(a),(.5+.45*cos(3*a+b))*sin(a),.45*sin(3*a+b))
    if kind=='development':return (1.15*cos(a),.55*sin(2*a+b),.35*sin(a+b))
    if kind=='security':return (cos(a)*(.58+.3*u),sin(a)*(.58+.3*u),.45*cos(5*a+b))
    if kind=='questions':return (cos(a)*(.4+.65*t),sin(a)*(.4+.65*t),.45*sin(a*3+b))
    if kind=='privacy':return (cos(a)*(.5+.4*cos(3*a+b)),sin(a)*(.5+.4*cos(3*a+b)),.52*sin(3*a+b))
    if kind=='daarx':return ((.6+.33*cos(4*a))*cos(a),(.6+.33*cos(4*a))*sin(a),.48*sin(a+b))
    return ((.75+.25*cos(3*a+b))*cos(a),(.75+.25*cos(3*a+b))*sin(a),.5*sin(3*a+b))

def svg(kind,print_mode=False):
    prefix='prism-'+kind+('-paper' if print_mode else '')
    colors=['#80ffc0','#ffe1a3','#92ecff','#d2adff'] if not print_mode else ['#146941','#946411','#12657b','#6a3998']
    paths=[]
    for k in range(28):
        u=k/28;pts=[]
        for j in range(97):
            t=j/96;x,y,z=shape(kind,t,u);angle=u*pi*.45
            x,z=x*cos(angle)+z*sin(angle),-x*sin(angle)+z*cos(angle)
            scale=145/(1+z*.17);pts.append(f'{260+x*scale:.1f},{205+y*scale:.1f}')
        paths.append('<polyline points="'+' '.join(pts)+'" stroke="url(#'+prefix+'-'+str(k%4)+')" stroke-width="'+str(1.1+(k%3)*.25)+'" opacity=".85"/>')
    gradients=''.join('<linearGradient id="'+prefix+'-'+str(i)+'" x1="0" y1="0" x2="1" y2="1"><stop stop-color="'+c+'"/><stop offset=".47" stop-color="'+colors[(i+1)%4]+'"/><stop offset="1" stop-color="'+colors[(i+2)%4]+'"/></linearGradient>' for i,c in enumerate(colors))
    return '<svg class="prism-fallback" viewBox="0 0 520 410" fill="none" aria-hidden="true" focusable="false"><defs>'+gradients+'</defs><g stroke-linecap="round" stroke-linejoin="round">'+''.join(paths)+'</g></svg>'

def scene(kind):
    eyebrow,stages=SCENES[kind]
    import html,json
    esc=html.escape
    return '<figure class="prism-scene" data-prism-scene="'+kind+'" data-prism-state="0" data-prism-renderer="svg" data-prism-frames="0" data-prism-content="'+esc(json.dumps(stages,ensure_ascii=False),quote=True)+'">'+svg(kind)+'<canvas data-prism-canvas aria-hidden="true"></canvas><span class="prism-coordinate" aria-hidden="true">'+eyebrow+' / 0<span data-prism-index>1</span></span><figcaption class="prism-caption"><strong data-prism-title>'+esc(stages[0][0])+'</strong><p data-prism-copy aria-live="polite" aria-atomic="true">'+esc(stages[0][1])+'</p><div class="prism-controls" role="group" aria-label="Explore '+eyebrow.lower()+'">'+''.join('<button type="button" data-prism-step="'+str(i)+'" aria-pressed="'+str(i==0).lower()+'">'+esc(stage[2])+'</button>'for i,stage in enumerate(stages))+'</div></figcaption></figure>'


def utility_diagram(kind):
    """Readable native schematics give the optical field a subject."""
    common='<g font-family="monospace" font-size="11" letter-spacing=".7" text-anchor="middle" fill="#e1f7e6">'
    def box(x,y,w,h,label,color):
        return f'<rect x="{x-w/2}" y="{y-h/2}" width="{w}" height="{h}" rx="3" fill="#081a15" fill-opacity=".88" stroke="{color}" stroke-width="1.5"/><text x="{x}" y="{y+4}">{label}</text>'
    def line(a,b,color,extra=''):
        return f'<path d="M{a[0]} {a[1]}L{b[0]} {b[1]}" fill="none" stroke="{color}" stroke-width="1.5" {extra}/>'
    body=''
    if kind=='privacy':
        body+=line((120,205),(260,120),'#83eac5','stroke-dasharray="3 5"')+line((260,120),(400,205),'#91dfff','stroke-dasharray="3 5"')+line((120,205),(220,302),'#d6b2ff','stroke-dasharray="2 6"')
        body+=box(105,205,100,40,'BROWSER','#89ffbe')+box(260,120,122,40,'WEB3FORMS','#ffdd96')+box(405,205,100,40,'PROTON','#94eaff')+box(275,302,148,40,'HOSTING METADATA','#cbb1ff')
        body+='<text x="265" y="88" fill="#d8efdc" font-size="10">OPTIONAL ENQUIRY</text>'
    elif kind=='testnet':
        for i,(x,y,label,col) in enumerate([(115,100,'DAARX','#89ffbe'),(405,100,'L10N','#ffdd96'),(115,310,'OPEN','#94eaff'),(405,310,'NXXXS','#cbb1ff')]):
            body+=line((260,205),(x,y),col,'stroke-dasharray="4 6"')+box(x,y,100,40,label,col)
        body+=box(260,205,150,62,'YOUR MACHINE','#dcf7de')
    elif kind=='security':
        for i,(label,col) in enumerate([('PROOFS','#89ffbe'),('NETWORK','#94eaff'),('WALLET','#cbb1ff')]):
            x=260;y=105+i*100;body+=box(x,y,250-i*40,56,label,col)
            if i<2:body+=line((x,y+28),(x,y+72),col)
    elif kind=='hardware':
        body+='<rect x="140" y="62" width="240" height="290" rx="5" fill="#081a1555" stroke="#e9c88d" stroke-width="1.5"/><rect x="170" y="90" width="180" height="230" fill="none" stroke="#91dfff" stroke-opacity=".6"/>'
        body+=box(260,180,116,90,'CPU','#ffdd96')
        for i in range(8):
            x=210+i*14;body+=line((x,120),(x,105),'#89ffbe')+line((x,240),(x,255),'#cbb1ff')
        body+='<text x="260" y="284" fill="#dce9cd">MEMORY / COOLING</text><text x="260" y="342" fill="#cbe1d2" font-size="10">CONFIGURATION STUDY</text>'
    elif kind=='development':
        for i,(label,col) in enumerate([('PROOFS','#89ffbe'),('INTEGRATION','#ffdd96'),('RELEASE','#94eaff'),('RECOVERY','#cbb1ff'),('PARTICIPATION','#b4fac9')]):
            y=75+i*65;body+=line((105,y),(425,y),col,'stroke-dasharray="4 5"')+box(260,y,156,32,label,col)
            body+=f'<circle cx="105" cy="{y}" r="4" fill="{col}"/><circle cx="425" cy="{y}" r="4" fill="{col}"/>'
    elif kind=='questions':
        for x,y,label,col in [(130,120,'COINS','#89ffbe'),(390,120,'MINING','#ffdd96'),(130,290,'WALLETS','#94eaff'),(390,290,'SERVICES','#cbb1ff')]:
            body+=line((260,205),(x,y),col,'stroke-dasharray="3 5"')+box(x,y,110,42,label,col)
        body+='<text x="260" y="210" font-size="36" fill="#efffe7">?</text>'
    else:return ''
    return '<svg class="utility-schematic" viewBox="0 0 520 410" aria-hidden="true" focusable="false">'+common+body+'</g></svg>'
