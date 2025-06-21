# RiffRaff Discord Bot 🤖

RiffRaff is a multi-feature community bot developed for the Misfit Marauders Discord server. Built on `discord.py`, it handles raffles, leaderboards, custom user commands, tickets, announcements, and community engagement features.

---

## 📦 Features

- 🎉 **Raffles** — Automatically picks winners from message reactions.
- 📈 **Leaderboard** — Pulls gain data from a custom endpoint and displays it.
- 🛠️ **Custom Commands** — Add, remove, and manage user-ping commands from Discord.
- 🎫 **Ticket System** — DM-based ticket creation with mod routing.
- 🎤 **Community Commands** — Fun utility commands like `!hydrate`, `!barehug`, and more.
- ⏰ **Scheduled Events** — Automated weekly announcements and reset alerts.
- 👋 **Welcome Messages** — DMs and public welcome + auto-role assignment on rules acceptance.
- 🔁 **Live Cog Refreshing** — Hot-reload bot features with `!refresh`.

---

## 🚀 Getting Started

### 1. Clone & Install
```bash
git clone https://github.com/yourname/RiffRaff.git
cd RiffRaff
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
```

### 2. Configure Environment
Create a `.env` file in the project root:

```env
DISCORD_TOKEN="your_bot_token_here"
COMMAND_PREFIX="!"
```

(Use `.env.example` as a template)

---

## 🧠 Project Structure

```
riffraff/
├── main.py                # Bot entry point
├── bot/
│   └── bot_client.py      # Bot subclass and Cog loader
├── cogs/                  # All bot features as cogs
├── config/
│   └── config.py          # Loads env vars and bot constants
├── utils/
│   └── logger.py          # Centralized logging
└── requirements.txt
```

---

## 🔧 Admin Tools

### Refresh All Cogs
```bash
!refresh
```

### Check Ownership
```bash
!whoami
```

### Custom Command System
```bash
!newcmd hello "Hello!" "Alice, Bob"
!commcmd hello
!commadd hello Charlie
!commremove hello Alice
```

---

## 🛡️ Permissions

- Owner-only commands use `@commands.is_owner()` or can be tied to `Config.DEV_IDS` if overridden in `bot_client.py`.
- Ticket routing, welcome roles, and announcement channels are all customizable via `config.py`.

---

## 💬 Support

Built with ❤️ by Ryan (a.k.a. Lord Ryn) for the Misfit Marauders Discord.  
Site: [https://wcs.business](https://wcs.business)

---

## 📄 License

MIT License
