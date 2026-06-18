# PTTM - Pomodoro Timer & Task Manager

PTTM is a terminal-based Pomodoro app built with [Textual](https://textual.textualize.io/). It provides a timer, task tracking, and configurable work/break settings in a compact TUI.

## Features

- Pomodoro timer with focus, short break, and long break modes
- Task list with per-task Pomodoro counts
- Persistent configuration stored as JSON
- Keyboard shortcuts for common timer and task actions
- In-app settings tab for adjusting timing values

## Requirements

- Python 3.10 or newer

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

- `q` quit
- `s` start or pause the timer
- `r` reset the current timer
- `ctrl+r` reset the full session
- `k` skip to the next timer mode
- `f` switch to focus mode
- `g` switch to short break mode
- `b` switch to long break mode
- `t` focus the new task input
- `ctrl+p` show or hide the shortcuts screen

## Configuration

The app reads and writes a JSON config file. By default, the file is stored in your user config directory. You can override the location by setting `PTTM_CONFIG_PATH` before launch.

Example:

```bash
export PTTM_CONFIG_PATH=./pttm_config.json
pttm
```

The config includes timer settings, completed focus session count, and task data.
