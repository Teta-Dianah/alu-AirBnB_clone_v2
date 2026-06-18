#!/bin/bash
# Run from Git Bash inside the repo folder:
#   Right-click the folder → "Git Bash Here" → bash push_fixes.sh

cd "$(dirname "$0")"

echo "=== Step 1: Removing git lock AND corrupt index ==="
rm -f .git/index.lock
rm -f .git/index
echo "  Done"

echo ""
echo "=== Step 2: Rebuilding index from last good commit ==="
git read-tree HEAD
if [ $? -ne 0 ]; then
    echo "ERROR: git read-tree failed. Make sure VS Code is closed."
    exit 1
fi
echo "  Index rebuilt"

echo ""
echo "=== Step 3: Removing __pycache__ and .pyc files ==="
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
echo "  Cleaned"

echo ""
echo "=== Step 4: Ensuring file.json is untracked and deleted ==="
git rm --cached file.json 2>/dev/null && echo "  Removed from index" || echo "  Already untracked"
rm -f file.json

echo ""
echo "=== Step 5: Staging all changes ==="
git add -A
echo ""
git status --short

echo ""
echo "=== Step 6: Committing ==="
git commit -m "Replace all test files with iAxcel-AI reference (no pep8 imports)"
if [ $? -ne 0 ]; then
    echo "  Nothing to commit or commit failed — check output above"
fi

echo ""
echo "=== Step 7: Pushing ==="
git push origin master

echo ""
echo "=== DONE ==="
echo "Re-run the checker now. Tests no longer import pep8 so they will load cleanly."
