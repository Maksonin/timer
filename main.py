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
        tree.insert("", END, values=("Старт", now.strftime("%H:%M:%S"),timerStr))  # запись данных в таблицу истории

        root.after(1000, timerPlus)  # вызов функции счета времени
    else:
        timerStatus = False
        btnS["text"] = "Старт"
        now = datetime.now()
        tree.insert("", END, values=("Пауза", now.strftime("%H:%M:%S"),timerStr))

# функция остановки таймера
# при вызове функции сбрасываются все переменные таймера и 
def timerStop():
    global timerStatus, hour, min, sec
    timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
    
    label["text"] = timerStr

    timerStatus = False
    btnS["text"] = "Старт"

    now = datetime.now()
    tree.insert("", END, values=("Стоп", now.strftime("%H:%M:%S"),timerStr))
    tree.insert("", END, values=("-","-","-"))

    sec = 0
    min = 0
    hour = 0
    label["text"] = "--:--:--"


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
            
        label["text"] = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
        root.after(1000, timerPlus)  # рекурсивный вызов этой функции для выполнения счета секунд


# ************************************************************************** #
root = Tk()
root.geometry("300x400")
root.minsize(300,400)   # минимальные размеры: ширина - 300, высота - 450
root.maxsize(300,400)   # максимальные размеры: ширина - 300, высота - 400
 
root.title("Timer")

# создаем набор вкладок
notebook = ttk.Notebook()
notebook.pack(expand=True, fill=BOTH)

# создаем пару фреймвов
frame1 = ttk.Frame(notebook)
frame2 = ttk.Frame(notebook)
frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)

# добавляем фреймы в качестве вкладок
notebook.add(frame1, text="Счетчик")
notebook.add(frame2, text="Таймер",state="disabled")

# настройка сетки
for c in range(2): frame1.columnconfigure(index=c, weight=1) # grid - 2 столбца
for r in range(4): frame1.rowconfigure(index=r, weight=1) # grid - 4 строки

# добавление label для отображения времени
label = ttk.Label(frame1, text="--:--:--", font=("Arial", 18),padding="5", )
label.grid(row=0,column=0,columnspan=2)

# добавление кнопок
btnS = ttk.Button(frame1, text="Старт", command=timerStart) # создаем кнопку из пакета ttk
btnS.grid(row=1,column=0)    # размещаем кнопку в окне
btnClear = ttk.Button(frame1, text="Сброс", command=timerStop) # создаем кнопку из пакета ttk
btnClear.grid(row=1,column=1)    # размещаем кнопку в окне

# определяем данные для отображения
people = [("Start", "10:22"), ("Pause", "10:25"), ("Stop", "10:32")]
 
# определяем столбцы
columns = ("task", "time", "timer")
 
tree = ttk.Treeview(frame1,columns=columns, show="headings")
tree.grid(row=2, column=0, rowspan=2, columnspan=2)
 
# определяем заголовки
tree.heading("task", text="Действие")
tree.heading("time", text="Время ПК")
tree.heading("timer", text="Таймер")

# настраиваем колонки
tree.column("#1", stretch=NO, width=90)
tree.column("#2", stretch=NO, width=90)
tree.column("#3", stretch=NO, width=90)

root.mainloop()