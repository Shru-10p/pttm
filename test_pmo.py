#!/usr/bin/env python3
import unittest
import os
import json
import pmo

class TestPomodoro(unittest.TestCase):
    
    def setUp(self):
        # Back up existing configuration if it exists to prevent overwriting user state
        self.config_backup_path = "pmo_config.json.bak"
        self.has_backup = False
        if os.path.exists(pmo.CONFIG_FILE):
            os.rename(pmo.CONFIG_FILE, self.config_backup_path)
            self.has_backup = True

    def tearDown(self):
        # Remove test configuration file
        if os.path.exists(pmo.CONFIG_FILE):
            os.remove(pmo.CONFIG_FILE)
            
        # Restore backup if we created one
        if self.has_backup:
            os.rename(self.config_backup_path, pmo.CONFIG_FILE)

    def test_load_default_config(self):
        # When file does not exist, load_config should return a copy of the default structure
        config = pmo.load_config()
        self.assertIn("settings", config)
        self.assertIn("tasks", config)
        self.assertEqual(config["settings"]["focus_time"], 25)
        self.assertEqual(config["settings"]["short_break_time"], 5)

    def test_save_and_load_config(self):
        # Write clean settings configuration
        test_config = {
            "settings": {
                "focus_time": 10,
                "short_break_time": 2,
                "long_break_time": 8,
                "long_break_interval": 3
            },
            "completed_focus_sessions": 3,
            "tasks": [
                {"id": "test-task-1", "title": "Write test cases", "completed": True, "pomodoros": 4}
            ]
        }
        pmo.save_config(test_config)
        
        # Verify it loads back accurately
        loaded = pmo.load_config()
        self.assertEqual(loaded["settings"]["focus_time"], 10)
        self.assertEqual(loaded["settings"]["short_break_time"], 2)
        self.assertEqual(loaded["completed_focus_sessions"], 3)
        self.assertEqual(len(loaded["tasks"]), 1)
        self.assertEqual(loaded["tasks"][0]["title"], "Write test cases")
        self.assertTrue(loaded["tasks"][0]["completed"])

    def test_make_clock_ascii(self):
        # Test 25 minutes formatting (1500 seconds)
        clock_text = pmo.make_clock_ascii(1500)
        lines = clock_text.split("\n")
        self.assertEqual(len(lines), 5)
        for line in lines:
            self.assertTrue(len(line) > 0)

        # Test 0 seconds formatting (00:00)
        clock_text_zero = pmo.make_clock_ascii(0)
        lines_zero = clock_text_zero.split("\n")
        self.assertEqual(len(lines_zero), 5)

if __name__ == "__main__":
    unittest.main()
