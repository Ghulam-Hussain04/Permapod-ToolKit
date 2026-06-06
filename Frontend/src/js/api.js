import { state } from '/src/js/state.js';
import {
  buildPostUserMessage,
  buildReplyUserMessage,
  buildRepostUserMessage,
  buildTrendTextUserMessage,
  buildTrendImageUserMessage,
} from '/src/js/prompts.js';

function buildPayload(mode) {
  if (mode === 'post') {
    return { prompt: buildPostUserMessage(), imageBase64: null, imageMime: null };
  }
  if (mode === 'reply') {
    return { prompt: buildReplyUserMessage(), imageBase64: null, imageMime: null };
  }
  if (mode === 'repost') {
    return { prompt: buildRepostUserMessage(), imageBase64: null, imageMime: null };
  }
  if (mode === 'trend' && state.tiMode === 'image') {
    if (!state.imgBase64) {
      throw new Error('Please upload an image first, or switch to Trend input mode.');
    }
    return {
      prompt: buildTrendImageUserMessage(),
      imageBase64: state.imgBase64,
      imageMime: state.imgType,
    };
  }
  if (mode === 'trend') {
    return { prompt: buildTrendTextUserMessage(), imageBase64: null, imageMime: null };
  }
  throw new Error(`Unknown generation mode: ${mode}`);
}

function renderResult(mode, generatedText, isVision) {
  const outEl = document.getElementById('out-' + mode);
  const outText = document.getElementById('otext-' + mode);

  outText.textContent = generatedText;

  const cc = document.getElementById('cc-' + mode);
  cc.textContent = generatedText.length + ' / 280 characters';
  cc.className = 'ci' + (generatedText.length > 280 ? ' warn' : '');
  if (isVision) cc.textContent += '  -  vision model';

  const tagMap = { post: 'tag tg', reply: 'tag tb', repost: 'tag tp', trend: 'tag tam' };
  const voiceMap = {
    post: state.postVoice,
    reply: state.replyVoice,
    repost: state.repostVoice,
    trend: state.trendVoice,
  };
  const tagEl = document.getElementById('tag-' + mode);
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
  btn.innerHTML = '<span class="spin"></span> Generating...';

  try {
    const payload = buildPayload(mode);
    const res = await fetch('/api/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });
    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.error || `Request failed with status ${res.status}`);
    }

    const generatedText = (data.text || '').trim();
    if (!generatedText) {
      throw new Error('Empty response. Try regenerating.');
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

export function saveKeyFromInlineInput() {}
