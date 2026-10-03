# EVEZ GitHub Manager

Autonomous code management for the EVEZ-OS mesh. One CLI to rule the repos: list, create, issue, release, and heartbeat — all through the GitHub API, zero dependencies.

## Install
```bash
pip install .
export GITHUB_TOKEN=ghp_xxx
evez-ghm status
```

## Usage
```bash
evez-ghm status                      # auth check + rate limit
evez-ghm repos list                  # list your repos
evez-ghm repos create my-new-repo    # create a repo
evez-ghm issue create repo "Title"   # open an issue
evez-ghm issue list repo             # list open issues
evez-ghm release create repo v1.0.0  # cut a release
```

Wired for the mesh: set `GITHUB_TOKEN` in the agent environment and Hermes can manage the full EvezArt catalog by voice command.
