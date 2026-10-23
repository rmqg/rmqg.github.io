---
title: Turning the 30-Day Song Recommendation Challenge into a Website
description: 'An introduction to the self-made open-source project 《Song Recommendation Challenge》: turning a thirty-day song recommendation questionnaire into an interactive website that supports day-by-day question release, song search and smart filtering, likes and comments, and an impression-song game mode, along with an explanation of the tech stack and operations plan.'

date: 2026-07-13T20:50:16+08:00
lastmod: 2026-10-23T21:51:19+08:00

categories:
  - Projects
  - Tech
tags:
  - Open Source
  - Music
  - Next.js
  - AI
---

A few days ago, I saw a "30-Day Song Recommendation Challenge" questionnaire image in a group chat, and it suddenly struck me that this kind of activity shouldn't just stay as a static image: if everyone could actually pick songs, listen to what others recommend, leave likes and comments, and have the results preserved, it would feel much more like an ongoing, miniature music exchange meetup.

And so, the **Song Recommendation Challenge** was born.

{{<link title="Song Recommendation Challenge · Try It Online" link="https://game.rmqg.org/">}}

{{<link title="playlist-challenge · GitHub" link="https://github.com/rmqg/playlist-challenge">}}

![Answering page of the Song Recommendation Challenge](challenge-wide.png)

## Not a Fixed 30-Question Survey

That initial image was merely an example—not some sacred "classic question pool," and certainly not the default content of the website. The question bank for a new challenge is empty by default; creators can write any number of questions themselves, load the 30-question template, or directly upload an existing challenge image for a vision model to recognize into an editable list of questions.

Questions can be made available all at once or unlocked one day at a time. Daily unlocks are calculated uniformly according to Beijing Time. The homepage displays only challenges that are currently unlocked and not yet answered by the user, ensuring completed items don't linger in the to-do area.

## Answering with Songs, Connecting Through Music

For each question, users can select one or more songs and add their reflections. Currently, Bilibili video links and NetEase Cloud Music track links are supported, allowing other participants to play directly from the source page, leave likes, and comment.

The site also retains the intriguing "impression song" mechanic from the original questionnaire: you give a fellow group member a keyword, and they pick a song for that word. These interactions are delivered via in-app notifications and take you straight to the corresponding question and answer.

Public challenges can be discovered in the Plaza, while token challenges use a 6-digit numeric invite credential. Share posters display up to 30 questions across a maximum of three columns and include a QR code; for token challenges, the QR code can directly embed the invitation info.

## How "Smart Search" Finds the Original Track

When only a song title is entered, the server fetches up to 50 real search results across the first three pages of Bilibili, then feeds evidence—such as titles, uploaders, descriptions, and publish dates—to a model for filtering. The model does not output BV IDs (which are prone to transcription errors); instead, it returns candidate index numbers, and the server resolves the actual links.

The filtered results are structured into categories like original work, cover, official remake, and derivative fan creation. View counts serve as weak secondary evidence, but never override title, source, or publish date. Successful results are permanently cached under normalized song titles, eliminating redundant model token expenditures for the same song in the future.

## Implementation and Operations

The project is built with Next.js 16, React 19, Better Auth, Drizzle ORM, and PostgreSQL 17, and deployed using Docker Compose. Image question banks are transcribed via an OpenRouter vision model, while song title filtering uses DeepSeek; all platform-specific logic is abstracted behind adapters.

The production environment includes health checks, database backups, platform cookie session monitoring, and Bark push notifications for session drops. Sensitive configurations are kept exclusively in server secrets, never leaking into frontends, logs, or the Git repository.

The project is open-sourced under **GPL-3.0-only**. The interface and rules will naturally continue to evolve, but at least the next time a song recommendation questionnaire pops up in a group chat, we can actually play together.

## Open Source Release Postscript

**GitHub:** [rmqg/playlist-challenge](https://github.com/rmqg/playlist-challenge)

`playlist-challenge` is now published as a complete public repository on [GitHub](https://github.com/rmqg/playlist-challenge). The homepage is written first for people wanting to share music with friends—how to create questions, how to answer, and how to exchange feelings—while the latter half provides entry points for self-hosting, deployment, and contributions.

The repository has been rounded out with GPL licensing and third-party notices, sanitized deployment boilerplate, contribution and security policies, as well as CI workflows that automatically run type checks, linters, tests, and production builds. Platform cookies, model API keys, Bark configurations, and runtime data are strictly kept out of the public repo.

For image question banks, overseas production servers still default to OpenRouter, as real-world access to SiliconFlow services yielded poor results. For developers deploying within mainland China who are willing to test latency and stability from their target servers, the repository also includes a [SiliconFlow SDK configuration reference](https://github.com/rmqg/playlist-challenge/blob/main/docs/SILICONFLOW.md).
