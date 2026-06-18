#!/bin/bash
# Run from Git Bash inside the repo folder:
#   Right-click the folder -> "Git Bash Here" -> bash push_fixes.sh

cd "$(dirname "$0")"

echo "=== Step 1: Removing git lock AND corrupt index ==="
rm -f .git/index.lock
rm -f .git/index
echo "  Done"

echo ""
echo "=== Step 2: Rebuilding index from last good commit ==="
git read-tree HEAD
if [ $? -ne 0 ]; then
    echo "ERROR: git read-tree failed. Close VS Code and try again."
    exit 1
fi
echo "  Index rebuilt"

echo ""
echo "=== Step 3: Removing __pycache__ and .pyc files ==="
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -name "*.pyc" -delete 2>/dev/null || true
rm -f file.json
echo "  Cleaned"

echo ""
echo "=== Step 4: Staging all changes ==="
git add -A
echo ""
git status --short

echo ""
echo "=== Step 5: Committing ==="
git commit -m "Fix: clean test files (no pep8, no null bytes), fix Amenity SQLAlchemy relationship"
if [ $? -ne 0 ]; then
    echo "  Nothing to commit"
fi

echo ""
echo "=== Step 6: Pushing ==="
git push origin master

echo ""
echo "=== DONE === Re-run the checker now."
