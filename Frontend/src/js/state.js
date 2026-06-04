/* ═══════════════════════════════════════════════
   state.js — Single source of truth for UI state
   ═══════════════════════════════════════════════ */

export const state = {
  // ── Voice selections per tab ──
  postVoice:   'protocol',
  replyVoice:  'protocol',
  repostVoice: 'protocol',
  trendVoice:  'protocol',

  // ── Pillar selections per tab ──
  postPillar:   'Onchain Lending',
  repostPillar: 'Onchain Lending',
  trendPillar:  'Onchain Lending',

  // ── Reply tab ──
  replyBucket: 'stablecoin',

  // ── Hook / closing modes ──
  // 'ai'   = model generates freely
  // string = exact forced line
  hook:        'ai',
  closing:     'ai',
  hookMode:    'ai',   // 'ai' | 'pick' — controls toggle UI
  closingMode: 'ai',

  // ── Trend / Image tab ──
  tiMode:    'trend',  // 'trend' | 'image'
  tiOutput:  'tweet',  // 'tweet' | 'reply' | 'repost'
  imgBase64: null,
  imgType:   null,
};
