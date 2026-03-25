---
name: docker-audit
description: Audit Dockerfiles and docker-compose.yml files for security issues, best-practice violations, and optimization opportunities. Use when reviewing container configurations, hardening Docker images, checking for root-user containers, exposed secrets, missing health checks, oversized images, or insecure base images. Triggers on phrases like "audit my Dockerfile", "check docker-compose security", "harden my container", "Docker best practices", "container security scan".
---

# Docker Audit

Scan Dockerfiles and docker-compose files for security and best-practice issues.

## Quick Start

```bash
# Audit a single Dockerfile
python3 scripts/docker_audit.py Dockerfile

# Audit a docker-compose file
python3 scripts/docker_audit.py docker-compose.yml

# Audit all Docker files in a directory
python3 scripts/docker_audit.py ./project/

# JSON output for pipeline integration
python3 scripts/docker_audit.py Dockerfile --format json
```

## What It Checks

### Dockerfile Checks
- Running as root (missing USER directive)
- Using `latest` tag (non-deterministic builds)
- Missing HEALTHCHECK
- ADD instead of COPY (security risk)
- Secrets in ENV or ARG
- Excessive LABEL/RUN layers (bloated images)
- Missing .dockerignore recommendation
- Insecure package installs (no version pinning)
- Unnecessary EXPOSE of privileged ports

### Docker-Compose Checks
- Privileged containers
- Host network mode
- Writable volume mounts to sensitive paths
- Missing resource limits (memory/CPU)
- Exposed ports without necessity
- Missing restart policies
- Environment secrets in plaintext

## Output Levels

- **CRITICAL** — Active security vulnerability (root user, privileged mode, secrets in env)
- **WARNING** — Best-practice violation (no healthcheck, latest tag, no resource limits)
- **INFO** — Optimization suggestion (layer consolidation, .dockerignore)
