# Antigravity Pomodoro TUI

A beautiful, highly-customizable, and colourful Pomodoro app with an integrated Todo system, written in Python using the modern `textual` terminal framework.

## Features

- **Dynamic Visual Themes**: Beautiful Catppuccin-themed interfaces that dynamically change their border and clock colors depending on the active state (Crimson for Focus, Green for Short Break, Blue for Long Break).
- **Retro ASCII Art Clock**: Displays a large digital countdown clock using character blocks.
- **Integrated Todo System**:
  - Add tasks instantly with the add form.
  - Select/deselect an active task to link with your focus session.
  - Visual strikethrough for completed tasks.
  - Track completed focus sessions per-task (e.g. `🍅 x 3`).
- **Fully Customizable Sessions**: Edit Focus duration, Short Break, Long Break, and long break interval (number of focus cycles) on-the-fly in the **Settings** tab.
- **Config Persistence**: Automatically saves and loads your settings, completed session count, and todo tasks locally inside a JSON file (`pmo_config.json`).
- **Notification Popups & Sound Alerts**: Displays terminal popups upon phase completion and triggers an audible/visual bell to alert you.

## Getting Started

1. **Activate the Virtual Environment & Run**:
   ```bash
   ./.venv/bin/python pmo.py
   ```

## Keybindings

- `q` : **Quit** the application.
- `s` : **Start / Pause** the timer.
- `r` : **Reset** the timer to the beginning of the current mode.
- `k` : **Skip** the current session (completes it and transitions to the next phase).
- `t` : **Focus** on the Todo text input field.
