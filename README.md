# PTTM - Pomodoro Terminal Timer & Manager

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

Install the dependencies from the project root:

```bash
pip install -r requirements.txt
```

## Run

From the repository root, start the app with:

```bash
python pttm.py
```

You can also run the app module directly:

```bash
python -m pttm.app
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

The app reads and writes a JSON config file. By default, the file is stored in your user config directory. You can override the location by setting `PMO_CONFIG_PATH` before launch.

Example:

```bash
export PMO_CONFIG_PATH=./pmo_config.json
python pttm.py
```

The config includes timer settings, completed focus session count, and task data.

## Tests

Run the test suite with:

```bash
python -m unittest test_pttm.py
```

## Project Layout

- `pttm/app.py` application entry point
- `pttm/config.py` config load/save helpers
- `pttm/clock.py` ASCII clock rendering
- `pttm/widgets/` UI components
- `pttm/pttm.css` Textual stylesheet
