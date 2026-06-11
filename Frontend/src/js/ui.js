/* ═══════════════════════════════════════════════
   ui.js — All UI helper functions
   Tab switching, voice/pillar selection,
   hook/closing toggles, image handling
   ═══════════════════════════════════════════════ */

import { state } from '/src/js/state.js';

/* ── TAB SWITCHING ─────────────────────────────── */
const TABS = {
  post:    'a-green',
  reply:   'a-blue',
  repost:  'a-purple',
  trend:   'a-amber',
  rules:   'a-gray',
};

export function sw(t) {
  Object.keys(TABS).forEach(k => {
    document.getElementById('tab-' + k).className   = 'nt' + (k === t ? ' ' + TABS[k] : '');
    document.getElementById('panel-' + k).className = 'panel' + (k === t ? ' active' : '');
  });
}

/* ── WEEKLY DAY STRIP (Updated for Parity) ── */
export function selDay(el, type, voice, pillar) {
  document.querySelectorAll('.db').forEach(b => b.classList.remove('active'));
  el.classList.add('active');
  
  // 1. Correctly update the brand voice state and UI selection globally
  setV('post', voice);
  
  // 2. Map and highlight the correct pillar matching the bot's cadence configurations
  const pills = document.querySelectorAll('#post-pills .pill');
  pills.forEach(p => p.classList.remove('sg'));
  
  const match = [...pills].find(p =>
    p.textContent.toLowerCase().includes(pillar.toLowerCase().split(' ')[0])
  );
  if (match) { 
    match.classList.add('sg'); 
    state.postPillar = pillar; 
  }
  
  document.getElementById('day-info-text').textContent =
    el.querySelector('.dn').textContent + ' — ' + type;
  document.getElementById('day-info').style.display = 'inline-flex';
}

/* ── VOICE SELECTION ───────────────────────────── */
export function setV(mode, v) {
  const map = {
    post:   { key: 'postVoice',   prefix: 'pvc',  cls: 'sel-g' },
    reply:  { key: 'replyVoice',  prefix: 'rvc',  cls: 'sel-b' },
    repost: { key: 'repostVoice', prefix: 'rpvc', cls: 'sel-p' },
    trend:  { key: 'trendVoice',  prefix: 'tvc',  cls: 'sel-g' },
  };
  const m = map[mode];
  if (!m) return;
  state[m.key] = v;
  document.getElementById(m.prefix + '-protocol').className = 'vc' + (v === 'protocol' ? ' ' + m.cls : '');
  document.getElementById(m.prefix + '-blipblop').className = 'vc' + (v === 'blipblop'  ? ' ' + m.cls : '');
}

/* ── PILLAR SELECTION ──────────────────────────── */
export function setP(mode, el, p) {
  const map = {
    post:   { key: 'postPillar',   cls: 'sg', id: 'post-pills'   },
    repost: { key: 'repostPillar', cls: 'sp', id: 'repost-pills' },
    trend:  { key: 'trendPillar',  cls: 'sg', id: 'trend-pills'  },
  };
  const m = map[mode];
  if (!m) return;
  state[m.key] = p;
  document.querySelectorAll('#' + m.id + ' .pill').forEach(x => {
    x.classList.remove('sg', 'sp');
  });
  el.classList.add(m.cls);
}

/* ── REPLY BUCKET ──────────────────────────────── */
export function setRB(el, b) {
  state.replyBucket = b;
  ['rb-s', 'rb-d', 'rb-z', 'rb-m'].forEach(id => {
    document.getElementById(id).className = 'pill';
  });
  el.className = 'pill sb';
}

/* ── HOOK / CLOSING TOGGLES ────────────────────── */
export function setHookMode(mode) {
  state.hookMode = mode;
  if (mode === 'ai') {
    state.hook = 'ai';
    document.querySelectorAll('input[name="hook"]').forEach(r => r.checked = false);
  }
  document.getElementById('hook-ai-btn').className   = 'hook-tog' + (mode === 'ai'   ? ' active' : '');
  document.getElementById('hook-pick-btn').className = 'hook-tog' + (mode === 'pick' ? ' active' : '');
  document.getElementById('hook-list').style.display = mode === 'pick' ? 'block' : 'none';
}

export function setClosingMode(mode) {
  state.closingMode = mode;
  if (mode === 'ai') {
    state.closing = 'ai';
    document.querySelectorAll('input[name="closing"]').forEach(r => r.checked = false);
  }
  document.getElementById('closing-ai-btn').className   = 'hook-tog' + (mode === 'ai'   ? ' active' : '');
  document.getElementById('closing-pick-btn').className = 'hook-tog' + (mode === 'pick' ? ' active' : '');
  document.getElementById('closing-list').style.display = mode === 'pick' ? 'block' : 'none';
}

/* ── TREND / IMAGE MODE ────────────────────────── */
export function setTIMode(m) {
  state.tiMode = m;
  document.getElementById('trend-section').style.display = m === 'trend' ? 'block' : 'none';
  document.getElementById('image-section').style.display = m === 'image' ? 'block' : 'none';
  document.getElementById('ti-mode-trend').className = 'pill' + (m === 'trend' ? ' sg' : '');
  document.getElementById('ti-mode-image').className = 'pill' + (m === 'image' ? ' sg' : '');
}

export function setTIOutput(el, v) {
  state.tiOutput = v;
  document.querySelectorAll('#ti-output-pills .pill').forEach(p => {
    p.classList.remove('sg');
  });
  el.classList.add('sg');
}

/* ── IMAGE HANDLING ────────────────────────────── */
export function handleImageUpload(file) {
  if (!file) return;
  const reader = new FileReader();
  reader.onload = e => {
    const dataUrl = e.target.result;
    state.imgBase64 = dataUrl.split(',')[1];
    state.imgType   = file.type;

    const preview = document.getElementById('img-preview');
    preview.src = dataUrl;
    preview.style.display = 'block';
    document.getElementById('img-placeholder').style.display = 'none';
    document.getElementById('img-drop').classList.add('has-img');
    document.getElementById('img-clear').style.display = 'inline-flex';
  };
  reader.readAsDataURL(file);
}

export function clearImg() {
  state.imgBase64 = null;
  state.imgType   = null;
  document.getElementById('img-preview').style.display     = 'none';
  document.getElementById('img-placeholder').style.display = 'block';
  document.getElementById('img-drop').classList.remove('has-img');
  document.getElementById('img-clear').style.display       = 'none';
  document.getElementById('img-input').value = '';
}

/* ── COPY TO CLIPBOARD ─────────────────────────── */
export function cp(textId, btnId) {
  navigator.clipboard.writeText(
    document.getElementById(textId).textContent
  ).then(() => {
    const b    = document.getElementById(btnId);
    const orig = b.innerHTML;
    b.innerHTML = '✓ Copied';
    setTimeout(() => { b.innerHTML = orig; }, 2000);
  });
}
