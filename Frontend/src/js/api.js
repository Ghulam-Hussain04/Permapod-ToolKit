/* ═══════════════════════════════════════════════
   api.js — Backend connection and display logic
   ═══════════════════════════════════════════════ */

import { state } from '/src/js/state.js';
import {
  buildPayload
} from './api_helpers.js'; // Internal extraction handling

function renderResult(mode, generatedText, isVision) {
  const outEl = document.getElementById('out-' + mode);
  const outText = document.getElementById('otext-' + mode);
  const cc = document.getElementById('cc-' + mode);
  const tagEl = document.getElementById('tag-' + mode);

  // Clear past data
  outText.innerHTML = '';

  // Parse double tweet layout structures safely matching the bot's raw formatting
  const tweets = generatedText.split(/Tweet \d+:/gi).map(t => t.trim()).filter(Boolean);

  if (tweets.length >= 2) {
    tweets.forEach((tweetContent, index) => {
      const idx = index + 1;
      const cleanText = tweetContent.replace(/^\[|\]$/g, '').trim();
      
      const tBlock = document.createElement('div');
      tBlock.className = 'tweet-option-block';
      tBlock.style.marginBottom = '16px';
      tBlock.style.borderBottom = index === 0 ? '1px dashed var(--color-border-tertiary)' : 'none';
      tBlock.style.paddingBottom = index === 0 ? '14px' : '0';

      const labelRow = document.createElement('div');
      labelRow.style.display = 'flex';
      labelRow.style.justifyContent = 'space-between';
      labelRow.style.marginBottom = '6px';

      const label = document.createElement('span');
      label.className = 'tag';
      label.style.background = 'var(--color-background-primary)';
      label.style.fontSize = '11px';
      label.textContent = `Option ${idx}`;

      const itemCopy = document.createElement('button');
      itemCopy.className = 'ibtn';
      itemCopy.textContent = '⎘ Copy Option';
      itemCopy.onclick = () => {
        navigator.clipboard.writeText(cleanText);
        itemCopy.textContent = '✓ Copied';
        setTimeout(() => { itemCopy.textContent = '⎘ Copy Option'; }, 1500);
      };

      labelRow.appendChild(label);
      labelRow.appendChild(itemCopy);

      const textBody = document.createElement('div');
      textBody.className = 'otext-body';
      textBody.style.fontFamily = 'var(--font)';
      textBody.style.fontSize = '14px';
      textBody.style.whiteSpace = 'pre-wrap';
      textBody.style.lineHeight = '1.7';
      textBody.textContent = cleanText;

      const metrics = document.createElement('div');
      metrics.className = 'ci';
      metrics.style.fontSize = '11px';
      metrics.style.marginTop = '6px';
      metrics.style.color = cleanText.length > 280 ? '#D85A30' : 'var(--color-text-tertiary)';
      metrics.textContent = `${cleanText.length} / 280 chars`;

      tBlock.appendChild(labelRow);
      tBlock.appendChild(textBody);
      tBlock.appendChild(metrics);
      outText.appendChild(tBlock);
    });

    cc.textContent = 'Dual choices compiled';
  } else {
    // Fallback single layout render wrapper
    outText.textContent = generatedText;
    cc.textContent = `${generatedText.length} / 280 characters`;
    cc.className = 'ci' + (generatedText.length > 280 ? ' warn' : '');
  }

  if (isVision) cc.textContent += '  ·  vision enabled';

  const tagMap = { post: 'tag tg', reply: 'tag tb', repost: 'tag tp', trend: 'tag tam' };
  const voiceMap = {
    post: state.postVoice,
    reply: state.replyVoice,
    repost: state.repostVoice,
    trend: state.trendVoice,
  };
  
  tagEl.className = tagMap[mode];
  tagEl.textContent = voiceMap[mode] === 'protocol' ? 'Protocol voice' : 'Blip Blop';

  outEl.className = 'output show';
}

export async function gen(mode) {
  const btn = document.getElementById('btn-' + mode);
  const outEl = document.getElementById('out-' + mode);
  const outText = document.getElementById('otext-' + mode);

  btn.disabled = true;
  const origLabel = btn.innerHTML;
  btn.innerHTML = '<span class="spin"></span> Generating variants...';

  try {
    const payload = buildPayload(mode);
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || `Failed with status ${res.status}`);
    }

    const generatedText = (data.text || '').trim();
    if (!generatedText) {
      throw new Error('Empty response. Please try spinning it up again.');
    }

    renderResult(mode, generatedText, Boolean(payload.imageBase64));
  } catch (e) {
    outText.textContent = e.message;
    outEl.className = 'output show';
  } finally {
    btn.disabled = false;
    btn.innerHTML = origLabel;
  }
}