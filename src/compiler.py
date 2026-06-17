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
        list[str]: Строки в формате списка"""
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
    code: list[str],
    commands: tuple[str, ...] = (
        "back",
        "forward",
        "left",
        "right",
        "color",
        "penup",
        "pendown",
        "width",
    ),
) -> list[dict[str, str | int]]:
    """Скомпилировать код в список действий
    Args:
        code: Строки кода списком
        commands: Кортеж с доступными командами
    Returns:
        list[dict[str, str | int]]: Скомпилированные действия"""
    line_num: int = 0
    actions: list[dict[str, str | int]] = []
    
    for line in code:
        line_num += 1
        parts: list[str] = line.split()
        if not parts:
            continue
        
        command: str = parts[0]

        if command in ("penup", "pendown"):
            if len(parts) == 1:
                actions.append({"side": command, "value": 0})
            else:
                raise RobotSyntaxError(
                    f"Ошибка синтаксиса в строке {line_num}: '{line}'"
                )

        elif command == "color":
            if len(parts) == 2 and not parts[1].isdigit():
                actions.append({"side": command, "value": parts[1]})
            else:
                raise RobotSyntaxError(
                    f"Ошибка синтаксиса в строке {line_num}: '{line}'"
                )

        elif len(parts) == 2 and parts[1].isdigit():
            if command in commands:
                actions.append({"side": command, "value": int(parts[1])})
            else:
                raise RobotNameError(
                    f"Неизвестная команда в строке {line_num}: '{line}'"
                )

        else:
            raise RobotSyntaxError(f"Ошибка синтаксиса в строке {line_num}: '{line}'")

    return actions


def parse_config(code: list[str]) -> tuple[dict[str, str | int | float | bool], list[str]]:
    """Отделить настройки от команд
    Args:
        code: Строки кода списком
    Returns:
        tuple[dict, list[str]]: (настройки, команды)"""
    config: dict[str, str | int | float | bool] = {}
    commands: list[str] = []

    for line in code:
        stripped: str = line.strip()
        if "=" in stripped and not stripped.startswith("//"):
            key: str
            value: str
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip()

            parsed_value: str | int | float | bool
            if value in ("true", "True"):
                parsed_value = True
            elif value in ("false", "False"):
                parsed_value = False
            elif value.replace(".", "").isdigit():
                parsed_value = float(value) if "." in value else int(value)
            else:
                parsed_value = value.strip('"').strip("'")

            config[key] = parsed_value
        else:
            commands.append(line)

    return config, commands


def launch(path: str) -> list[dict[str, str | int]] | None:
    """Запустить программу и вернуть результат
    Args:
        path: Путь к файлу для компиляции
    Returns:
        list[dict[str, str | int]] | None: Скомпилированные действия или None при ошибке"""
    code: list[str] = read_file(path)
    if not code:
        logging.warning(f"Файл {path} пуст, или не существует. Нет кода для компиляции")
        return None
    try:
        compiled: list[dict[str, str | int]] = compiler_code(code)
        return compiled
    except (RobotNameError, RobotSyntaxError) as e:
        logging.error(f"Ошибка {e}")
        return None


if __name__ == "__main__":
    testfile: str = "robot.bot"
    launch(testfile)
