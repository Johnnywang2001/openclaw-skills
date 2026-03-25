# Skills QA Review — Improvements Log

**Date:** 2026-03-25
**Reviewed:** 72 skills in `/tmp/openclaw-skills/skills/`

## Summary

- **Bug fixes:** 2 scripts fixed (crash on missing file input)
- **Duplicate skills flagged:** 5 pairs cross-referenced with "See also" notes
- **Outdated branding fixed:** 2 SKILL.md files updated from Clawdbot/Moltbot to OpenClaw
- **Deprecation notice added:** 1 skill marked as superseded

## Bug Fixes

### 1. csv-toolkit/scripts/csv_toolkit.py — FileNotFoundError crash
**Before:** `read_csv()` opened files without checking existence, causing raw Python traceback on missing files.
**Fix:** Added `os.path.isfile()` check with clean error message before `open()`.

### 2. exif-toolkit/scripts/exif_toolkit.py — FileNotFoundError crash
**Before:** `get_exif_data()` and `cmd_strip()` called `Image.open()` without checking if file exists, causing raw Pillow traceback.
**Fix:** Added `os.path.isfile()` checks with clean error messages in both `get_exif_data()` and `cmd_strip()`.

## Duplicate Skills Flagged (Cross-Referenced)

### 1. net-speed-test ↔ network-speed-test
**Overlap:** Both measure download/upload speed and latency using Cloudflare endpoints.
**Difference:** `network-speed-test` (272 lines) is more complete with configurable test sizes; `net-speed-test` (197 lines) is simpler.
**Action:** Added deprecation notice to `net-speed-test` pointing to `network-speed-test`.

### 2. env-file-toolkit ↔ jrv-env-doctor
**Overlap:** Both validate .env files for syntax, duplicates, empty values.
**Difference:** `env-file-toolkit` focuses on management (diff, merge, template); `jrv-env-doctor` focuses on security (secret detection, leaked API keys).
**Action:** Added "See also" cross-references to both SKILL.md files.

### 3. yaml-validator ↔ jrv-yaml-toolkit
**Overlap:** Both validate YAML syntax.
**Difference:** `yaml-validator` is a focused linter; `jrv-yaml-toolkit` adds format, convert, query, merge.
**Action:** Added "See also" cross-references to both SKILL.md files.

### 4. dep-audit ↔ dep-vuln-scanner
**Overlap:** Both scan for dependency vulnerabilities.
**Difference:** `dep-audit` covers outdated packages + license issues + vulns; `dep-vuln-scanner` focuses on CVE scanning via OSV.dev API.
**Action:** Added "See also" cross-references to both SKILL.md files.

### 5. memory-setup ↔ openclaw-memory-upgrade
**Overlap:** Both configure agent memory systems.
**Difference:** `memory-setup` is basic config; `openclaw-memory-upgrade` is a comprehensive 6-step guide.
**Action:** Added "See also" cross-references to both SKILL.md files.

### 6. http-sec-audit ↔ http-status-ref (partial)
**Overlap:** Both can check HTTP security headers.
**Difference:** `http-sec-audit` is dedicated security header auditing with grades; `http-status-ref` is primarily a status code reference with header checking as a secondary feature.
**Action:** Added "See also" note to `http-sec-audit`.

## Branding Updates

### 1. auto-updater/SKILL.md
**Before:** Referenced `Clawdbot`, `clawdbot`, `clawdhub` throughout.
**Fix:** Updated all references to `OpenClaw`, `openclaw`, `clawhub`. Updated docs URLs.

### 2. memory-setup/SKILL.md
**Before:** Referenced `Moltbot/Clawdbot`, `~/.clawdbot/clawdbot.json`, `clawdbot gateway restart`.
**Fix:** Updated to `OpenClaw`, `~/.openclaw/openclaw.json`, `openclaw gateway restart`.

## Security Audit Results

**No security issues found.** Checked all scripts for:
- `eval()` / `exec()` usage: None
- `os.system()` calls: None
- `subprocess` with `shell=True`: None
- Hardcoded secrets/tokens: None (all API keys read from environment)

## Quality Notes

### Well-Structured Skills (no changes needed)
The majority of skills are well-written with:
- Proper argparse with `--help`
- Error handling around network calls (try/except)
- Clean exit codes
- JSON output options
- No external dependencies (pure Python stdlib)

### ASO Scripts (app-store-optimization)
8 scripts lack argparse because they're library modules (imported, not CLI entry points). This is by design.

### Shell Scripts
All shell scripts use `set -e` or `set -euo pipefail`. The `extract-skill.sh` has proper `--help` and argument validation. `save-to-obsidian.sh` has good error handling. Hook scripts (`activator.sh`, `error-detector.sh`) are minimal by design.

### Truncated Directory Name
`obsidian-daily-mai` — directory name appears truncated (should be `obsidian-daily-mail` or similar). This is the published slug in `_meta.json` so cannot be changed without re-publishing.
