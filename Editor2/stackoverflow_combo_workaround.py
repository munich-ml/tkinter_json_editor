"""
Stackoverflow workaround for FocusOut Problem of ttk.Combobox
https://stackoverflow.com/questions/66145976/behavior-of-focusout-event-of-ttk-combobox
"""


import tkinter as tk
from tkinter import ttk


class EntryPopup(ttk.Entry):

    def __init__(self, parent, iid, col, text, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = col

        self.insert(0, text)
        self.select_range(0, tk.END)

        self.focus_force()
        self.bind("<Return>", self.on_return)
        self.bind("<Escape>", self.on_escape)

    def on_return(self, event):
        self.close()

    def on_escape(self, event):
        self.destroy()

    def close(self):
        if self.col == '#0':
            self.tv.item(self.iid, text=self.get())
        else:
            self.tv.set(self.iid, self.col, self.get())
        self.destroy()


class ComboPopup(ttk.Combobox):

    def __init__(self, parent, iid, col, **kw):
        super().__init__(parent, **kw)
        self.tv = parent
        self.iid = iid
        self.col = col
        self.old_text = self.tv.set(iid, col)
        self.set(self.old_text)

        self.focus()
        self.bind("<Escape>", self.on_escape)
        self.bind("<<ComboboxSelected>>", self.new_selection)
        self.bind("<Return>", self.on_return)

    def new_selection(self, event=None):
        self.tv.set(self.iid, self.col, self.get())

    def on_return(self, event):
        self.close()

    def on_escape(self, event):
        self.tv.set(self.iid, self.col, self.old_text)
        self.destroy()

    def close(self):
        self.new_selection()
        self.destroy()


class App(ttk.Frame):

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.popup = None

        # Create Treeview
        self.tree = ttk.Treeview(self.parent, column=('A', 'B'), selectmode='browse', height=7)
        self.tree.pack(expand=True, fill='both', side='top')

        # Setup column heading
        self.tree.heading('#0', text=' Items', anchor='center')
        self.tree.heading('#1', text=' A', anchor='center')
        self.tree.heading('#2', text=' B', anchor='center')

        self.tree.bind("<Button-1>", lambda event: self.destroy_cell_popup())
        self.tree.bind("<Double-Button-1>", self.on_double_click)

        self.tree.insert('', 'end', text="First item", value=("A's value 1", "B's value 1"))
        self.tree.insert('', 'end', text="Second item", value=("A's value 2", "B's value 2"))


    def destroy_cell_popup(self):
        if self.popup and self.popup.winfo_exists():
            self.popup.close()
            self.popup = None


    def on_double_click(self, event):
        """ Executed, when a row is single or double-clicked.
        Opens EntryPopup or ComboPopup above the item's column,
        so it is possible to select text """
        self.destroy_cell_popup()

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
            self.popup = ComboPopup(self.tree, rowid, column, values=("A", "b", "3"))
            
        self.popup.place(x=x, y=y, width=width, height=height, anchor='w')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('600x200+200+100')
    App(root)
    root.mainloop()