# Robot Lang

DSL для управления роботом.

## Установка

1. Убедись что `install.bat` и `robot.exe` в одной папке
2. Запусти `install.bat` от имени администратора

## Использование

```bash
robot example.bot
```

Или двойной клик по `.bot` файлу.

## Пример

```bot
// Рисуем квадрат
forward 100
right 90
forward 100
right 90
forward 100
right 90
forward 100
```


## Команды

| Команда | Описание |
|---------|----------|
| `forward N` | Вперёд на N пикселей |
| `back N` | Назад на N пикселей |
| `right N` | Поворот направо на N градусов |
| `left N` | Поворот налево на N градусов |
| `// ...` | Комментарий |

## Сборка

```bash
pip install pyinstaller
pyinstaller --onefile --noconsole --name robot robot_cli.py
```

## Структура проекта
```
Robot/
├── src/
│   ├── compiler.py    # компилятор
│   └── robot.py       # робот + логгер
├── robot.exe          # интерпретатор
├── install.bat        # установщик
├── example.bot        # пример
└── README.md
```
