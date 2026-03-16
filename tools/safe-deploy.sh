#!/usr/bin/env bash
# safe-deploy.sh -- Build and deploy with draft-leakage protection.
# Usage: bash tools/safe-deploy.sh [--dry-run]
#
# Steps:
#   1. Branch guard (only deploy from main)
#   2. Sensitive file source-path check
#   3. render_drafts config guard
#   4. hexo clean
#   5. hexo generate
#   6. Draft-leakage check (compare public/ vs source/_drafts/)
#   7. Print deploy/draft summary
#   8. Interactive confirmation + hexo deploy

set -euo pipefail

BLOG_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BLOG_ROOT"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# ------------------------------------------------------------------
# 1. Branch guard: only deploy from main
# ------------------------------------------------------------------
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
DEPLOY_BRANCH="${DEPLOY_ALLOW_BRANCH:-main}"
if [[ "$CURRENT_BRANCH" != "$DEPLOY_BRANCH" ]]; then
    echo "[FAIL] Deploying from branch '$CURRENT_BRANCH' is not allowed."
    echo "       Switch to '$DEPLOY_BRANCH' before deploying."
    echo "       To override: DEPLOY_ALLOW_BRANCH=$CURRENT_BRANCH bash tools/safe-deploy.sh"
    exit 1
fi
echo "[OK] On branch '$CURRENT_BRANCH'."

# ------------------------------------------------------------------
# 2. Sensitive content guard: check source paths, not public slugs
# ------------------------------------------------------------------
SENSITIVE_FILES=(
    "source/_posts/Behavioral-Interview-Questions-Crack.md"
    "source/_posts/brainteaser_1.md"
)

FOUND_SENSITIVE=""
for f in "${SENSITIVE_FILES[@]}"; do
    if [ -f "$f" ]; then
        FOUND_SENSITIVE="${FOUND_SENSITIVE}  - ${f}\n"
    fi
done

if [ -n "$FOUND_SENSITIVE" ]; then
    echo "[FAIL] Sensitive files detected in source/_posts/:"
    echo -e "$FOUND_SENSITIVE"
    echo "These files must remain in source/_drafts/. Move them before deploying."
    exit 1
fi
echo "[OK] No sensitive files in source/_posts/."

# ------------------------------------------------------------------
# 3. Config guard: ensure render_drafts is false
# ------------------------------------------------------------------
if grep -qE '^\s*render_drafts:\s*true' _config.yml; then
    echo "[FAIL] render_drafts is set to true in _config.yml."
    echo "       Drafts contain sensitive content. Set render_drafts: false."
    exit 1
fi
echo "[OK] render_drafts is false."

# ------------------------------------------------------------------
# 4. Clean
# ------------------------------------------------------------------
echo ""
echo "[STEP 4/8] Cleaning previous build..."
npx hexo clean

# ------------------------------------------------------------------
# 5. Generate (regular build -- no --draft flag)
# ------------------------------------------------------------------
echo ""
echo "[STEP 5/8] Generating site (production build, no drafts)..."
npx hexo generate

# ------------------------------------------------------------------
# 6. Draft-leakage check
# ------------------------------------------------------------------
echo ""
echo "[STEP 6/8] Checking for draft leakage..."

# Collect source post slugs (filenames without .md)
SOURCE_POSTS=$(find source/_posts -maxdepth 1 -name "*.md" -exec basename {} .md \; | sort)
SOURCE_COUNT=$(echo "$SOURCE_POSTS" | wc -l | tr -d ' ')

# Collect draft slugs
DRAFT_SLUGS=""
DRAFT_COUNT=0
if [ -d source/_drafts ]; then
    DRAFT_SLUGS=$(find source/_drafts -maxdepth 1 -name "*.md" -exec basename {} .md \; | sort)
    if [ -n "$DRAFT_SLUGS" ]; then
        DRAFT_COUNT=$(echo "$DRAFT_SLUGS" | wc -l | tr -d ' ')
    fi
fi

# Check if any draft slug appears in public/
LEAKED=""
if [ -n "$DRAFT_SLUGS" ]; then
    while IFS= read -r slug; do
        # Check common URL patterns: /year/month/day/slug/ or /slug/
        if find public/ -type d -name "$slug" 2>/dev/null | grep -q .; then
            LEAKED="${LEAKED}  - ${slug}\n"
        fi
    done <<< "$DRAFT_SLUGS"
fi

if [ -n "$LEAKED" ]; then
    echo "[FAIL] Draft leakage detected! The following drafts were found in public/:"
    echo -e "$LEAKED"
    echo "Aborting deployment. Run 'hexo clean && hexo g' without --draft flag."
    exit 1
fi

echo "[OK] No draft leakage detected."

# ------------------------------------------------------------------
# 7. Print deploy/draft summary
# ------------------------------------------------------------------
echo ""
echo "[STEP 7/8] Posts that WILL be deployed (${SOURCE_COUNT} posts):"
echo "------------------------------------------------------------"
echo "$SOURCE_POSTS" | while IFS= read -r slug; do
    echo "  [+] $slug"
done

echo ""
if [ "$DRAFT_COUNT" -gt 0 ]; then
    echo "Drafts that will NOT be deployed (${DRAFT_COUNT} drafts):"
    echo "------------------------------------------------------------"
    echo "$DRAFT_SLUGS" | while IFS= read -r slug; do
        echo "  [-] $slug"
    done
else
    echo "No drafts found."
fi

# ------------------------------------------------------------------
# 8. Confirmation + Deploy
# ------------------------------------------------------------------
echo ""
echo "============================================================"
echo "  Ready to deploy ${SOURCE_COUNT} posts to production."
if [ "$DRAFT_COUNT" -gt 0 ]; then
    echo "  ${DRAFT_COUNT} draft(s) will be EXCLUDED."
fi
echo "============================================================"

if [ "$DRY_RUN" = true ]; then
    echo ""
    echo "[DRY RUN] Skipping deployment. Everything looks good."
    exit 0
fi

echo ""
read -rp "Deploy now? (y/N): " CONFIRM
if [[ "$CONFIRM" != "y" && "$CONFIRM" != "Y" ]]; then
    echo "Deployment cancelled."
    exit 0
fi

echo ""
echo "[STEP 8/8] Deploying..."
npx hexo deploy

echo ""
echo "[DONE] Deployment complete. Check https://umiao.github.io/ to verify."
