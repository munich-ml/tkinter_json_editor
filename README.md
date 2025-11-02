# Tkinter JSON Editor

A versatile Tkinter GUI application for viewing and editing JSON files. JSON files can be used for all kinds of configurations and data (such as test results), making this editor a useful building block for Tkinter GUI applications.

## Features

- Load and save JSON files with a graphical tree view
- Edit values directly by double-clicking cells or pressing Enter
- Type-aware editing with appropriate widgets for each data type:

  | Data Type | Widget | Behavior |
  |-----------|--------|----------|
  | `str` | `ttk.Entry` | Basic text entry |
  | `int` | `ttk.Entry` | Value accepted only if it can be typecast to integer |
  | `float` | `ttk.Entry` | Value accepted only if it can be typecast to float |
  | `bool` | `ttk.Checkbutton` | Toggle between True/False |
  | `str` with choices | `ttk.Combobox` | Dropdown selection from predefined choices |

- Combobox choices are configured via `combo_choice.json`. For example:
  ```json
  {"pattern": ["PRBS7", "PRBS31", "fast-clock", "slow-clock"]}
  ```
- Expand/collapse tree view for better navigation
- Keyboard navigation support

## Usage

Run the editor:
```bash
python json_editor.py
```

## References

This project is inspired by:
- [PyJSONViewer](https://github.com/AtsushiSakai/PyJSONViewer) - well programmed but viewing only
- [tkinter-json-editor](https://github.com/zargit/tkinter-json-editor) - includes cell editing
- [ttk.Treeview with Entry widget for cell editing](https://www.youtube.com/watch?v=n5gItcGgIkk)
