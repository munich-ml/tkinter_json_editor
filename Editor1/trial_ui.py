import tkinter as tk
import tkinter.ttk as ttk

app = tk.Tk()
tk.Button(app, text="print hi", command=lambda: print("hi")).pack()

box = ttk.Combobox(app, values=["January", "February", "March", "April"])
box.current(1)
box.bind("<<ComboboxSelected>>", lambda e: print(e.widget.get()))
box.pack()    

app.geometry("200x100")
app.mainloop()
