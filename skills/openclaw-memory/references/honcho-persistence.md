---
title: "Honcho + PostgreSQL Persistence"
summary: "Critical setup guide for self-hosted Honcho — ensuring postgres data survives container restarts"
read_when:
  - Setting up Honcho for the first time
  - Deploying on Railway, Fly.io, Docker, or any containerized environment
  - Diagnosing Honcho data loss after a container restart
---

# Honcho + PostgreSQL Persistence

Self-hosted Honcho uses PostgreSQL as its data store. **If postgres data is on ephemeral container storage, all memory is lost on every container restart.** This guide covers the critical setup steps to ensure your Honcho data persists across restarts.

## ⚠️ The Danger: Ephemeral Storage

Most container platforms (Railway, Fly.io, Docker with default volumes, etc.) use **ephemeral filesystem** for the default data directory. PostgreSQL's default `data_directory` is typically `/var/lib/postgresql/<version>/main`, which is **on the ephemeral layer**.

**If you installed Honcho and didn't configure postgres data_directory, your memory is living on borrowed time.**

Symptoms after container restart:
- `psql` shows 0 messages, 0 sessions — like a fresh install
- Honcho API responds but has no memory of past conversations
- All workspace memory appears lost

## Step 1: Choose a Persistent Data Path

Use a persistent volume mount. Common patterns:

| Platform | Persistent path |
|----------|----------------|
| Railway | `/data/postgres/15/main` |
| Fly.io | `/var/lib/postgresql` (if volume mounted) |
| Docker | Host volume mount `-v /host/path:/var/lib/postgresql/15/main` |
| Bare metal | Default `/var/lib/postgresql/15/main` is fine |

For Railway, use `/data/` which persists across restarts.

## Step 2: Configure postgres data_directory

Edit the postgres config:

```bash
# Find the config file
sudo nano /etc/postgresql/15/main/postgresql.conf

# Set the data_directory to your persistent path
data_directory = '/data/postgres/15/main'
```

Or set it dynamically at startup (before `pg_ctlcluster`):

```bash
# Create the persistent directory and fix ownership
mkdir -p /data/postgres/15/main
chown postgres:postgres /data/postgres/15/main

# Start postgres with explicit data_directory
su postgres -c "/usr/lib/postgresql/15/bin/postgres \
  -D /data/postgres/15/main \
  -c config_file=/etc/postgresql/15/main/postgresql.conf \
  -p 5432"
```

## Step 3: Verify at Startup

Add this check to your Honcho startup script (e.g., `honcho-startup.sh`):

```bash
#!/bin/bash
# honcho-startup.sh — run on every container boot

# 0. Ensure postgres data_directory points to PERSISTENT storage
POSTGRES_CONF="/etc/postgresql/15/main/postgresql.conf"
if grep -q "data_directory = '/var/lib/postgresql" "$POSTGRES_CONF" 2>/dev/null; then
    echo "[startup] WARNING: postgres data_directory is ephemeral! Fixing..."
    sed -i "s|data_directory = '/var/lib/postgresql/15/main'|data_directory = '/data/postgres/15/main'|" "$POSTGRES_CONF"
fi

# Check if data exists at persistent path
if [ ! -f "/data/postgres/15/main/PG_VERSION" ]; then
    echo "[startup] ERROR: No postgres data at /data/postgres/15/main!"
    exit 1
fi

# Start postgres
pg_ctlcluster 15 main start || true
```

## Step 4: Verify Honcho Data After Startup

```bash
# Check postgres is using persistent data_directory
su postgres -c "psql -d honcho -c 'SHOW data_directory;'"

# Verify data is present (should show messages from before restart)
su postgres -c "psql -d honcho -c 'SELECT COUNT(*) as messages FROM messages;'"
su postgres -c "psql -d honcho -c 'SELECT COUNT(*) as sessions FROM sessions;'"
su postgres -c "psql -d honcho -c 'SELECT COUNT(*) as conclusions FROM conclusions;'"

# Check Honcho API is responding
curl -s http://127.0.0.1:8000/health
```

## Step 5: Backup Strategy

For production, configure WAL archiving + regular pg_dump backups:

```bash
# Add to postgresql.conf for WAL archiving
archive_mode = on
archive_command = 'test ! -f /data/postgres/wal/%f && cp %p /data/postgres/wal/%f'

# Daily pg_dump cron
0 3 * * * su postgres -c "pg_dump honcho" > /data/backups/honcho-$(date +\%Y\%m\%d).sql
```

Or use a simple cron to verify data integrity:
```bash
# Check every hour that postgres data_directory is persistent
0 * * * * grep -q "data_directory = '/data" /etc/postgresql/15/main/postgresql.conf || \
  echo "[ALERT] postgres data_directory may be ephemeral!" | tee /tmp/postgres-alert.log
```

## Step 6: If Data Was Already Lost

If you restarted and data is gone (empty database), you cannot recover the ephemeral data. But if you have a recent backup:

```bash
# Restore from pg_dump backup
su postgres -c "psql -d honcho -f /data/backups/honcho-YYYYMMDD.sql"
```

If you don't have a backup, the data is unfortunately unrecoverable from ephemeral storage.

## Quick Diagnosis Checklist

- [ ] `psql -d honcho -c 'SHOW data_directory;'` returns a persistent path (not `/var/lib/postgresql`)
- [ ] Database contains messages from before the last restart
- [ ] `honcho-startup.sh` checks and corrects `data_directory` on every boot
- [ ] Backups are configured via pg_dump or WAL archiving
- [ ] `curl -s http://127.0.0.1:8000/health` returns `{"status":"ok"}`
