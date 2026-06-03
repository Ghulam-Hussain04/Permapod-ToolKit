/* ═══════════════════════════════════════════════
   config.js — API configuration
   Reads the API key injected by the server at
   build time via index.html template substitution.
   Falls back to localStorage for local dev.
   ═══════════════════════════════════════════════ */

export const OPENROUTER_ENDPOINT = 'https://openrouter.ai/api/v1/chat/completions';

/*
  TWO MODELS:
  - TEXT_MODEL  : all text-only tabs (post, reply, repost, trend-text)
  - VISION_MODEL: trend-image tab only (requires vision support)

  openai/gpt-oss-120b:free     — does NOT support vision/image input
  google/gemini-2.0-flash-exp:free — supports vision and is free
*/
export const TEXT_MODEL   = 'openai/gpt-oss-120b:free';
export const VISION_MODEL = 'google/gemini-2.0-flash-exp:free';

/**
 * Retrieves the OpenRouter API key.
 * Priority order:
 *  1. Server-injected value (window.PERMAPOD_API_KEY set via index.html)
 *  2. localStorage (saved inline by the user)
 * Returns null if neither is available.
 */
export function getKey() {
  if (window.PERMAPOD_API_KEY && window.PERMAPOD_API_KEY.length > 10) {
    return window.PERMAPOD_API_KEY;
  }
  const stored = localStorage.getItem('permapod_or_key');
  if (stored && stored.length > 10) return stored;
  return null;
}

/**
 * Persists a key entered inline by the user into localStorage.
 */
export function saveInlineKey(value) {
  if (value && value.length > 10) {
    localStorage.setItem('permapod_or_key', value.trim());
    return true;
  }
  return false;
}
