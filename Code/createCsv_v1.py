import pandas as pd
from datetime import datetime

# tolgo solo il primo elemento della lista, tolgo count e uso len(lista)
# funzione per prendere la prima riga in base ad un anno dato in input
def takeIndex(dates, dateStart):
    i = 0
    for date in dates:
        dtObj = datetime.strptime(date, '%Y-%m-%d').date()
        if dateStart == dtObj:
            break
        i += 1

    return i

# funzione per creare il CSV da un giorno
def createCsv (data, start, finish, name):
    csv1g = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])
    for i in range(start, finish + 1):
        csv1g = csv1g.append(data.iloc[i], ignore_index = True)
    csv1g.to_csv(name, index = False)

# funzione per prendere il massimo il minimo e la somma dei volumi
def getHLS (list):
    highest = list[0].iloc[2]
    lowest = list[0].iloc[3]
    sumVolume = list[0].iloc[6]
    i = 0
    for item in list:
        if i != 0:
            if highest < item.iloc[2]:
                highest = item.iloc[2]

            if lowest > item.iloc[3]:
                lowest = item.iloc[3]

            sumVolume += item.iloc[6]
        i += 1
    return highest, lowest, sumVolume

# funzione per creare i cvs divisi per giorni
def createCSV_V2 (data, start, finish, name, div, flag):
    csv = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'])

    list = [data.iloc[start]]
    for i in range(start + 1, finish + 1):
        list.append(data.iloc[i])
        if len(list) == div:
            highest, lowest, sumVolume = getHLS(list)
            row = {'Date': [list[0].iloc[0] + "/" + list[len(list) - 1].iloc[0]], 'Open': [list[0].iloc[1]],
                   'High': [highest], 'Low': [lowest], 'Close': [list[len(list) - 1].iloc[4]],
                   'Adj Close': [list[len(list) - 1].iloc[5]], 'Volume': [sumVolume]}
            dataFrame = pd.DataFrame(row)
            csv = csv.append(dataFrame, ignore_index=True)
            list.pop(0)

    '''
    if flag:
        for item in list:
            highest, lowest, sumVolume = getHLS(list)
            row = {'Date': [list[0].iloc[0] + "/" + list[len(list) - 1].iloc[0]], 'Open': [list[0].iloc[1]],
                   'High': [highest], 'Low': [lowest], 'Close': [list[len(list) - 1].iloc[4]],
                   'Adj Close': [list[len(list) - 1].iloc[5]], 'Volume': [sumVolume]}
            dataFrame = pd.DataFrame(row)
            csv = csv.append(dataFrame, ignore_index=True)
            list.pop(0)

    '''
    if len(list) and flag:
        highest, lowest, sumVolume = getHLS(list)
        row = {'Date': [list[0].iloc[0] + "/" + list[len(list) - 1].iloc[0]], 'Open': [list[0].iloc[1]],
               'High': [highest], 'Low': [lowest], 'Close': [list[len(list) - 1].iloc[4]],
               'Adj Close': [list[len(list) - 1].iloc[5]], 'Volume': [sumVolume]}
        dataFrame = pd.DataFrame(row)
        csv = csv.append(dataFrame, ignore_index=True)

    csv.to_csv(name, index=False)

# MAIN
# leggo il cvs
data = pd.read_csv("DXYN.csv")
# estrazione date
dates = data.loc[:, "Date"]

div = int(input("Scegliere il numero di giorni per cui dividere: "))
while div > 0:
    # leggo la data di inizio e converto la stringa in data
    dateStart = input("Da che data iniziare: ")
    start = takeIndex(dates, datetime.strptime(dateStart, '%Y-%m-%d').date())

    dateFinish = input("A che data finire: ")
    finish = takeIndex(dates, datetime.strptime(dateFinish, '%Y-%m-%d').date())

    flag = int(input("Aggiungere le ultime date che possono rimanere alla fine della divisione ? (Si = 1, No = 0):  "))

    name = input("Scrivere il nome (ricordarsi il .csv): ")

    print("Creazione csv...")
    if div == 1:
        createCsv(data, start, finish, name)
    else:
        createCSV_V2(data, start, finish, name, div, flag)

    print("Creazione conclusa.")
    div = int(input("Creare altri file? (scrivere 0 per dire NO, il numero dei giorni per cui vuoi dividere per dire SI): "))
