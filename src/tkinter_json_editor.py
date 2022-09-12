import json, os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, font, messagebox, Tk

class JSONTreeFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X)
        tk.Label(self.control_frame, text="control_frame").pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="Button 1").pack(side=tk.RIGHT)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame)
        #self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.grid(row=0, column=0, sticky=(tk.N, tk.S, tk.E, tk.W))
        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky=(tk.N, tk.S))        

        
if __name__ == '__main__':
    app = tk.Tk()
    app.title('Tkinter JSON Editor')
    app.geometry("500x500")
    jtf = JSONTreeFrame(app)
    jtf.pack(fill=tk.BOTH, expand=True)
    app.mainloop()