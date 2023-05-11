import pandas as pd
from datetime import datetime


def takeIndex(dates, dateStart):
    i = 0
    for date in dates:
        dtObj = datetime.strptime(date, '%Y-%m-%d').date()
        if dateStart == dtObj:
            break
        i += 1

    return i

def getLabel(data, i, close):
    list = [data.iloc[i + 1]]
    closeNextDay = list[0].iloc[4]

    if close == closeNextDay : return 2

    if close > closeNextDay : return 1

    if close < closeNextDay : return 0

def addLabel1g(data: pd.DataFrame, name):
    csv1g = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])

    for i in range(0, data.shape[0]):
        list = [data.iloc[i]]
        if(i + 1 < data.shape[0]):
            row = {'Date': [list[0].iloc[0]], 'Open': [list[0].iloc[1]],
                   'High': [list[0].iloc[2]], 'Low': [list[0].iloc[3]], 'Close': [list[0].iloc[4]],
                   'Adj Close': [list[0].iloc[5]], 'Volume': [list[0].iloc[6]], 'Label' : [getLabel(data, i, list[0].iloc[4])]}

        else:
            row = {'Date': [data.iloc[i].iloc[0]], 'Open': [data.iloc[i].iloc[1]],
                   'High': [data.iloc[i].iloc[2]], 'Low': [data.iloc[i].iloc[3]], 'Close': [data.iloc[i].iloc[4]],
                   'Adj Close': [data.iloc[i].iloc[5]], 'Volume': [data.iloc[i].iloc[6]],
                   'Label': [None]}

        dataFrame = pd.DataFrame(row)
        csv1g = csv1g.append(dataFrame, ignore_index=True)

    csv1g.to_csv(name, index=False)

def getLabelNg(date, close, dates, data1g):
    lastDate = date[date.find('/') + 1 : len(date)]
    i = takeIndex(dates, datetime.strptime(lastDate, '%Y-%m-%d').date())

    list = [data1g.iloc[i + 1]]
    closeNextDay = list[0].iloc[4]

    if close == closeNextDay: return 2

    if close > closeNextDay: return 1

    if close < closeNextDay: return 0

def addLabelnG(data: pd.DataFrame, data1g: pd.DataFrame, name, dates):
    csv = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])

    for i in range(0, data.shape[0]):
        list = [data.iloc[i]]

        if(i + 1 < data.shape[0]):
            row = {'Date': [list[0].iloc[0]], 'Open': [list[0].iloc[1]],
                   'High': [list[0].iloc[2]], 'Low': [list[0].iloc[3]], 'Close': [list[0].iloc[4]],
                   'Adj Close': [list[0].iloc[5]], 'Volume': [list[0].iloc[6]],
                   'Label': [getLabelNg(list[0].iloc[0], list[0].iloc[4], dates, data1g)]}
        else:
            row = {'Date': [data.iloc[i].iloc[0]], 'Open': [data.iloc[i].iloc[1]],
                   'High': [data.iloc[i].iloc[2]], 'Low': [data.iloc[i].iloc[3]], 'Close': [data.iloc[i].iloc[4]],
                   'Adj Close': [data.iloc[i].iloc[5]], 'Volume': [data.iloc[i].iloc[6]],
                   'Label': [None]}

        dataFrame = pd.DataFrame(row)
        csv = csv.append(dataFrame, ignore_index=True)

    csv.to_csv(name, index=False)

data1g = pd.read_csv("div1.csv")
dates = data1g.loc[:, "Date"]
data2g = pd.read_csv("div2.csv")
data4g = pd.read_csv("div4.csv")
data5g = pd.read_csv("div5.csv")

addLabelnG(data4g, data1g, "div4Label.csv", dates)
addLabelnG(data5g, data1g, "div5Label.csv", dates)
#addLabelnG(data2g, data1g, "div2Label.csv", dates)
#addLabel1g(data1g, "div1Label.csv")
