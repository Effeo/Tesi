from datetime import datetime
import pandas as pd

def createWalks(data, start, finsih, name):
    csv = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])

    for i in range(start, finsih + 1):
        csv = csv.append(data.iloc[i], ignore_index=True)

    csv.to_csv(name, index = False)


def takeIndex(dates, dateFind):
    i = 0
    for date in dates:
        dtObj = datetime.strptime(date, '%Y-%m-%d').date()
        if dateFind == dtObj:
            break
        i += 1

    return i

def takeIndex2(dates, dateFind):
    i = 0
    for date in dates:
        firstDate = date[0 : date.find('/')]
        dtObj = datetime.strptime(firstDate, '%Y-%m-%d').date()
        if dateFind == dtObj:
            break
        i += 1

    return i

def takeIndex3(dates, dateFind):
    i = 0
    for date in dates:
        lastDate = date[date.find('/') + 1 : len(date)]
        dtObj = datetime.strptime(lastDate, '%Y-%m-%d').date()
        if dateFind == dtObj:
            break
        i += 1

    return i

def main():
    data1 = pd.read_csv("div1Label.csv")
    data2 = pd.read_csv("div2Label.csv")
    data4 = pd.read_csv("div4Label.csv")
    data5 = pd.read_csv("div5Label.csv")

    dates1 = data1.loc[:, "Date"]
    dates2 = data2.loc[:, "Date"]
    dates4 = data4.loc[:, "Date"]
    dates5 = data5.loc[:, "Date"]

    #training day 1
    '''
    start = takeIndex(dates1, datetime.strptime("2000-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2009-01-30", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining1_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2000-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining2_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2001-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining3_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2001-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining4_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2002-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining5_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2002-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining6_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2003-02-03", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining7_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2003-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining8_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2004-02-02", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining9_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2004-08-02", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining10_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2005-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTraining11_day1.csv")
    
    #training day 2
    '''
    start = takeIndex2(dates2, datetime.strptime("2000-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2009-01-30", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining1_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2000-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining2_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2001-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining3_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2001-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining4_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2002-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining5_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2002-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining6_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2003-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining7_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2003-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining8_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2004-02-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining9_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2004-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining10_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2005-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTraining11_day2.csv")

    #training day 4

    start = takeIndex2(dates4, datetime.strptime("2000-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2009-01-30", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining1_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2000-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining2_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2001-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining3_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2001-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining4_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2002-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining5_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2002-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining6_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2003-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining7_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2003-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining8_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2004-02-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining9_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2004-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining10_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2005-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTraining11_day4.csv")

    #training day 5

    start = takeIndex2(dates5, datetime.strptime("2000-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2009-01-30", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining1_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2000-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining2_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2001-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining3_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2001-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining4_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2002-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining5_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2002-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining6_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2003-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining7_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2003-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining8_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2004-02-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining9_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2004-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining10_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2005-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTraining11_day5.csv")

    #validation day 1
    '''
    start = takeIndex(dates1, datetime.strptime("2009-02-02", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation1_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation2_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation3_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation4_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation5_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation6_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation7_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation8_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation9_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation10_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkValidation11_day1.csv")
    '''

    #validation day 2

    start = takeIndex2(dates2, datetime.strptime("2009-02-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation1_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation2_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation3_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation4_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation5_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation6_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation7_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation8_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation9_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation10_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkValidation11_day2.csv")

    #validation day 4

    start = takeIndex2(dates4, datetime.strptime("2009-02-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation1_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation2_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation3_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation4_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation5_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation6_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation7_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation8_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation9_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation10_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkValidation11_day4.csv")

    #validation day 5

    start = takeIndex2(dates5, datetime.strptime("2009-02-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2009-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation1_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation2_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation3_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation4_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation5_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation6_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation7_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation8_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation9_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation10_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkValidation11_day5.csv")

    #testing day 1
    '''
    start = takeIndex(dates1, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting1_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting2_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting3_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting4_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting5_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting6_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting7_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting8_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting9_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting10_day1.csv")

    start = takeIndex(dates1, datetime.strptime("2014-08-01", '%Y-%m-%d').date())
    finish = takeIndex(dates1, datetime.strptime("2015-01-30", '%Y-%m-%d').date())
    createWalks(data1, start, finish, "WalkTesting11_day1.csv")
    '''
    #testing day 2

    start = takeIndex2(dates2, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting1_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting2_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting3_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting4_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting5_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting6_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting7_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting8_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting9_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting10_day2.csv")

    start = takeIndex2(dates2, datetime.strptime("2014-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates2, datetime.strptime("2015-01-30", '%Y-%m-%d').date())
    createWalks(data2, start, finish, "WalkTesting11_day2.csv")

    #testing day 4

    start = takeIndex2(dates4, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting1_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting2_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting3_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting4_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting5_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting6_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting7_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting8_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting9_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting10_day4.csv")

    start = takeIndex2(dates4, datetime.strptime("2014-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates4, datetime.strptime("2015-01-30", '%Y-%m-%d').date())
    createWalks(data4, start, finish, "WalkTesting11_day4.csv")
    
    #testing day 5
    start = takeIndex2(dates5, datetime.strptime("2009-08-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2010-01-29", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting1_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2010-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2010-07-30", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting2_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2010-08-02", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2011-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting3_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2011-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2011-07-29", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting4_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2011-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2012-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting5_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2012-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2012-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting6_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2012-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2013-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting7_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2013-02-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2013-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting8_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2013-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2014-01-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting9_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2014-02-03", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2014-07-31", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting10_day5.csv")

    start = takeIndex2(dates5, datetime.strptime("2014-08-01", '%Y-%m-%d').date())
    finish = takeIndex3(dates5, datetime.strptime("2015-01-30", '%Y-%m-%d').date())
    createWalks(data5, start, finish, "WalkTesting11_day5.csv")

main()