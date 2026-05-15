---
name: openclaw-install
description: Install, update, migrate, or uninstall OpenClaw. Use when: installing OpenClaw from scratch, deploying to Docker, Railway, Fly, GCP, Azure, Kubernetes, Hetzner, Podman, Bun, Nix, or from source; updating OpenClaw to a new version; migrating from another platform; uninstalling. Triggers on: "install", "update", "upgrade", "docker", "railway", "fly", "gcp", "azure", "kubernetes", "hetzner", "podman", "bun", "nix", "migration", "migrate", "uninstall", "from source".
---

# OpenClaw Install Reference

## Install methods

| Method | Use when |
|--------|----------|
| [Installer script](./references/index.md) | Fastest install, macOS/Linux/WSL2/Windows |
| [Docker](./references/docker.md) | Containerized deployment, VPS |
| [Fly.io](./references/fly.md) | Single-command Fly deploy |
| [From source](./references/installer.md) | Building from npm source |
| [Migrating](./references/migrating-matrix.md) | Moving from another platform |
| [Updating](./references/updating.md) | Upgrading OpenClaw |

## Quick install

```bash
# macOS / Linux / WSL2
curl -fsSL https://openclaw.ai/install.sh | bash

# Skip onboarding wizard
curl -fsSL https://openclaw.ai/install.sh | bash -s -- --no-onboard
```

## Cloud deploys

| Platform | Guide |
|----------|-------|
| Railway | See [Docker](./references/docker.md) + deploy from Dockerfile |
| Fly.io | [Fly.io deploy](./references/fly.md) |
| GCP | Docker-based deployment |
| Azure | Docker-based deployment |
| Kubernetes | Docker-based + kubectl |
| Hetzner | Docker-based via cloud init |

## Update

```bash
openclaw update
# or
OPENCLAW_NO_ONBOARD=1 curl -fsSL https://openclaw.ai/install.sh | bash
```

## References

- `references/index.md` — full install options, system requirements
- `references/docker.md` — Docker setup, docker-compose, VPS
- `references/fly.md` — Fly.io single-command deploy
- `references/installer.md` — installer internals, flags, CI usage
- `references/updating.md` — update paths and troubleshooting
- `references/migrating-matrix.md` — migration from other platforms
- `references/migrating.md` — older migration guide
- `references/migrating-hermes.md` — migrating from Hermes platform
- `references/ansible.md` — Ansible-based deployment
