"""
Stackoverflow workaround for FocusOut Problem of ttk.Combobox
https://stackoverflow.com/questions/66145976/behavior-of-focusout-event-of-ttk-combobox
"""


import tkinter as tk
from tkinter import ttk


class EntryPopup(ttk.Entry):

    def __init__(self, parent, iid, col, text, **kwargs):
        super().__init__(parent, **kwargs)
        self.tree = parent
        self.iid = iid
        self.col = col

        self.insert(0, text)
        self.select_range(0, tk.END)

        self.focus()
        self.bind("<Return>", lambda event: self.update())
        self.bind("<Escape>", lambda event: self.destroy())

    def update(self):
        if self.col == '#0':
            self.tree.item(self.iid, text=self.get())
        else:
            self.tree.set(self.iid, self.col, self.get())
        self.destroy()


class ComboPopup(ttk.Combobox):

    def __init__(self, parent, iid, col, text, **kwargs):
        super().__init__(parent, **kwargs)
        self.tree = parent
        self.iid = iid
        self.col = col

        self.set(text)

        self.focus()
        self.bind("<Return>", lambda event: self.update())
        self.bind("<Escape>", lambda event: self.destroy())

    def update(self):
        self.tree.set(self.iid, self.col, self.get())
        self.destroy()


class TreeFrame(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.popup = None
        
        # Create Treeview
        self.tree = ttk.Treeview(self.parent, column=('A', ), selectmode='browse', height=7)
        self.tree.pack(expand=True, fill='both', side='top')

        # Setup column heading
        self.tree.heading('#0', text=' Items', anchor='center')
        self.tree.heading('#1', text=' A', anchor='center')

        self.tree.bind("<Button-1>", lambda event: self.close_cell_popup())
        self.tree.bind("<Double-Button-1>", self.on_double_click)

        self.tree.insert('', 'end', text="First item", value=("A's value 1", ))
        self.tree.insert('', 'end', text="Second item", value=("A's value 2", ))


    def close_cell_popup(self):
        if self.popup and self.popup.winfo_exists():
            self.popup.update()
            self.popup = None


    def on_double_click(self, event):
        """ Executed, when a row is single or double-clicked.
        Opens EntryPopup or ComboPopup above the item's column,
        so it is possible to select text """
        self.close_cell_popup()

        # What row and column was clicked on
        rowid = self.tree.identify_row(event.y)      # like "I001"
        column = self.tree.identify_column(event.x)  # like "#0"

        # Check if the double click was on some row or empty space
        if rowid == '':
            return

        # get cell position info
        x, y, width, height = self.tree.bbox(rowid, column)
        y += height / 2
        height *= 1.2    # make the popup a little larger than the regular cell

        # place Entry popup properly
        if column == '#0':
            text = self.tree.item(rowid, 'text')
            self.popup = EntryPopup(self.tree, rowid, column, text)
        else:
            text = self.tree.set(rowid, column)
            self.popup = ComboPopup(self.tree, rowid, column, text, values=("A", "b", "3"))
            
        self.popup.place(x=x, y=y, width=width, height=height, anchor='w')


if __name__ == '__main__':
    app = tk.Tk()
    app.geometry('600x200+200+100')
    TreeFrame(app)
    app.mainloop()