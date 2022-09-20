import json, os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox


class EntryPopup(ttk.Entry):
    """Popup edit widget for str, int and float type fields
    """
    def __init__(self, parent, iid, col, inital_value, **kwargs):
        super().__init__(parent, **kwargs)
        self.tree = parent
        self.iid = iid
        self.col = col

        self.insert(0, inital_value)
        self.select_range(0, tk.END)

    def update(self):
        """Updates the tree value at the respective iid (row) and column and
           depending on the type of the value (specified in tags)
        """
        new_value = self.get()
        if self.col == '#0':
            self.tree.item(self.iid, text=new_value)
        else:
            tags = self.tree.item(self.iid)["tags"]
            try:
                if "int" in tags:
                    new_value = int(new_value)
                elif "float" in tags:
                    new_value = float(new_value)
            except ValueError:
                pass   # don't do a change if conversion fails
            else:  
                self.tree.item(self.iid, values=[new_value])
        self.tree.focus_set()
        self.destroy()


class ComboPopup(ttk.Combobox):
    """Popup edit widget for str type fields with combo_choice
    """
    def __init__(self, parent, iid, inital_value, **kwargs):
        super().__init__(parent, state="readonly", **kwargs)
        self.tree = parent
        self.iid = iid
        self.choices = kwargs["values"]

        self.set(inital_value)

    def update(self):
        self.tree.item(self.iid, values=[self.get()])
        self.tree.focus_set()
        self.destroy()
        
        
class CheckPopup(ttk.Checkbutton):
    """Popup edit widget for bool type fields
    """
    def __init__(self, parent, iid, inital_value, **kwargs):
        self.is_checked = tk.BooleanVar(parent)
        self.is_checked.set("True" == inital_value)  # Treeview stores also bools as str!
        super().__init__(parent, onvalue=True, offvalue=False, variable=self.is_checked, **kwargs)
        self.tree = parent
        self.iid = iid

    def update(self):
        checked = "selected" in self.state()
        self.tree.item(self.iid, values=[checked])
        self.tree.focus_set()
        self.destroy()

                
