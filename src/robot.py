import turtle
import time
from datetime import datetime
import compiler
import os


class Robot:
    """Робот. Может читать и выполнять действия"""

    def __init__(
        self,
        codepath: str = "robot.bot",
        close: bool = True,
        stopped: float = 1,
        logger: "Logger | None" = None,
        name: str = "Robot",
    ) -> None:
        """Инициализировать робота
        Args:
            codepath: Путь к файлу с кодом для робота
            close: Закрывать ли окно при завершении всех действий
            stopped: Время остановки между действиями"""

        self.robot = turtle.Turtle()
        self.codepath = codepath
        self.name = name
        self.logger = logger or Logger(name)
        self.close = close
        self.stopped = stopped
        if not isinstance(stopped, (int, float)):
            self.logger.error(
                f"'stopped' должно быть числом, а не {type(stopped).__name__}"
            )
            raise TypeError(
                f"'stopped' должно быть числом, а не {type(stopped).__name__}"
            )

    def get_actions(self) -> list[dict[str, str | int]] | None:
        """Получить действия для робота из компилятора
        Returns:
            list[dict[str, str | int]] | None"""
        self.logger.debug("Действия из файла успешно получены")
        return compiler.launch(self.codepath)

    def execute(self) -> "Robot":
        self.logger.start_session()
        self.logger.info("Робот успешно запущен")
        """Прочитать и воспроизвести действия из кода"""
        actions: list[dict[str, str | int] | None] = self.get_actions()
        if not actions:
            self.logger.warning(f"Файл {self.codepath} пуст или не существует")
            return

        for action in actions:
            method: str = str(action["side"])
            value: int = int(action["value"])
            getattr(self.robot, method)(value)
            self.logger.debug(f"Вызван метод {method} со значением {value}")
            time.sleep(self.stopped)
        self.logger.info("Работа робота завершена")
        if not self.close:
            self.logger.info("Окно остается открытым")
            turtle.exitonclick()

        return self


class Logger:
    def __init__(self, robot_name: str = "Robot"):
        self.robot_name = robot_name
        self.log_file_name = f"{robot_name}.log"
        self.create_log_file()

    def create_log_file(self):
        if not os.path.exists(self.log_file_name):
            with open(self.log_file_name, "w", encoding="utf-8") as f:
                f.write("")

    def _write(self, level: str, message: str) -> None:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_file_name, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] [{self.robot_name}] {level}: {message}\n")

    def separator(self) -> None:
        """Разделитель между сессиями"""
        with open(self.log_file_name, "a", encoding="utf-8") as f:
            f.write(f"{'='*50}\n")

    def start_session(self) -> None:
        """Начало новой сессии"""
        self.separator()
        self.info("Сессия запущена")

    def info(self, message: str) -> None:
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        self._write("WARNING", message)

    def error(self, message: str) -> None:
        self._write("ERROR", message)

    def debug(self, message: str) -> None:
        self._write("DEBUG", message)


if __name__ == "__main__":
    logger = Logger()
    logger.info("Тестовый запуск")
    robot = Robot("robot.bot", stopped=0.1).execute()
    turtle.done()
