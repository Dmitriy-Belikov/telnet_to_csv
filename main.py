import asyncio, telnetlib3, datetime, csv
import time


async def shell(reader, writer):
    #nowdate = '19.01.2023'  # для теста
    #nowdate = 456
    nowdate = str(input('Введите сегодняшнюю дату в формате ДД.мм.ГГ\nНапример: 13.01.2023\n'))

    dt_pc = datetime.datetime.today() #Текущая дата компьютера для расчета дельты времени

    dt_now = datetime.datetime(int(nowdate[6:10]), int(nowdate[3:5]), int(nowdate[0:2]))  # получение текущей даты от пользователя
    delta = dt_now - datetime.datetime(dt_pc.year, dt_pc.month,
                                       dt_pc.day)  # получаем разницу в формате 6 days, 0:00:00
    while True:
        line = await reader.readline()
        if not line:
            break
        #print(line.rstrip(), flush=True) #line.rstrip приходящие значения из телнет
        dt_pc = datetime.datetime.today() #Текущая дата компьютера для прибавления дельты и получения реальной даты
        real_date = dt_pc + delta  # Реальная дата
        real_date = str(real_date) #преобразование даты в строку
        date_tetra = real_date[5:7] + real_date[8:10] + real_date[2:4]#получние даты и времени в формате 011323,000300
        time_tetra = real_date[11:13] + real_date[14:16] + real_date[17:19]
        arr1 = line.rstrip().split(',') #преобразование в массив для замены даты и времени
        try:
            arr1[0] = date_tetra
            arr1[1] = time_tetra
        except IndexError:
            pass
        arr2 = []
        arr2.append(arr1)#Костыль для нормальной записи csv (список в список)
        print(','.join(arr1))
        with open('C:/CSV/orion.csv', 'a', newline='') as f:
            writer = csv.writer(f)
            for row in arr2:
                writer.writerow(row)



if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    coro = telnetlib3.open_connection(host="127.0.0.1",port=23, shell=shell)
    asyncio.set_event_loop(loop)
    reader, writer = loop.run_until_complete(coro)
    try:
        loop.run_until_complete(writer.protocol.waiter_closed)
    except KeyboardInterrupt:
        pass