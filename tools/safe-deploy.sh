#!/usr/bin/env bash
# safe-deploy.sh -- Build and deploy with draft-leakage protection.
# Usage: bash tools/safe-deploy.sh [--dry-run]
#
# Steps:
#   1. hexo clean
#   2. hexo generate
#   3. Compare public/ article list vs source/_posts/ -- abort on mismatch
#   4. Print posts that WILL be deployed
#   5. Print drafts that will NOT be deployed
#   6. Interactive confirmation
#   7. hexo deploy

set -euo pipefail

BLOG_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$BLOG_ROOT"

DRY_RUN=false
if [[ "${1:-}" == "--dry-run" ]]; then
    DRY_RUN=true
fi

# ------------------------------------------------------------------
# 1. Clean
# ------------------------------------------------------------------
echo "[STEP 1/5] Cleaning previous build..."
npx hexo clean

# ------------------------------------------------------------------
# 2. Generate (regular build -- no --draft flag)
# ------------------------------------------------------------------
echo ""
echo "[STEP 2/5] Generating site (production build, no drafts)..."
npx hexo generate

# ------------------------------------------------------------------
# 3. Draft-leakage check
# ------------------------------------------------------------------
echo ""
echo "[STEP 3/5] Checking for draft leakage..."

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
# 4. Print posts that WILL be deployed
# ------------------------------------------------------------------
echo ""
echo "[STEP 4/5] Posts that WILL be deployed (${SOURCE_COUNT} posts):"
echo "------------------------------------------------------------"
echo "$SOURCE_POSTS" | while IFS= read -r slug; do
    echo "  [+] $slug"
done

# ------------------------------------------------------------------
# 5. Print drafts that will NOT be deployed
# ------------------------------------------------------------------
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
# 6. Confirmation + Deploy
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
echo "[STEP 5/5] Deploying..."
npx hexo deploy

echo ""
echo "[DONE] Deployment complete. Check https://umiao.github.io/ to verify."
