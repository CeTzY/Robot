import logging

logging.basicConfig(level=logging.INFO)


class RobotNameError(Exception):
    """Ошибка названия команды"""

    pass


class RobotSyntaxError(Exception):
    """Ошибка синтаксиса в коде робота"""

    pass


def read_file(filename: str) -> list[str]:
    """Прочитать файл, вернуть списком строк
    Args:
        filename: Путь к файлу для чтения
    Returns:
        list[str] Строки в формате списка"""
    try:
        with open(filename, "r", encoding="utf-8") as file:
            lines: list[str] = []
            for line in file:
                stripped: str = line.strip()
                if stripped and not stripped.startswith("//"):
                    lines.append(stripped)
        return lines
    except FileNotFoundError:
        logging.error(f"Файл {filename} не найден")
        return []


def compiler_code(
    code: list[str], commands: tuple[str, ...] = ("back", "forward", "left", "right")
) -> list[dict[str, str | int]]:
    """Взять список строк, скомпилировать команды, вернуть значения списком
    Args:
        code: строки кода списком
        commands: кортеж с доступными командами
    Returns:
        list[dict[str, str | int]]: Скомпилированные значения в формате списка словарей
    """
    line_num: int = 0
    actions: list[dict[str, str | int]] = []
    for line in code:
        line_num += 1
        parts: list[str] = line.split()
        if not parts:
            continue
        command: str = parts[0]
        if len(parts) == 2 and parts[1].isdigit():
            if command in commands:
                actions.append({"side": command, "value": int(parts[1])})
            else:
                raise RobotNameError(
                    f"Неизвестная команда в строке {line_num}: '{line}'"
                )
        else:
            raise RobotSyntaxError(f"Ошибка синтаксиса в строке {line_num}: '{line}'")
    return actions


def launch(path: str) -> list[dict[str, str | int]] | None:
    """Запустить программу и вернуть результат
    Args:
        path: Путь к файлу для компиляции
    Returns:
        list[dict[str, str | int]] | None"""
    code: list[str] = read_file(path)
    if not code:
        logging.warning(f"Файл {path} пуст, или не существует. Нет кода для компиляции")
        return
    try:
        compiled = compiler_code(code)
        return compiled
    except (RobotNameError, RobotSyntaxError) as e:
        logging.error(f"Ошибка {e}")


if __name__ == "__main__":
    testfile = "robot.bot"
    launch(testfile)
