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
        ttk.Frame.__init__(self, parent)
        self.parent = parent
        self.cellPopup = None
        self.single_click = False

        # Create Treeview
        self.tree = ttk.Treeview(self.parent, column=('A', 'B'), selectmode='browse', height=7)
        self.tree.pack(expand=True, fill='both', side='top')

        # Setup column heading
        self.tree.heading('#0', text=' Items', anchor='center')
        self.tree.heading('#1', text=' A', anchor='center')
        self.tree.heading('#2', text=' B', anchor='center')

        self.tree.bind("<Double-Button-1>", lambda event: self.on_click(event, 101))
        self.tree.bind("<Button-1>", lambda event: self.on_click(event, 1))

        self.tree.insert('', 'end', text="First item", value=("A's value 1", "B's value 1"))
        self.tree.insert('', 'end', text="Second item", value=("A's value 2", "B's value 2"))

    def destroy_cell_popup(self):
        if self.single_click:
            self.single_click = False
            if self.cellPopup and self.cellPopup.winfo_exists():
                self.cellPopup.close()
                self.cellPopup = None

    def on_click(self, event, extra=None):
        """ Executed, when a row is single or double-clicked.
        Opens EntryPopup or ComboPopup above the item's column,
        so it is possible to select text """
        if extra == 1:
            self.single_click = True
            self.parent.after(200, self.destroy_cell_popup)
            return
        elif extra == 101:
            self.single_click = False
            if self.cellPopup and self.cellPopup.winfo_exists():
                self.cellPopup.close()
                self.cellPopup = None

        # What row and column was clicked on
        rowid = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        # Check if the double click was on some row or empty space
        if rowid == '':
            return

        # get cell position info
        x, y, width, height = self.tree.bbox(rowid, column)

        # y-axis offset
        pady = height / 2

        # place Entry popup properly
        if column == '#0':
            text = self.tree.item(rowid, 'text')
            self.cellPopup = EntryPopup(self.tree, rowid, column, text)
        else:
            self.cellPopup = ComboPopup(self.tree, rowid, column, values=("A", "b", "3"))
        self.cellPopup.place(x=x, y=y + pady, width=width, height=1.25 * height, anchor='w')


if __name__ == '__main__':
    root = tk.Tk()
    root.geometry('900x600+300+300')
    App(root)
    root.mainloop()