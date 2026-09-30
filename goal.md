# Project Goal: AI News Curation Pipeline

## Objective
Build a standalone, asynchronous backend pipeline that automates the curation of localized news articles from social media video links (Instagram, TikTok, X). 

## Business Logic
We have a live Flutter/Laravel news application (based on a CodeCanyon template). To preserve the ability to update that live app, this curation system must be built as a **completely separate, standalone service**. 

This new service will do the heavy lifting of downloading media, extracting context, using AI to write a localized news article, and storing it for human review. Once approved, this service will push the final article to the live Laravel app via a REST API webhook.

## Core User Flow
1. **Ingestion:** A user submits a social media video URL to this system.
2. **Acquisition:** The system bypasses social media scrapers to download the raw video.
3. **Extraction:** The system extracts the audio track and keyframe images.
4. **Context Gathering:** The system reverse-searches the keyframes to determine the actual location and context of the video (preventing old/fake news).
5. **AI Generation:** The system passes the audio, images, and context to an LLM (Gemini 1.5 Pro) to generate a structured, localized news article (Headline, Summary, Content, SEO Tags).
6. **Approval & Push:** The article sits in a local "Draft" database. Once approved, a payload is POSTed to our live Laravel API to publish the article.