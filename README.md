# clipping-setup

Backup of the D:\Clipping project (code only, no footage) plus Claude Code config.

- `twitch_auto_clipper.py`, `clipflow/`, `gtavi-claudecode/`, `podcli/` – pipeline code (venvs, node_modules, captures and rendered clips excluded)
- `claude-config/` – copy of `~/.claude`: `settings.json`, `skills/`, `agents/`, `projects/D--Clipping/memory/`

To restore the config, copy the contents of `claude-config/` back into `%USERPROFILE%\.claude\`.
Reinstall deps: `pip install -r gtavi-claudecode/requirements.txt`, `npm install` in `podcli/`.
