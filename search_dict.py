"""
English Dictionary Search

A desktop dictionary application built with Python and Tkinter.
"""

from __future__ import annotations

import json
import sys
import tkinter as tk
from dataclasses import dataclass
from difflib import get_close_matches
from pathlib import Path
from tkinter import ttk
from typing import Iterable, Mapping, Sequence


def resource_path(relative_path: str) -> Path:
    """Resolve resources for source runs and PyInstaller bundles."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    base = Path(bundle_root) if bundle_root else Path(__file__).resolve().parent
    return base / relative_path


PROJECT_ROOT = Path(__file__).resolve().parent
DATA_FILE = resource_path("data.json")


@dataclass(frozen=True)
class SearchResult:
    word: str
    meanings: tuple[str, ...]
    suggestions: tuple[str, ...] = ()


class DictionaryService:
    """Loads and searches the local dictionary JSON database."""

    def __init__(self, data_file: Path = DATA_FILE) -> None:
        self.data_file = Path(data_file)
        self._dictionary = self._load()

    def _load(self) -> dict[str, list[str]]:
        if not self.data_file.is_file():
            raise FileNotFoundError(f"Dictionary data file not found: {self.data_file}")

        with self.data_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("Dictionary data must be a JSON object")

        clean: dict[str, list[str]] = {}
        for word, meanings in data.items():
            if not isinstance(word, str) or not isinstance(meanings, list):
                continue
            cleaned = tuple(
                meaning.strip()
                for meaning in meanings
                if isinstance(meaning, str) and meaning.strip()
            )
            if word.strip() and cleaned:
                clean[word.strip()] = list(dict.fromkeys(cleaned))
        return clean

    @property
    def word_count(self) -> int:
        return len(self._dictionary)

    def get_suggestions(self, word: str, limit: int = 5) -> tuple[str, ...]:
        if not word.strip():
            return ()
        matches = get_close_matches(
            word.lower().strip(),
            (key.lower() for key in self._dictionary),
            n=limit,
            cutoff=0.55,
        )
        lower_keys = {key.lower(): key for key in self._dictionary}
        return tuple(lower_keys[match] for match in matches)

    def search(self, word: str) -> SearchResult:
        query = word.strip()
        if not query:
            return SearchResult("", ())

        candidates = (query, query.lower(), query.title(), query.upper())
        for candidate in candidates:
            if candidate in self._dictionary:
                return SearchResult(candidate, tuple(self._dictionary[candidate]))

        suggestions = self.get_suggestions(query)
        return SearchResult(query, (), suggestions)


def translate(word: str, dictionary: Mapping[str, Sequence[str]]) -> Sequence[str] | str | None:
    """Backward-compatible helper for callers that use the original API."""
    query = word.strip()
    if not query:
        return None
    candidates = (query, query.lower(), query.title(), query.upper())
    for candidate in candidates:
        if candidate in dictionary:
            return dictionary[candidate]
    matches = get_close_matches(query, dictionary.keys(), n=3, cutoff=0.8)
    return f"Closest match: {matches[0]}" if matches else None


class SearchApp(ttk.Frame):
    def __init__(self, master: tk.Tk, service: DictionaryService) -> None:
        super().__init__(master)
        self.master = master
        self.service = service
        self._configure_window()
        self._configure_styles()
        self._build_ui()
        self.pack(fill=tk.BOTH, expand=True)

    def _configure_window(self) -> None:
        self.master.title("English Dictionary Search")
        self.master.geometry("760x620")
        self.master.minsize(620, 500)
        self.master.configure(background="#F4F7FB")

    def _configure_styles(self) -> None:
        style = ttk.Style(self.master)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("App.TFrame", background="#F4F7FB")
        style.configure("Header.TFrame", background="#153A5B")
        style.configure("HeaderTitle.TLabel", background="#153A5B", foreground="white",
                        font=("Segoe UI", 22, "bold"))
        style.configure("HeaderMeta.TLabel", background="#153A5B", foreground="#C9DBEA",
                        font=("Segoe UI", 10))
        style.configure("Search.TFrame", background="#F4F7FB")
        style.configure("Search.TEntry", padding=(12, 8), font=("Segoe UI", 12))
        style.configure("Primary.TButton", font=("Segoe UI", 11, "bold"), padding=(16, 8))
        style.configure("Secondary.TButton", font=("Segoe UI", 10), padding=(12, 7))
        style.configure("Result.TFrame", background="white")
        style.configure("ResultTitle.TLabel", background="white", foreground="#153A5B",
                        font=("Segoe UI", 16, "bold"))
        style.configure("Status.TLabel", background="#F4F7FB", foreground="#587083",
                        font=("Segoe UI", 9))

    def _build_ui(self) -> None:
        self.configure(style="App.TFrame")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(2, weight=1)

        header = ttk.Frame(self, style="Header.TFrame")
        header.grid(row=0, column=0, sticky="ew")
        header.columnconfigure(0, weight=1)

        ttk.Label(
            header,
            text="English Dictionary",
            style="HeaderTitle.TLabel",
            padding=(24, 18, 24, 2),
        ).grid(row=0, column=0, sticky="w")
        ttk.Label(
            header,
            text=f"{self.service.word_count:,} words available",
            style="HeaderMeta.TLabel",
            padding=(24, 0, 24, 14),
        ).grid(row=1, column=0, sticky="w")

        search = ttk.Frame(self, style="Search.TFrame", padding=(24, 20, 24, 12))
        search.grid(row=1, column=0, sticky="ew")
        search.columnconfigure(0, weight=1)

        self.query_entry = ttk.Entry(search, style="Search.TEntry")
        self.query_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.query_entry.bind("<Return>", lambda _event: self.search())
        self.query_entry.bind("<Escape>", lambda _event: self.clear())
        self.query_entry.focus()

        ttk.Button(search, text="Search", style="Primary.TButton",
                   command=self.search).grid(row=0, column=1)
        ttk.Button(search, text="Clear", style="Secondary.TButton",
                   command=self.clear).grid(row=0, column=2, padx=(8, 0))

        result_card = ttk.Frame(self, style="Result.TFrame", padding=(24, 20))
        result_card.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 8))
        result_card.columnconfigure(0, weight=1)
        result_card.rowconfigure(1, weight=1)

        self.result_title = ttk.Label(
            result_card,
            text="Ready to search",
            style="ResultTitle.TLabel",
        )
        self.result_title.grid(row=0, column=0, sticky="w", pady=(0, 10))

        text_frame = tk.Frame(result_card, background="white")
        text_frame.grid(row=1, column=0, sticky="nsew")
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)

        self.result_text = tk.Text(
            text_frame,
            wrap="word",
            font=("Segoe UI", 11),
            foreground="#263746",
            background="white",
            relief="flat",
            padx=4,
            pady=4,
            spacing1=4,
            spacing3=6,
        )
        self.result_text.grid(row=0, column=0, sticky="nsew")

        scrollbar = ttk.Scrollbar(text_frame, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.result_text.configure(yscrollcommand=scrollbar.set)
        self.result_text.configure(state="disabled")

        self.status_label = ttk.Label(
            self,
            text="Tip: press Enter to search",
            style="Status.TLabel",
            padding=(24, 8, 24, 12),
        )
        self.status_label.grid(row=3, column=0, sticky="ew")

    def _set_result_text(self, text: str) -> None:
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert("1.0", text)
        self.result_text.configure(state="disabled")

    def search(self) -> None:
        query = self.query_entry.get().strip()
        if not query:
            self.result_title.configure(text="Word required")
            self._set_result_text("Enter a word to search.")
            self.status_label.configure(text="No search term entered")
            self.query_entry.focus()
            return

        result = self.service.search(query)
        if result.meanings:
            self.result_title.configure(text=result.word)
            content = "\n\n".join(f"{index}. {meaning}" for index, meaning in enumerate(result.meanings, 1))
            self._set_result_text(content)
            self.status_label.configure(text=f"Found {len(result.meanings)} meaning(s)")
        elif result.suggestions:
            self.result_title.configure(text=f'No exact match for "{result.word}"')
            content = "Did you mean:\n\n" + "\n".join(f"- {item}" for item in result.suggestions)
            self._set_result_text(content)
            self.status_label.configure(text=f"{len(result.suggestions)} suggestion(s) found")
        else:
            self.result_title.configure(text=f'No match for "{result.word}"')
            self._set_result_text("Try checking the spelling or searching for a shorter term.")
            self.status_label.configure(text="No match found")

    def clear(self) -> None:
        self.query_entry.delete(0, tk.END)
        self.result_title.configure(text="Ready to search")
        self._set_result_text("")
        self.status_label.configure(text="Tip: press Enter to search")
        self.query_entry.focus()


def main() -> None:
    service = DictionaryService()
    root = tk.Tk()
    SearchApp(root, service)
    root.mainloop()


if __name__ == "__main__":
    main()
