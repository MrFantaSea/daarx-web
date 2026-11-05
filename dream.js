/* Local visual studies. No analytics, storage, wallet connection or external API. */
(function () {
  'use strict';
  const doc = document;
  const hero = doc.querySelector('.home-hero');
  const names = ['daarx', 'l10n', 'open', 'nexus'];
  const currents = {
    daarx: ['Own', 'Private capital · Peak issuance near year 7.77'],
    l10n: ['Move', 'Private cash · Permanent miner funding'],
    open: ['Authorize', 'Public accounts · Mandates and HALO'],
    nexus: ['Prove', 'Paid services · Evidence and native collateral']
  };
  let realm = names.indexOf((doc.body.className.match(/(daarx|l10n|open|nexus)-page/) || [])[1]);
  if (realm < 0) realm = 0;
  let paused = doc.body.classList.contains('motion-paused');
  const scenes = [];

  function choose(id) {
    if (!currents[id]) return;
    realm = names.indexOf(id);
    doc.documentElement.dataset.current = id;
    if (hero) {
      hero.dataset.current = id;
      const word = hero.querySelector('[data-realm-word]');
      const caption = hero.querySelector('[data-realm-caption]');
      word.textContent = currents[id][0];
      caption.textContent = currents[id][1];
      const artifact = hero.querySelector('[data-portal-art]');
      artifact.src = '/assets/dream-' + id + '-v1.webp';
      artifact.parentElement.className = 'dream-object ' + id;
      doc.querySelectorAll('[data-realm-choice]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.realmChoice === id)));
    }
    scenes.forEach(scene => scene.paint());
  }
  doc.querySelectorAll('[data-realm-choice]').forEach(button => {
    button.addEventListener('click', () => {
      const tab = doc.getElementById('coin-tab-' + button.dataset.realmChoice);
      if (tab) tab.click();
      choose(button.dataset.realmChoice);
    });
  });
  doc.querySelectorAll('.coin-row[role="tab"]').forEach(tab => {
    tab.addEventListener('click', () => choose(tab.id.replace('coin-tab-', '')));
  });
  // Keyboard-driven tab activation also changes the surrounding material.
  new MutationObserver(() => {
    if (doc.documentElement.dataset.coin) choose(doc.documentElement.dataset.coin);
  }).observe(doc.documentElement, { attributes: true, attributeFilter: ['data-coin'] });
  choose(names[realm]);

  const emission = doc.querySelector('[data-emission]');
  if (emission) {
    const data = JSON.parse(doc.getElementById('emission-data').textContent);
    const range = doc.getElementById('time-range');
    const display = doc.getElementById('time-output');
    const cursor = emission.querySelector('.time-cursor');
    function update() {
      const year = Number(range.value);
      const index = Math.max(0, Math.min(2500, Math.round(year * 100)));
      display.value = year.toFixed(2);
      range.setAttribute('aria-valuetext', year.toFixed(2) + ' target years');
      const x = 56 + year / 25 * 1088;
      cursor.setAttribute('x1', x.toFixed(3));
      cursor.setAttribute('x2', x.toFixed(3));
      names.forEach(id => {
        const value = Number(data.coins[id].rewards[index]);
        emission.querySelector('[data-reward="' + id + '"]').value = value.toLocaleString('en-US', { maximumFractionDigits: value < 1 ? 6 : 3 });
      });
      emission.dataset.year = year.toFixed(2);
    }
    range.addEventListener('input', update);
    const chart = emission.querySelector('.emission-chart');
    chart.addEventListener('pointerdown', event => {
      const box = chart.getBoundingClientRect();
      const ratio = ((event.clientX - box.left) / box.width * 1200 - 56) / 1088;
      range.value = Math.max(.01, Math.min(25, ratio * 25)).toFixed(2);
      update();
    });
    update();
  }

  const work = doc.querySelector('[data-work-study]');
  const pulse = doc.querySelector('[data-work-pulse]');
  let pulseTimer = 0;
  if (work && pulse) pulse.addEventListener('click', () => {
    clearTimeout(pulseTimer);
    work.classList.remove('pulse-active');
    if (!paused) { void work.offsetWidth; work.classList.add('pulse-active'); }
    work.querySelector('[data-work-message]').textContent = 'DAARX target + three child commitments. Each chain checks its own outcome.';
    pulse.setAttribute('aria-pressed', 'true');
    pulseTimer = window.setTimeout(() => { work.classList.remove('pulse-active'); pulse.setAttribute('aria-pressed', 'false'); }, 2700);
  });
  doc.querySelectorAll('[data-inspect]').forEach(button => {
    button.addEventListener('click', () => {
      const scene = button.closest('[data-proof-scene]');
      const active = scene.classList.toggle('inspected');
      scene.querySelectorAll('[data-proof-description]').forEach(detail => { detail.hidden = !active; });
      button.setAttribute('aria-pressed', String(active));
      button.innerHTML = active ? 'Close inspection <span aria-hidden="true">−</span>' : 'Inspect the structure <span aria-hidden="true">＋</span>';
    });
  });

  doc.querySelectorAll('[data-art-object]').forEach(object => {
    const scene = object.closest('section');
    if (!scene) return;
    scene.addEventListener('pointermove', event => {
      if (paused || event.pointerType === 'touch') return;
      const box = scene.getBoundingClientRect();
      const x = Math.max(-.5, Math.min(.5, (event.clientX-box.left)/box.width-.5));
      const y = Math.max(-.5, Math.min(.5, (event.clientY-box.top)/box.height-.5));
      object.style.setProperty('--tilt-x', (-y*10).toFixed(2)+'deg');
      object.style.setProperty('--tilt-y', (x*16).toFixed(2)+'deg');
    }, { passive: true });
    scene.addEventListener('pointerleave', () => {
      object.style.setProperty('--tilt-x','0deg');
      object.style.setProperty('--tilt-y','0deg');
    }, { passive: true });
  });

  // Each scene owns a bounded WebGL canvas over a complete image fallback.
  // The image is the material. Slow refraction, pointer displacement and scroll
  // change its optical field; no scroll interception or cursor replacement.
  const vertexSource = 'attribute vec2 a_position; varying vec2 v_uv; void main(){v_uv=(a_position+1.0)*.5;gl_Position=vec4(a_position,0.,1.);}';
  const fragmentSource = `precision mediump float;
    varying vec2 v_uv;
    uniform sampler2D u_image;
    uniform vec2 u_size;
    uniform vec2 u_imageSize;
    uniform vec2 u_pointer;
    uniform float u_time;
    uniform float u_realm;
    uniform float u_scroll;
    void main(){
      vec2 uv=vec2(v_uv.x,1.0-v_uv.y);
      float aspect=u_size.x/u_size.y;
      float imageAspect=u_imageSize.x/u_imageSize.y;
      vec2 cover=vec2(min(aspect/imageAspect,1.0),min(imageAspect/aspect,1.0));
      uv=(uv-.5)*cover+.5;
      vec2 p=uv-vec2(.65,.5);
      vec2 mouse=uv-u_pointer;
      float dist=length(mouse*vec2(imageAspect,1.0));
      float breathe=sin(u_time*.35+length(p)*9.0)*.003;
      float ripple=sin(dist*23.0-u_time*.85)*exp(-dist*3.5)*.007;
      vec2 flow=vec2(sin(uv.y*9.0+u_time*.21),cos(uv.x*8.0-u_time*.19))*.002;
      vec2 offset=p*(breathe+u_scroll*.009)+flow+mouse*ripple;
      float split=.0006+exp(-dist*5.0)*.0009;
      vec2 q=clamp(uv+offset,vec2(.002),vec2(.998));
      vec3 color=vec3(texture2D(u_image,q+vec2(split,0.)).r,texture2D(u_image,q).g,texture2D(u_image,q-vec2(split,0.)).b);
      vec3 tint=u_realm<.5?vec3(.88,1.0,.90):u_realm<1.5?vec3(1.0,.92,.72):u_realm<2.5?vec3(.72,1.0,1.0):vec3(.88,.74,1.0);
      color=mix(color,color*tint,0.24);
      gl_FragColor=vec4(color,1.0);
    }`;

  doc.querySelectorAll('[data-dream-canvas]').forEach(canvas => {
    const art = canvas.parentElement;
    const img = art.querySelector('img');
    const section = art.closest('section');
    let gl = null, program = null, uniforms = null, ready = false, visible = true;
    let frame = 0, last = -100, clock = 0, pointer = [.65, .5], target = [.65, .5], scroll = 0;
    let stopped = false;
    function stop() { if (frame) cancelAnimationFrame(frame); frame = 0; }
    function draw(time) {
      if (!ready || !gl || stopped) return;
      clock = paused ? 0 : time * .001;
      pointer[0] += (target[0] - pointer[0]) * .08;
      pointer[1] += (target[1] - pointer[1]) * .08;
      gl.useProgram(program);
      gl.uniform2f(uniforms.size, canvas.width, canvas.height);
      gl.uniform2f(uniforms.imageSize, img.naturalWidth, img.naturalHeight);
      gl.uniform2f(uniforms.pointer, pointer[0], pointer[1]);
      gl.uniform1f(uniforms.time, clock);
      gl.uniform1f(uniforms.realm, realm);
      gl.uniform1f(uniforms.scroll, paused ? 0 : scroll);
      gl.drawArrays(gl.TRIANGLES, 0, 6);
    }
    function tick(time) {
      frame = 0;
      if (paused || !visible || doc.hidden || !ready || stopped) return;
      if (time - last > 40) { draw(time); last = time; }
      frame = requestAnimationFrame(tick);
    }
    function start() { if (!frame && ready && visible && !paused && !doc.hidden && !stopped) frame = requestAnimationFrame(tick); }
    function resize() {
      if (!ready) return;
      const box = art.getBoundingClientRect();
      const scale = Math.min(1.25, window.devicePixelRatio || 1, 1500 / Math.max(1, box.width));
      canvas.width = Math.round(box.width * scale);
      canvas.height = Math.round(box.height * scale);
      gl.viewport(0, 0, canvas.width, canvas.height);
      draw(0);
    }
    function initialize() {
      if (ready || stopped || paused || !img.complete || !img.naturalWidth) return;
      try {
        gl = canvas.getContext('webgl', { alpha: false, antialias: false, depth: false, stencil: false, powerPreference: 'low-power' });
        if (!gl) { art.dataset.renderer = 'image'; stopped = true; return; }
        function shader(type, source) {
          const s = gl.createShader(type); gl.shaderSource(s, source); gl.compileShader(s);
          if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error('Visual shader unavailable');
          return s;
        }
        program = gl.createProgram();
        gl.attachShader(program, shader(gl.VERTEX_SHADER, vertexSource));
        gl.attachShader(program, shader(gl.FRAGMENT_SHADER, fragmentSource));
        gl.linkProgram(program);
        if (!gl.getProgramParameter(program, gl.LINK_STATUS)) throw new Error('Visual program unavailable');
        gl.useProgram(program);
        const buffer = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buffer);
        gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]), gl.STATIC_DRAW);
        const attr = gl.getAttribLocation(program, 'a_position'); gl.enableVertexAttribArray(attr); gl.vertexAttribPointer(attr,2,gl.FLOAT,false,0,0);
        const texture = gl.createTexture(); gl.bindTexture(gl.TEXTURE_2D,texture);
        gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_S,gl.CLAMP_TO_EDGE); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_WRAP_T,gl.CLAMP_TO_EDGE);
        gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MIN_FILTER,gl.LINEAR); gl.texParameteri(gl.TEXTURE_2D,gl.TEXTURE_MAG_FILTER,gl.LINEAR);
        gl.texImage2D(gl.TEXTURE_2D,0,gl.RGB,gl.RGB,gl.UNSIGNED_BYTE,img);
        uniforms = {};
        ['size','imageSize','pointer','time','realm','scroll'].forEach(n => { uniforms[n] = gl.getUniformLocation(program,'u_'+n); });
        ready = true; art.dataset.renderer = 'webgl'; resize(); art.classList.add('canvas-ready'); start();
      } catch (_) {
        stop(); stopped = true; art.dataset.renderer = 'image'; art.classList.remove('canvas-ready');
      }
    }
    if (img.complete) initialize(); else img.addEventListener('load', initialize, { once: true });
    art.dataset.renderer = art.dataset.renderer || 'image';
    canvas.addEventListener('webglcontextlost', event => { event.preventDefault(); stop(); stopped = true; art.classList.remove('canvas-ready'); art.dataset.renderer = 'image'; });
    if ('ResizeObserver' in window) new ResizeObserver(resize).observe(art);
    else window.addEventListener('resize', resize, { passive: true });
    if ('IntersectionObserver' in window) new IntersectionObserver(entries => { visible=entries[0].isIntersecting; if (visible) start(); else stop(); }).observe(section);
    section.addEventListener('pointermove', event => {
      if (paused || event.pointerType === 'touch') return;
      const box = art.getBoundingClientRect();
      target = [(event.clientX-box.left)/box.width,(event.clientY-box.top)/box.height];
    }, { passive: true });
    section.addEventListener('pointerleave', () => { target=[.65,.5]; }, { passive: true });
    window.addEventListener('scroll', () => { const box=section.getBoundingClientRect(); scroll=Math.max(-1,Math.min(1,-box.top/Math.max(1,box.height))); }, { passive: true });
    doc.addEventListener('visibilitychange', () => { if (doc.hidden) stop(); else start(); });
    scenes.push({ paint: () => draw(0), motion: () => { if (paused) { stop(); draw(0); } else { initialize(); start(); } } });
  });
  doc.addEventListener('daarx:motion', event => {
    paused = event.detail.paused;
    scenes.forEach(scene => scene.motion());
    if (paused && work) work.classList.remove('pulse-active');
  });
}());
