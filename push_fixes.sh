#!/bin/bash
# Run from Git Bash inside the repo folder:
#   Right-click the folder → "Git Bash Here" → bash push_fixes.sh

cd "$(dirname "$0")"

echo "=== Removing git lock ==="
rm -f .git/index.lock

echo "=== Untracking file.json (main bug: causes stale objects in checker) ==="
git rm --cached file.json 2>/dev/null && echo "  Removed file.json" || echo "  Already untracked"

echo "=== Untracking all __pycache__ and .pyc files ==="
git rm -r --cached "__pycache__" 2>/dev/null || true
git rm -r --cached "models/__pycache__" 2>/dev/null || true
git rm -r --cached "models/engine/__pycache__" 2>/dev/null || true
git rm -r --cached "tests/__pycache__" 2>/dev/null || true
git rm -r --cached "tests/test_models/__pycache__" 2>/dev/null || true
git rm -r --cached "tests/test_models/test_engine/__pycache__" 2>/dev/null || true

echo "=== Staging all changes ==="
git add -A

echo "=== Committing ==="
git commit -m "Fix: untrack file.json and __pycache__ - file.json caused stale objects in checker" || echo "Nothing new to commit"

echo "=== Pushing ==="
git push origin master

echo ""
echo "=== DONE ==="
echo "Now re-run the checker. file.json is gone so 'all BaseModel' will be clean."
