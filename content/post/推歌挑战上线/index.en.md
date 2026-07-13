---
title: Turning a 30-Day Song Questionnaire into a Website
description: The design, implementation, and open-source release of Song Recommendation Challenge

date: 2026-07-13T20:50:16+08:00
lastmod: 2026-07-13T20:50:16+08:00

categories:
  - Projects
tags:
  - Open Source
  - Music
  - Next.js
  - AI
---

A few days ago, a “30-Day Song Recommendation Challenge” image appeared in a group chat. It felt like the idea deserved more than a static questionnaire. If everyone could attach real songs, listen to other recommendations, leave likes and comments, and keep the results, it could become a small, ongoing music exchange.

That idea became **Song Recommendation Challenge**.

{{<link title="Song Recommendation Challenge · Live" link="https://game.rmqg.org/">}}

{{<link title="playlist-challenge · GitHub" link="https://github.com/rmqg/playlist-challenge">}}

![The challenge answer page](challenge-wide.png)

## Not a fixed 30-question form

The original image is only an example, not a “classic questionnaire” or the site's default content. A new challenge starts with an empty question bank. Its creator may write any number of questions, load the 30-question example, or upload an existing questionnaire image and let a vision model turn it into an editable list.

Questions may all open at once or unlock one per day. Daily releases use Beijing time consistently. The home page only shows joined challenges with an open, unanswered question, so completed work does not remain in the task area.

## Answer with songs, then talk about them

Each question accepts one or multiple songs plus a short note. Bilibili videos and NetEase Cloud Music tracks are currently supported. Other participants can open the original media page, like an answer, and comment on it.

The site also keeps the questionnaire's “impression song” idea: give a friend a keyword and ask them to choose a song for it. Notifications link directly to the relevant question and answer.

Public challenges appear in the discovery area. Token challenges use a six-digit invitation token. Share posters can show up to 30 questions in three columns and include a QR code; private invitations can carry the token in that QR code.

## How Smart Search finds the original upload

When given only a song title, the server collects up to 50 real results from the first three Bilibili search pages. A model evaluates the title, uploader, description, publication date, and other evidence. It returns candidate indexes rather than error-prone BV identifiers; the server restores the real URLs afterward.

Results include structured labels such as original upload, cover, official remake, and derivative work. View counts are only weak supporting evidence. Successful searches are permanently cached by normalized song title, so later requests do not spend model tokens again.

## Implementation and operations

The project uses Next.js 16, React 19, Better Auth, Drizzle ORM, and PostgreSQL 17, deployed with Docker Compose. OpenRouter vision models transcribe question images, while DeepSeek filters song searches. Platform-specific behavior stays behind adapters.

Production includes health checks, database backups, platform-session monitoring, and Bark alerts. Sensitive values remain in server-side secret files and never enter the browser bundle, logs, or repository.

The project is open sourced under **GPL-3.0-only**. The interface and rules will keep evolving, but the next time a song questionnaire appears in a group chat, we can actually play it together.
