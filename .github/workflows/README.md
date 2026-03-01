# GitHub Actions Workflows

This directory contains automated CI/CD workflows for the CSV Data Ingestion Platform.

## Workflow Execution Order

Workflows run **sequentially** in this order:

1. **Lint** - Code quality checks (Ruff, ESLint, TypeScript)
2. **Test** - Unit tests (Pytest, Vitest)
3. **Build** - Docker image building and pushing

Each stage only runs if the previous stage passes.

## Workflows Overview

### 1. **test.yml** - Lint, Test & Build

Comprehensive workflow that runs linting, tests, and builds.

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**Jobs (Sequential):**

#### Lint Job
Checks code quality and formatting for both backend and frontend:

**Backend:**
- Sets up Python 3.12 environment
- Installs dependencies with `uv`
- Runs Ruff linter
- Checks code formatting

**Frontend:**
- Sets up Bun runtime
- Installs dependencies
- Runs ESLint
- Runs TypeScript type checking

#### Backend Tests Job
Runs after lint completes:
- Starts PostgreSQL 18 service
- Runs database migrations
- Runs Pytest

#### Frontend Tests Job
Runs after lint completes (in parallel with backend tests):
- Installs dependencies
- Runs TypeScript type checking
- Runs Vitest unit tests
- Builds the application

**Required secrets:** None

---

### 2. **build-images.yml** - Build & Push Docker Images

Builds Docker images and pushes to GitHub Container Registry (GHCR).

**Triggers:**
- Push to `main` branch
- Push of version tags (e.g., `v1.0.0`)
- Manual workflow dispatch (Actions tab)

**Requirements:**
- Only runs if `test.yml` passes
- Does NOT run on pull requests

**What it does:**

**Backend Image:**
- Builds Docker image from `backend/Dockerfile`
- Pushes to `ghcr.io/{owner}/{repo}-backend`
- Tags with branch name, version, git SHA, and `latest`

**Frontend Image:**
- Builds Docker image from `frontend/Dockerfile`
- Pushes to `ghcr.io/{owner}/{repo}-frontend`
- Tags with branch name, version, git SHA, and `latest`

**Image Tags:**
- `branch` - Branch name (e.g., `main`)
- `vX.Y.Z` - Version tags from git tags
- `X.Y` - Major/minor version
- `sha-{7-char-hash}` - Commit SHA
- `latest` - Latest main branch build

**Required secrets:**
- `GITHUB_TOKEN` - Automatically provided by GitHub Actions

---

### 3. **lint.yml** - Orchestrator Workflow

Simplified workflow that orchestrates the test and build workflows.

**Triggers:**
- Push to `main` or `develop` branches
- Pull requests to `main` or `develop` branches

**What it does:**
- Calls `test.yml` workflow
- Calls Docker build step (only on main branch)
- Ensures sequential execution

**Required secrets:** None

---

## Accessing Test Results

### GitHub UI

1. Go to **Actions** tab in your repository
2. Click on a workflow run to see details
3. Expand individual jobs to see logs

### Viewing Test Output

- **Linting issues:** Click "Run Ruff" or "Run ESLint" step
- **Backend tests:** Click "Run tests" step under backend-tests job
- **Frontend tests:** Click "Run tests" step under frontend-tests job
- **Build results:** Click build steps for Docker image building details

### Status Badge

Add to your main README:

```markdown
![Tests](https://github.com/{owner}/{repo}/workflows/Tests/badge.svg)
```

---

## Troubleshooting

### Tests Failing Locally But Passing in CI

- Ensure you're using the same Python/Node versions
- Check for timezone-dependent tests
- Verify database migration order
- Run `make test` locally before pushing

### Docker Build Failures

- Check `docker build` works locally: `docker build -t test ./backend`
- Verify all required files are tracked in git
- Check Docker layer caching issues

### Lint Failures

If a workflow fails at lint stage:
1. Run linting locally: `cd backend && ruff check app tests`
2. Run frontend lint: `cd frontend && bun run lint`
3. Fix issues and commit

### Test Failures

If lint passes but tests fail:
1. Run tests locally: `pytest` (backend) or `bun test` (frontend)
2. Check PostgreSQL is running for backend tests
3. Verify all dependencies are installed

### Docker Image Build Failures

If tests pass but image building fails:
1. Verify Dockerfile is valid: `docker build ./backend`
2. Check all build context files exist
3. Verify no secrets are hardcoded in images

### Permission Errors

- Ensure `GITHUB_TOKEN` has appropriate permissions
- Check workflow file permissions (`permissions:` section)
- Verify repository settings allow Actions

---

## Local Testing

Run the same checks locally before pushing:

```bash
# Lint backend
cd backend
. .venv/bin/activate
ruff check app tests
ruff format --check app tests

# Lint frontend
cd frontend
bun run lint
bun run type-check

# Test backend
cd backend
pytest -v

# Test frontend
cd frontend
bun test

# Build frontend
cd frontend
bun run build

# Build Docker images
docker build -t csv-backend ./backend
docker build -t csv-frontend ./frontend
```

Or use the Makefile:

```bash
make test        # Run all tests
make lint        # Run linting
```

---

## Customization

### Changing Python Version

Edit `.github/workflows/test.yml`:

```yaml
python-version: '3.12'  # Change this
```

### Changing Bun Version

Edit `.github/workflows/test.yml`:

```yaml
bun-version: latest  # Change to specific version (e.g., '1.0.0')
```

### Adding New Workflows

1. Create a new `.yml` file in this directory
2. Define `name`, `on` (triggers), and `jobs`
3. Reference actions using `uses:`
4. Use `run:` for shell commands

Example workflow structure:

```yaml
name: My Workflow

on:
  push:
    branches: [main]

jobs:
  my-job:
    needs: lint  # Make it depend on lint job
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4
      - name: Do something
        run: echo "Hello"
```

### Running Workflows on Different Branches

Update the `on.push.branches` and `on.pull_request.branches` sections:

```yaml
on:
  push:
    branches: [main, develop, staging]  # Add branches here
  pull_request:
    branches: [main, develop, staging]
```

---

## GitHub Secrets

To add secrets for additional workflows:

1. Go to **Settings** → **Secrets and variables** → **Actions**
2. Click **New repository secret**
3. Add secret name and value
4. Use in workflows: `${{ secrets.SECRET_NAME }}`

---

## Monitoring & Alerts

### Branch Protection Rules

Set up protection for `main` branch:

1. Go to **Settings** → **Branches**
2. Add rule for `main`
3. Enable "Require status checks to pass before merging"
4. Select `test` workflow to require

### Slack Notifications

To get Slack notifications on workflow failure, add this step to any job:

```yaml
- name: Notify Slack
  if: failure()
  uses: slackapi/slack-github-action@v1
  with:
    webhook-url: ${{ secrets.SLACK_WEBHOOK }}
    payload: |
      {
        "text": "Workflow failed: ${{ github.server_url }}/${{ github.repository }}/actions/runs/${{ github.run_id }}"
      }
```

First add `SLACK_WEBHOOK` to repository secrets.

---

## Performance Tips

1. **Use `--frozen-lockfile`** for dependencies (already done)
2. **Cache dependencies** between runs (GitHub Actions does this automatically)
3. **Parallel jobs** - Frontend and backend tests run simultaneously
4. **Docker build cache** - Reduces build time for subsequent runs

---

## References

- [GitHub Actions Documentation](https://docs.github.com/actions)
- [Action Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax](https://docs.github.com/actions/using-workflows/workflow-syntax-for-github-actions)
- [GitHub CLI for Actions](https://cli.github.com/manual/gh_run)
