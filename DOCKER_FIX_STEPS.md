# Docker Version Tag Fix - Next Steps

## What was fixed

1. **workflow_call issue**: Removed the `workflow_call` trigger from `release.yml` that was causing docker-build to run in main branch context instead of tag context
2. **Docker Hub README**: Changed condition to update Docker Hub description on all non-PR builds
3. **Manual trigger**: Added `workflow_dispatch` to docker-build.yml for manual triggering

## What needs to be done

### Step 1: Merge the PR
Merge the pull request that fixes the workflow configuration.

### Step 2: Rebuild v0.0.7 Docker images
After the PR is merged to main, run the rebuild script:

```bash
./rebuild-v0.0.7.sh
```

This will:
- Delete the existing v0.0.7 tag (locally and remotely)
- Recreate the v0.0.7 tag
- Push it to trigger the docker-build workflow automatically
- The workflow will now create proper version tags: `0.0.7`, `0.0`, and `0`

### Step 3: Verify
Check that the Docker images are available:

```bash
# Docker Hub
docker pull benni1390/fddb-exporter:0.0.7
docker pull benni1390/fddb-exporter:0.0
docker pull benni1390/fddb-exporter:latest

# GitHub Container Registry
docker pull ghcr.io/benni1390/fddb-exporter:0.0.7
docker pull ghcr.io/benni1390/fddb-exporter:0.0
docker pull ghcr.io/benni1390/fddb-exporter:latest
```

Check Docker Hub for README: https://hub.docker.com/r/benni1390/fddb-exporter

## Future releases

With this fix, all future releases will automatically:
1. Create proper version tags when the VERSION file is updated
2. Push Docker images with correct version tags
3. Update Docker Hub README
