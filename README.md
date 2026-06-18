# PTTM - Pomodoro Timer & Task Manager

A beautiful, highly customizable, and colorful Pomodoro timer with an integrated Todo system, built for the terminal using Python's modern `textual` framework.

## Screenshots

| Focus Mode | Settings & Todo List |
| --- | --- |
| ![Focus Phase](docs/screenshots/focus.png) | ![Settings and Todo](docs/screenshots/settings.png) |

---

## Features

- **Dynamic Catppuccin Themes**: Beautiful, responsive interfaces that shift colors dynamically based on the current timer phase (Crimson for Focus, Green for Short Break, Blue for Long Break).
- **Retro ASCII Art Clock**: A large, easy-to-read digital countdown clock rendered with character blocks.
- **Integrated Todo System**:
  - Add tasks instantly from within the application.
  - Link any active task to your current focus session.
  - Track completed focus sessions per-task.
  - Visual completion states (with clean strikethrough styling).
- **Fully Customizable Sessions**: Edit Focus duration, Short Break, Long Break, and long break intervals on-the-fly via the Settings tab.
- **Config Persistence**: Automatically saves and loads your settings, session counts, and task list locally.
- **Notifications & Sound Alerts**: Dispatches terminal popups and plays an audio bell when a phase transitions.

---

## Installation

The recommended way to install and run **pttm** as a standalone application is using [pipx](https://github.com/pypa/pipx):

```bash
pipx install pttm
```

Alternatively, you can install it using standard pip (preferably in a virtual environment):

```bash
pip install pttm
```

---

## Usage

Once installed, simply launch the application from your terminal:

```bash
ts-pmo
```

### Keybindings

| Key | Action |
| --- | --- |
| `s` | **Start / Pause** the timer |
| `r` | **Reset** the current session's timer |
| `k` | **Skip** the current phase (instantly transition to the next phase) |
| `t` | **Focus** on the Todo input field |
| `q` | **Quit** the application |

---

## Configuration

Your settings, tasks, and history are persisted locally in `pttm_config.json`. This file is loaded automatically on startup, so you never lose your progress or custom configurations.

---

## Development

If you want to run the application from source or contribute to development:

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/pmo.git
   cd pmo
   ```

2. Create a virtual environment and install dependencies:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```

3. Run the development wrapper

   ```bash
   python pmo.py
   ```

4. Run the test suite:

   ```bash
   python -m unittest -v
   ```

---

## License

This project is licensed under the MIT License.
