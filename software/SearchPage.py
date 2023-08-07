import math
import os
import threading

from datetime import datetime
from pathlib import Path

import tkinter
from tkinter import ttk
import tkinter as tk
import tkinter.messagebox
from tkinterdnd2 import DND_FILES

import pandas as pd
from DataTable import DataTable

from dateutil.relativedelta import relativedelta


class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # ListBox
        self.file_names_listbox = tk.Listbox(parent, selectmode=tk.SINGLE, background="darkgray")
        self.file_names_listbox.place(relheight=0.5, relwidth=0.25)
        self.file_names_listbox.drop_target_register(DND_FILES)
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        self.file_names_listbox.bind("<Double-1>", self._display_file)

        # Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(rely=0, relx=0.25, relwidth=0.75, relheight=1)
        self.path_map = {}

        # Generate button
        self.button = tk.Button(parent, text="Generate", command=self.on_button_click_generete, width=20, height=2,
                                bd=2,
                                highlightthickness=2, bg="#a9a9a9")
        self.button.place(relx=0.17, rely=0.95, anchor="sw")

        # Start date edit box
        font = ("Arial", 12)
        self.default_text_start_date = "Start Date: YYYY-MM-DD"
        self.hint_color = "gray"  # Light gray color for the hint

        self.edit_box_start_date = tk.Entry(parent, width=25, font=font)
        self.edit_box_start_date.insert(0, self.default_text_start_date)
        self.edit_box_start_date.config(foreground=self.hint_color)
        self.edit_box_start_date.bind("<FocusIn>", lambda event: self.remove_default_text(event, self.default_text_start_date, self.edit_box_start_date))
        self.edit_box_start_date.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.default_text_start_date, self.edit_box_start_date))
        self.edit_box_start_date.place(relx=0.01, rely=0.55, anchor="sw")

        # End date edit box
        self.default_text_end_date = "End Date: YYYY-MM-DD"

        self.edit_box_end_date = tk.Entry(parent, width=25, font=font)
        self.edit_box_end_date.insert(0, self.default_text_end_date)
        self.edit_box_end_date.config(foreground=self.hint_color)
        self.edit_box_end_date.bind("<FocusIn>", lambda event: self.remove_default_text(event, self.default_text_end_date, self.edit_box_end_date))
        self.edit_box_end_date.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.default_text_end_date, self.edit_box_end_date))
        self.edit_box_end_date.place(relx=0.01, rely=0.59, anchor="sw")

        # Percentage training edit box
        self.default_text_training = "Percentage training:"

        self.edit_box_training = tk.Entry(parent, width=25, font=font)
        self.edit_box_training.insert(0, self.default_text_training)
        self.edit_box_training.config(foreground=self.hint_color)
        self.edit_box_training.bind("<FocusIn>", lambda event: self.remove_default_text(event, self.default_text_training, self.edit_box_training))
        self.edit_box_training.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.default_text_training, self.edit_box_training))
        self.edit_box_training.place(relx=0.01, rely=0.63, anchor="sw")

        # Percentage validation edit box
        self.default_text_validation = "Percentage validation:"

        self.edit_box_validation = tk.Entry(parent, width=25, font=font)
        self.edit_box_validation.insert(0, self.default_text_validation)
        self.edit_box_validation.config(foreground=self.hint_color)
        self.edit_box_validation.bind("<FocusIn>", lambda event: self.remove_default_text(event, self.default_text_validation, self.edit_box_validation))
        self.edit_box_validation.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.default_text_validation, self.edit_box_validation))
        self.edit_box_validation.place(relx=0.01, rely=0.66, anchor="sw")

        # Percentage testing edit box
        self.default_text_testing = "Percentage testing:"

        self.edit_box_testing = tk.Entry(parent, width=25, font=font)
        self.edit_box_testing.insert(0, self.default_text_testing)
        self.edit_box_testing.config(foreground=self.hint_color)
        self.edit_box_testing.bind("<FocusIn>", lambda event: self.remove_default_text(event, self.default_text_testing,
                                                                                       self.edit_box_testing))
        self.edit_box_testing.bind("<FocusOut>",
                                   lambda event: self.restore_default_text(event, self.default_text_testing,
                                                                           self.edit_box_testing))
        self.edit_box_testing.place(relx=0.01, rely=0.69, anchor="sw")

        # Intervals edit box
        self.default_text_intervals = "Intervals:"

        self.edit_box_intervals = tk.Entry(parent, width=25, font=font)
        self.edit_box_intervals.insert(0, self.default_text_intervals)
        self.edit_box_intervals.config(foreground=self.hint_color)
        self.edit_box_intervals.bind("<FocusIn>", lambda event: self.remove_default_text(event, self.default_text_intervals, self.edit_box_intervals))
        self.edit_box_intervals.bind("<FocusOut>", lambda event: self.restore_default_text(event, self.default_text_intervals, self.edit_box_intervals))
        self.edit_box_intervals.place(relx=0.01, rely=0.725, anchor="sw")

        # Text for generation type: folders, images, both
        self.text_generation = tk.Text(parent, width=37, height=1, font=font, highlightthickness=0,
                                       background="#f0f0f0", bd=0)
        self.text_generation.insert(tk.END, "Do you want to generate CSV files or images?")
        self.text_generation.place(relx=0.01, rely=0.75, anchor="sw")

        # Generation type radio buttons
        self.radio_var_generation = tk.StringVar(value="empty")  # Set initial value to an empty string

        # radio button: files
        self.radio_button_files = tk.Radiobutton(parent, text="Files", variable=self.radio_var_generation,
                                                 value="files", font=font)
        self.radio_button_files.place(relx=0.01, rely=0.8, anchor="sw")

        # radio button: images
        self.radio_button_images = tk.Radiobutton(parent, text="Images", variable=self.radio_var_generation,
                                                  value="images", font=font)
        self.radio_button_images.place(relx=0.07, rely=0.8, anchor="sw")

        # radio button: both
        self.radio_button_both = tk.Radiobutton(parent, text="Both", variable=self.radio_var_generation,
                                                value="Both", font=font)
        self.radio_button_both.place(relx=0.15, rely=0.8, anchor="sw")

        # Text for generation method: GADF, GASF, both
        self.text_generation = tk.Text(parent, width=37, height=1, font=font, highlightthickness=0,
                                       background="#f0f0f0", bd=0)
        self.text_generation.insert(tk.END, "Wich encoding method do you want to use?")
        self.text_generation.place(relx=0.01, rely=0.85, anchor="sw")

        # Generation type radio buttons
        self.radio_var_method = tk.StringVar(value="empty")  # Set initial value to an empty string

        # radio button: Gadf
        self.radio_button_Gadf = tk.Radiobutton(parent, text="GADF", variable=self.radio_var_method,
                                                value="GADF", font=font)
        self.radio_button_Gadf.place(relx=0.01, rely=0.9, anchor="sw")

        # radio button: Gasf
        self.radio_button_Gasf = tk.Radiobutton(parent, text="GASF", variable=self.radio_var_method,
                                                value="GASF", font=font)
        self.radio_button_Gasf.place(relx=0.07, rely=0.9, anchor="sw")

        # radio button: both methods
        self.radio_button_both_methods = tk.Radiobutton(parent, text="Both", variable=self.radio_var_method,
                                                        value="Both", font=font)
        self.radio_button_both_methods.place(relx=0.15, rely=0.9, anchor="sw")

        # Label button
        self.button = tk.Button(parent, text="Create label", command=self.on_button_click_label, width=20, height=2,
                                bd=2,
                                highlightthickness=2, bg="#a9a9a9")
        self.button.place(relx=0.08, rely=0.95, anchor="sw")

    def remove_default_text(self, event, default_text, edit_box):
        if edit_box.get() == default_text:
            edit_box.delete(0, tk.END)
            edit_box.config(foreground="black")  # Change text color to black

    def restore_default_text(self, event, default_text, edit_box):
        if not edit_box.get():
            edit_box.insert(0, default_text)
            edit_box.config(foreground=self.hint_color)  # Change text color to the hint color

    def drop_inside_list_box(self, event):
        file_paths = self._parse_drop_files(event.data)
        current_listbox_items = set(self.file_names_listbox.get(0, "end"))
        for file_path in file_paths:
            if file_path.endswith(".csv"):
                path_object = Path(file_path)
                file_name = path_object.name
                if file_name not in current_listbox_items:
                    self.file_names_listbox.insert("end", file_name)
                    self.path_map[file_name] = file_path

    def _display_file(self, event):
        file_name = self.file_names_listbox.get(self.file_names_listbox.curselection())
        path = self.path_map[file_name]
        df = pd.read_csv(path)
        self.data_table.set_datatable(dataframe=df)

    def _parse_drop_files(self, filename):
        # 'C:/Users/Owner/Downloads/RandomStock Tickers.csv C:/Users/Owner/Downloads/RandomStockTickers.csv'
        size = len(filename)
        res = []  # list of file paths
        name = ""
        idx = 0
        while idx < size:
            if filename[idx] == "{":
                j = idx + 1
                while filename[j] != "}":
                    name += filename[j]
                    j += 1
                res.append(name)
                name = ""
                idx = j
            elif filename[idx] == " " and name != "":
                res.append(name)
                name = ""
            elif filename[idx] != " ":
                name += filename[idx]
            idx += 1
        if name != "":
            res.append(name)
        return res

    def search_table(self, event):
        # column value. [[column,value],column2=value2]....
        entry = self.search_entrybox.get()
        if entry == "":
            self.data_table.reset_table()
        else:
            entry_split = entry.split(",")
            column_value_pairs = {}
            for pair in entry_split:
                pair_split = pair.split("=")
                if len(pair_split) == 2:
                    col = pair_split[0]
                    lookup_value = pair_split[1]
                    column_value_pairs[col] = lookup_value
            self.data_table.find_value(pairs=column_value_pairs)

    def on_button_click_generete(self):
        print(self.radio_var_method.get())
        print(self.radio_var_generation.get())

        checkDate, startDate, endDate = self.checkDate()

        if checkDate:
            checkPercentage, trainingPercentage, testingPercentage, validationPercentage = self.checkPercentage()

            if checkPercentage:
                checkIntervals, intervals = self.checkIntervals()

                if checkIntervals:
                    checkRadioButtons, var_generation, var_method = self.checkRadioButtons()

                    if checkRadioButtons:
                        try:
                            selected_index = self.file_names_listbox.curselection()
                            if selected_index:
                                name = self.file_names_listbox.get(self.file_names_listbox.curselection())
                                name = name[0:name.index(".")]
                                self.createCsv_with_progress(self.data_table.stored_dataframe, startDate, endDate, trainingPercentage, testingPercentage, validationPercentage, name, intervals)
                            else:
                                tkinter.messagebox.showerror("Error", "No item selected")
                        except tk.TclError as e:
                            print(f"TclError: {e}")
                            tkinter.messagebox.showerror("Error", "An error occurred")

    def createCsv_with_progress(self, data, startDate, endDate, trainingPercentage, testingPercentage, validationPercentage, name, intervals):
        top = tk.Toplevel()
        top.title('Progress')

        message = "Processing..."
        self.center_window(top, message)
        top.grab_set()
        top.protocol("WM_DELETE_WINDOW", lambda: None)

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
                top.destroy()
                tkinter.messagebox.showerror("Error", "Invalid value: can't find one of the two dates")
                return

            #Div 1d
            csv1g = pd.DataFrame(columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])
            rows = []
            for i in range(startIndex, endIndex):
                list = [data.iloc[i]]
                row = row = {'Date': [list[0].iloc[0]], 'Open': [list[0].iloc[1]],
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
                        row = pd.DataFrame({'Date': [list[0].iloc[0] + "/" + list[len(list) - 1].iloc[0]], 'Open': [list[0].iloc[1]],
                               'High': [highest], 'Low': [lowest], 'Close': [list[len(list) - 1].iloc[4]],
                               'Adj Close': [list[len(list) - 1].iloc[5]], 'Volume': [sumVolume], 'Label' : [list[len(list) - 1].iloc[7]]}, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label'])

                        csv = pd.concat([csv, row], ignore_index=True)
                        list.pop(0)

                # Concatenate the path of the "result" folder with the file name
                file_path = os.path.join(desktop_path_div, name + "_Div_" + str(div[j]) + ".csv")
                csv.to_csv(file_path, index=False)

            percentage6month = (1 / ((int(datetime.strptime(endDate2, '%Y-%m-%d').date().strftime('%Y')) - int(datetime.strptime(startDate2, '%Y-%m-%d').date().strftime('%Y'))) * 2)) * 100
            nWalks = math.ceil((100 - (trainingPercentage + validationPercentage + testingPercentage)) / percentage6month)

            div = ["1", "2", "4", "5"]
            columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume', 'Label']
            desktop_path_walks = os.path.join(os.path.expanduser("~"), "Desktop", "result/" + name + "/Walks")

            # Create the "result" folder if it doesn't exist already
            os.makedirs(desktop_path_walks, exist_ok=True)

            for el in div:
                file_path_div = os.path.join(desktop_path_div, name + "_Div_" + el + ".csv")
                data_div = pd.read_csv(file_path_div)

                path_walk_training = os.path.join(os.path.expanduser("~"), "Desktop", "result/" + name + "/Walks/WalkTraining/WalkTraining_day" + el)
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
                endIndexTesting =  int(data_div.shape[0] * (testingPercentage / 100))

                for i in range(0, nWalks):
                    if i != 0:
                        startIndex = self.takeIndex2(startIndex, data_div, el)

                    file_path_training = os.path.join(path_walk_training, "WalkTraining_day" + el + "_" + str(i + 1) + ".csv")
                    file_path_validation = os.path.join(path_walk_validation, "WalkValidation_day" + el + "_" + str(i + 1) + ".csv")
                    file_path_testing = os.path.join(path_walk_testing, "WalkTesting_day" + el + "_" + str(i + 1) + ".csv")

                    csv = pd.DataFrame(columns=columns)
                    rows_to_append = [data_div.iloc[j + startIndex] for j in range(0, endIndexTraining)]
                    concatenated_df = pd.DataFrame(rows_to_append, columns=columns)
                    csv = pd.concat([csv, concatenated_df], ignore_index=True)
                    csv.to_csv(file_path_training, index=False)

                    csv = pd.DataFrame(columns=columns)
                    rows_to_append = [data_div.iloc[j + (endIndexTraining + startIndex)] for j in range(0, endIndexValidation)]
                    concatenated_df = pd.DataFrame(rows_to_append, columns=columns)
                    csv = pd.concat([csv, concatenated_df], ignore_index=True)
                    csv.to_csv(file_path_validation, index=False)

                    csv = pd.DataFrame(columns=columns)
                    rows_to_append = [data_div.iloc[j + (endIndexTraining + startIndex + endIndexValidation - 1)] for j in range(0, endIndexTesting)]
                    concatenated_df = pd.DataFrame(rows_to_append, columns=columns)
                    csv = pd.concat([csv, concatenated_df], ignore_index=True)
                    csv.to_csv(file_path_testing, index=False)

            desktop_path_walks_interval_training = os.path.join(os.path.expanduser("~"), "Desktop", "result/" + name + "/Walks_interval/WalkTraining_interval")
            os.makedirs(desktop_path_walks_interval_training, exist_ok=True)

            for i in range(0, nWalks):
                print("in training")
                data5 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTraining/WalkTraining_day5/WalkTraining_day5_" + str(i + 1) + ".csv"))

                data1 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTraining/WalkTraining_day1/WalkTraining_day1_" + str(i + 1) + ".csv"))
                data2 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTraining/WalkTraining_day2/WalkTraining_day2_" + str(i + 1) + ".csv"))
                data4 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTraining/WalkTraining_day4/WalkTraining_day4_" + str(i + 1) + ".csv"))

                path_training_interval = os.path.join(os.path.expanduser("~"), "Desktop",
                             "result/" + name + "/Walks_interval/WalkTraining_interval/WalkTraining_interval_" + str(i + 1))
                os.makedirs(path_training_interval, exist_ok=True)

                self.createWalks(data5, data1, data2, data4, path_training_interval, intervals)

            desktop_path_walks_interval_validation = os.path.join(os.path.expanduser("~"), "Desktop",
                                                                "result/" + name + "/Walks_interval/WalkValidation_interval")
            os.makedirs(desktop_path_walks_interval_validation, exist_ok=True)

            for i in range(0, nWalks):
                print("in validation")
                data5 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkValidation/WalkValidation_day5/WalkValidation_day5_" + str(i + 1) + ".csv"))
                data1 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkValidation/WalkValidation_day1/WalkValidation_day1_" + str(i + 1) + ".csv"))
                data2 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkValidation/WalkValidation_day2/WalkValidation_day2_" + str(i + 1) + ".csv"))
                data4 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkValidation/WalkValidation_day4/WalkValidation_day4_" + str(i + 1) + ".csv"))

                path_validation_interval = os.path.join(os.path.expanduser("~"), "Desktop",
                                                      "result/" + name + "/Walks_interval/WalkValidation_interval/WalkValidation_interval_" + str(
                                                          i + 1))
                os.makedirs(path_validation_interval, exist_ok=True)
                self.createWalks(data5, data1, data2, data4, path_validation_interval, intervals)

            desktop_path_walks_interval_testing = os.path.join(os.path.expanduser("~"), "Desktop",
                                                                "result/" + name + "/Walks_interval/WalkTesting_interval")
            os.makedirs(desktop_path_walks_interval_testing, exist_ok=True)
            for i in range(0, nWalks):
                print("in testing")
                data5 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTesting/WalkTesting_day5/WalkTesting_day5_" + str(i + 1) + ".csv"))
                data1 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTesting/WalkTesting_day1/WalkTesting_day1_" + str(i + 1) + ".csv"))
                data2 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTesting/WalkTesting_day2/WalkTesting_day2_" + str(i + 1) + ".csv"))
                data4 = pd.read_csv(os.path.join(os.path.expanduser("~"), "Desktop",
                                                  "result/" + name + "/Walks/WalkTesting/WalkTesting_day4/WalkTesting_day4_" + str(i + 1) + ".csv"))

                path_testing_interval = os.path.join(os.path.expanduser("~"), "Desktop",
                                                        "result/" + name + "/Walks_interval/WalkTesting_interval/Walktesting_interval_" + str(
                                                            i + 1))
                os.makedirs(path_testing_interval, exist_ok=True)
                self.createWalks(data5, data1, data2, data4, path_testing_interval, intervals)

            top.destroy()
            tk.messagebox.showinfo("Success", "Creation completed")

        thread = threading.Thread(target=createCsv())
        thread.start()

    def createWalks(self, data5, data1, data2, data4, name, intervals):
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

                    csv5.to_csv(os.path.join(path, f"{lastData}_{label}_day_5.csv"), index=False)
                    csv1.to_csv(os.path.join(path, f"{lastData}_{label}_day_1.csv"), index=False)
                    csv2.to_csv(os.path.join(path, f"{lastData}_{label}_day_2.csv"), index=False)
                    csv4.to_csv(os.path.join(path, f"{lastData}_{label}_day_4.csv"), index=False)

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

                csv5.to_csv(os.path.join(path, f"{lastData}_{label}_day_5.csv"), index=False)
                csv1.to_csv(os.path.join(path, f"{lastData}_{label}_day_1.csv"), index=False)
                csv2.to_csv(os.path.join(path, f"{lastData}_{label}_day_2.csv"), index=False)
                csv4.to_csv(os.path.join(path, f"{lastData}_{label}_day_4.csv"), index=False)

            if count == 20:
                count += 1

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

    def checkRadioButtons(self):
        var_method = self.radio_var_method.get()
        var_generation = self.radio_var_generation.get()

        if var_method == "empty" or var_generation == "empty":
            tkinter.messagebox.showerror("Error", "Missing parameter: choose what do you want to generete and the encoding method")
            return False, "", ""

        return True, var_generation, var_method

    def checkIntervals(self):
        intervals = self.edit_box_intervals.get()

        if not intervals.isnumeric():
            tkinter.messagebox.showerror("Error", "Invalid value: intervalls value is not valid")
            return False, 0

        intervals = int(intervals)

        if intervals <= 0:
            tkinter.messagebox.showerror("Error", "Invalid value: intervalls value is not valid")
            return False, 0

        return True, intervals

    def isfloat(self, num):
        try:
            float(num)
            return True
        except ValueError:
            return False

    def checkPercentage(self):
        training, validation, testing = self.edit_box_training.get(), self.edit_box_validation.get(), self.edit_box_testing.get()

        if not self.isfloat(training) or not self.isfloat(validation) or not self.isfloat(testing):
            tkinter.messagebox.showerror("Error", "Invalid value: some percentage value is incorrect")
            return False, 0, 0, 0

        training, validation, testing = float(training), float(validation), float(testing)

        if training + validation + testing > 100:
            tkinter.messagebox.showerror("Error", "Invalid value: the sum of percentage is grater than 100%")
            return False, 0, 0, 0

        return True, training, testing, validation

    def checkDate(self):
        # Actions to be performed when the button is clicked
        startDate = ""
        endDate = ""

        if self.edit_box_start_date.get() != self.default_text_start_date:
            try:
                startDate = datetime.strptime(self.edit_box_start_date.get(), '%Y-%m-%d').date()
            except ValueError as e:
                tkinter.messagebox.showerror("Error", "Invalid value: leave it blank or enter a valid date.")
                return False, "", ""

        if self.edit_box_end_date.get() != self.default_text_end_date:
            try:
                endDate = datetime.strptime(self.edit_box_end_date.get(), '%Y-%m-%d').date()
            except ValueError as e:
                tkinter.messagebox.showerror("Error", "Invalid value: leave it blank or enter a valid date.")
                return False, "", ""

        if startDate and endDate and startDate >= endDate:
            tk.messagebox.showerror("Error", "Invalid date range: start date must be earlier than end date.")
            return False, "", ""

        return True, startDate, endDate

    def on_button_click_label(self):
        check, startDate, endDate = self.checkDate()

        if check:
            try:
                selected_index = self.file_names_listbox.curselection()
                if selected_index:
                    name = self.file_names_listbox.get(self.file_names_listbox.curselection())
                    name = name[0:name.index(".")] + "_label.csv"

                    self.addLabel1g_with_progress(self.data_table.stored_dataframe, name, startDate, endDate)
                else:
                    tkinter.messagebox.showerror("Error", "No item selected")
            except tk.TclError as e:
                print(f"TclError: {e}")
                tkinter.messagebox.showerror("Error", "An error occurred")

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

    def center_window(self, window, message):
        progressbar = ttk.Progressbar(window, mode='indeterminate')
        progressbar.pack(pady=10)
        progressbar.start()

        message_width = len(message) * 10  # Width proportional to the message length
        message_height = 100  # Fixed height

        tk.Message(window, text=message, padx=20, pady=20, width=message_width, aspect=400).pack()

        window.update_idletasks()

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        x = (screen_width // 2) - (message_width // 2)
        y = (screen_height // 2) - (message_height // 2)

        window.geometry(f"{message_width}x{message_height}+{x}+{y}")

    def addLabel1g_with_progress(self, data: pd.DataFrame, name, startDate, endDate):
        top = tk.Toplevel()
        top.title('Progress')

        message = "Creating the csv..."
        self.center_window(top, message)
        top.grab_set()
        top.protocol("WM_DELETE_WINDOW", lambda: None)

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
                top.destroy()
                tkinter.messagebox.showerror("Error", "Invalid value: can't find one of the two dates")
                return

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

            top.destroy()
            tk.messagebox.showinfo("Success", "File CSV created.")

        thread = threading.Thread(target=add_label1g)
        thread.start()
