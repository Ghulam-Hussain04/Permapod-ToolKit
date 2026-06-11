import { state } from '/src/js/state.js';
import {
  buildPostUserMessage,
  buildReplyUserMessage,
  buildRepostUserMessage,
  buildTrendTextUserMessage,
  buildTrendImageUserMessage,
} from '/src/js/prompts.js';

export function buildPayload(mode) {
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
      throw new Error('Please upload a reference image, or switch to Trend text input mode.');
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
  throw new Error(`Unknown generation type: ${mode}`);
}