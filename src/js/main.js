/* ═══════════════════════════════════════════════
   main.js — App entry point
   Imports all modules, exposes globals for
   inline HTML event handlers, runs init
   ═══════════════════════════════════════════════ */

import { state }                          from '/src/js/state.js';
import { sw, selDay, setV, setP, setRB,
         setHookMode, setClosingMode,
         setTIMode, setTIOutput,
         handleImageUpload, clearImg,
         cp }                             from '/src/js/ui.js';
import { gen, saveKeyFromInlineInput }    from '/src/js/api.js';

/* ── Expose functions to window so inline HTML
   onclick="sw('post')" etc. keep working ── */
window.sw              = sw;
window.selDay          = selDay;
window.setV            = setV;
window.setP            = setP;
window.setRB           = setRB;
window.setHookMode     = setHookMode;
window.setClosingMode  = setClosingMode;
window.setTIMode       = setTIMode;
window.setTIOutput     = setTIOutput;
window.handleImageUpload = handleImageUpload;
window.clearImg        = clearImg;
window.cp              = cp;
window.gen             = gen;
window._saveKey        = saveKeyFromInlineInput;

/* ── Hook radio change handlers ── */
document.querySelectorAll('input[name="hook"]').forEach(r => {
  r.addEventListener('change', () => { state.hook = r.value; });
});
document.querySelectorAll('input[name="closing"]').forEach(r => {
  r.addEventListener('change', () => { state.closing = r.value; });
});

/* ── Image drop zone ── */
const imgInput = document.getElementById('img-input');
if (imgInput) {
  imgInput.addEventListener('change', e => {
    if (e.target.files[0]) handleImageUpload(e.target.files[0]);
  });
}

/* ── Init default UI state ── */
setTIMode('trend');
const firstOutputPill = document.querySelector('#ti-output-pills .pill');
if (firstOutputPill) setTIOutput(firstOutputPill, 'tweet');
