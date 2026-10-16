"""Unit-тесты для проверки регулярного выражения путей Windows."""

import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock
from main import is_valid_path, find_in_text, find_in_file, find_in_url


class TestWinPath(unittest.TestCase):
    """Набор тестов для проверки функций модуля main."""

    def test_valid_paths(self):
        """Проверка корректных путей Windows."""
        valid = [
            r"C:\Windows\System32\cmd.exe",
            r"D:\Projects\Лаба 2\отчет.docx",
            r"E:\root_file.txt"
        ]
        for p in valid:
            self.assertTrue(is_valid_path(p))

    def test_invalid_paths(self):
        """Проверка некорректных путей (запрещенные символы, слеши, точки)."""
        invalid = [
            r"C:/Windows/cmd.exe",       # Прямые слеши
            r"Windows\cmd.exe",          # Нет диска
            r"C:\Folder\file?.txt",      # Запрещенный символ ?
            r"C:\Folder.\file.txt",      # Точка в конце имени папки
            r"C:\Folder\file.txt ",      # Пробел в конце
            r"C:\\Windows\cmd.exe"       # Двойной слеш
        ]
        for p in invalid:
            self.assertFalse(is_valid_path(p))

    def test_find_in_text(self):
        """Проверка поиска путей в строке."""
        text = r"Файлы C:\Logs\app.log и D:\data.json, а C:/bad/path.txt нет."
        self.assertEqual(find_in_text(text), [r"C:\Logs\app.log", r"D:\data.json"])

    def test_find_in_file(self):
        """Проверка поиска путей в файле."""
        with tempfile.NamedTemporaryFile('w', encoding='utf-8', delete=False) as f:
            f.write(r"Путь: C:\Windows\notepad.exe")
            name = f.name
        try:
            self.assertEqual(find_in_file(name), [r"C:\Windows\notepad.exe"])
        finally:
            os.remove(name)

    @patch('main.requests.get')
    def test_find_in_url(self, mock_get):
        """Проверка поиска путей по URL через Mock."""
        mock_get.return_value = MagicMock(status_code=200, text=r"C:\drv\gpu.sys")
        self.assertEqual(find_in_url("http://localhost"), [r"C:\drv\gpu.sys"])


if __name__ == '__main__':
    unittest.main()