import unittest
import json
import os
from datetime import datetime

class TestTrainingPlanner(unittest.TestCase):
    
    def test_date_validation_correct(self):
        date_str = "2026-05-04"
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            is_valid = True
        except ValueError:
            is_valid = False
        self.assertTrue(is_valid)

    def test_date_validation_incorrect(self):
        date_str = "04-05-2026"
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            is_valid = True
        except ValueError:
            is_valid = False
        self.assertFalse(is_valid)

    def test_duration_validation_positive(self):
        duration = "45"
        try:
            val = int(duration)
            if val <= 0: raise ValueError
            is_valid = True
        except ValueError:
            is_valid = False
        self.assertTrue(is_valid)

    def test_duration_validation_negative(self):
        duration = "-10"
        try:
            val = int(duration)
            if val <= 0: raise ValueError
            is_valid = True
        except ValueError:
            is_valid = False
        self.assertFalse(is_valid)

    def test_json_save_load(self):
        test_data = [{"id": 1, "date": "2026-05-04", "type": "Бег", "duration": 30}]
        filename = "test_temp.json"
        
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(test_data, f)
        
        with open(filename, "r", encoding="utf-8") as f:
            loaded = json.load(f)
            
        self.assertEqual(loaded[0]["type"], "Бег")
        os.remove(filename)

if __name__ == "__main__":
    unittest.main()
