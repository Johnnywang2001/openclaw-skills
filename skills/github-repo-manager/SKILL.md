---
name: github-repo-manager
description: Manage GitHub repositories with practical workflows for branching, pull requests, versioning, releases, branch protection, repository settings, and CI/CD hygiene. Use when working on GitHub-hosted software projects that need repo setup, day-to-day branch management, conventional commits, semantic versioning, tagged releases, GitHub CLI operations, pull request review/merge flows, release publishing, changelog maintenance, or repository governance.
---

# GitHub Repo Manager

Use this skill to manage a GitHub repository like a production codebase, not a scratch folder. Prefer repeatable workflows, small PRs, tagged releases, and protected default branches.

## Core operating rules

- Treat `main` as releasable unless the repository explicitly uses a different default branch.
- Prefer GitHub Flow for most teams and products.
- Keep branches short-lived.
- Keep commits atomic and descriptive.
- Open PRs early, merge cleanly, delete merged branches.
- Tag releases consistently.
- Never commit secrets, generated junk, or local environment files.

## Choose a branching model

### Recommended default: GitHub Flow

Use GitHub Flow for most projects.

Workflow:
1. Branch from `main`
2. Make a focused change
3. Push the branch
4. Open a PR into `main`
5. Run CI and review
6. Merge
7. Delete the branch
8. Tag and release when appropriate

Example:

```bash
git checkout main
git pull origin main
git checkout -b feature/add-billing-webhook
```

Use this when:
- The team deploys frequently
- `main` should stay stable
- Work is organized around reviewable features/fixes

### Alternative: Trunk-based development

Use trunk-based development for very small teams, rapid iteration, or tightly coordinated engineering groups.

Workflow:
- Keep branches extremely short-lived, often hours not days
- Merge to `main` quickly
- Hide incomplete work behind feature flags when needed

Use this when:
- 1-3 developers are moving quickly
- CI is fast and reliable
- The team is disciplined about tiny changes

Do not use long-running feature branches with trunk-based development.

## Branch naming

Use predictable prefixes:

- `feature/...` for new features
- `fix/...` for bug fixes
- `chore/...` for maintenance and tooling

Examples:

```bash
git checkout -b feature/user-invite-flow
git checkout -b fix/login-redirect-loop
git checkout -b chore/update-github-actions
```

Prefer lowercase, hyphen-separated names. Include the intent, not just a ticket number.

Good:
- `feature/export-csv-report`
- `fix/null-pointer-on-startup`
- `chore/remove-deprecated-config`

Weak:
- `feature/stuff`
- `fix/bug`
- `john-branch`

## Commit standards

Use conventional commits whenever possible.

Supported prefixes:
- `feat:` new feature
- `fix:` bug fix
- `chore:` maintenance
- `docs:` documentation
- `refactor:` code restructuring without behavior change
- `test:` tests added or updated
- `ci:` CI/CD pipeline or workflow changes

Examples:

```bash
git commit -m "feat: add CSV export for invoice reports"
git commit -m "fix: prevent duplicate webhook processing"
git commit -m "chore: remove unused Docker compose file"
git commit -m "docs: document local development setup"
git commit -m "refactor: simplify token refresh service"
git commit -m "test: add coverage for rate limiter"
git commit -m "ci: cache pnpm dependencies in GitHub Actions"
```

### Keep commits atomic

A commit should represent one logical change.

Do:
- Separate refactors from behavior changes
- Separate docs updates from code changes unless tightly coupled
- Separate CI edits from product code when possible

Avoid:
- Huge commits mixing feature work, formatting, refactors, and unrelated fixes
- Commit messages like `update stuff` or `misc fixes`

Useful workflow:

```bash
git status
git add path/to/file1 path/to/file2
git commit -m "feat: add repository archive endpoint"
```

If the diff is too broad, split it before committing.

## Versioning with SemVer

Use `MAJOR.MINOR.PATCH`.

### When to bump PATCH

Increment PATCH for backward-compatible bug fixes.

Examples:
- Fix incorrect validation
- Patch a broken API response mapping
- Correct a release packaging issue

Example: `1.2.3` -> `1.2.4`

### When to bump MINOR

Increment MINOR for backward-compatible new functionality.

Examples:
- Add a new endpoint
- Add a new settings page
- Add a new CLI command without breaking existing commands

Example: `1.2.3` -> `1.3.0`

### When to bump MAJOR

Increment MAJOR for breaking changes.

Examples:
- Remove or rename public APIs
- Change required configuration format
- Introduce behavior that breaks integrations

Example: `1.2.3` -> `2.0.0`

### Tag a release

Create and push an annotated tag:

```bash
git tag -a v1.2.3 -m "Release v1.2.3"
git push origin v1.2.3
```

Before tagging, make sure:
- `main` contains the intended release commit
- CI is green
- `CHANGELOG.md` is updated if the repo uses a maintained changelog
- Version files are committed if the project stores version in code/package metadata

## GitHub Releases

