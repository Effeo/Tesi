import tkinter as tk
from pathlib import Path
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

import pandas as pd

'''
    - selezionare le righe per data X
    - pulsante generazione immagine X
    - che metodo di generazione
    - crea sia le cartelle che le immagini (selezionando) X
    - crea colonna Label
    - tarpare colonna (togliere colonna)
    - selezionare le righe con data di inizio e fine oppure per intervalli (dalle due righe selezionate ogni quante bisogna generare le immagini)
    
    - dire le percentuali per le parti di training, validation e testing
'''
class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.set_window_size_to_screen()
        self.search_page = SearchPage(parent=self.main_frame)

    def set_window_size_to_screen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f"{screen_width}x{screen_height}")


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

        #Search bar che a me non serve
        '''
        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.75)
        self.search_entrybox.bind("<Return>", self.search_table)
        '''

        # Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(rely=0, relx=0.25, relwidth=0.75, relheight=1)

        self.path_map = {}

        # Pulsante genera
        self.button = tk.Button(parent, text="Genera", command=self.on_button_click, width=20, height=2, bd=2, highlightthickness=2, bg = "#a9a9a9")
        self.button.place(relx=0.17, rely=0.95, anchor="sw")

        # EditBox data inizio
        font = ("Arial", 12)
        self.default_text_data_inizio = "Data inizio: AAAA-MM-GG"
        self.hint_color = "gray"  # Colore grigio chiaro per l'hint

        self.edit_box_data_inizio = tk.Entry(parent, width=25, font=font)
        self.edit_box_data_inizio.insert(0, self.default_text_data_inizio)
        self.edit_box_data_inizio.config(foreground=self.hint_color)
        self.edit_box_data_inizio.bind("<FocusIn>", self.remove_default_text_data_inizio)
        self.edit_box_data_inizio.bind("<FocusOut>", self.restore_default_text_data_inizio)
        self.edit_box_data_inizio.place(relx=0.01, rely=0.55, anchor="sw")

        # EditBox data finale
        self.default_text_data_fine = "Data fine: AAAA-MM-GG"

        self.edit_box_data_fine = tk.Entry(parent, width=25, font=font)
        self.edit_box_data_fine.insert(0, self.default_text_data_fine)
        self.edit_box_data_fine.config(foreground=self.hint_color)
        self.edit_box_data_fine.bind("<FocusIn>", self.remove_default_text_data_fine)
        self.edit_box_data_fine.bind("<FocusOut>", self.restore_default_text_data_fine)
        self.edit_box_data_fine.place(relx=0.01, rely=0.59, anchor="sw")

        # Text tipo fi generazione: cartelle, immagini entrambi
        self.text_generazione = tk.Text(parent, width=30, height=1, font=font, highlightthickness=0, background="#f0f0f0", bd=0)
        self.text_generazione.insert(tk.END, "Vuoi generare file csv o immagini:")
        self.text_generazione.place(relx=0.01, rely=0.75, anchor="sw")

        # Radio button per il tipo di generazione
        self.radio_var_generazione = tk.StringVar(value="vuoto")  # Imposta il valore iniziale su una stringa vuota

        # radio button: file
        self.radio_button_cartelle = tk.Radiobutton(parent, text="File", variable=self.radio_var_generazione,
                                                    value="file", font=font)
        self.radio_button_cartelle.place(relx=0.01, rely=0.8, anchor="sw")

        # radio button: immagini
        self.radio_button_immagini = tk.Radiobutton(parent, text="Immagini", variable=self.radio_var_generazione,
                                                    value="Immagini", font=font)
        self.radio_button_immagini.place(relx=0.07, rely=0.8, anchor="sw")

        # radio button: entrambi
        self.radio_button_entrambi = tk.Radiobutton(parent, text="Entrambi", variable=self.radio_var_generazione,
                                                    value="entrambi", font=font)
        self.radio_button_entrambi.place(relx=0.15, rely=0.8, anchor="sw")

    def remove_default_text_data_fine(self, event):
        if self.edit_box_data_fine.get() == self.default_text_data_fine:
            self.edit_box_data_fine.delete(0, tk.END)
            self.edit_box_data_fine.config(foreground="black")  # Cambia il colore del testo a nero

    def restore_default_text_data_fine(self, event):
        if not self.edit_box_data_fine.get():
            self.edit_box_data_fine.insert(0, self.default_text_data_fine)
            self.edit_box_data_fine.config(foreground=self.hint_color)  # Cambia il colore del testo all'hint color


    def remove_default_text_data_inizio(self, event):
        if self.edit_box_data_inizio.get() == self.default_text_data_inizio:
            self.edit_box_data_inizio.delete(0, tk.END)
            self.edit_box_data_inizio.config(foreground="black")  # Cambia il colore del testo a nero

    def restore_default_text_data_inizio(self, event):
        if not self.edit_box_data_inizio.get():
            self.edit_box_data_inizio.insert(0, self.default_text_data_inizio)
            self.edit_box_data_inizio.config(foreground=self.hint_color)  # Cambia il colore del testo all'hint color

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

    def on_button_click(self):
        # Azioni da eseguire quando il pulsante viene prem
        print("Pulsante premuto")


if __name__ == "__main__":
    root = Application()
    root.mainloop()