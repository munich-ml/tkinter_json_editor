# Tkinter JSON Editor
The idea is to load JSON content into a Tkinter GUI for viewing and editing. JSON files can by used for all kind of configurations and data (such as test results). Therefore a JSON Editor can be a versatile building block for Tkinter GUI applications.

# Editor1
Editor1 fullfils already most requirements and looks as follows:

![Editor1](Editor1/Editor1.png)

## References
Editor1 is inspired by:
- [PyJSONViewer](https://github.com/AtsushiSakai/PyJSONViewer), well programmed but viewing only.
- [tkinter-json-editor](https://github.com/zargit/tkinter-json-editor), includes cell editing, though awkward 
- [ttk.Treeview with Entry widgit for cell editing](https://www.youtube.com/watch?v=n5gItcGgIkk) 

## Pros - what Editor1 can do
- The __tree__ (`Tkinter.Treeview`) is build from the Python object upon `load JSON file`.
- Vice versa, upon `save JSON file` the JSON is reconstructed from the __tree__. 
- By double clicking any tree cell an editing widget is placed on top of the cell. The exact widget and behaviour depends on the `type` of the field or value:

  cell type | widget                    | function 
  --------- | ------------------------- | ----------------------------------------------  
  `str`     | `Tkinter.ttk.Entry`       | basic text entry
  `int`     | `Tkinter.ttk.Entry`       | value take over only if entry can be typecased
  `float`   | `Tkinter.ttk.Entry`       | value take over only if entry can be typecased
  `bool`    | `Tkinter.ttk.Checkbutton` | 
  `str`     | `Tkinter.ttk.Combobox`    | Coices according to `combo.choice.json` file
  
  The last list item brings up a __Combobox__ if a field name is present as key in the `combo.choice.json` file:
  ```JSON
  {"pattern": ["PRBS7", "PRBS31", "fast-clock", "slow-clock"]}
  ```

## Cons - why there is Editor2
Interacting with the __Combobox__ is no fun, because the `<FocusOut> Event` doesn't work as expected. The strange behaviour is discussed within
https://stackoverflow.com/questions/66145976/behavior-of-focusout-event-of-ttk-combobox without having a solution - just a workaround which leads to Editor2.

# Editor2

