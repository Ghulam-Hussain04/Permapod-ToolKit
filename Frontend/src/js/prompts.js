/* ═══════════════════════════════════════════════
   prompts.js — All AI prompts, voice instructions,
   pillar instructions, and message builders
   ═══════════════════════════════════════════════ */

import { state } from '/src/js/state.js';

/* ── STRICT WRITING GUARDRAILS (FORCED ON ALL GENERATIONS) ── */
const WRITING_GUARDRAILS = `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL FORMATTING & SPELLING RULES (NEVER VIOLATE)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- NEVER use em dashes (—) or en dashes (–). Replace with a period, a new line, or rewrite.
- NEVER write "DeFi". Only "Defi" or "defi" are accepted.
- NEVER write "on-chain" or "on chain". Always "onchain" as one word.
- Always write "Permapod", never "PermaPod".
- Prefer "onchain credit market" over just "lending protocol".
- Prefer "supply / borrow" over "lend / borrow" where natural.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TONE & QUALITY STANDARDS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
- Write grounded, clear, direct, quietly confident. No hype. No CT slang. Human and clean.
- Every line must earn its place. Cut abstract AI-style filler entirely.
- Vary sentence rhythm. Mix short punchy lines with one slightly longer observation. No exclamation marks in Protocol voice.
- Avoid generic crypto clichés like "revolutionary", "game-changing", "paradigm shift", "next-generation", "WAGMI", "moon", "degen", "yield farming", or "maximize your passive income".
- Never use stacked filler rhythm: "more X, more Y, more Z" three or more times in a row.
- Always connect features, metrics, and ecosystem news back to: onchain credit, productive capital, lending, borrowing, collateral, liquidity, or market activity.
`;

/* ── VOICE INSTRUCTIONS ────────────────────────── */
export const VOICE_INSTRUCTIONS = {
  protocol: 'Use Protocol Voice: grounded, clear, direct, transparent, quietly confident, data-led when possible, not overhyped. Short punchy lines. Vary rhythm — mix short lines with one slightly longer observation. No exclamation marks. No hype language. Sound like a sharp human, not a bot.',
  blipblop: 'Use Blip Blop Voice: write as the Blip Blop character in third person. Warm, punchy, slightly robotic, builder-coded, short, lightly playful, not cringe. 2-3 short punchy lines. Add 🤖 at the very end. Use approved Blip Blop phrases where natural: "Blip Blop ran the numbers", "Blip Blop checked the leaderboard", "Blip Blop checked the wiring", "systems nominal", "back to building", "beep". Do NOT say "Blip Blop is the onchain credit market".',
};

/* ── PILLAR INSTRUCTIONS ───────────────────────── */
export const PILLAR_INSTRUCTIONS = {
  'Onchain Lending':         'Pillar focus: onchain lending markets, liquidity, productive capital deployment, lending infrastructure. Themes: what is onchain credit, why borrowing matters, how lending and borrowing work together, why utilization matters, why TVL alone is not the full story, how capital becomes productive.',
  'Stablecoin Utility':      'Pillar focus: stablecoins put to work in lending markets instead of sitting still. Your USDC has somewhere better to be. Put your capital to work. Make your assets productive. Connect APY to real borrowing demand, not just the number. If referencing APY, always say "up to ~X%" and note APY may change. Never use guaranteed yield language.',
  'Lending Demand':          'Pillar focus: yield comes from real lending activity and market demand. The source of APY matters more than the number itself. APY reflects borrowing demand. TVL is a signal, credit is the story. Ranking validates market activity. Stablecoin capital is finding productive use.',
  'Credit Infrastructure':   'Pillar focus: Permapod as a financial primitive and credit infrastructure layer, bigger than a single app. Lending is the first layer, credit is the larger system. Strong ecosystems need more than assets — they need lending, liquidity, and financial infrastructure.',
  'ZIGChain Ecosystem':      'Pillar focus: Permapod contributing lending and credit primitives to ZIGChain. Strong ecosystems need lending infrastructure. More liquidity means deeper markets. More assets onchain means more future utility. For ZIGChain x Ondo content: be vague, talk about what more assets onchain can enable over time.',
  'Product Education':       'Pillar focus: explain one clear aspect of what Permapod does in simple terms. Themes: what is onchain credit, why borrowing matters, why supply caps exist, how lending and borrowing work together, what health factor means, why utilization matters.',
  'Benchmark & Performance': 'Pillar focus: reference lending activity, participation, rankings, or growth. Lending Benchmark is available in Analytics — lets users compare USDC lending markets across top protocols (Morpho and Maple excluded). Metrics: Base APY, TVL, 30D growth. Data from DeFiLlama.',
  'Blip Blop':               'Pillar focus: use the Blip Blop mascot voice. Observational, playful, community-native. Suitable for: points reminders, leaderboard posts, community updates, light milestones, educational whiteboard posts. Blip Blop is a mascot, not the protocol itself.',
};

/* ── REPLY BUCKET ANGLES ───────────────────────── */
export const BUCKET_ANGLES = {
  stablecoin: 'Replying under a stablecoin post. Angle: stablecoin supply is only one side of the story. The stronger question is where lending demand comes from. Connect to the onchain credit market and productive capital.',
  defi:       'Replying under a Defi yield post. Angle: the APY number gets attention but the source of yield determines long-term sustainability. Always write "Defi" or "defi" — never "DeFi".',
  zig:        'Replying under a ZIGChain ecosystem post. Angle: strong ecosystems need lending primitives and financial infrastructure. More liquidity means deeper markets. More assets onchain means more future utility for the credit market.',
  mention:    'Replying to a direct Permapod mention. Angle: appreciate the mention, stay focused. Reinforce that Permapod is building useful onchain credit infrastructure. Keep it grounded and product-led.',
};

