# Permapod X Content Manager

AI-powered X/Twitter content tool for Permapod. It generates on-brand posts, replies, quote-repost comments, and trend/image responses using the Permapod voice and messaging rules.

The project has two run modes:

- Web frontend served by a small Python backend.
- Telegram bot.

Both modes use the OpenAI API. API keys stay on the Python backend and are not exposed in browser JavaScript.

## Project Structure

```text
TweetGeneration/
|-- Bot/
|   |-- ai_client.py          # OpenAI text and image calls
|   |-- bot.py                # Telegram bot entry point
|   |-- handlers.py           # Telegram flow handlers
|   |-- prompts.py            # Prompt builders and brand rules
|   |-- requirements.txt      # Python dependencies
|   `-- web_app.py            # Local web server for the frontend
|-- Frontend/
|   |-- index.html            # Web UI shell
|   `-- src/
|       |-- css/styles.css
|       `-- js/
|           |-- api.js        # Calls local /api/generate backend
|           |-- main.js
|           |-- prompts.js
|           |-- state.js
|           `-- ui.js
|-- tweets_output.txt         # Extracted tweets file, not used by the app yet
|-- .env.example
|-- docker-compose.yml
`-- README.md
```

## Setup

Create and activate a virtual environment:

```powershell
cd TweetGeneration
python -m venv .venv
.\.venv\Scripts\activate
pip install -r Bot\requirements.txt
```

On macOS/Linux, activate the environment with:

```bash
source .venv/bin/activate
```

Create `.env` in the project root:

```env
TELEGRAM_BOT_TOKEN=your_telegram_bot_token_here
PORT=8080

OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
OPENAI_VISION_MODEL=gpt-4.1-mini
```

## Run The Web Frontend

Use this when you want the browser UI:

```powershell
.\.venv\Scripts\activate
python Bot\web_app.py
```

Open:

```text
http://127.0.0.1:8080
```

The frontend calls the local Python backend at `/api/generate`, and the backend calls OpenAI.

## Run The Telegram Bot

Use this when you want the Telegram bot:

```powershell
.\.venv\Scripts\activate
python Bot\bot.py
```

In Telegram, start the bot with:

```text
/start
```

## Environment Variables

| Variable | Required | Default | Description |
| --- | --- | --- | --- |
| `OPENAI_API_KEY` | Yes | none | OpenAI API key used by the backend. |
| `OPENAI_BASE_URL` | No | `https://api.openai.com/v1` | API base URL. Keep default for direct OpenAI. |
| `OPENAI_MODEL` | No | `gpt-4.1-mini` | Text model for posts, replies, reposts, and trend text. |
| `OPENAI_VISION_MODEL` | No | same as `OPENAI_MODEL` | Vision-capable model for uploaded images/screenshots. |
| `TELEGRAM_BOT_TOKEN` | Telegram only | none | Token from BotFather. |
| `PORT` | No | `8080` | Local web server port. |

## Models

Default model:

```text
gpt-4.1-mini
```

It is used for both text and image understanding by default. If you change `OPENAI_VISION_MODEL`, make sure the model supports image input.

## Features

| Tab | What it does |
| --- | --- |
| New post | Generates original posts with weekly cadence, voice, pillar, hook, and closing controls. |
| Reply | Generates replies for stablecoin, DeFi, ZIGChain, or mention contexts. |
| Repost + comment | Generates quote-repost comments. |
| Trend / Image | Responds to text trends or uploaded screenshots/images. |
| Brand rules | Shows Permapod messaging dos, don'ts, hooks, closers, and risk-language rules. |

## ChromaDB / Tweet Memory

`tweets_output.txt` is present in the repo, but the current app does not ingest it.

There is currently:

- No ChromaDB startup build.
- No vector database.
- No retrieval-augmented generation from extracted tweets.

If tweet memory is needed later, add a separate ingestion step that builds a persistent ChromaDB folder from `tweets_output.txt`, then query it before generation.

## Notes

- Do not commit `.env`.
- The browser never receives `OPENAI_API_KEY`.
- If image generation/analysis fails, confirm `OPENAI_VISION_MODEL` supports image input.
- Always check official Permapod docs and X before publishing posts that depend on live APY, TVL, supported assets, or campaign details.

## Official References

| Resource | Link |
| --- | --- |
| Protocol docs | https://permapod.gitbook.io/home |
| X account | https://x.com/PermaPod_xyz |
| Telegram | https://t.me/+H2rZ-U_E0po2MWY1 |
