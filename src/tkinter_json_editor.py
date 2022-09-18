import json
from msilib.schema import ComboBox
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox

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
        
        self.tree = ttk.Treeview(tree_frame, columns=("#1", ))
        self.tree.grid(row=0, column=0, sticky="nsew")
        self.tree.heading("#0", text="field")
        self.tree.heading("#1", text="value")
        ysb = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=ysb.set)
        ysb.grid(row=0, column=1, sticky="ns")        
        self.tree.bind("<Double-1>", self.on_double_click)
        
        with open("multiple_choice.json", "r") as file:
            self.multiple_choice = json.load(file)


    def on_double_click(self, event: tk.Event) -> None:
        """Handle double click events on the tree (Tk.treeview) widget

        Args:
            event (tk.Event): event.x/y hold the x/y coordinates of the click event
        """
        region = self.tree.identify_region(event.x, event.y)
        # region is "tree" if the field column is double clicked and "cell" for value column
        if region not in ("tree", "cell"):
            return
        
        selected_node = self.tree.focus()  # node id like "I001"
        selected_item = self.tree.item(selected_node)
        
        if "NoneType" in selected_item["tags"]:
            return  # no editing of NoneType items
        
        if region == "tree":
            selected_value = selected_item["text"]
        else:
            try:
                selected_value = selected_item["values"][0]
            except IndexError:   # This happens in list and dict rows and value column -> not editable
                return
        
        selected_col = {"tree": "#0", "cell": "#1"}[region]
        x, y, w, h = self.tree.bbox(selected_node, selected_col)  # bounding box of selected cell
        
        if "bool" in selected_item["tags"]:
            self.is_checked = tk.BooleanVar(self.tree)
            self.is_checked.set("True" == selected_value)
            widget = ttk.Checkbutton(self.tree, onvalue=True, offvalue=False, variable=self.is_checked, width=w)
            
        elif region != "tree" and selected_item["text"] in self.multiple_choice:
            choices = self.multiple_choice[selected_item["text"]]
            widget = ttk.Combobox(self.tree_frame, width=w, values=choices)
            try:
                idx = choices.index(selected_value)
            except ValueError:
                idx = 0
            else:
                widget.current(idx)
            
        else:
            widget = ttk.Entry(self.tree_frame, width=w)
            widget.insert(0, selected_value)      # insert selected text in the entry widget    
            widget.select_range(0, tk.END)
            
        widget.editing_node = selected_node  # store node in the widget object for later use 
        widget.editing_region = region       # store region in the widget object for later use 
        widget.focus()
        widget.bind("<Escape>", self.on_focus_out)            
        widget.bind("<FocusOut>", self.on_focus_out)            
        widget.bind("<Return>", self.on_enter_pressed)      
        widget.place(x=x, y=y, width=w, height=h)


    def on_focus_out(self, event: tk.Event) -> None:
        """Handles focus out events of the Entry widget

        Args:
            event (tk.Event): event.widget holds the source widget (tree)
        """
        if type(event.widget)==ttk.Checkbutton:
            checked = "selected" in event.widget.state()
            self.tree.item(event.widget.editing_node, values=[checked])
            
        elif type(event.widget) in (ttk.Entry, ttk.Combobox):
            new_text = event.widget.get()
            if event.widget.editing_region == "tree":
                self.tree.item(event.widget.editing_node, text=new_text)
            else:
                tags = self.tree.item(event.widget.editing_node)["tags"]
                if "int" in tags:
                    try:
                        new_text = int(new_text)
                    except:
                        event.widget.destroy()  # don't do a change
                        return  
                elif "float" in tags:
                    try:
                        new_text = float(str(new_text).replace(",", "."))
                    except:
                        event.widget.destroy()  # don't do a change
                        return 
                    
                self.tree.item(event.widget.editing_node, values=[new_text])    
                
        event.widget.destroy()
        
        
    def on_enter_pressed(self, event: tk.Event) -> None:
        self.tree_frame.focus()  # focus out of the Entry widget

    
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
        fp = filedialog.askopenfilename(filetypes=[("JSON files", "*.json"), ("All Files", "*.*")])
        if not fp:
            return
        
        try:
            with open(fp, "r") as file:
                obj = json.load(file)
        except Exception as e:
            messagebox.showwarning(title="Warning", message=f"Could not open '{fp}'!")
        else:        
            self.delete_tree_nodes()
            self.insert_tree_node(file.name, value=obj)
            self.expand_tree()


    def save_json_file(self):
        """Launches a filepicker and saves the current tree content as json to that file path.
        """
        fp = filedialog.asksaveasfilename(filetypes=[("JSON files", "*.json"), ("All Files", "*.*")])
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
    app.title('Tkinter JSON Editor')
    app.geometry("500x500")
    JSONTreeFrame(app)
    app.mainloop()