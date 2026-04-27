# Examples

Each JSON file is a ready-to-use config snippet. Apply with `openclaw config merge examples/NAME.json`.

| Example | What it does | When to use |
|---------|-------------|-------------|
| `discord-single.json` | Minimal single-server Discord setup | First Discord install, no frills |
| `discord-full.json` | Full-featured Discord config | Production Discord with multiple servers, exec approvals, thread bindings |
| `discord-telegram.json` | Discord + Telegram side-by-side | Running both channels together |
| `tts-minimax.json` | MiniMax TTS voice output | Enable voice replies on Discord/Telegram/WhatsApp |
| `memory-builtin.json` | Builtin memory with embeddings | Simple local memory, no external services |
| `memory-honcho.json` | Honcho (PostgreSQL) memory | Full memory system with semantic search |
| `multi-agent-discord.json` | Multiple agents on Discord | Route different tasks to different agents |
| `per-agent-sandbox.json` | Sandboxed agent profiles | Lock down untrusted agents, coding isolation |

## Applying an example

```bash
# Review before applying
cat examples/NAME.json

# Apply to your config
openclaw config merge examples/NAME.json

# Restart to pick up changes
openclaw gateway restart
```

## Quick reference

```
First time?         → discord-single.json + memory-builtin.json
Want voice replies? → tts-minimax.json
Want memory search?  → memory-honcho.json
Running two channels? → discord-telegram.json
```
