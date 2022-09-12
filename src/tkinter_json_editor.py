import json, os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, font, messagebox, Tk



class JSONTreeFrame(ttk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X)
        tk.Label(self.control_frame, text="control_frame").pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="load JSON file", command=self.load_json_file).pack(side=tk.RIGHT)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame)
        self.tree.grid(row=0, column=0, sticky="nsew")
        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky="ns")        


    def load_json_file(self):
        fp = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All Files", "*.*")])
        if fp is None:
            return
        
        try:
            with open(fp, "r") as file:
                obj = json.load(file)
        except Exception as e:
            messagebox.showwarning(title="Warning", message=f"Could not open '{fp}'!")
            return
        
        print(fp)
        print(obj)


if __name__ == '__main__':
    app = tk.Tk()
    app.title('Tkinter JSON Editor')
    app.geometry("500x500")
    JSONTreeFrame(app)
    app.mainloop()