#!/bin/bash
set -e

echo "This script will rebuild Docker images for v0.0.7"
echo "Make sure the PR is merged first!"
echo ""

# Delete and recreate the v0.0.7 tag to trigger docker-build workflow
echo "Deleting v0.0.7 tag locally and remotely..."
git tag -d v0.0.7 || true
git push origin :refs/tags/v0.0.7 || true

echo "Getting commit SHA for version 0.0.7..."
VERSION_COMMIT=$(git log --all --grep="0.0.7" --format="%H" -1)

if [ -z "$VERSION_COMMIT" ]; then
    echo "Error: Could not find commit for version 0.0.7"
    echo "Please specify the commit SHA manually"
    exit 1
fi

echo "Found commit: $VERSION_COMMIT"
echo "Creating v0.0.7 tag..."
git tag -a v0.0.7 $VERSION_COMMIT -m "Release v0.0.7"

echo "Pushing v0.0.7 tag..."
git push origin v0.0.7

echo ""
echo "Done! The docker-build workflow should now be triggered automatically."
echo "Check: https://github.com/benni1390/fddb-exporter/actions"
