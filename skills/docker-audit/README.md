# Docker Audit

Audit Dockerfiles and docker-compose.yml files for security issues, best-practice violations, and optimization opportunities. Use when reviewing container configurations, hardening Docker images, checking for root-user containers, exposed secrets, missing health checks, oversized images, or insecure base images.

## Installation

```bash
clawhub install docker-audit
```

## Usage

```bash
# Audit a single Dockerfile
python3 scripts/docker_audit.py Dockerfile
# Audit a docker-compose file
python3 scripts/docker_audit.py docker-compose.yml
```

## Requirements

- Python 3.7+

## License

MIT
