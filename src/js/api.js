/* ═══════════════════════════════════════════════
   api.js — OpenRouter API call handler
   Selects correct model, builds request,
   handles errors and renders output
   ═══════════════════════════════════════════════ */

import { state }                           from '/src/js/state.js';
import { getKey, saveInlineKey,
         OPENROUTER_ENDPOINT,
         TEXT_MODEL, VISION_MODEL }        from '/src/js/config.js';
import { SYSTEM_PROMPT,
         buildPostUserMessage,
         buildReplyUserMessage,
         buildTrendTextUserMessage,
         buildTrendImageUserMessage }      from '/src/js/prompts.js';

/**
 * Main generation function.
 * @param {string} mode — 'post' | 'reply' | 'repost' | 'trend'
 */
export async function gen(mode) {
  const btn     = document.getElementById('btn-' + mode);
  const outEl   = document.getElementById('out-' + mode);
  const outText = document.getElementById('otext-' + mode);

  btn.disabled  = true;
  const origLabel = btn.innerHTML;
  btn.innerHTML = '<span class="spin"></span> Generating...';

  /* ── API key gate ── */
  const apiKey = getKey();
  if (!apiKey) {
    outText.innerHTML = `
      <span style="color:var(--color-text-secondary)">
        No API key found. Paste your OpenRouter key below and click Save.
      </span>
      <div style="margin-top:12px;display:flex;gap:8px">
        <input type="text" id="inline-key-input" placeholder="sk-or-v1-..."
               style="flex:1;font-size:12px">
        <button onclick="window._saveKey()"
                style="padding:6px 12px;font-size:12px;border:0.5px solid var(--color-border-secondary);
                       border-radius:6px;background:var(--color-background-primary);cursor:pointer;
                       color:var(--color-text-primary)">
          Save key
        </button>
      </div>`;
    outEl.className = 'output show';
    btn.disabled = false;
    btn.innerHTML = origLabel;
    return;
  }

  /* ── Build messages and pick model ── */
  let messages   = [];
  let modelToUse = TEXT_MODEL;
  let isVision   = false;

  if (mode === 'post') {
    messages = [{ role: 'user', content: buildPostUserMessage() }];

  } else if (mode === 'reply') {
    messages = [{ role: 'user', content: buildReplyUserMessage() }];

  } else if (mode === 'repost') {
    messages = [{ role: 'user', content: buildRepostUserMessage() }];

  } else if (mode === 'trend') {
    if (state.tiMode === 'image' && state.imgBase64) {
      isVision   = true;
      modelToUse = VISION_MODEL;
      messages   = [{
        role: 'user',
        content: [
          {
            type:      'image_url',
            image_url: { url: `data:${state.imgType};base64,${state.imgBase64}` },
          },
          { type: 'text', text: buildTrendImageUserMessage() },
        ],
      }];
    } else if (state.tiMode === 'trend') {
      messages = [{ role: 'user', content: buildTrendTextUserMessage() }];
    } else {
      outText.textContent = 'Please upload an image first, or switch to Trend input mode.';
      outEl.className     = 'output show';
      btn.disabled        = false;
      btn.innerHTML       = origLabel;
      return;
    }
  }

  /* ── Send to OpenRouter ── */
  try {
    const res = await fetch(OPENROUTER_ENDPOINT, {
      method:  'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': 'Bearer ' + apiKey,
        'HTTP-Referer':  'https://permapod.xyz',
        'X-Title':       'Permapod Content Manager',
      },
      body: JSON.stringify({
        model:       modelToUse,
        max_tokens:  350,
        temperature: 0.9,
        messages: [
          { role: 'system', content: SYSTEM_PROMPT },
          ...messages,
        ],
      }),
    });

    const data = await res.json();

    if (!res.ok) {
      const errMsg  = data?.error?.message || 'Unknown error';
      const errCode = res.status;
      if      (errCode === 401) outText.textContent = 'Invalid API key. Check your OpenRouter key.';
      else if (errCode === 429) outText.textContent = 'Rate limit hit. Free tier: 50 req/day (1000/day after $10 top-up at openrouter.ai).';
      else if (errCode === 503) outText.textContent = 'Model busy. Wait 30 seconds and try again.';
      else if (errCode === 404) outText.textContent = `Model not found: ${modelToUse}. Check openrouter.ai/models for available free models.`;
      else                      outText.textContent = `Error ${errCode}: ${errMsg}`;
      outEl.className = 'output show';
      btn.disabled    = false;
      btn.innerHTML   = origLabel;
      return;
    }

    const generatedText = data.choices?.[0]?.message?.content?.trim() || '';

    if (!generatedText) {
      outText.textContent = 'Empty response. Try regenerating.';
      outEl.className     = 'output show';
      btn.disabled        = false;
      btn.innerHTML       = origLabel;
      return;
    }

    /* ── Render output ── */
    outText.textContent = generatedText;

    const cc = document.getElementById('cc-' + mode);
    cc.textContent = generatedText.length + ' / 280 characters';
    cc.className   = 'ci' + (generatedText.length > 280 ? ' warn' : '');
    if (isVision) cc.textContent += '  ·  vision model';

    const tagMap   = { post: 'tag tg', reply: 'tag tb', repost: 'tag tp', trend: 'tag tam' };
    const voiceMap = {
      post:   state.postVoice,
      reply:  state.replyVoice,
      repost: state.repostVoice,
      trend:  state.trendVoice,
    };
    const tagEl = document.getElementById('tag-' + mode);
    tagEl.className   = tagMap[mode];
    tagEl.textContent = voiceMap[mode] === 'protocol' ? 'Protocol voice' : 'Blip Blop';

    outEl.className = 'output show';

    if (data.usage) {
      console.log(`[Permapod] Tokens — prompt:${data.usage.prompt_tokens} completion:${data.usage.completion_tokens} total:${data.usage.total_tokens} model:${modelToUse}`);
    }

  } catch (e) {
    outText.textContent = 'Network error: ' + e.message;
    outEl.className     = 'output show';
  }

  btn.disabled  = false;
  btn.innerHTML = origLabel;
}

/* ── Inline key save (exposed to window for inline HTML onclick) ── */
export function saveKeyFromInlineInput() {
  const input = document.getElementById('inline-key-input');
  if (!input) return;
  if (saveInlineKey(input.value)) {
    document.getElementById('otext-post').textContent = 'Key saved. Click Generate to try again.';
  }
}
