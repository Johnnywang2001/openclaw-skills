# Seamless Model Switching in OpenClaw

A guide to switching LLM models in OpenClaw without crashes, context loss, or broken sessions.

## The Problem

Switching models mid-session in OpenClaw frequently causes crashes, context overflow errors, and memory loss. This guide explains the four root causes and provides six fixes — from simple config changes to architectural patterns.

## Read the Full Guide

**[→ Seamless Model Switching Guide](article.md)**

## Quick Fixes

1. **Standardize context windows** — cap all models to the same window size
2. **Compact before switching** — always run /compact before changing models
3. **Use fallback chains** — let OpenClaw handle model routing automatically
4. **Start new sessions** — switch models between sessions, not during them
5. **Raise compaction thresholds** — more buffer for emergency compaction
6. **Enable context pruning** — TTL-based cleanup keeps sessions lean

## License

MIT
