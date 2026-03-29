# GitHub Repo Manager

Manage GitHub repositories like production codebases — not scratch folders. Provides comprehensive workflows for branching, pull requests, versioning, releases, branch protection, and CI/CD hygiene.

## What It Does

This skill turns your agent into a disciplined GitHub operations partner. It covers the complete lifecycle of repository management:

- **Branching strategies** — GitHub Flow and trunk-based development with clear decision rules
- **Branch naming conventions** — Predictable `feature/`, `fix/`, `chore/` prefixes
- **Conventional commits** — `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`, `ci:` with atomic commit discipline
- **Semantic versioning** — MAJOR.MINOR.PATCH with clear bump decision rules
- **Pull request workflows** — Create, review, merge (squash preferred), with PR template recommendations
- **GitHub Releases** — Tagged releases with manual or auto-generated notes, CHANGELOG.md maintenance
- **Branch protection** — Require PRs, reviews, status checks; restrict force pushes
- **CI/CD hygiene** — Workflow best practices, secret management, release automation
- **Repo maintenance** — `.gitignore`, essential repo files, stale branch cleanup, repo settings via `gh`

## When to Use

- Setting up a new GitHub repository with proper conventions
- Day-to-day branch management and PR workflows
- Deciding version bumps and creating releases
- Configuring branch protection rules
- Reviewing or improving CI/CD pipelines
- Cleaning up stale branches and repo hygiene

## Installation

```bash
# From GitHub
cp -r openclaw-skills/skills/github-repo-manager ~/.openclaw/workspace/skills/

# Or symlink (stays updated)
ln -s /path/to/openclaw-skills/skills/github-repo-manager ~/.openclaw/workspace/skills/github-repo-manager
```

Restart the gateway:
```bash
openclaw gateway restart
```

## Key Features

- Complete end-to-end workflow example (feature idea → GitHub release)
- Decision trees for branching model, version bumps, merge style, and release notes
- Common mistakes to avoid (force pushing main, committing secrets, giant commits)
- Practical defaults for repos without existing standards
- All operations use the `gh` CLI for automation

## License

MIT
