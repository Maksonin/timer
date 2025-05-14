from datetime import datetime,timedelta
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showerror, showwarning, showinfo
import os
import glob
import enum

hour = 0
min = 0
sec = 0

preHour = 0
preMin = 0
preSec = 0

class timerCondition(enum.Enum):
    stop = 0
    start = 1
    pause = 2

timerStatus = timerCondition.stop # переменная для хранения статуса работы таймера. От этой переменной зависит работа счетчика времени
timerMode = "seconds" # переменная для хранения режима работы таймера

# функция запуска таймера
# при вызове функции - если таймер выключен, то происходит включение, и наоборот
def timerStart():
    global timerStatus, timerCondition, timerMode, hour, min, sec
    timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
    timeLabel["text"] = timerStr

    clearHistory()
    historyFileGet()

    now = datetime.now()
    timeNow = now.strftime("%H:%M:%S")
    
    # если таймер не запущен 
    if timerStatus != timerCondition.start: 
        # если таймер остановлен (timerStatus = 0 (timerCondition.stop)), то записываем дату запуска таймера
        if timerStatus != timerCondition.pause:
            print(now.date())
            historyFileSave(str(now.date()) + "\n")

        # если режим не счетчик времени
        # то расцениваем пустые ячейки ввода времени как 0
        if timerMode != "seconds":
            # если таймер не на паузе
            if hourEnty.get() == "":
                hour = 0
            else: hour = int(hourEnty.get())
            if minuteEnty.get() == "":
                min = 0
            else: min = int(minuteEnty.get())
            if secondsEnty.get() == "":
                sec = 0
            else: sec = int(secondsEnty.get())
        
        # если режим работы - таймер
        # расчет времени окончания счета таймера
        if timerMode == "timer":
            endTime = now + timedelta(hours=int(hour), minutes=int(min), seconds=int(sec))
            infoLabel["text"] = "Таймер закончит - " + endTime.strftime("%H:%M:%S")
        
        # таймер включается
        timerStatus = timerCondition.start 
        btnS["text"] = "Пауза" 

        # смена состояния компонентов формы для выбора режимов
        modeSelect.configure(state = "disable")
        for child in settingFrame.winfo_children():
            child.configure(state='disable')
        btnStop["state"] = "normal"
        timerSelect["state"] = "disable"
        # запись начального значения времени в label - timeLabel
        timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
        timeLabel["text"] = timerStr
        
        statusText = "Старт - " + timeNow # подготовка строки текста для описания текущего состояния работы
        statusLabel["text"] = statusText # вывод статусной строки в соответствующий label
        
        # сохранение в файл такущего состояния
        historyFileSave(modeSelect.get() + " " + statusText + " - " + timerStr + "\n")
        # запись данных в таблицу истории
        tree.insert("", 0, values=(modeSelect.get() + ". Старт", timeNow, timerStr))  

        root.after(1000, timerPlus)  # вызов функции счета времени
        
    else: # иначе, если таймер включен
        timerStatus = timerCondition.pause # таймер устанавливает статус - пауза
        btnS["text"] = "Продолжить"

        statusText = "Пауза - " + timeNow
        statusLabel["text"] = statusText

        historyFileSave(statusText + " - " + timerStr + "\n")
        tree.insert("", 0, values=("Пауза", timeNow, timerStr))


# функция остановки таймера
# при вызове функции сбрасываются все переменные таймера и 
def timerStop():
    global timerStatus, timerCondition, hour, min, sec
    timerStr = str(f'{hour:02}') + ':' + str(f'{min:02}') + ':' + str(f'{sec:02}')
    timeLabel["text"] = timerStr

    # записываем данные в историю
    now = datetime.now()
    timeNow = now.strftime("%H:%M:%S")
    statusText = "Стоп - " + timeNow
    statusLabel["text"] = statusText

    historyFileSave(statusText + " - " + timerStr + "\n" + "---" + "\n")
    tree.insert("", 0, values=("Стоп", timeNow, timerStr))
    tree.insert("", 0, values=("-","-","-"))

    # обнуляем временные переменные
    sec = 0
    min = 0
    hour = 0
    
    # заполняем все признаки остановки
    timerStatus = timerCondition.stop
    btnS["text"] = "Старт"
    btnStop["state"] = "disable"
    timerSelect["state"] = "enable"
    infoLabel["text"] = "Счетчик"
    
    timerSelect["value"] = getHistoryFile()

    if timerMode != "seconds":
        for child in settingFrame.winfo_children():
            child.configure(state='enable')
    modeSelect.configure(state = "enable")

# функция счета времени таймера. Вызывается каждую секунду
def timerPlus():
    global timerStatus, timerCondition,  timerMode, hour, min, sec
    if timerStatus == timerCondition.start:
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
def modeSelectDef(event):
    global timerMode
    mode = modeSelect.get() 
    print(mode)
    if mode == "Счетчик":
        timerMode = "seconds"
        infoLabel["text"] = "Счетчик"
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

# Функция срабатывающая при изменении комбобокса timerSelect
def timerSelectDef(event):
    # global timerNum
    print("timerSelect!")
    timerSelect["value"] = getHistoryFile()
    timerNum.set(timerSelect.get())
    clearHistory()
    historyFileGet()

