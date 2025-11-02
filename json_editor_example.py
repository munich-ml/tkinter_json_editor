"""
JSON Editor Example - Demonstrates usage of TreeEditFrame for JSON file editing.

This is an example application showing how to use the TreeEditFrame component
to create a JSON file editor with load/save functionality.
"""

import json
import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog, messagebox
from tree_edit_frame import TreeEditFrame


class JSONEditorApp(ttk.Frame):
    """Example application demonstrating JSON editing with TreeEditFrame.

    This class shows how to use TreeEditFrame for a specific use case:
    editing JSON files with file loading/saving capabilities.
    """

    def __init__(self, master):
        super().__init__(master)
        self.pack(fill=tk.BOTH, expand=True)

        # Create control frame with buttons
        self.control_frame = ttk.Frame(self)
        self.control_frame.pack(fill=tk.X)
        ttk.Button(self.control_frame, text="load JSON file", command=self.load_json_file).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="save JSON file", command=self.save_json_file).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="expand", command=self.expand_tree).pack(side=tk.LEFT)
        ttk.Button(self.control_frame, text="collapse", command=self.collapse_tree).pack(side=tk.LEFT)

        # Load combo choices configuration
        self.path = os.path.dirname(__file__)
        combo_choices = {}
        try:
            with open(os.path.join(self.path, "combo_choice.json"), "r") as file:
                combo_choices = json.load(file)
        except FileNotFoundError:
            pass  # combo_choice.json is optional

        # Create the reusable TreeEditFrame component
        self.tree_editor = TreeEditFrame(self, combo_choices=combo_choices)

    def expand_tree(self):
        """Expand all nodes in the tree"""
        self.tree_editor.expand_tree(expand=True)

    def collapse_tree(self):
        """Collapse all nodes in the tree"""
        self.tree_editor.expand_tree(expand=False)

    def load_json_file(self) -> None:
        """Launches a file picker to select a JSON file and loads it into the tree.
        """
        fp = filedialog.askopenfilename(
            initialdir=self.path,
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")]
        )
        if not fp:
            return

        try:
            with open(fp, "r") as file:
                obj = json.load(file)
        except json.JSONDecodeError as e:
            messagebox.showerror(title="Error", message=f"Invalid JSON: {e}")
            return
        except Exception as e:
            messagebox.showwarning(title="Warning", message=f"Could not open '{fp}': {e}")
            return

        # Use TreeEditFrame's load_data method with the filename as root
        self.tree_editor.load_data(obj, root_name=os.path.basename(fp))

    def save_json_file(self):
        """Launches a file picker and saves the current tree content as JSON to that file path.
        """
        fp = filedialog.asksaveasfilename(
            initialdir=self.path,
            filetypes=[("JSON files", "*.json"), ("All Files", "*.*")]
        )
        if not fp:
            return

        # Use TreeEditFrame's get_data method to extract the data
        obj = self.tree_editor.get_data()

        try:
            with open(fp, "w") as file:
                json.dump(obj, file, indent=2)
        except Exception as e:
            messagebox.showwarning(title="Warning", message=f"Could not save to '{fp}': {e}")
        else:
            messagebox.showinfo(title="Success", message=f"Saved to '{fp}'")


if __name__ == '__main__':
    app = tk.Tk()
    app.title('JSON Editor Example - TreeEditFrame Demo')
    app.geometry("600x400")
    JSONEditorApp(app)
    app.mainloop()