class JSONTreeFrame(ttk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X)
        ttk.Button(self.control_frame, text="load JSON file", command=self.load_json_file).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="save JSON file", command=self.save_json_file).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="expand", command=self.expand_tree).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="collape", command=lambda: self.expand_tree(expand=False)).pack(side=tk.LEFT)
        
        tree_frame = ttk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)
        self.tree_frame = tree_frame
        
        self.tree = ttk.Treeview(tree_frame, selectmode="browse", columns=("#1", ))
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading("#0", text="field")
        self.tree.heading("#1", text="value")
        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky="ns")        
        self.tree.bind("<Button-1>", lambda event: self.close_cell_popup())
        self.tree.bind("<Double-1>", self.on_double_click)
        self.tree.bind("<Return>", self.on_return_press)
        
        self.popup = None    # Popup widget for cell editing
        
        self.path = os.path.dirname(__file__)
        with open(os.path.join(self.path, "combo_choice.json"), "r") as file:
            self.combo_choice = json.load(file)


    def close_cell_popup(self):
        """Closes Edit pop-up widget, if is exists
        """
        if self.popup and self.popup.winfo_exists():
            self.popup.update()
            self.popup = None
            
            
    def on_return_press(self, event):
        print(event, self.tree.focus())
        self.make_popup(rowid=self.tree.focus(), column="#1")


    def on_double_click(self, event: tk.Event) -> None:
        """Handle double click events on the tree (Tk.treeview) widget

        Args:
            event (tk.Event): event.x/y hold the x/y coordinates of the click event
        """
        rowid = self.tree.identify_row(event.y)      # like "I001"
        column = self.tree.identify_column(event.x)  # like "#0"

        self.make_popup(rowid, column)        


    def make_popup(self, rowid, column):
        self.close_cell_popup()

        if rowid == '':  # happens if clicked in empty space or header 
            return        
        
        selected_item = self.tree.item(rowid)
        
        if "NoneType" in selected_item["tags"]:
            return  # no editing of NoneType items
        
        if column == "#0":
            selected_value = selected_item["text"]
        else:
            try:
                selected_value = selected_item["values"][0]
            except IndexError:   # This happens in list and dict rows and value column -> not editable
                return
        
        # get cell position info
        x, y, width, height = self.tree.bbox(rowid, column)
        y += height / 2
        height *= 1.2    # make the popup a little larger than the regular cell
                
        if "bool" in selected_item["tags"]:
            self.popup = CheckPopup(self.tree, rowid, selected_value)
                    
        elif column != "#0" and selected_item["text"] in self.combo_choice:
            choices = self.combo_choice[selected_item["text"]]
            self.popup = ComboPopup(self.tree, rowid, selected_value, values=choices)
            
        else:
            self.popup = EntryPopup(self.tree, rowid, column, selected_value)
            
        self.popup.focus()                                                # This code would usually be in 
        self.popup.bind("<Return>", lambda event: self.popup.update())    # the Popup __init__, but that 
        self.popup.bind("<Escape>", lambda event: self.popup.destroy())   # would result in 3 copies
        
        self.popup.place(x=x, y=y, width=width, height=height, anchor='w')

    
    def get_all_children(self, item: str = "") -> list[str]:
        children = self.tree.get_children(item)
        for child in children:
            children += self.get_all_children(child)
        return children
    
    
    def expand_tree(self, expand: bool = True) -> None:
        for item in self.get_all_children():
            self.tree.item(item, open=expand)
            
                     
    def load_json_file(self) -> None:
        """Launches a filepicker to select a file, that will be read as json and inserted into the tree.
        """
        fp = filedialog.askopenfilename(initialdir=self.path, filetypes=[("JSON files", "*.json"), ("All Files", "*.*")])
        if not fp:
            return
        
        try:
            with open(fp, "r") as file:
                obj = json.load(file)
        except Exception as e:
            messagebox.showwarning(title="Warning", message=f"Could not open '{fp}'!")
            return
                
        self.delete_tree_nodes()
        self.insert_tree_node(file.name, value=obj)
        self.expand_tree()
        
        # set selection and allow keyboard browsing
        first = self.tree.get_children()[0]
        self.tree.selection_set(first) # move selection
        self.tree.focus(first) # move focus
        self.tree.see(first) # scroll to show it
        self.tree.focus_set()


    def save_json_file(self):
        """Launches a filepicker and saves the current tree content as json to that file path.
        """
        fp = filedialog.asksaveasfilename(initialdir=self.path, filetypes=[("JSON files", "*.json"), ("All Files", "*.*")])
        if not fp:
            return

        obj = self.extract_obj_from_tree()
        try:
            with open(fp, "w") as file:
                json.dump(obj, file)
        except Exception as e:
            messagebox.showwarning(title="Warning", message=f"Could not open '{fp}'!")
        

    def insert_tree_node(self, field: str, value: object, node: str = '') -> None:
        """Inserts a tree node (consisting of field name and value) at the node (tree position).
        If value is a (JSON-able) tree object (incl. lists and dicts) it will be inserted hierarchically.

        Args:
            field (str): field name in the tree
            value (JSON-able object): Value in the tree
            node (str, optional): _description_. Defaults to ''.
        """
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
        for child in self.tree.get_children():
            self.tree.delete(child)


    def extract_obj_from_tree(self, node: str = "I001") -> object:
        """Extracts the (JSON-able) Python object from the tree (Tkinter TreeView)

        Args:
            node (str, optional): TreeView node reference. Defaults to "I001" (root).

        Returns:
            object: Python object extracted from the treeview
        """
        if not self.tree.exists(node):
            return None
        
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
    app.title('Tkinter JSON Editor2')
    app.geometry("500x300-10+30")
    JSONTreeFrame(app)
    app.mainloop()