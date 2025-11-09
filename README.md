# TreeEditFrame - Hierarchical Data Editor for Tkinter

A reusable Tkinter component for viewing and editing hierarchical data structures (dicts, lists, primitives) with an in-place tree editor. The project includes both the reusable component and a JSON editor example application.

## Project Structure

- **[src/tree_edit_frame.py](src/tree_edit_frame.py)** - Reusable TreeEditFrame component (use this in your own applications)
- **[examples/json_editor_example.py](examples/json_editor_example.py)** - Example application demonstrating JSON file editing
- **[examples/example.json](examples/example.json)** - Sample JSON file for testing
- **[tests/](tests/)** - Test suite (to be implemented)

## TreeEditFrame Component

The `TreeEditFrame` is a reusable Tkinter widget that provides a Treeview with in-place editing capabilities for hierarchical data.

### Features

- Edit values directly by double-clicking cells or pressing Enter
- Type-aware editing with appropriate widgets for each data type:

  | Data Type | Widget | Behavior |
  |-----------|--------|----------|
  | `str` | `ttk.Entry` | Basic text entry |
  | `int` | `ttk.Entry` | Value accepted only if it can be typecast to integer |
  | `float` | `ttk.Entry` | Value accepted only if it can be typecast to float |
  | `bool` | `ttk.Checkbutton` | Toggle between True/False |
  | `str` with choices | `ttk.Combobox` | Dropdown selection from predefined choices |

- Headless component (no file I/O - you control data loading/saving)
- Optional combo choices for dropdown field selection
- Expand/collapse tree navigation
- Keyboard navigation support

### Basic Usage

```python
import tkinter as tk
from tree_edit_frame import TreeEditFrame

# Create your application window
app = tk.Tk()

# Create the TreeEditFrame component
tree_editor = TreeEditFrame(app, combo_choices={'status': ['active', 'inactive']})
tree_editor.pack(fill=tk.BOTH, expand=True)

# Load your data
data = {'name': 'Example', 'value': 42, 'nested': {'key': 'value'}}
tree_editor.set_data(data)

# ... user edits the data ...

# Get the edited data back
edited_data = tree_editor.get_data()
print(edited_data)

# For read-only viewing:
# readonly_tree = TreeEditFrame(app, editable=False)
# readonly_tree.set_data(data)

# Or toggle editing dynamically:
# tree_editor.set_editable(False)  # Make read-only
# tree_editor.set_editable(True)   # Make editable again

app.mainloop()
```

### API Reference

**Constructor:**
```python
TreeEditFrame(master, combo_choices=None, editable=True)
```
- `master`: Parent Tkinter widget
- `combo_choices` (optional): Dict mapping field names to lists of valid choices
- `editable` (optional): Enable/disable editing mode (default: True)

**Methods:**
- `set_data(data, root_name="root")` - Load Python object into tree
- `get_data()` - Extract Python object from tree
- `set_combo_choices(combo_choices)` - Update combo choices dictionary
- `set_editable(editable)` - Enable/disable editing mode dynamically
- `expand_tree(expand=True)` - Expand/collapse all tree nodes

## JSON Editor Example

The [json_editor_example.py](json_editor_example.py) demonstrates how to use TreeEditFrame to build a complete JSON file editor with load/save functionality.

### Running the Example

```bash
python json_editor_example.py
```

### Example Features

- Load JSON files via file dialog
- Save edited JSON with proper indentation
- Demonstrates combo choices for field-specific dropdowns (see "pattern" field in [example.json](example.json))
- Expand/collapse buttons for tree navigation

### Combo Choices

The example demonstrates how to configure dropdown choices for specific fields. In [json_editor_example.py](json_editor_example.py), combo choices are defined as:

```python
combo_choices = {
    "pattern": ["PRBS7", "PRBS31", "fast-clock", "slow-clock"]
}
```

When editing a field named "pattern", a dropdown will appear with these predefined choices instead of a text entry field.

## Installation

### For Users

```bash
# Install from PyPI (when published)
pip install tree-edit-frame

# Or install from source
git clone https://github.com/munich-ml/tkinter_json_editor.git
cd tkinter_json_editor
pip install .
```

### For Development

```bash
# Clone the repository
git clone https://github.com/munich-ml/tkinter_json_editor.git
cd tkinter_json_editor

# Install in editable mode (changes to code take effect immediately)
uv pip install -e .
# Or with regular pip:
# pip install -e .

# Run the example
python examples/json_editor_example.py
```

## Architecture

TreeEditFrame is a **headless component** - it provides the tree editing UI but does NOT handle file I/O. You control how data is loaded and saved, making it reusable for any hierarchical data source.

## Use Cases

TreeEditFrame can be used for editing any hierarchical data structure:
- JSON configuration files
- YAML config editors
- XML data viewers
- Application settings interfaces
- Test result viewers
- API response explorers
- Database record editors

## Requirements

- Python 3.x with tkinter (standard library - no additional dependencies)

## References

This project is inspired by:
- [PyJSONViewer](https://github.com/AtsushiSakai/PyJSONViewer) - well programmed but viewing only
- [tkinter-json-editor](https://github.com/zargit/tkinter-json-editor) - includes cell editing
- [ttk.Treeview with Entry widget for cell editing](https://www.youtube.com/watch?v=n5gItcGgIkk)
