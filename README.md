# Permapod X Content Manager

AI-powered X (Twitter) content tool for Permapod — generates on-brand posts, replies, repost comments, and trend responses using the Permapod brand voice and messaging framework.

---

## Project Structure

```
permapod-content-manager/
├── index.html                  # App shell — markup only, no inline JS/CSS
├── src/
│   ├── css/
│   │   └── styles.css          # All styles
│   └── js/
│       ├── state.js            # Single source of truth for UI state
│       ├── config.js           # API config, key management
│       ├── prompts.js          # System prompt, voice/pillar instructions, message builders
│       ├── ui.js               # All UI helper functions
│       ├── api.js              # OpenRouter API call handler
│       └── main.js             # Entry point — imports all modules, exposes globals, inits app
├── Dockerfile                  # nginx:alpine image, key injection via entrypoint
├── docker-entrypoint.sh        # Injects OPENROUTER_API_KEY into HTML at container start
├── docker-compose.yml          # One-command local run
├── nginx.conf                  # Static file serving config
├── .env.example                # Env template — copy this, fill in your key
├── .gitignore                  # Excludes .env so keys never hit Git
└── README.md
```

---

## Quick Start (Docker)

**Step 1 — Clone and set up your env**
```bash
git clone <your-repo-url>
cd permapod-content-manager
cp .env.example .env
```

**Step 2 — Add your OpenRouter API key to `.env`**
```
OPENROUTER_API_KEY=sk-or-v1-your-key-here
```

**Step 3 — Build and run**
```bash
docker compose up --build
```

**Step 4 — Open the app**
```
http://localhost:8080
```

---

## API Key Security

The API key is **never hardcoded** in any source file.

Flow:
1. You put your key in `.env` (which is in `.gitignore` — never committed)
2. `docker-compose.yml` passes it as an environment variable to the container
3. `docker-entrypoint.sh` runs at container startup and injects it into `index.html` via `sed`
4. The browser receives the key only at runtime, not from the repo

**When sharing the repo** — teammates get `.env.example`. They copy it to `.env` and add their own key.

---

## Running Without Docker (Local Dev)

Since this is a static app with ES modules, you need a local server (browsers block `file://` ES module imports).

```bash
# Option 1 — Python
python3 -m http.server 8080

# Option 2 — Node
npx serve .

# Option 3 — VS Code
# Install the "Live Server" extension and click "Go Live"
```

For local dev the API key falls back to localStorage — enter it once in the app and it's saved.

---

## Environment Variables

| Variable            | Required | Default | Description                        |
|---------------------|----------|---------|------------------------------------|
| `OPENROUTER_API_KEY`| Yes      | —       | Your OpenRouter key (`sk-or-v1-…`) |
| `PORT`              | No       | `8080`  | Port the container listens on      |

---

## Models Used

| Use case         | Model                              |
|------------------|------------------------------------|
| All text tabs    | `openai/gpt-oss-120b:free`         |
| Image/screenshot | `google/gemini-2.0-flash-exp:free` |

Both are free tier on OpenRouter. Get a key at [openrouter.ai/keys](https://openrouter.ai/keys).

---

## Tabs

| Tab | What it does |
|-----|-------------|
| ✏️ New post | Generates original posts with weekly cadence, voice, pillar, hook/closing controls |
| 💬 Reply | Generates replies with bucket targeting (stablecoin / DeFi / ZIGChain / mention) |
| 🔁 Repost + comment | Generates quote-tweet comments |
| 🔥 Trend / Image | Responds to trending topics or uploaded screenshots |
| 🛡️ Brand rules | Quick reference for dos/don'ts and risk language |

---

## Official References

| Resource | Link |
|----------|------|
| Protocol docs | https://permapod.gitbook.io/home |
| X account | https://x.com/PermaPod_xyz |
| Telegram | https://t.me/+H2rZ-U_E0po2MWY1 |

> Always check the docs and X account before publishing anything that depends on current APY, TVL, supported assets, or live campaign details.
