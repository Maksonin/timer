from datetime import datetime,timedelta
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo

hour = 0
min = 0
sec = 0

preHour = 0
preMin = 0
preSec = 0

timerStatus = 0 # переменная для хранения статуса работы таймера. От этой переменной зависит работа счетчика времени
timerMode = "seconds" # переменная для хранения режима работы таймера

# функция запуска таймера
# при вызове функции - если таймер выключен, то происходит включение, и наоборот
def timerStart():
    global timerStatus, timerMode, hour, min, sec
    timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
    timeLabel["text"] = timerStr
    if timerStatus != 1: # если таймер выключен или на паузе
        
        
        btnS["text"] = "Пауза" 

        now = datetime.now()
        timeNow = now.strftime("%H:%M:%S")

        # if timerMode == "seconds":
        #     timeLabel["text"] = timerStr
        
        if timerMode == "timer" and timerStatus != 2:
            if hourEnty.get() == "":
                hour = 0
            else: hour = int(hourEnty.get())
            if minuteEnty.get() == "":
                min = 0
            else: min = int(minuteEnty.get())
            if secondsEnty.get() == "":
                sec = 0
            else: sec = int(secondsEnty.get())
        
        if timerMode == "timer":
            endTime = now + timedelta(hours=int(hour), minutes=int(min), seconds=int(sec))
            infoLabel["text"] = "Таймер закончит - " + endTime.strftime("%H:%M:%S")
        
        timerStatus = 1 # таймер включается
        # смена состояния компонентов для выбора режимов
        combobox.configure(state = "disable")
        for child in settingFrame.winfo_children():
            child.configure(state='disable')
        btnStop["state"] = "normal"
        # запись начального значения времени в label - timeLabel
        timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
        timeLabel["text"] = timerStr
        root.after(1000, timerPlus)  # вызов функции счета времени
        statusLabel["text"] = "Старт в " + timeNow
        tree.insert("", END, values=(combobox.get() + ". Старт", timeNow, timerStr))  # запись данных в таблицу истории
        
    else: # иначе, если таймер включен
        timerStatus = 2 # таймер устанавливает статус - пауза
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
    infoLabel["text"] = "Считать указанное количество времени"
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
    
    if timerMode != "seconds":
        for child in settingFrame.winfo_children():
            child.configure(state='enable')
    combobox.configure(state = "enable")


# функция счета времени таймера. Вызывается каждую секунду
def timerPlus():
    global timerStatus, timerMode, hour, min, sec
    if timerStatus == 1:
        # если выбран режим таймер
        if timerMode == "timer":
            #print(str(hour) + " " + str(min)  + " " + str(sec))
            # если таймер досчитал до конца
            if (hour == 0) and  (min == 0) and (sec == 0) :
                showinfo(title="Информация", message="Таймер посчитал ^_^")
                timerStop()
                return
            
            sec = sec - 1
            if sec == -1:
                sec = 59
                min = min - 1
            if min == -1:
                min = 59
                hour = hour - 1
            if hour == -1:
                hour = 23
        # в остальных режимах
        else:
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


# функция обработчик выбора режима таймера
def selected(event):
    global timerMode
    mode = combobox.get() 
    print(mode)
    if mode == "Счетчик":
        timerMode = "seconds"
        infoLabel["text"] = "Счет времени"
        for child in settingFrame.winfo_children():
            child.configure(state='disable')
    elif mode == "Таймер":
        timerMode = "timer"
        infoLabel["text"] = "Отсчет введенного времени"
        for child in settingFrame.winfo_children():
            child.configure(state='enable')
    else:
        timerMode = "seconds"
        infoLabel["text"] = "Функционал в разработке"
        for child in settingFrame.winfo_children():
            child.configure(state='disable')
    
    #print(timerMode)


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
for r in range(5): frame1.rowconfigure(index=r, weight=1) # grid - 5 строки

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
languages = ["Счетчик", "Таймер", "Счет до времени", "Последовательности"]
combobox = ttk.Combobox(frame1, values=languages, state="readonly")
combobox.grid(row=3,column=0,columnspan=2)
combobox.bind("<<ComboboxSelected>>", selected)
combobox.current(0)

infoLabel = ttk.Label(frame1, text="-")
infoLabel.grid(row=4,column=0,columnspan=2,ipady=6)

# 
settingFrame = ttk.Frame(frame1)
settingFrame.grid(row=5, column=0, columnspan=2)
for c in range(8): settingFrame.columnconfigure(index=c, weight=1) # grid - 8 столбца
for r in range(3): settingFrame.rowconfigure(index=r, weight=1) # grid - 3 строки

infoLabelH = ttk.Label(settingFrame, text="Часы", state="disable")
infoLabelH.grid(row=1,column=0,columnspan=2)
hourEnty = ttk.Spinbox(settingFrame, width=6, from_=0, to=24,state="disable")
hourEnty.grid(row=2,column=0,columnspan=2)

infoLabelM = ttk.Label(settingFrame, text="Минуты", state="disable")
infoLabelM.grid(row=1,column=3,columnspan=2)
minuteEnty = ttk.Spinbox(settingFrame, width=6, from_=0, to=60, state="disable")
minuteEnty.grid(row=2,column=3,columnspan=2)

infoLabelS = ttk.Label(settingFrame, text="Секунды", state="disable")
infoLabelS.grid(row=1,column=6,columnspan=2)
secondsEnty = ttk.Spinbox(settingFrame, width=6, from_=0, to=60, state="disable")
secondsEnty.grid(row=2,column=6,columnspan=2)

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

historyInfo = ttk.Label(frame2, justify=CENTER, text="Внимание!\nИстория на данный момент никуда не сохраняется \nи удаляется после закрытия программы", background="#FFCDD2")
historyInfo.pack(expand=True)

root.mainloop()