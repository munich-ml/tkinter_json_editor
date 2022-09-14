from email.errors import ObsoleteHeaderDefect
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
        ttk.Button(self.control_frame, text="save JSON file", command=self.save_json_file).pack(side=tk.RIGHT)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        
        self.tree = ttk.Treeview(tree_frame, columns=("#1", ))
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading("#0", text="field")
        self.tree.heading("#1", text="value")
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
        else:        
            self.delete_tree_nodes()
            self.insert_tree_node(file.name, value=obj)


    def save_json_file(self):
        obj = self.extract_obj_from_tree()
        print(obj)
        

    def insert_tree_node(self, field: str, value= object, node: str = '') -> None:
        type_tag = str(type(value)).split("'")[1]
        if type(value) is dict:
            node = self.tree.insert(node, tk.END, text=field, tags=type_tag)
            for key, val in value.items():
                self.insert_tree_node(key, val, node)
                
        elif type(value) is list:
            node = self.tree.insert(node, tk.END, text=field, tags=type_tag)
            for i, val in enumerate(value):
                self.insert_tree_node(i, val, node)

        else:
            self.tree.insert(node, tk.END, text=field, values=[value], tags=type_tag)        
        
        
    def delete_tree_nodes(self):
        for i in self.tree.get_children():
            self.tree.delete(i)


    def extract_obj_from_tree(self, node: str = "I001") -> object:
        """Extracts the (json-able) Python object from the tree (Tkinter TreeView)

        Args:
            node (str, optional): TreeView node reference. Defaults to "I001" (root).

        Returns:
            object: Python object extracted from the treeview
        """
        if self.tree.tag_has("dict", node):
            obj = {}
            for child in self.tree.get_children(node):
                obj[self.tree.item(child)["text"]] = self.extract_obj_from_tree(child)
            return obj
                
        if self.tree.tag_has("list", node):
            return [self.extract_obj_from_tree(child) for child in self.tree.get_children(node)]
        
        if self.tree.tag_has("NoneType", node):
            return None
        
        obj = self.tree.item(node)['values'][0]
        
        if self.tree.tag_has("bool", node):
            return obj == "True"
        
        if self.tree.tag_has("int", node):
            try:
                return int(obj)
            except ValueError:
                return obj
            
        if self.tree.tag_has("float", node):
            try:
                return float(obj)
            except ValueError:
                return obj        
        
        return obj  # that covers the regular 'str' type

if __name__ == '__main__':
    app = tk.Tk()
    app.title('Tkinter JSON Editor')
    app.geometry("500x500")
    JSONTreeFrame(app)
    app.mainloop()