After pushing the tag, create a GitHub release.

### Release with manual notes

```bash
gh release create v1.2.3 --title "v1.2.3" --notes "changelog here"
```

Use manual notes when:
- You want a curated summary
- Breaking changes need special callouts
- Upgrade instructions matter

### Release with generated notes

```bash
gh release create v1.2.3 --generate-notes
```

Use generated notes when:
- PR titles are clean
- The repository merges through disciplined PRs
- You need a fast, decent baseline

### Maintain CHANGELOG.md

If the repo has `CHANGELOG.md`, update it before release.

Recommended structure:

```markdown
## [1.2.3] - 2026-03-28

### Added
- Added CSV export for reports

### Fixed
- Fixed duplicate webhook processing

### Changed
- Improved CI dependency caching
```

Simple rule:
- Update changelog in the same PR if the change is user-visible
- For internal-only chores, changelog entry is optional unless the repo standard says otherwise

## Pull request workflow

### Create a PR

Push the branch first:

```bash
git push -u origin feature/add-billing-webhook
```

Open the PR:

```bash
gh pr create --title "feat: add billing webhook" --body "## Summary
- add webhook endpoint
- validate signatures
- store event receipts

## Testing
- added unit tests
- verified with local replay
" --base main
```

Use PR bodies with:
- Summary of change
- Testing performed
- Risks or rollout notes
- Linked issues if relevant

### Review a PR

Approve after checking correctness, scope, tests, and release impact:

```bash
gh pr review --approve
```

Request changes when needed instead of approving by default.

### Merge a PR

Prefer squash merge for most repositories unless the repo explicitly prefers merge commits or rebasing.

```bash
gh pr merge --squash
```

Squash merge is usually best when:
- A branch contains several work-in-progress commits
- You want clean history on `main`
- Conventional commit PR titles are enforced

### PR templates

Use `.github/pull_request_template.md` to standardize quality.

Practical template:

```markdown
## Summary
- 

## Testing
- 

## Checklist
- [ ] CI passes
- [ ] Docs updated if needed
- [ ] CHANGELOG updated if needed
- [ ] No secrets committed
```

Use templates to reduce missing context and improve review quality.

## Branch protection

Protect `main` in production repositories.

Minimum protections:
- Require pull requests before merging
- Require at least one review
- Require status checks to pass
- Restrict force pushes
- Restrict direct deletion when appropriate

Inspect protection settings:

```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

Replace `{owner}` and `{repo}` with actual values.

Example:

```bash
gh api repos/acme/payments-api/branches/main/protection
```

Use branch protection when:
- Multiple people contribute
- CI matters
- Releases come from `main`
- You want to prevent accidental direct pushes

## Repo maintenance

### `.gitignore` best practices

Ignore:
- Dependency directories like `node_modules/`
- Build artifacts like `dist/`, `build/`, `.next/`
- Local env files like `.env`, `.env.local`
- IDE junk like `.DS_Store`, `.idea/`, `.vscode/` as appropriate
- OS-specific clutter and temporary files

Do not ignore files that are required for reproducible builds unless the team deliberately generated them.

Always verify ignored files before first commit:

```bash
git status --ignored
```

### Essential repo files

Prefer every serious repository to include:
- `README.md` - what the project does, how to run it, how to contribute
- `LICENSE` - legal terms for use/distribution
- `CONTRIBUTING.md` - contribution workflow, coding standards, PR expectations

Also consider:
- `.github/pull_request_template.md`
- `.github/ISSUE_TEMPLATE/`
- `CODEOWNERS`
- `SECURITY.md`
- `CHANGELOG.md`

### Edit repo settings with GitHub CLI

Use `gh repo edit` for common repository settings.

Examples:

```bash
gh repo edit --description "Internal billing service" --homepage "https://example.com/docs"
gh repo edit --enable-issues=false
gh repo edit --enable-wiki=false
gh repo edit --default-branch main
```

Run from the cloned repository or specify `OWNER/REPO` if needed.

### Clean up stale branches

After a PR is merged, remove local branches you no longer need:

```bash
git branch -d feature/add-billing-webhook
```

List recently closed PRs to identify branches that can be cleaned up:

```bash
gh pr list --state closed
```

Also prune deleted remote references periodically:

```bash
git fetch --prune
```

If a local branch is already gone on remote and fully merged, delete it locally.

## CI/CD hygiene

Treat CI/CD as part of repo management, not an afterthought.

Minimum expectations:
- CI runs on pull requests
- Failing tests block merges
- Release workflows are explicit
- Secrets stay in GitHub Actions secrets or another secret manager, never in git

Common CI tasks in `.github/workflows/`:
- Install dependencies
- Run lint
- Run tests
- Build artifacts
- Publish packages or deploy on tags/releases

Typical examples of CI-related changes use `ci:` commits.

Example:

```bash
git checkout -b chore/update-release-workflow
# edit .github/workflows/release.yml
git add .github/workflows/release.yml
git commit -m "ci: publish artifacts on version tags"
```

## Decision tree

Use this quick routing logic.

### If starting new work
- Is it a normal feature or fix? -> Use GitHub Flow
- Is the team tiny and merging several times a day? -> Trunk-based development may fit

### If naming a branch
- New user-facing capability? -> `feature/...`
- Bug? -> `fix/...`
- Tooling, dependency, docs, cleanup? -> `chore/...`

### If deciding version bump
- Breaking change? -> MAJOR
- New backward-compatible functionality? -> MINOR
- Backward-compatible fix only? -> PATCH

### If deciding release notes style
- Need curated explanation or upgrade notes? -> Manual `--notes`
- PR titles are already clean and speed matters? -> `--generate-notes`

### If deciding merge style
- Repo wants tidy history and branch has WIP commits? -> `gh pr merge --squash`
- Repo explicitly uses merge commits for history preservation? -> follow repo convention

## Common mistakes to avoid

### Force pushing to `main`

Do not rewrite shared production history unless there is a very controlled incident response plan.

Bad:
- `git push --force origin main`

Prefer protected branches so this is blocked.

### Not tagging releases

If users or deployments depend on versions, tags are not optional. A merged PR is not the same as a release.

### Committing secrets

Never commit:
- `.env`
- API keys
- Private certificates
- Service account JSON files
- Production tokens in workflow files or source

If a secret is committed, rotate it immediately. Cleaning git history alone is not sufficient.

### Giant commits

Large mixed commits make review worse, rollback harder, and release notes noisy.

### Forgetting to update `CHANGELOG.md`

If the repo uses a changelog and the change is user-visible, update it in the same PR. Do not leave release documentation for later if you can avoid it.

## Complete workflow example: from feature idea to GitHub release

Scenario: add a new CSV export feature and release it as `v1.3.0`.

### 1. Sync local `main`

```bash
git checkout main
git pull origin main
```

### 2. Create a feature branch

```bash
git checkout -b feature/csv-export
```

### 3. Implement the change

Edit code, tests, and docs as needed.

### 4. Stage and commit atomic changes

Example split:

```bash
git add src/exporter.ts src/routes/reports.ts
git commit -m "feat: add CSV export endpoint for reports"

