# Multi-Brand Content Manager

AI-powered Telegram content assistant for two brands inside one bot:

- `Permapod` - the onchain credit market on ZIGChain
- `Nawa` - vault infrastructure for ethical finance

The bot generates X content, stores approved outputs, and learns from those approvals over time through PostgreSQL storage and ChromaDB semantic retrieval.

## What It Does

After `/start`, the bot asks which brand to manage.

Each brand has its own content workspace with these flows:

- `New Post`
- `Reply`
- `Repost + Comment`
- `Trend / Image`
- `Brand Rules`
- `Weekly Cadence`
- `My Approvals`

Each generation returns two options:

- `Tweet 1`
- `Tweet 2`

Users can approve either option, regenerate, or return to the main menu.

## Multi-Brand Behavior

Permapod and Nawa share the same Telegram bot, but they do not share brand memory.

Each brand has its own:

- prompt rules
- voice options
- pillar options
- reply buckets
- weekly cadence
- approved tweet history
- semantic example retrieval

This means Nawa learns from Nawa approvals, and Permapod keeps learning from Permapod approvals.

## Learning System

The bot improves over time using approved content.

### PostgreSQL Memory Layer

Approved tweets are stored with structured metadata including:

- `brand`
- `flow`
- `voice`
- `pillar`
- `bucket`
- `hook`
- `closing`
- `output_type`
- `context`
- `source_tweet`
- `trend_input`
- `approved_at`

Existing historical approvals are treated as `permapod` by default through the startup migration.

### ChromaDB Semantic Memory

After approval:

1. The approved tweet is saved in PostgreSQL.
2. The tweet is embedded into ChromaDB.
3. Metadata is stored for retrieval, including:
   `brand`, `voice`, `pillar`, `flow`, and `bucket`.

Future generations search only within the selected brand's approved content.

### Dynamic Prompt Injection

When generating content:

1. The bot searches ChromaDB for relevant approved tweets from the selected brand.
2. If ChromaDB is unavailable, it falls back to PostgreSQL examples for that brand.
3. Matching examples are injected into the system prompt.
4. OpenAI generates new content (including autonomous hooks and closing lines) using those examples as style references.

This creates a feedback loop:

`Generate -> Approve -> Store -> Learn -> Improve`

## My Approvals

`My Approvals` shows recent approved content for the currently selected brand only.

Each entry includes:

- flow
- voice
- pillar
- approval date
- tweet preview

## Architecture

```text
Telegram Bot
-> Brand Selector
-> Conversation Flow Engine
-> Brand-Aware Prompt Builder
-> Dynamic Example Retrieval
-> OpenAI
-> Approval System
-> PostgreSQL
-> ChromaDB Embeddings
```

## Tech Stack

Backend:

- Python
- python-telegram-bot
- PostgreSQL
- ChromaDB
- OpenAI API
- aiohttp

Storage:

- PostgreSQL for approved content
- ChromaDB for semantic search

AI:

- OpenAI Responses API
- OpenAI Vision

Infrastructure:

- Docker
- Docker Compose

## Running Locally

From the project root:

```bash
docker compose up --build
```

The bot service:

- initializes the database
- applies the `brand` column migration if needed
- starts Telegram polling

## Basic Smoke Test

After the bot starts:

1. Send `/start`
2. Confirm the brand picker shows `Permapod` and `Nawa`
3. Choose `Permapod` and generate a post
4. Switch to `Nawa` and generate a post
5. Approve one tweet under each brand
6. Open `My Approvals` for each brand and confirm the histories are separate

## Core Philosophy

The goal is not simply to generate tweets.

The goal is to build a content system that learns from real approvals and gradually converges on the exact style each brand team prefers.
