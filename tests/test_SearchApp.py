import json
import os
import tempfile
import unittest
from pathlib import Path

from search_dict import DictionaryService, SearchResult, translate


class TestDictionaryService(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.data_file = Path(self.temp_dir.name) / "dictionary.json"
        self.data_file.write_text(
            json.dumps({
                "Apple": ["A fruit.", "A technology company."],
                "river": ["A natural flowing watercourse."],
                "data": ["Facts and statistics.", "Facts and statistics."],
            }),
            encoding="utf-8",
        )
        self.service = DictionaryService(self.data_file)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_exact_search_is_case_insensitive(self):
        result = self.service.search("APPLE")
        self.assertEqual(result.word, "Apple")
        self.assertEqual(result.meanings, ("A fruit.", "A technology company."))

    def test_empty_search(self):
        self.assertEqual(self.service.search("   "), SearchResult("", ()))

    def test_unknown_word_returns_suggestions(self):
        result = self.service.search("rivr")
        self.assertEqual(result.meanings, ())
        self.assertIn("river", result.suggestions)

    def test_completely_unknown_word_has_no_suggestions(self):
        result = self.service.search("xyzzy")
        self.assertEqual(result.suggestions, ())

    def test_duplicate_meanings_are_removed_during_load(self):
        result = self.service.search("data")
        self.assertEqual(result.meanings, ("Facts and statistics.",))

    def test_missing_data_file_raises_clear_error(self):
        missing = Path(self.temp_dir.name) / "missing.json"
        with self.assertRaises(FileNotFoundError):
            DictionaryService(missing)


class TestDictionaryDataAndCompatibility(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.project_root = Path(__file__).resolve().parent.parent
        cls.service = DictionaryService(cls.project_root / "data.json")

    def test_project_data_file_exists(self):
        self.assertTrue((self.project_root / "data.json").is_file())

    def test_project_dictionary_has_entries(self):
        self.assertGreater(self.service.word_count, 1000)

    def test_real_dictionary_exact_search(self):
        result = self.service.search("acid rain")
        self.assertTrue(result.meanings)

    def test_translate_remains_compatible(self):
        result = translate("river", {"river": ["A natural flowing watercourse."]})
        self.assertEqual(result, ["A natural flowing watercourse."])

    def test_translate_returns_none_for_unknown_word(self):
        self.assertIsNone(translate("xyzzy", {"river": ["A river."]}))


@unittest.skipUnless(
    os.name == "nt",
    "Automatic application screenshots are supported on Windows desktop agents",
)
class TestApplicationScreenshot(unittest.TestCase):
    def test_application_screenshot_capture(self):
        try:
            import tkinter as tk
            from PIL import ImageGrab
            from search_dict import SearchApp
        except ImportError:
            self.skipTest("Tkinter or Pillow is unavailable")

        try:
            root = tk.Tk()
        except tk.TclError as error:
            self.skipTest(f"A graphical desktop is unavailable: {error}")

        root.geometry("760x620+100+100")
        root.update_idletasks()
        app = SearchApp(root, DictionaryService(
            Path(__file__).resolve().parent.parent / "data.json"
        ))
        app.query_entry.insert(0, "acid rain")
        app.search()
        root.update()

        output_dir = Path(__file__).resolve().parent.parent / "test-reports"
        output_dir.mkdir(parents=True, exist_ok=True)
        output = output_dir / "application-screenshot.png"

        try:
            bbox = (
                root.winfo_rootx(),
                root.winfo_rooty(),
                root.winfo_rootx() + root.winfo_width(),
                root.winfo_rooty() + root.winfo_height(),
            )
            screenshot = ImageGrab.grab(bbox=bbox)
            screenshot.save(output)
            self.assertGreater(output.stat().st_size, 0)
        finally:
            root.destroy()


if __name__ == "__main__":
    unittest.main()
