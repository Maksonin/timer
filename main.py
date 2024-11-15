from datetime import datetime
from tkinter import *
from tkinter import ttk

hour = 0
min = 0
sec = 0

timerStatus = False # переменная для хранения статуса работы таймера. От этой переменной зависит работа счетчика времени

# функция запуска таймера
# при вызове функции - если таймер выключен, то происходит включение, и наоборот
def timerStart():
    global timerStatus
    timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
    if timerStatus == False: # если таймер выключен
        timerStatus = True # таймер включается
        btnS["text"] = "Пауза" 

        now = datetime.now()
        timeNow = now.strftime("%H:%M:%S")
        statusLabel["text"] = "Старт в " + timeNow
        tree.insert("", END, values=("Старт", timeNow, timerStr))  # запись данных в таблицу истории

        root.after(1000, timerPlus)  # вызов функции счета времени
        btnStop["state"] = "normal"
    else: # иначе, если таймер включен
        timerStatus = False # таймер выключается
        btnS["text"] = "Старт"
        now = datetime.now()
        timeNow = now.strftime("%H:%M:%S")
        statusLabel["text"] = "Пауза в " + timeNow
        tree.insert("", END, values=("Пауза", timeNow, timerStr))

# функция остановки таймера
# при вызове функции сбрасываются все переменные таймера и 
def timerStop():
    global timerStatus, hour, min, sec
    timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
    
    timeLabel["text"] = timerStr

    # заполняем все признаки остановки
    timerStatus = False
    btnS["text"] = "Старт"
    btnStop["state"] = "disable"

    # записываем данные в историю
    now = datetime.now()
    timeNow = now.strftime("%H:%M:%S")
    statusLabel["text"] = "Стоп в " + timeNow
    tree.insert("", END, values=("Стоп", timeNow, timerStr))
    tree.insert("", END, values=("-","-","-"))

    # обнуляем временные переменные
    sec = 0
    min = 0
    hour = 0
    timeLabel["text"] = "--:--:--"    


# функция счета времени таймера. Вызывается каждую секунду
def timerPlus():
    global timerStatus, hour, min, sec
    if timerStatus:
        sec = sec + 1
        if sec == 60:
            sec = 0
            min = min + 1
        if min == 60:
            min = 0
            hour = hour + 1
        if hour == 24:
            hour = 0
            
        timeLabel["text"] = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
        root.after(1000, timerPlus)  # рекурсивный вызов этой функции для выполнения счета секунд

#
def selected(event):
    print(combobox.get())

# очистка таблицы истории
def clearHistory():
    tree.delete(*tree.get_children())


# ************************************************************************** #
root = Tk()
root.geometry("300x400")
root.minsize(300,400)   # минимальные размеры: ширина - 300, высота - 400
root.maxsize(300,400)   # максимальные размеры: ширина - 300, высота - 400
 
root.title("Timer")

# создаем набор вкладок
notebook = ttk.Notebook()
notebook.pack()

# создаем пару фреймвов
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)

# добавляем фреймы в качестве вкладок
notebook.add(frame1, text="Счетчик")
# notebook.add(frame2, text="Таймер",state="disabled")
notebook.add(frame2, text="История")

# настройка сетки
for c in range(2): frame1.columnconfigure(index=c, weight=1) # grid - 2 столбца
for r in range(5): frame1.rowconfigure(index=r, weight=1) # grid - 4 строки

# добавление label для отображения времени
timeLabel = ttk.Label(frame1, text="--:--:--", font=("Arial", 20), padding="5")
timeLabel.grid(row=0,column=0,columnspan=2)

# добавление label для определения времени последнего события
statusLabel = ttk.Label(frame1, text="-")
statusLabel.grid(row=1,column=0,columnspan=2)

# добавление кнопок для управления таймером
btnS = ttk.Button(frame1, text="Старт", command=timerStart) # создаем кнопку из пакета ttk
btnS.grid(row=2,column=0)    # размещаем кнопку в окне
btnStop = ttk.Button(frame1, text="Стоп", command=timerStop, state="disable") # создаем кнопку из пакета ttk
btnStop.grid(row=2,column=1)    # размещаем кнопку в окне

# добавление чекбокса с выбором режимов
languages = ["Счетчик", "Счет минут", "Счет секунд", "Счет до времени", "Последовательности"]
combobox = ttk.Combobox(frame1, values=languages, state="readonly")
combobox.grid(row=3,column=0,columnspan=2)
combobox.bind("<<ComboboxSelected>>", selected)
combobox.current(0)


# ************************************************************************** #
# Вкладка "История"
# Настройка таблицы истории
# Определяем столбцы
columns = ("task", "time", "timer")
 
tree = ttk.Treeview(frame2,columns=columns, show="headings")
tree.pack()
 
# определяем заголовки
tree.heading("task", text="Действие")
tree.heading("time", text="Время ПК")
tree.heading("timer", text="Таймер")

# настраиваем колонки
tree.column("#1", stretch=NO, width=90)
tree.column("#2", stretch=NO, width=90)
tree.column("#3", stretch=NO, width=90)

btnClearHistory = ttk.Button(frame2, text="Очистить историю", command=clearHistory, padding=0)
btnClearHistory.pack()

root.mainloop()