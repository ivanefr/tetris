<h1 align="center">Tetris</h1>

## О проекте
Этот проект представляет собой реализацию популярной игры тетрис с использованием фреймворка pygame

## Библиотеки
 - pygame==2.5.2

## Установка зависимостей
```bash
pip install pygame
```
или
```bash
pip install -r requirements.txt
```

## Запуск игры
```bash
python main.py
```

## Правила игры

Случайные фигурки тетрамино
падают сверху в прямоугольный стакан шириной 10 и высотой 20 клеток.
В полёте игрок может поворачивать фигурку на 90° (стрелка вверх) и двигать её по горизонтали (< >).
Также можно «сбрасывать» фигурку (Enter), или ускорять её падение (стрелочка вниз). Фигурка летит до тех пор,
пока не наткнётся на другую фигурку либо
на дно стакана. Если при этом заполнился горизонтальный ряд из 10 клеток, он пропадает и всё
, что выше него, опускается на одну клетку. Дополнительно показывается фигурка, которая будет следовать после
текущей — это подсказка, которая позволяет игроку планировать действия.
Игра заканчивается, когда новая фигурка не может поместиться в стакан. Игрок получает очки за каждый заполненный
ряд и сброшенную фигуру, поэтому его задача — заполнять горизонтальные ряды, не заполняя сам стакан (предотвращая/не допуская его
заполнение по вертикали) как можно дольше, чтобы таким образом получить как можно больше очков.

## Подсчёт очков
 - 10 за каждую сброшенную фигурку 
 - 100 за одну линию
 - 200 за 2 линии
 - 700 за 3 линии
 - 1500 за 4 линии убранных за раз
 - -2 * n, где n - количество поворотов фигурки
 - 3 * h, где h - высота "сбрасываемой фигурки"

### Автор
Ефремов Иван
Жуков Арсений
