
from tkinter import *
from tkinter.ttk import Combobox
import asyncio, telnetlib3, datetime, csv
import time
from threading import Thread
from tkcalendar import Calendar

potok = True
#Функция обработки значений
async def shell(reader, writer):
    global potok
    nowdate = calendar.get_date()

    dt_pc = datetime.datetime.today()  # Текущая дата компьютера для расчета дельты времени

    dt_now = datetime.datetime(int(nowdate[6:10]), int(nowdate[3:5]),
                               int(nowdate[0:2]))  # получение текущей даты от пользователя
    delta = dt_now - datetime.datetime(dt_pc.year, dt_pc.month,
                                       dt_pc.day)  # получаем разницу в формате 6 days, 0:00:00
    while True:
        line = await reader.readline()
        if not line:
            break
        dt_pc = datetime.datetime.today()  # Текущая дата компьютера для прибавления дельты и получения реальной даты
        real_date = dt_pc + delta  # Реальная дата
        real_date = str(real_date)  # преобразование даты в строку
        date_tetra = real_date[5:7] + real_date[8:10] + real_date[
                                                        2:4]  # получние даты и времени в формате 011323,000300
        time_tetra = real_date[11:13] + real_date[14:16] + real_date[17:19]
        arr1 = line.rstrip().split(',')  # преобразование в массив для замены даты и времени
        try:
            arr1[0] = date_tetra
            arr1[1] = time_tetra
        except IndexError:
            pass
        arr2 = []
        arr2.append(arr1)  # Костыль для нормальной записи csv (список в список)
        print(','.join(arr1))
        with open('C:/CSV/orion.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for row in arr2:
                writer.writerow(row)
        data = ','.join(arr1) + '\n'
        text.insert(1.0, data)

        if potok == True:
            continue
        else:
            print('Работа остановлена\nЗапись не идет!')
            text.insert(1.0, 'Работа остановлена. Запись не идет!\n' )
            break #Функия

#Запуск телнет клиента и запуск функции shell
def run():
    loop = asyncio.new_event_loop()
    coro = telnetlib3.open_connection(host="127.0.0.1", port=23, shell=shell)
    asyncio.set_event_loop(loop)
    reader, writer = loop.run_until_complete(coro)
    try:
        loop.run_until_complete(writer.protocol.waiter_closed)
    except KeyboardInterrupt:
        pass


#Обработка кнопки запуск, блокировка ввода значений, проверка соединения, запуск функции run
def button_run():
    text.delete(1.0, END)
    p1 = Thread(target=run, daemon=True)
    p1.start()# запускается функция в отдельном потоке
    global potok
    potok = True
    time.sleep(3)

    '''
    if p1.is_alive() == False:
        text.insert(1.0, 'Не удалось соедениться!\nПроверьте настройки Orion\n')
    else:
        dd.config(state=DISABLED)
        mm.config(state=DISABLED)
        gg.config(state=DISABLED)
        pass'''
#Обработка кнопки стоп, разблокировка ввода значений, остановка функции shell
def button_stop():
    global potok
    potok = False



#Код для GUI приложения
window = Tk()
window.title("Скрипт для ТетраСофт")
window.geometry('500x700')

lbl = Label(window, text='Выберите сегодняшнюю дату', font=('Calibri', 20))
lbl.grid(row=0, column=0, columnspan=3, ipadx=10, ipady=6, padx=5, pady=5)



btn_run = Button(window, text="Начать работу", command=button_run)
btn_run.grid(row=5, column=0, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)

btn_stop = Button(window, text="Остановить работу", command=button_stop)
btn_stop.grid(row=6, column=0, columnspan=3, ipadx=70, ipady=6, padx=5, pady=5)

#Текстовое поле с выводом информации
text = Text(window,height=20,width=13)
text.grid(row=7, column=0, columnspan=3, ipadx=190, ipady=1, padx=5, pady=5)

calendar = Calendar(locale='ru_RU', date_pattern='dd.MM.yyyy')
calendar.grid(row=1, column=0, columnspan=3, ipadx=1, ipady=1, padx=5, pady=5)


window.mainloop()