git add test/reports-export.test.ts
git commit -m "test: add coverage for CSV report export"

git add README.md CHANGELOG.md
git commit -m "docs: document CSV export and changelog entry"
```

### 5. Push branch to GitHub

```bash
git push -u origin feature/csv-export
```

### 6. Open the PR

```bash
gh pr create --title "feat: add CSV export for reports" --body "## Summary
- add CSV export endpoint
- return properly formatted report data
- document usage

## Testing
- added unit tests
- verified export locally

## Release impact
- minor release
" --base main
```

### 7. Let CI run and address review feedback

If reviewers request changes:

```bash
# make edits
git add .
git commit -m "fix: handle empty report export results"
git push
```

### 8. Approve and merge

Reviewer action:

```bash
gh pr review --approve
```

Merge action:

```bash
gh pr merge --squash
```

### 9. Sync `main` after merge

```bash
git checkout main
git pull origin main
```

### 10. Delete the feature branch

Remote branch is often deleted by GitHub automatically after merge. Remove local branch:

```bash
git branch -d feature/csv-export
```

### 11. Decide the version bump

Decision:
- Backward-compatible new feature -> MINOR bump
- Old version `1.2.3` -> new version `1.3.0`

If the project stores version in a file like `package.json`, update and commit it before tagging.

Example:

```bash
git add package.json CHANGELOG.md
git commit -m "chore: prepare release v1.3.0"
git push origin main
```

### 12. Tag the release

```bash
git tag -a v1.3.0 -m "Release v1.3.0"
git push origin v1.3.0
```

### 13. Publish the GitHub release

Manual notes version:

```bash
gh release create v1.3.0 --title "v1.3.0" --notes "## Added
- CSV export for reports

## Improved
- Test coverage for report exporting
"
```

Or generated notes:

```bash
gh release create v1.3.0 --generate-notes
```

### 14. Verify repo protection and release hygiene

Inspect branch protection:

```bash
gh api repos/{owner}/{repo}/branches/main/protection
```

Check recent PR history if needed:

```bash
gh pr list --state closed
```

### 15. Final state checklist

Before calling the workflow done, confirm:
- PR merged into `main`
- CI green
- `CHANGELOG.md` updated if required
- Tag pushed
- GitHub release published
- Feature branch deleted
- No secrets leaked

## Practical defaults

If the repository does not already define standards, default to this:
- Branching model: GitHub Flow
- Default branch: `main`
- Branch prefixes: `feature/`, `fix/`, `chore/`
- Commit style: conventional commits
- Merge style: squash merge
- Release style: annotated git tag plus GitHub release
- Protection: require PR + 1 review + passing checks on `main`

These defaults are boring in the right way. Keep them unless the repo has a deliberate, documented reason to differ.