# Функция считывает файл в соответствии с комбоксом timerSelect и записывает содержимое в таблицу с историей
def historyFileGet():
    try:
        f = open('h_' + timerSelect.get() + '.txt','r')
        history = f.readlines()
        for h in history:
            h = h.split(" - ")
            print(h)
            if len(h) < 2:
                tree.insert("", 0, values=("-", h[0], "-"))
            else:
                tree.insert("", 0, values=(h[0], h[1], h[2]))
        f.close()
    except Exception as e:
        print("Ошибка считывания файла " + str(e))

# Функция сохранении истории в файл выбранный в timerSelect
def historyFileSave(str):
    try:
        f = open('h_' + timerSelect.get()+'.txt','a+')
        f.write(str)
        f.close()
    except Exception as e:
        print("Ошибка сохранения в файл " + str(e))

# получает список файлов хранящих историю
def getHistoryFile():
    print("getHistoryFile")
    # Получаем список файлов
    files = glob.glob('h_*.txt')
    files_update = [file.replace(".txt","") for file in files]
    files_update = [file.replace("h_","",1) for file in files_update]
        
    print(files_update)

    return files_update

# очистка таблицы истории
def clearHistory():
    tree.delete(*tree.get_children())

# полная очистка файла и очистка таблицы истории
def clearFileHistory():
    clearHistory()
    open('h_' + timerSelect.get() + '.txt', 'w').close()


# функция вызываемая при событии закрытия приложения
def closeTimer():
    root.destroy()  # ручное закрытие окна и всего приложения
    print("Close!")


# ************************************************************************** #
root = Tk()
root.geometry("250x300")
root.minsize(250,350)   # минимальные размеры: ширина - 300, высота - 400
root.maxsize(300,400)   # максимальные размеры: ширина - 300, высота - 400
 
root.title("Timer")

# виджет с выбором истории
timers = getHistoryFile()
timerSelect = ttk.Combobox(values=timers, justify=CENTER)
timerSelect.pack(fill=X , padx=5, pady=2)
timerSelect.bind("<<ComboboxSelected>>", timerSelectDef)
if len(timers) > 0: # если файлы истории есть
    timerSelect.current(0) # то выбирается первый из массива файлов
  
# создаем набор вкладок
notebook = ttk.Notebook()
notebook.pack()

# создаем пару фреймвов
frame1 = ttk.Frame(notebook,borderwidth=1, relief=SOLID, padding=[8, 5])
frame2 = ttk.Frame(notebook,borderwidth=1, relief=SOLID)
frame1.pack(fill=BOTH, expand=True)
frame2.pack(fill=BOTH, expand=True)

# добавляем фреймы в качестве вкладок
notebook.add(frame1, text="Счетчик")
# notebook.add(frame2, text="Таймер",state="disabled")
notebook.add(frame2, text="История")

# настройка сетки
for c in range(2): frame1.columnconfigure(index=c, weight=1) # grid - 2 столбца
for r in range(5): frame1.rowconfigure(index=r, weight=2) # grid - 5 строки

# добавление label для отображения времени
timeLabel = ttk.Label(frame1, text="00:00:00", font=("Arial", 25))
timeLabel.grid(row=1,column=0,columnspan=2)

# добавление label для определения времени последнего события
statusLabel = ttk.Label(frame1, text="-")
statusLabel.grid(row=2,column=0,columnspan=2)

# добавление кнопок для управления таймером
btnS = ttk.Button(frame1, text="Старт", command=timerStart) # создаем кнопку из пакета ttk
btnS.grid(row=3,column=0)    # размещаем кнопку в окне
btnStop = ttk.Button(frame1, text="Стоп", command=timerStop, state="disable") # создаем кнопку из пакета ttk
btnStop.grid(row=3,column=1)    # размещаем кнопку в окне

# добавление чекбокса с выбором режимов
languages = ["Счетчик", "Таймер", "Счет до времени", "Последовательности"]
modeSelect = ttk.Combobox(frame1, values=languages, state="readonly")
modeSelect.grid(row=4,column=0,columnspan=2)
modeSelect.bind("<<ComboboxSelected>>", modeSelectDef)
modeSelect.current(0)

infoLabel = ttk.Label(frame1, text="-")
infoLabel.grid(row=5,column=0,columnspan=2,ipady=6)

# 
settingFrame = ttk.Frame(frame1)
settingFrame.grid(row=6, column=0, columnspan=2)
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

timerNum = StringVar()

timerSelectLabel = ttk.Label(frame2, justify=CENTER, textvariable=timerNum, padding=2)
timerSelectLabel.pack(expand=True)

tree = ttk.Treeview(frame2, columns=columns, show="headings")
tree.pack()

# определяем заголовки
tree.heading("task", text="Действие")
tree.heading("time", text="Время ПК")
tree.heading("timer", text="Таймер")

# настраиваем колонки
tree.column("#1", stretch=NO, width=100)
tree.column("#2", stretch=NO, width=70)
tree.column("#3", stretch=NO, width=70)

btnClearHistory = ttk.Button(frame2, text="Очистить историю", command=clearHistory, padding=0)
btnClearHistory.pack()
btnClearFileHistory = ttk.Button(frame2, text="Очистить файл", command=clearFileHistory, padding=0)
btnClearFileHistory.pack()

# historyInfo = ttk.Label(frame2, justify=CENTER, text="Внимание!\nИстория на данный момент никуда\nне сохраняется и удаляется после\nзакрытия программы", background="#FFCDD2")
# historyInfo.pack(expand=True)

timerSelectDef(None)

root.protocol("WM_DELETE_WINDOW", closeTimer)

root.mainloop()