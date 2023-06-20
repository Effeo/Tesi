import tkinter as tk
from pathlib import Path
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

import pandas as pd

'''
    - select rows by date X
    - generate image button X
    - generation method X
    - create both folders and images (selecting) X
    - create Label column X
    - trim column (remove column)
    - select rows with start and end date or intervals (from the two selected rows, how often images need to be generated) X
    - specify percentages for training, validation, and testing parts X
'''


'''
block the resize

'''
class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.set_window_size_to_screen()
        self.set_minimum_window_size()
        self.search_page = SearchPage(parent=self.main_frame)

    def set_window_size_to_screen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")

    def set_minimum_window_size(self):
        self.wm_minsize(width=800, height=600)


class DataTable(ttk.Treeview):
    def __init__(self, parent):
        super().__init__(parent)
        scroll_Y = tk.Scrollbar(self, orient="vertical", command=self.yview)
        scroll_X = tk.Scrollbar(self, orient="horizontal", command=self.xview)
        self.configure(yscrollcommand=scroll_Y.set, xscrollcommand=scroll_X.set)
        scroll_Y.pack(side="right", fill="y")
        scroll_X.pack(side="bottom", fill="x")
        self.stored_dataframe = pd.DataFrame()

    def set_datatable(self, dataframe):
        self.stored_dataframe = dataframe
        self._draw_table(dataframe)

    def _draw_table(self, dataframe):
        self.delete(*self.get_children())
        columns = list(dataframe.columns)
        self.__setitem__("column", columns)
        self.__setitem__("show", "headings")

        for col in columns:
            self.heading(col, text=col)

        df_rows = dataframe.to_numpy().tolist()
        for row in df_rows:
            self.insert("", "end", values=row)
        return None

    def find_value(self, pairs):
        # pairs is a dictionary
        new_df = self.stored_dataframe
        for col, value in pairs.items():
            query_string = f"{col}.str.contains('{value}')"
            new_df = new_df.query(query_string, engine="python")
        self._draw_table(new_df)

    def reset_table(self):
        self._draw_table(self.stored_dataframe)


class SearchPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
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
        self.button = tk.Button(parent, text="Generate", command=self.on_button_click_generete, width=20, height=2, bd=2,
                                highlightthickness=2, bg="#a9a9a9")
        self.button.place(relx=0.17, rely=0.95, anchor="sw")

        # Start date edit box
        font = ("Arial", 12)
        self.default_text_start_date = "Start Date: YYYY-MM-DD"
        self.hint_color = "gray"  # Light gray color for the hint

        self.edit_box_start_date = tk.Entry(parent, width=25, font=font)
        self.edit_box_start_date.insert(0, self.default_text_start_date)
        self.edit_box_start_date.config(foreground=self.hint_color)
        self.edit_box_start_date.bind("<FocusIn>", self.remove_default_text_start_date)
        self.edit_box_start_date.bind("<FocusOut>", self.restore_default_text_start_date)
        self.edit_box_start_date.place(relx=0.01, rely=0.55, anchor="sw")

        # End date edit box
        self.default_text_end_date = "End Date: YYYY-MM-DD"

        self.edit_box_end_date = tk.Entry(parent, width=25, font=font)
        self.edit_box_end_date.insert(0, self.default_text_end_date)
        self.edit_box_end_date.config(foreground=self.hint_color)
        self.edit_box_end_date.bind("<FocusIn>", self.remove_default_text_end_date)
        self.edit_box_end_date.bind("<FocusOut>", self.restore_default_text_end_date)
        self.edit_box_end_date.place(relx=0.01, rely=0.59, anchor="sw")

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
                                                value="both", font=font)
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
        self.button = tk.Button(parent, text="Create label", command=self.on_button_click_label, width=20, height=2, bd=2,
                                highlightthickness=2, bg="#a9a9a9")
        self.button.place(relx=0.08, rely=0.95, anchor="sw")

        # Percentage training edit box
        self.default_text_training = "Percentage training:"

        self.edit_box_training = tk.Entry(parent, width=25, font=font)
        self.edit_box_training.insert(0, self.default_text_training)
        self.edit_box_training.config(foreground=self.hint_color)
        self.edit_box_training.bind("<FocusIn>", self.remove_default_text_training)
        self.edit_box_training.bind("<FocusOut>", self.restore_default_text_training)
        self.edit_box_training.place(relx=0.01, rely=0.63, anchor="sw")

        # Percentage testing edit box
        self.default_text_testing = "Percentage testing:"

        self.edit_box_testing = tk.Entry(parent, width=25, font=font)
        self.edit_box_testing.insert(0, self.default_text_testing)
        self.edit_box_testing.config(foreground=self.hint_color)
        self.edit_box_testing.bind("<FocusIn>", self.remove_default_text_testing)
        self.edit_box_testing.bind("<FocusOut>", self.restore_default_text_testing)
        self.edit_box_testing.place(relx=0.01, rely=0.66, anchor="sw")

        # Percentage validation edit box
        self.default_text_validation = "Percentage validation:"

        self.edit_box_validation = tk.Entry(parent, width=25, font=font)
        self.edit_box_validation.insert(0, self.default_text_validation)
        self.edit_box_validation.config(foreground=self.hint_color)
        self.edit_box_validation.bind("<FocusIn>", self.remove_default_text_validation)
        self.edit_box_validation.bind("<FocusOut>", self.restore_default_text_validation)
        self.edit_box_validation.place(relx=0.01, rely=0.69, anchor="sw")

        # Intervals edit box
        self.default_text_intervals = "Intervals:"

        self.edit_box_intervals = tk.Entry(parent, width=25, font=font)
        self.edit_box_intervals.insert(0, self.default_text_intervals)
        self.edit_box_intervals.config(foreground=self.hint_color)
        self.edit_box_intervals.bind("<FocusIn>", self.remove_default_text_intervals)
        self.edit_box_intervals.bind("<FocusOut>", self.restore_default_text_intervals)
        self.edit_box_intervals.place(relx=0.01, rely=0.725, anchor="sw")

        # Remove column button
        self.label = tk.Label(parent, text="Columns to have:", width=20, height=1,
                                bd=2,
                                highlightthickness=2, font=font)
        self.label.place(relx=0.15, rely=0.552, anchor="sw")

    def remove_default_text_intervals(self, event):
        if self.edit_box_intervals.get() == self.default_text_intervals:
            self.edit_box_intervals.delete(0, tk.END)
            self.edit_box_intervals.config(foreground="black")  # Change text color to black

    def restore_default_text_intervals(self, event):
        if not self.edit_box_intervals.get():
            self.edit_box_intervals.insert(0, self.default_text_intervals)
            self.edit_box_intervals.config(foreground=self.hint_color) # Change text color to the hint color

    def remove_default_text_validation(self, event):
        if self.edit_box_validation.get() == self.default_text_validation:
            self.edit_box_validation.delete(0, tk.END)
            self.edit_box_validation.config(foreground="black")  # Change text color to black

    def restore_default_text_validation(self, event):
        if not self.edit_box_validation.get():
            self.edit_box_validation.insert(0, self.default_text_validation)
            self.edit_box_validation.config(foreground=self.hint_color) # Change text color to the hint color

    def remove_default_text_testing(self, event):
        if self.edit_box_testing.get() == self.default_text_testing:
            self.edit_box_testing.delete(0, tk.END)
            self.edit_box_testing.config(foreground="black")  # Change text color to black

    def restore_default_text_testing(self, event):
        if not self.edit_box_testing.get():
            self.edit_box_testing.insert(0, self.default_text_testing)
            self.edit_box_testing.config(foreground=self.hint_color) # Change text color to the hint color

    def remove_default_text_training(self, event):
        if self.edit_box_training.get() == self.default_text_training:
            self.edit_box_training.delete(0, tk.END)
            self.edit_box_training.config(foreground="black")  # Change text color to black

    def restore_default_text_training(self, event):
        if not self.edit_box_training.get():
            self.edit_box_training.insert(0, self.default_text_training)
            self.edit_box_training.config(foreground=self.hint_color) # Change text color to the hint color

    def remove_default_text_end_date(self, event):
        if self.edit_box_end_date.get() == self.default_text_end_date:
            self.edit_box_end_date.delete(0, tk.END)
            self.edit_box_end_date.config(foreground="black")  # Change text color to black

    def restore_default_text_end_date(self, event):
        if not self.edit_box_end_date.get():
            self.edit_box_end_date.insert(0, self.default_text_end_date)
            self.edit_box_end_date.config(foreground=self.hint_color) # Change text color to the hint color

    def remove_default_text_start_date(self, event):
        if self.edit_box_start_date.get() == self.default_text_start_date:
            self.edit_box_start_date.delete(0, tk.END)
            self.edit_box_start_date.config(foreground="black")  # Change text color to black

    def restore_default_text_start_date(self, event):
        if not self.edit_box_start_date.get():
            self.edit_box_start_date.insert(0, self.default_text_start_date)
            self.edit_box_start_date.config(foreground=self.hint_color)  # Change text color to the hint color

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
        # Actions to be performed when the button is clicked
        print("Button clicked")
        #print(list(self.data_table.stored_dataframe.columns))
    def on_button_click_label(self):
        # Actions to be performed when the button is clicked
        print("Button clicked")

    def on_button_click_remove_column(self):
        # Actions to be performed when the button is clicked
        global my_list_of_entries
        for _ in range(4):
            my_list_of_entries.append(tk.Entry(self.parent))
            my_list_of_entries[-1].pack()

if __name__ == "__main__":
    root = Application()
    root.mainloop()