import tkinter as tk
from pathlib import Path
from tkinter import ttk

from tkinterdnd2 import DND_FILES, TkinterDnD

import pandas as pd


class Application(TkinterDnD.Tk):
    def __init__(self):
        super().__init__()
        self.title("CSV Viewer")
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill="both", expand="true")
        self.geometry("900x500")
        self.search_page = SearchPage(parent=self.main_frame)


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
        self.file_names_listbox.place(relheight=1, relwidth=0.25)
        self.file_names_listbox.drop_target_register(DND_FILES)
        self.file_names_listbox.dnd_bind("<<Drop>>", self.drop_inside_list_box)
        self.file_names_listbox.bind("<Double-1>", self._display_file)

        self.search_entrybox = tk.Entry(parent)
        self.search_entrybox.place(relx=0.25, relwidth=0.75)
        self.search_entrybox.bind("<Return>", self.search_table)

        # Treeview
        self.data_table = DataTable(parent)
        self.data_table.place(rely=0.05, relx=0.25, relwidth=0.75, relheight=0.95)

        self.path_map = {}

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


if __name__ == "__main__":
    root = Application()
    root.mainloop()


'''
import tkinter as tk
import tkinter.font as tkfont

def open_csv_file():
    file_path = "2000-03-06_1_day_1.csv"  # Aggiungi il percorso del tuo file CSV
    with open(file_path, "r") as file:
        csv_content = file.read()
        text_widget.configure(state=tk.NORMAL)  # Abilita la modalità di modifica
        text_widget.delete(1.0, tk.END)  # Cancella il contenuto precedente
        text_widget.insert(tk.END, csv_content)  # Inserisci il contenuto del file CSV nel widget Text

        # Creazione di un nuovo stile di font bold
        bold_font = tkfont.Font(text_widget, text_widget.cget("font"))
        bold_font.configure(weight="bold", size=16)  # Impostazione del grassetto e della dimensione del font

        # Creazione di un nuovo stile di font per le righe successive
        normal_font = tkfont.Font(text_widget, text_widget.cget("font"))
        normal_font.configure(size=14)  # Impostazione della dimensione del font per le righe successive

        # Applicazione dello stile di font alle righe successive
        text_widget.tag_add("normal", "2.0", tk.END)  # Applica lo stile a partire dalla seconda riga fino alla fine
        text_widget.tag_configure("normal", font=normal_font)

        # Applicazione dello stile di font alla prima riga
        text_widget.tag_add("bold", "1.0", "1.end")
        text_widget.tag_configure("bold", font=bold_font)

        # Aggiungi linee verticali
        num_columns = csv_content.split("\n")[0].count(",") + 1
        for i in range(1, num_columns):
            x_position = f"{i}.0"
            text_widget.create_line(x_position, 0, x_position, text_widget.winfo_height())

        # Aggiungi linee orizzontali
        num_rows = csv_content.count("\n") + 1
        for i in range(1, num_rows):
            y_position = f"{i}.0"
            text_widget.create_line(0, y_position, text_widget.winfo_width(), y_position)

        text_widget.configure(state=tk.DISABLED)  # Disabilita la modalità di modifica

# Crea una nuova finestra
window = tk.Tk()

# Crea un widget Text
text_widget = tk.Text(window, state=tk.DISABLED)
text_widget.pack(anchor=tk.NW, expand=True, fill="both")

# Crea un pulsante per aprire il file CSV
open_button = tk.Button(window, text="Apri CSV", command=open_csv_file)
open_button.pack(anchor=tk.NW)

window.mainloop()
'''