/* ── MANDATORY OUTPUT FORMAT ───────────────────── */
function getFormatRules(typeLabel) {
  return `
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
MANDATORY OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Always generate exactly 2 different ${typeLabel} options. Label them exactly as shown below. Nothing else outside the two variants — no preamble, no explanation, no commentary. Each variant must fit within 280 characters.

Tweet 1:
[text here]

Tweet 2:
[text here]`;
}

/* ── MESSAGE BUILDERS ──────────────────────────── */

export function buildPostUserMessage() {
  const voice  = state.postVoice;
  const pillar = state.postPillar;
  const ctx    = document.getElementById('post-ctx').value.trim();

  const hookLine = (state.hookMode === 'pick' && state.hook !== 'ai')
    ? `Opening hook: start Tweet 1 and Tweet 2 each with a DIFFERENT approach, but Tweet 1 must open with exactly this line: "${state.hook}"`
    : `Opening hook: write a fresh, original opening line for each tweet. Do NOT copy from the hooks library word for word.`;

  const closingLine = (state.closingMode === 'pick' && state.closing !== 'ai')
    ? `Closing line: end Tweet 1 with exactly this line: "${state.closing}" — Tweet 2 should use a different closer.`
    : `Closing line: write a fresh, original closing line for each tweet. Do NOT copy from the closers library word for word.`;

  return [
    'Write exactly 2 different X (Twitter) posts for Permapod.',
    WRITING_GUARDRAILS,
    VOICE_INSTRUCTIONS[voice],
    PILLAR_INSTRUCTIONS[pillar],
    hookLine,
    closingLine,
    ctx ? `Additional context to incorporate: ${ctx}` : '',
    getFormatRules('tweets')
  ].filter(Boolean).join('\n');
}

export function buildReplyUserMessage() {
  const tweetBeingReplied = document.getElementById('reply-tweet').value.trim();
  const replyCtx          = document.getElementById('reply-ctx').value.trim();
  const voice             = state.replyVoice;
  const bucket            = state.replyBucket;

  return [
    `Write exactly 2 different replies to this tweet for the Permapod X account.`,
    WRITING_GUARDRAILS,
    `Tweet being replied to: "${tweetBeingReplied || '(no tweet provided — write a general on-brand reply)'}"`,
    VOICE_INSTRUCTIONS[voice],
    BUCKET_ANGLES[bucket],
    replyCtx ? `Additional context: ${replyCtx}` : '',
    getFormatRules('replies')
  ].filter(Boolean).join('\n');
}

export function buildRepostUserMessage() {
  const tweetBeingReposted = document.getElementById('repost-tweet').value.trim();
  const repostCtx          = document.getElementById('repost-ctx').value.trim();
  const voice              = state.repostVoice;
  const pillar             = state.repostPillar;

  return [
    `Write exactly 2 different quote-repost comments for the Permapod X account.`,
    WRITING_GUARDRAILS,
    `Tweet being quote-reposted: "${tweetBeingReposted || '(no tweet provided)'}"`,
    VOICE_INSTRUCTIONS[voice],
    `Content angle: ${PILLAR_INSTRUCTIONS[pillar]}`,
    repostCtx ? `Specific take to incorporate: ${repostCtx}` : '',
    getFormatRules('repost comments')
  ].filter(Boolean).join('\n');
}

export function buildTrendTextUserMessage() {
  const trend   = document.getElementById('trend-input').value.trim();
  const ctx     = document.getElementById('trend-ctx').value.trim();
  const voice   = state.trendVoice;
  const pillar  = state.trendPillar;
  const outType = { tweet: 'original tweet', reply: 'reply', repost: 'quote-repost comment' }[state.tiOutput] || 'tweet';

  return [
    `Trending topic or tweet: "${trend || '(no trend provided)'}"`,
    WRITING_GUARDRAILS,
    `Generate exactly 2 different Permapod ${outType}s that connect this trend to Permapod's narrative.`,
    VOICE_INSTRUCTIONS[voice],
    `Content angle: ${PILLAR_INSTRUCTIONS[pillar]}`,
    ctx ? `Extra context: ${ctx}` : '',
    getFormatRules(outType + 's')
  ].filter(Boolean).join('\n');
}

export function buildTrendImageUserMessage() {
  const ctx     = document.getElementById('trend-ctx').value.trim();
  const voice   = state.trendVoice;
  const pillar  = state.trendPillar;
  const outType = { tweet: 'original tweet', reply: 'reply', repost: 'quote-repost comment' }[state.tiOutput] || 'tweet';

  return [
    `Look at this screenshot (a tweet, announcement, or market update).`,
    WRITING_GUARDRAILS,
    `Based on what you see in the image, generate exactly 2 different Permapod ${outType}s that respond to or connect with it.`,
    VOICE_INSTRUCTIONS[voice],
    `Content angle: ${PILLAR_INSTRUCTIONS[pillar]}`,
    ctx ? `Extra context from the team: ${ctx}` : '',
    getFormatRules(outType + 's')
  ].filter(Boolean).join('\n');
}