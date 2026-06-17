import tkinter as tk
import math
import time
import compiler
import os
from datetime import datetime


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
            stopped: Время остановки между действиями
            logger: Логгер для записи событий
            name: Имя робота"""
        code: list[str] = compiler.read_file(codepath)
        config: dict[str, str | int | float | bool]
        config, code = compiler.parse_config(code)

        self.code: list[str] = code
        self.codepath: str = codepath
        self.name: str = str(config.get("name", name))
        self.close: bool = bool(config.get("close", close))
        self.stopped: float = float(config.get("stopped", stopped))
        self.logger: Logger = logger or Logger(self.name)
        self._running: bool = True

        self.logger.info("Робот инициализирован")

        self.x: float = 400
        self.y: float = 300
        self.angle: float = 0
        self.pen_color: str = "black"
        self.pen_width: int = 2
        self.pen_down: bool = True

        self.root: tk.Tk = tk.Tk()
        self.root.title(f"Robot Lang — {self.name}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self.canvas: tk.Canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack()

        self.control_frame: tk.Frame = tk.Frame(self.root)
        self.control_frame.pack(fill=tk.X, padx=5, pady=5)

        self.status_label: tk.Label = tk.Label(
            self.control_frame, text="Готов", fg="gray"
        )
        self.status_label.pack(side=tk.LEFT)

        self.coords_label: tk.Label = tk.Label(
            self.control_frame,
            text=f"X: {self.x} Y: {self.y} Угол: {self.angle}°",
        )
        self.coords_label.pack(side=tk.RIGHT)

        self.turtle_id: int | None = None
        self.root.update()
        self.draw_turtle()

    def _on_close(self) -> None:
        """Обработать закрытие окна"""
        self.logger.info("Окно закрыто пользователем")
        self._running = False
        try:
            self.root.destroy()
        except tk.TclError:
            pass

    def draw_turtle(self) -> None:
        """Нарисовать робота"""
        if not self._running:
            return
        try:
            if self.turtle_id:
                self.canvas.delete(self.turtle_id)

            rad: float = math.radians(self.angle)
            tip_x: float = self.x + 15 * math.cos(rad)
            tip_y: float = self.y + 15 * math.sin(rad)
            rad_left: float = math.radians(self.angle + 140)
            rad_right: float = math.radians(self.angle - 140)
            left_x: float = self.x + 10 * math.cos(rad_left)
            left_y: float = self.y + 10 * math.sin(rad_left)
            right_x: float = self.x + 10 * math.cos(rad_right)
            right_y: float = self.y + 10 * math.sin(rad_right)

            self.turtle_id = self.canvas.create_polygon(
                tip_x,
                tip_y,
                left_x,
                left_y,
                right_x,
                right_y,
                fill="#4CAF50",
                outline="#2E7D32",
                width=1,
            )
        except tk.TclError:
            self._running = False

    def update_status(self) -> None:
        """Обновить статус и координаты"""
        if not self._running:
            return
        try:
            self.coords_label.config(
                text=f"X: {int(self.x)} Y: {int(self.y)} Угол: {int(self.angle) % 360}°"
            )
        except tk.TclError:
            self._running = False

    def forward(self, distance: int) -> None:
        """Движение вперёд
        Args:
            distance: Расстояние в пикселях"""
        if not self._running:
            return
        self.logger.debug(f"Движение вперёд на {distance}")
        try:
            if self.stopped > 0:
                steps: int = max(1, int(abs(distance) / 2))
                step: float = distance / steps
                for _ in range(steps):
                    if not self._running:
                        return
                    rad: float = math.radians(self.angle)
                    new_x: float = self.x + step * math.cos(rad)
                    new_y: float = self.y + step * math.sin(rad)
                    if self.pen_down:
                        self.canvas.create_line(
                            self.x,
                            self.y,
                            new_x,
                            new_y,
                            fill=self.pen_color,
                            width=self.pen_width,
                        )
                    self.x, self.y = new_x, new_y
                    self.draw_turtle()
                    self.root.update()
                    time.sleep(self.stopped / 30)
            else:
                rad: float = math.radians(self.angle)
                new_x: float = self.x + distance * math.cos(rad)
                new_y: float = self.y + distance * math.sin(rad)
                if self.pen_down:
                    self.canvas.create_line(
                        self.x,
                        self.y,
                        new_x,
                        new_y,
                        fill=self.pen_color,
                        width=self.pen_width,
                    )
                self.x, self.y = new_x, new_y
                self.draw_turtle()
                self.root.update()
            self.update_status()
        except tk.TclError:
            self._running = False

    def back(self, distance: int) -> None:
        """Движение назад
        Args:
            distance: Расстояние в пикселях"""
        self.logger.debug(f"Движение назад на {distance}")
        self.forward(-distance)

    def right(self, degrees: int) -> None:
        """Поворот направо
        Args:
            degrees: Угол в градусах"""
        if not self._running:
            return
        self.logger.debug(f"Поворот направо на {degrees}°")
        self.angle += degrees
        self.draw_turtle()
        self.update_status()
        self.root.update()

    def left(self, degrees: int) -> None:
        """Поворот налево
        Args:
            degrees: Угол в градусах"""
        if not self._running:
            return
        self.logger.debug(f"Поворот налево на {degrees}°")
        self.angle -= degrees
        self.draw_turtle()
        self.update_status()
        self.root.update()

    def penup(self) -> None:
        """Поднять перо"""
        self.pen_down = False
        self.logger.debug("Перо поднято")

    def pendown(self) -> None:
        """Опустить перо"""
        self.pen_down = True
        self.logger.debug("Перо опущено")

    def color(self, color: str) -> None:
        """Изменить цвет линии
        Args:
            color: Название цвета или HEX-код"""
        self.pen_color = color
        self.logger.debug(f"Цвет изменён на {color}")

    def width(self, w: int) -> None:
        """Изменить толщину линии
        Args:
            w: Толщина в пикселях"""
        self.pen_width = int(w)
        self.logger.debug(f"Толщина изменена на {w}")

    def get_actions(self) -> list[dict[str, str | int]]:
        """Получить действия для робота из компилятора
        Returns:
            list[dict[str, str | int]]: Список действий"""
        self.logger.debug("Действия из файла успешно получены")
        return compiler.compiler_code(self.code)

    def execute(self) -> "Robot":
        """Прочитать и воспроизвести действия из кода"""
        self.logger.start_session()
        self.logger.info("Робот успешно запущен")
        self.status_label.config(text="Выполнение...", fg="blue")
        self.root.update()

        actions: list[dict[str, str | int]] = self.get_actions()
        if not actions:
            self.logger.warning(f"Файл {self.codepath} пуст или не существует")
            self.status_label.config(text="Ошибка: файл пуст", fg="red")
            self.root.update()
            time.sleep(2)
            self.root.destroy()
            return self

        for action in actions:
            if not self._running:
                break
            method: str = str(action["side"])
            value: str | int = action["value"]
            getattr(self, method)(value)

        if self._running:
            self.logger.info("Работа робота завершена")
            try:
                self.status_label.config(text="Завершено", fg="green")
                self.root.update()
            except tk.TclError:
                pass

        if self._running and self.close:
            time.sleep(2)
            try:
                self.root.destroy()
            except tk.TclError:
                pass
        elif self._running:
            self.root.mainloop()

        return self


class Logger:
    """Логгер для записи событий робота"""

    def __init__(self, robot_name: str = "Robot") -> None:
        """Инициализировать логгер
        Args:
            robot_name: Имя робота для имени файла и меток"""
        self.robot_name: str = robot_name
        log_dir: str = os.path.join(os.environ.get("APPDATA", "."), "RobotLang", "logs")
        os.makedirs(log_dir, exist_ok=True)
        self.log_file_name: str = os.path.join(log_dir, f"{robot_name}.log")
        self.create_log_file()

    def create_log_file(self) -> None:
        """Создать файл лога, если его нет"""
        if not os.path.exists(self.log_file_name):
            with open(self.log_file_name, "w", encoding="utf-8") as f:
                f.write("")
            self._write("INFO", "Лог-файл создан")

    def _write(self, level: str, message: str) -> None:
        """Записать сообщение в лог-файл
        Args:
            level: Уровень важности
            message: Текст сообщения"""
        timestamp: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
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
        """Записать информационное сообщение
        Args:
            message: Текст сообщения"""
        self._write("INFO", message)

    def warning(self, message: str) -> None:
        """Записать предупреждение
        Args:
            message: Текст сообщения"""
        self._write("WARNING", message)

    def error(self, message: str) -> None:
        """Записать ошибку
        Args:
            message: Текст сообщения"""
        self._write("ERROR", message)

    def debug(self, message: str) -> None:
        """Записать отладочное сообщение
        Args:
            message: Текст сообщения"""
        self._write("DEBUG", message)


if __name__ == "__main__":
    robot: Robot = Robot("robot.bot", stopped=0.5, name="dildo")
    robot.execute()
