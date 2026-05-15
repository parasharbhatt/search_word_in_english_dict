
import unittest
import os
import importlib.util

class TestSearchWordApp(unittest.TestCase):
    def test_dictionary_data_exists_in_root(self):
        # 1. Get the directory where this test file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # 2. Go up one level to the project root
        project_root = os.path.join(current_dir, "..")
        # 3. Define the path to the target file
        file_path = os.path.join(project_root, "data.json")
        # 4. Assert that the file exists and is a file
        self.assertTrue(os.path.isfile(file_path), f"File not found at: {file_path}")

    def test_pillow_installed(self):
        # Name of the module you want to check
        module_name = 'PIL'
        # find_spec returns None if the module is not found
        spec = importlib.util.find_spec(module_name)
        self.assertIsNotNone(spec, f"Module '{module_name}' is not installed.")

    def test_pathlib_installed(self):
        # Name of the module you want to check
        module_name = 'pathlib'
        # find_spec returns None if the module is not found
        spec = importlib.util.find_spec(module_name)
        self.assertIsNotNone(spec, f"Module '{module_name}' is not installed.")

if __name__ == "__main__":
    unittest.main()     