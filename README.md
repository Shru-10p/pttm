# PTTM - Pomodoro Timer & Task Manager

PTTM is a terminal-based Pomodoro app built with [Textual](https://textual.textualize.io/). It provides a timer, task tracking, and configurable work/break settings in a compact TUI.

## Features

- Pomodoro timer with focus, short break, and long break modes
- Audible ding sound on every mode transition (synthesised at first launch, cached as `ding.wav`)
- Task list with per-task Pomodoro counts
- Persistent configuration stored as JSON
- Keyboard shortcuts for all timer and task actions
- In-app settings tab for adjusting timing values
- **Auto-start next timer** — optionally begin the next timer automatically when the current one ends
- Full keyboard navigation in the Tasks and Settings tabs (arrow keys, Escape)

## Requirements

- Python 3.10 or newer
- `aplay` (ALSA/PipeWire) for audio — pre-installed on most Linux desktops

## Installation

You can install the application globally from PyPI using [pipx](https://github.com/pypa/pipx):

```bash
pipx install pttm
```

To install it locally for development, clone the repository and install it in editable mode:

```bash
git clone https://github.com/Shru-10p/pttm.git
cd pttm
pipx install -e .
```

## Run

Start the app with:

```bash
pttm
```

## Keyboard Shortcuts

### Global

| Key | Action |
| --- | --- |
| `q` | Quit |
| `Space` / `s` | Start or pause the timer |
| `r` | Reset the current timer |
| `Ctrl+R` | Reset the current interval |
| `k` | Skip to the next timer mode |
| `f` | Switch to Focus mode |
| `g` | Switch to Short Break mode |
| `b` | Switch to Long Break mode |
| `t` | Focus the new task input |
| `Ctrl+P` | Show / hide the shortcuts overlay |
| `Esc` | Focus the tab bar (from Tasks or Settings tab) |

### Tasks tab

| Key | Action |
| --- | --- |
| `↓` | Move focus to the next task (from input, enters the list) |
| `↑` | Move focus to the previous task (from first task, returns to input) |
| `Esc` | Return focus to the task input box |
| `Space` / `Enter` | Toggle task completion |
| `f` | Set task as the active Pomodoro target |
| `e` | Rename task inline |
| `d` | Delete task (returns focus to input) |

### Settings tab

| Key | Action |
| --- | --- |
| `↓` | Move focus to the next field |
| `↑` | Move focus to the previous field |
| `Enter` | Activate the focused button / toggle switch |

## Configuration

The app reads and writes a JSON config file. By default, the file is stored in your user config directory. You can override the location by setting `PTTM_CONFIG_PATH` before launch.

```bash
export PTTM_CONFIG_PATH=./pttm_config.json
pttm
```

### Settings

| Setting | Default | Description |
| --- | --- | --- |
| Focus session | 25 min | Length of each focus block |
| Short break | 5 min | Length of a short break |
| Long break | 15 min | Length of a long break |
| Sessions before long break | 4 | How many focus sessions before a long break |
| Auto-start next session | Off | Automatically begin the next timer when the current one ends |

The config also persists the completed focus session count and all task data across launches.

## Audio

On first launch, PTTM synthesises a short bell-tone (`ding.wav`) using only Python's standard library and stores it next to the config file. From then on the cached file is reused directly — no re-synthesis, no network access, and no extra Python dependencies.
