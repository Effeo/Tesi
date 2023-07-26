import tkinter as tk
from tkinterdnd2 import DND_FILES, TkinterDnD
from SearchPage import SearchPage
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
        self.wm_minsize(width=1900, height=900)


if __name__ == "__main__":
    root = Application()
    root.mainloop()
