import json
import os
import platformdirs

CONFIG_PATH_ENV = os.getenv("PTTM_CONFIG_PATH")
if CONFIG_PATH_ENV:
    CONFIG_FILE = CONFIG_PATH_ENV
else:
    CONFIG_DIR = platformdirs.user_config_dir("pttm", appauthor=False)
    CONFIG_FILE = os.path.join(CONFIG_DIR, "pttm_config.json")

DEFAULT_CONFIG = {
    "settings": {
        "focus_time": 25,
        "short_break_time": 5,
        "long_break_time": 15,
        "long_break_interval": 4
    },
    "completed_focus_sessions": 0,
    "tasks": [
        {"id": "1", "title": "Task 1", "completed": True, "pomodoros": 1},
        {"id": "2", "title": "Task 2", "completed": False, "pomodoros": 0},
        {"id": "3", "title": "Task 3", "completed": False, "pomodoros": 0}
    ]
}

def load_config():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r") as f:
                config = json.load(f)
                # Ensure all sections exist
                if "settings" not in config:
                    config["settings"] = DEFAULT_CONFIG["settings"]
                if "tasks" not in config:
                    config["tasks"] = DEFAULT_CONFIG["tasks"]
                if "completed_focus_sessions" not in config:
                    config["completed_focus_sessions"] = 0
                return config
        except Exception:
            return DEFAULT_CONFIG.copy()
    return DEFAULT_CONFIG.copy()

def save_config(config):
    try:
        dir_name = os.path.dirname(CONFIG_FILE)
        if dir_name:
            os.makedirs(dir_name, exist_ok=True)
        with open(CONFIG_FILE, "w") as f:
            json.dump(config, f, indent=4)
    except Exception:
        pass

