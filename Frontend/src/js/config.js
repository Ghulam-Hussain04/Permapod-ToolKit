export const GROQ_ENDPOINT = 'https://api.groq.com/openai/v1/chat/completions';

// TEXT_MODEL: best for all text tabs — fast, high quality, free
export const TEXT_MODEL   = 'llama-3.3-70b-versatile';

// VISION_MODEL: for screenshot/image tab
export const VISION_MODEL = 'meta-llama/llama-4-scout-17b-16e-instruct';

export function getKey() {
  if (window.GROQ_API_KEY && window.GROQ_API_KEY.length > 10) {
    return window.GROQ_API_KEY;
  }
  const stored = localStorage.getItem('permapod_groq_key');
  if (stored && stored.length > 10) return stored;
  return null;
}

export function saveInlineKey(value) {
  if (value && value.length > 10) {
    localStorage.setItem('permapod_groq_key', value.trim());
    return true;
  }
  return false;
}