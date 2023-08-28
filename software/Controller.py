import math
import os
import threading

import tkinter.messagebox
import tkinter as tk
from datetime import datetime

import pandas as pd

from dateutil.relativedelta import relativedelta

import matplotlib.pyplot as plt
from pyts.image import GramianAngularField

class Controller():
    def addLabel1g_with_progress(self, data: pd.DataFrame, name, startDate, endDate):
        def add_label1g():
            csv1g = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
            rows = []

            startIndex = 0
            endIndex = data.shape[0]

            if startDate != "":
                startIndex = self.takeIndex(data.loc[:, "Date"], startDate)

            if endDate != "":
                endIndex = self.takeIndex(data.loc[:, "Date"], endDate) + 1

            if math.isnan(startIndex) or math.isnan(endIndex):
                tkinter.messagebox.showerror("Error", "Invalid value: can't find one of the two dates")

            for i in range(startIndex, endIndex):
                list = [data.iloc[i]]

                if i != data.shape[0] - 1:
                    row = {'Date': [list[0].iloc[0]], 'Open': [list[0].iloc[1]],
                           'High': [list[0].iloc[2]], 'Low': [list[0].iloc[3]], 'Close': [list[0].iloc[4]],
                           'Adj Close': [list[0].iloc[5]], 'Volume': [list[0].iloc[6]],
                           'Label': [self.getLabel(data, i, list[0].iloc[4])]}

                else:
                    row = {'Date': [data.iloc[i].iloc[0]], 'Open': [data.iloc[i].iloc[1]],
                           'High': [data.iloc[i].iloc[2]], 'Low': [data.iloc[i].iloc[3]], 'Close': [data.iloc[i].iloc[4]],
                           'Adj Close': [data.iloc[i].iloc[5]], 'Volume': [data.iloc[i].iloc[6]],
                           'Label': [None]}

                rows.append(pd.DataFrame(row))

            csv1g = pd.concat(rows, ignore_index=True)

            # Get the path of the "result" folder on the desktop
            desktop_path = os.path.join(os.path.expanduser("~"), "Desktop", "result")

            # Create the "result" folder if it doesn't exist already
            os.makedirs(desktop_path, exist_ok=True)

            # Concatenate the path of the "result" folder with the file name
            file_path = os.path.join(desktop_path, name)

            csv1g.to_csv(file_path, index=False)

            tk.messagebox.showinfo("Success", "File CSV created.")

        thread = threading.Thread(target=add_label1g)
        thread.start()

    def createCsv_with_progress(self, data, startDate, endDate, trainingPercentage, testingPercentage, validationPercentage,
                                name, intervals, var_generation, var_method):
        def createCsv():
            if startDate == "":
                startIndex = 0
                startDate2 = data.iloc[0, 0]
            else:
                startIndex = self.takeIndex(data.loc[:, "Date"], startDate)
                startDate2 = startDate

            if endDate == "":
                endIndex = data.shape[0]
                endDate2 = data.iloc[-1, 0]
            else:
                endIndex = self.takeIndex(data.loc[:, "Date"], endDate) + 1
                endDate2 = endDate

            if math.isnan(startIndex) or math.isnan(endIndex):
                tkinter.messagebox.showerror("Error", "Invalid value: can't find one of the two dates")
                return

            # Div 1d
            csv1g = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
            rows = []
            for i in range(startIndex, endIndex):
                list = [data.iloc[i]]
                row = {'Date': [list[0].iloc[0]], 'Open': [list[0].iloc[1]],
                       'High': [list[0].iloc[2]], 'Low': [list[0].iloc[3]], 'Close': [list[0].iloc[4]],
                       'Adj Close': [list[0].iloc[5]], 'Volume': [list[0].iloc[6]],
                       'Label': [list[0].iloc[7]]}
                rows.append(pd.DataFrame(row))

            csv1g = pd.concat(rows, ignore_index=True)

            # Get the path of the "result" folder on the desktop
            desktop_path_div = os.path.join(os.path.expanduser("~"), "Desktop", "result/" + name + "/Div")

            # Create the "result" folder if it doesn't exist already
            os.makedirs(desktop_path_div, exist_ok=True)

            # Concatenate the path of the "result" folder with the file name
            file_path = os.path.join(desktop_path_div, name + "_Div_1.csv")

            csv1g.to_csv(file_path, index=False)

            div = [2, 4, 5]
            for j in range(0, 3):
                csv = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
                list = [data.iloc[startIndex]]

                for i in range(startIndex + 1, endIndex):
                    print(i)
                    list.append(data.iloc[i])
                    if len(list) == div[j]:
                        highest, lowest, sumVolume = self.getHLS(list)
                        row = pd.DataFrame(
                            {'Date': [list[0].iloc[0] + "/" + list[len(list) - 1].iloc[0]], 'Open': [list[0].iloc[1]],
                             'High': [highest], 'Low': [lowest], 'Close': [list[len(list) - 1].iloc[4]],
                             'Adj Close': [list[len(list) - 1].iloc[5]], 'Volume': [sumVolume],
                             'Label': [list[len(list) - 1].iloc[7]]},
                            columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])

                        csv = pd.concat([csv, row], ignore_index=True)
                        list.pop(0)

                # Concatenate the path of the "result" folder with the file name
                file_path = os.path.join(desktop_path_div, name + "_Div_" + str(div[j]) + ".csv")
                csv.to_csv(file_path, index=False)

            percentage6month = (1 / ((int(datetime.strptime(endDate2, '%Y-%m-%d').date().strftime('%Y')) - int(
                datetime.strptime(startDate2, '%Y-%m-%d').date().strftime('%Y'))) * 2)) * 100
            nWalks = math.ceil((100 - (trainingPercentage + validationPercentage + testingPercentage)) / percentage6month)

            div = ["1", "2", "4", "5"]
            columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label']
            desktop_path_walks = os.path.join(os.path.expanduser("~"), "Desktop", "result/" + name + "/Walks")

            # Create the "result" folder if it doesn't exist already
            os.makedirs(desktop_path_walks, exist_ok=True)

            for el in div:
                file_path_div = os.path.join(desktop_path_div, name + "_Div_" + el + ".csv")
                data_div = pd.read_csv(file_path_div)

                path_walk_training = os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTraining/WalkTraining_day" + el)
                os.makedirs(path_walk_training, exist_ok=True)

                path_walk_validation = os.path.join(os.path.expanduser("~"), "Desktop",
                                                    "result/" + name + "/Walks/WalkValidation/WalkValidation_day" + el)
                os.makedirs(path_walk_validation, exist_ok=True)

                path_walk_testing = os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTesting/WalkTesting_day" + el)
                os.makedirs(path_walk_testing, exist_ok=True)

                startIndex = 0
                endIndexTraining = int(data_div.shape[0] * (trainingPercentage / 100))
                endIndexValidation = int(data_div.shape[0] * (validationPercentage / 100))
                endIndexTesting = int(data_div.shape[0] * (testingPercentage / 100))

                for i in range(0, nWalks):
                    if i != 0:
                        startIndex = self.takeIndex2(startIndex, data_div, el)

                    file_path_training = os.path.join(path_walk_training,
                                                      "WalkTraining_day" + el + "_" + str(i + 1) + ".csv")
                    file_path_validation = os.path.join(path_walk_validation,
                                                        "WalkValidation_day" + el + "_" + str(i + 1) + ".csv")
                    file_path_testing = os.path.join(path_walk_testing, "WalkTesting_day" + el + "_" + str(i + 1) + ".csv")

                    csv = pd.DataFrame(columns=columns)
                    rows_to_append = [data_div.iloc[j + startIndex] for j in range(0, endIndexTraining)]
                    concatenated_df = pd.DataFrame(rows_to_append, columns=columns)
                    csv = pd.concat([csv, concatenated_df], ignore_index=True)
                    csv.to_csv(file_path_training, index=False)

                    csv = pd.DataFrame(columns=columns)
                    rows_to_append = [data_div.iloc[j + (endIndexTraining + startIndex)] for j in
                                      range(0, endIndexValidation)]
                    concatenated_df = pd.DataFrame(rows_to_append, columns=columns)
                    csv = pd.concat([csv, concatenated_df], ignore_index=True)
                    csv.to_csv(file_path_validation, index=False)

                    csv = pd.DataFrame(columns=columns)
                    rows_to_append = [data_div.iloc[j + (endIndexTraining + startIndex + endIndexValidation - 1)] for j in
                                      range(0, endIndexTesting)]
                    concatenated_df = pd.DataFrame(rows_to_append, columns=columns)
                    csv = pd.concat([csv, concatenated_df], ignore_index=True)
                    csv.to_csv(file_path_testing, index=False)

            desktop_path_walks_interval_training = os.path.join(os.path.expanduser("~"), "Desktop",
                                                                "result/" + name + "/Walks_interval/WalkTraining_interval")
            os.makedirs(desktop_path_walks_interval_training, exist_ok=True)

            for i in range(0, nWalks):
                print("in training")
                data5 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTraining/WalkTraining_day5/WalkTraining_day5_" + str(
                                                     i + 1) + ".csv"))

                data1 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTraining/WalkTraining_day1/WalkTraining_day1_" + str(
                                                     i + 1) + ".csv"))
                data2 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTraining/WalkTraining_day2/WalkTraining_day2_" + str(
                                                     i + 1) + ".csv"))
                data4 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTraining/WalkTraining_day4/WalkTraining_day4_" + str(
                                                     i + 1) + ".csv"))

                path_training_interval = os.path.join(os.path.expanduser("~"), "Desktop",
                                                      "result/" + name + "/Walks_interval/WalkTraining_interval/WalkTraining_interval_" + str(
                                                          i + 1))
                os.makedirs(path_training_interval, exist_ok=True)

                self.createWalks(data5, data1, data2, data4, path_training_interval, intervals, var_method, var_generation)

            desktop_path_walks_interval_validation = os.path.join(os.path.expanduser("~"), "Desktop",
                                                                  "result/" + name + "/Walks_interval/WalkValidation_interval")
            os.makedirs(desktop_path_walks_interval_validation, exist_ok=True)

            for i in range(0, nWalks):
                print("in validation")
                data5 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkValidation/WalkValidation_day5/WalkValidation_day5_" + str(
                                                     i + 1) + ".csv"))
                data1 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkValidation/WalkValidation_day1/WalkValidation_day1_" + str(
                                                     i + 1) + ".csv"))
                data2 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkValidation/WalkValidation_day2/WalkValidation_day2_" + str(
                                                     i + 1) + ".csv"))
                data4 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkValidation/WalkValidation_day4/WalkValidation_day4_" + str(
                                                     i + 1) + ".csv"))

                path_validation_interval = os.path.join(os.path.expanduser("~"), "Desktop",
                                                        "result/" + name + "/Walks_interval/WalkValidation_interval/WalkValidation_interval_" + str(
                                                            i + 1))
                os.makedirs(path_validation_interval, exist_ok=True)
                self.createWalks(data5, data1, data2, data4, path_validation_interval, intervals, var_method,
                                 var_generation)

            desktop_path_walks_interval_testing = os.path.join(os.path.expanduser("~"), "Desktop",
                                                               "result/" + name + "/Walks_interval/WalkTesting_interval")
            os.makedirs(desktop_path_walks_interval_testing, exist_ok=True)
            for i in range(0, nWalks):
                print("in testing")
                data5 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTesting/WalkTesting_day5/WalkTesting_day5_" + str(
                                                     i + 1) + ".csv"))
                data1 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTesting/WalkTesting_day1/WalkTesting_day1_" + str(
                                                     i + 1) + ".csv"))
                data2 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTesting/WalkTesting_day2/WalkTesting_day2_" + str(
                                                     i + 1) + ".csv"))
                data4 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                 "result/" + name + "/Walks/WalkTesting/WalkTesting_day4/WalkTesting_day4_" + str(
                                                     i + 1) + ".csv"))

                path_testing_interval = os.path.join(os.path.expanduser("~"), "Desktop",
                                                     "result/" + name + "/Walks_interval/WalkTesting_interval/Walktesting_interval_" + str(
                                                         i + 1))
                os.makedirs(path_testing_interval, exist_ok=True)
                self.createWalks(data5, data1, data2, data4, path_testing_interval, intervals, var_method, var_generation)

            tk.messagebox.showinfo("Success", "Creation completed")

        thread = threading.Thread(target=createCsv())
        thread.start()

    def createWalks(self, data5, data1, data2, data4, name, intervals, var_method, var_generation):
        print(var_generation)
        columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label']
        csv5 = pd.DataFrame(columns=columns)
        csv1 = pd.DataFrame(columns=columns)
        csv2 = pd.DataFrame(columns=columns)
        csv4 = pd.DataFrame(columns=columns)

        i_1 = data1.shape[0] - data5.shape[0]
        i_2 = data2.shape[0] - data5.shape[0]
        i_4 = data5.shape[0] - data5.shape[0]
        count = 0

        for i in range(0, len(data5)):
            print(i)
            if count < intervals:
                csv5 = pd.concat([csv5, pd.DataFrame([data5.iloc[i]], columns=columns)], ignore_index=True)
                csv4 = pd.concat([csv4, pd.DataFrame([data4.iloc[i_4]], columns=columns)], ignore_index=True)
                csv2 = pd.concat([csv2, pd.DataFrame([data2.iloc[i_2]], columns=columns)], ignore_index=True)
                csv1 = pd.concat([csv1, pd.DataFrame([data1.iloc[i_1]], columns=columns)], ignore_index=True)

                count += 1
                i_1 += 1
                i_2 += 1
                i_4 += 1

                if count == intervals:
                    lastData = csv1.iloc[-1, 0]
                    label = csv1.iloc[-1, 7]

                    path = os.path.join(name, f"{lastData}_{label}")
                    os.makedirs(path, exist_ok=True)

                    name_day_5 = os.path.join(path, f"{lastData}_{label}_day_5")
                    name_day_1 = os.path.join(path, f"{lastData}_{label}_day_1")
                    name_day_2 = os.path.join(path, f"{lastData}_{label}_day_2")
                    name_day_4 = os.path.join(path, f"{lastData}_{label}_day_4")

                    if var_generation == "File":
                        csv5.to_csv(name_day_5 + ".csv", index=False)
                        csv1.to_csv(name_day_1 + ".csv", index=False)
                        csv2.to_csv(name_day_2 + ".csv", index=False)
                        csv4.to_csv(name_day_4 + ".csv", index=False)

                    if var_generation == "Images":
                        self.generete_images(csv1, name_day_1, var_method)
                        self.generete_images(csv2, name_day_2, var_method)
                        self.generete_images(csv4, name_day_4, var_method)
                        self.generete_images(csv5, name_day_5, var_method)

                    if var_generation == "Both":
                        self.generete_images(csv1, name_day_1, var_method)
                        self.generete_images(csv2, name_day_2, var_method)
                        self.generete_images(csv4, name_day_4, var_method)
                        self.generete_images(csv5, name_day_5, var_method)

                        csv5.to_csv(name_day_5 + ".csv", index=False)
                        csv1.to_csv(name_day_1 + ".csv", index=False)
                        csv2.to_csv(name_day_2 + ".csv", index=False)
                        csv4.to_csv(name_day_4 + ".csv", index=False)

            if count > 20:
                csv5 = pd.concat([csv5, pd.DataFrame([data5.iloc[i]], columns=columns)], ignore_index=True)
                csv4 = pd.concat([csv4, pd.DataFrame([data4.iloc[i_4]], columns=columns)], ignore_index=True)
                csv2 = pd.concat([csv2, pd.DataFrame([data2.iloc[i_2]], columns=columns)], ignore_index=True)
                csv1 = pd.concat([csv1, pd.DataFrame([data1.iloc[i_1]], columns=columns)], ignore_index=True)

                i_1 += 1
                i_2 += 1
                i_4 += 1

                csv5 = csv5.drop(csv5.index[0])
                csv4 = csv4.drop(csv4.index[0])
                csv2 = csv2.drop(csv2.index[0])
                csv1 = csv1.drop(csv1.index[0])

                lastData = csv1.iloc[-1, 0]
                label = csv1.iloc[-1, 7]

                path = os.path.join(name, f"{lastData}_{label}")
                os.makedirs(path, exist_ok=True)

                name_day_5 = os.path.join(path, f"{lastData}_{label}_day_5")
                name_day_1 = os.path.join(path, f"{lastData}_{label}_day_1")
                name_day_2 = os.path.join(path, f"{lastData}_{label}_day_2")
                name_day_4 = os.path.join(path, f"{lastData}_{label}_day_4")

                if var_generation == "File":
                    csv5.to_csv(name_day_5 + ".csv", index=False)
                    csv1.to_csv(name_day_1 + ".csv", index=False)
                    csv2.to_csv(name_day_2 + ".csv", index=False)
                    csv4.to_csv(name_day_4 + ".csv", index=False)

                if var_generation == "Images":
                    self.generete_images(csv1, name_day_1, var_method)
                    self.generete_images(csv2, name_day_2, var_method)
                    self.generete_images(csv4, name_day_4, var_method)
                    self.generete_images(csv5, name_day_5, var_method)

                if var_generation == "Both":
                    self.generete_images(csv1, name_day_1, var_method)
                    self.generete_images(csv2, name_day_2, var_method)
                    self.generete_images(csv4, name_day_4, var_method)
                    self.generete_images(csv5, name_day_5, var_method)

                    csv5.to_csv(name_day_5 + ".csv", index=False)
                    csv1.to_csv(name_day_1 + ".csv", index=False)
                    csv2.to_csv(name_day_2 + ".csv", index=False)
                    csv4.to_csv(name_day_4 + ".csv", index=False)

            if count == 20:
                count += 1

    def generete_images(self, csv, name, var_method):
        df_copy = csv.copy()
        df_copy = df_copy.drop(columns=['Date'])

        # Get the values from the dataframe
        X = df_copy.iloc[:, 1:].values.T

        # Compute Gramian angular fields
        if var_method == "GADF":
            gaf = GramianAngularField(method='difference')
            X_gaf = gaf.fit_transform(X)

            # Plot the Gramian angular fields without white space
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(X_gaf[0], cmap='rainbow', origin='lower', extent=[0, 1, 0, 1])

            # Remove axis labels and ticks
            ax.set_xticks([])
            ax.set_yticks([])

            plt.tight_layout()  # Adjust layout to remove any overlapping

            fig.savefig(name + "_GADF.png", dpi=300, bbox_inches='tight')
            plt.close(fig)

        if var_method == "GASF":
            gaf = GramianAngularField(method='summation')
            X_gaf = gaf.fit_transform(X)

            # Plot the Gramian angular fields without white space
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(X_gaf[0], cmap='rainbow', origin='lower', extent=[0, 1, 0, 1])

            # Remove axis labels and ticks
            ax.set_xticks([])
            ax.set_yticks([])

            plt.tight_layout()  # Adjust layout to remove any overlapping

            fig.savefig(name + "_GASF.png", dpi=300, bbox_inches='tight')
            plt.close(fig)

        if var_method == "Both":
            gaf = GramianAngularField(method='difference')
            X_gaf = gaf.fit_transform(X)

            # Plot the Gramian angular fields without white space
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(X_gaf[0], cmap='rainbow', origin='lower', extent=[0, 1, 0, 1])

            # Remove axis labels and ticks
            ax.set_xticks([])
            ax.set_yticks([])

            plt.tight_layout()  # Adjust layout to remove any overlapping

            fig.savefig(name + "_GADF.png", dpi=300, bbox_inches='tight')

            plt.close(fig)

            gaf = GramianAngularField(method='summation')
            X_gaf = gaf.fit_transform(X)

            # Plot the Gramian angular fields without white space
            fig, ax = plt.subplots(figsize=(6, 6))
            ax.imshow(X_gaf[0], cmap='rainbow', origin='lower', extent=[0, 1, 0, 1])

            # Remove axis labels and ticks
            ax.set_xticks([])
            ax.set_yticks([])

            plt.tight_layout()  # Adjust layout to remove any overlapping

            fig.savefig(name + "_GASF.png", dpi=300, bbox_inches='tight')

            plt.close(fig)

    def takeIndex2(self, startIndex, data_div, el):
        date = data_div.iloc[startIndex, 0]
        if el != "1":
            date = date[0:date.index("/")]

        new_date = datetime.strptime(date, '%Y-%m-%d').date() + relativedelta(months=6)

        for i in range(startIndex, data_div.shape[0]):
            date = data_div.iloc[i, 0]

            if el != "1":
                date = date[0:date.index("/")]

            date = datetime.strptime(date, '%Y-%m-%d').date()
            if date >= new_date:
                return i

        return i

    def getHLS(self, list):
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

    def getLabel(self, data, i, close):
        list = [data.iloc[i + 1]]
        closeNextDay = list[0].iloc[4]

        if close == closeNextDay: return 2

        if close > closeNextDay: return 1

        if close < closeNextDay: return 0

    def takeIndex(self, dates, dateFind):
        i = 0
        flag = True
        for date in dates:
            dtObj = datetime.strptime(date, '%Y-%m-%d').date()
            if dateFind == dtObj:
                flag = False
                break
            i += 1

        if flag: i = math.nan

        return i