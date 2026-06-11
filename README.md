# Permapod Content Manager

AI-powered Telegram content assistant for Permapod, the onchain credit market on ZIGChain.

The system helps generate high-quality X content while continuously learning from previously approved content through PostgreSQL storage and ChromaDB semantic retrieval.

---

# Features

## Content Generation Flows

✏️ New Post
💬 Reply
🔁 Repost + Comment
🔥 Trend / Image

---

## Approval Workflow

Every generation produces:

* Tweet 1
* Tweet 2

Users can:

* Approve Tweet 1
* Approve Tweet 2
* Regenerate
* Return to Main Menu

Approved content becomes part of the system's memory.

---

# Learning System

The bot improves over time using approved content.

## PostgreSQL Memory Layer

Approved tweets are stored with:

* Flow
* Voice
* Pillar
* Bucket
* Hook
* Closing
* Context
* Source tweet
* Trend input
* Approval timestamp

This creates a structured content archive.

---

## ChromaDB Semantic Memory

After approval:

1. Tweet is saved in PostgreSQL
2. Tweet is embedded into ChromaDB
3. Metadata is stored:

   * Voice
   * Pillar
   * Flow
   * Bucket

Future generations perform semantic similarity search against approved content.

This means the AI learns what the team actually approves instead of relying only on static prompting.

---

## Dynamic Prompt Injection

When generating content:

1. Bot searches ChromaDB for relevant approved tweets.
2. If ChromaDB is unavailable, it falls back to PostgreSQL examples.
3. Matching examples are injected into the system prompt.
4. OpenAI generates content using real approved content as style references.

This creates a feedback loop:

Generate → Approve → Store → Learn → Improve

---

## 📋 My Approvals

View recently approved content including:

* Flow
* Voice
* Pillar
* Approval date
* Tweet preview

---

# Architecture

Telegram Bot
↓
Conversation Flow Engine
↓
Prompt Builder
↓
Dynamic Example Retrieval
↓
OpenAI
↓
Approval System
↓
PostgreSQL
↓
ChromaDB Embeddings

---

# Tech Stack

Backend

* Python
* python-telegram-bot
* PostgreSQL
* ChromaDB
* OpenAI API
* aiohttp

Storage

* PostgreSQL for approved content
* ChromaDB for semantic search

AI

* OpenAI Responses API
* OpenAI Vision

Infrastructure

* Docker
* Docker Compose

---

# Core Philosophy

The goal is not simply to generate tweets.

The goal is to build a content system that learns from real approvals and gradually converges on the exact style the Permapod team prefers.
