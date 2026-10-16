"""Проверка и поиск полных путей до файлов в ОС Windows (Вариант 19)."""

import re
import requests

# Сегмент пути: без запрещенных символов Windows и без точки/пробела на конце
SEG = r'[^<>:"/\\|?*\x00-\x1f]+(?<![\s.])'

# Паттерн для строгой проверки одного пути и паттерн для поиска в тексте
VALID_RE = re.compile(rf'^[a-zA-Z]:\\(?:{SEG}\\)*{SEG}$')
# Паттерн для поиска путей в тексте (корректно захватывает расширение файлов, исключая знаки препинания в конце)
SEARCH_RE = re.compile(
    rf'[a-zA-Z]:\\(?:{SEG}\\)*'
    r'[^<>:"/\\|?*\x00-\x1f\s]+'
    r'(?<![\s.])'
)


def is_valid_path(path: str) -> bool:
    """Проверяет синтаксическую корректность полного пути Windows."""
    return bool(VALID_RE.match(path)) and len(path) <= 260


def find_in_text(text: str) -> list[str]:
    """Ищет все корректные пути Windows в переданной строке."""
    return SEARCH_RE.findall(text)


def find_in_file(filepath: str) -> list[str]:
    """Ищет пути Windows в локальном текстовом файле."""
    with open(filepath, 'r', encoding='utf-8') as f:
        return find_in_text(f.read())


def find_in_url(url: str) -> list[str]:
    """Ищет пути Windows на веб-странице по URL."""
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return find_in_text(response.text)


if __name__ == '__main__':
    mode = input("Режим (1-Проверка пути, 2-Текст, 3-Файл, 4-URL): ").strip()
    data = input("Введите данные (путь / текст / имя файла / URL): ").strip()
    if mode == '1':
        print("Корректен:", is_valid_path(data))
    elif mode == '2':
        print("Найдено:", find_in_text(data))
    elif mode == '3':
        print("Найдено в файле:", find_in_file(data))
    elif mode == '4':
        print("Найдено на странице:", find_in_url(data))