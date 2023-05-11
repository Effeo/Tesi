from datetime import datetime
import pandas as pd
import os

def createWalks(data5, data1, data2, data4, name):
    csv5 = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
    csv1 = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
    csv2 = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
    csv4 = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])

    i_1 = 4
    i_2 = 3
    i_4 = 1
    count = 0

    for i in range(0, len(data5)):
        if count < 20:
            csv5 = csv5.append(data5.iloc[i], ignore_index=True)
            csv4 = csv4.append(data4.iloc[i_4], ignore_index=True)
            csv2 = csv2.append(data2.iloc[i_2], ignore_index=True)
            csv1 = csv1.append(data1.iloc[i_1], ignore_index=True)

            count += 1
            i_1 += 1
            i_2 += 1
            i_4 += 1

            if count == 20:
                lastData = csv1.iloc[-1, 0]
                label = csv1.iloc[-1, 7]
                nameDir = name + str(lastData) + "_" + str(label)

                os.mkdir(nameDir)
                csv5.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_5.csv", index=False)
                csv1.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_1.csv", index=False)
                csv2.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_2.csv", index=False)
                csv4.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_4.csv", index=False)

        if count > 20:
            csv5 = csv5.append(data5.iloc[i], ignore_index=True)
            csv4 = csv4.append(data4.iloc[i_4], ignore_index=True)
            csv2 = csv2.append(data2.iloc[i_2], ignore_index=True)
            csv1 = csv1.append(data1.iloc[i_1], ignore_index=True)

            i_1 += 1
            i_2 += 1
            i_4 += 1

            csv5 = csv5.drop(csv5.index[0])
            csv4 = csv4.drop(csv4.index[0])
            csv2 = csv2.drop(csv2.index[0])
            csv1 = csv1.drop(csv1.index[0])

            lastData = csv1.iloc[-1, 0]
            label = csv1.iloc[-1, 7]
            nameDir = name + str(lastData) + "_" + str(label)

            os.mkdir(nameDir)
            csv5.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_5.csv", index=False)
            csv1.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_1.csv", index=False)
            csv2.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_2.csv", index=False)
            csv4.to_csv(nameDir + "/" + str(lastData) + "_" + str(label) + "_day_4.csv", index=False)

        if count == 20: count += 1

def main():

    '''
    os.mkdir("WalkTraining_div20")
    for i in range(1, 12):
        data5 = pd.read_csv("WalkTraining/WalkTraining_day5/WalkTraining" + str(i) + "_day5.csv")
        data1 = pd.read_csv("WalkTraining/WalkTraining_day1/WalkTraining" + str(i) + "_day1.csv")
        data2 = pd.read_csv("WalkTraining/WalkTraining_day2/WalkTraining" + str(i) + "_day2.csv")
        data4 = pd.read_csv("WalkTraining/WalkTraining_day4/WalkTraining" + str(i) + "_day4.csv")

        os.mkdir("WalkTraining_div20/WalkTraining_div20_" + str(i))
        createWalks(data5, data1, data2, data4, "WalkTraining_div20/WalkTraining_div20_" + str(i) + "/")

    '''
    os.mkdir("WalkValidation_div20")
    for i in range(1, 12):
        data5 = pd.read_csv("WalkValidation/WalkValidation_day5/WalkValidation" + str(i) + "_day5.csv")
        data1 = pd.read_csv("WalkValidation/WalkValidation_day1/WalkValidation" + str(i) + "_day1.csv")
        data2 = pd.read_csv("WalkValidation/WalkValidation_day2/WalkValidation" + str(i) + "_day2.csv")
        data4 = pd.read_csv("WalkValidation/WalkValidation_day4/WalkValidation" + str(i) + "_day4.csv")

        os.mkdir("WalkValidation_div20/WalkValidation_div20_" + str(i))
        createWalks(data5, data1, data2, data4, "WalkValidation_div20/WalkValidation_div20_" + str(i) + "/")

    os.mkdir("WalkTesting_div20")
    for i in range(1, 12):
        data5 = pd.read_csv("WalkTesting/WalkTesting_day5/WalkTesting" + str(i) + "_day5.csv")
        data1 = pd.read_csv("WalkTesting/WalkTesting_day1/WalkTesting" + str(i) + "_day1.csv")
        data2 = pd.read_csv("WalkTesting/WalkTesting_day2/WalkTesting" + str(i) + "_day2.csv")
        data4 = pd.read_csv("WalkTesting/WalkTesting_day4/WalkTesting" + str(i) + "_day4.csv")

        os.mkdir("WalkTesting_div20/WalkTesting_div20_" + str(i))
        createWalks(data5, data1, data2, data4, "WalkTesting_div20/WalkTesting_div20_" + str(i) + "/")

main()