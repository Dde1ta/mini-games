import tkinter as tk

root = tk.Tk()

l1 = tk.Label(root, text="Hover over me",
              width=40, bd=2, relief="groove",
              background="lightblue")
l2 = tk.Label(root)
l1.pack(side="top", fill="x", padx=10, pady=10)
l2.pack(side="top", fill="both", expand=True)

def handle_enter(event):

    event.widget.configure(background="pink")
    l2.configure(text="you entered the widget")

def handle_leave(event):

    event.widget.configure(background="lightblue")
    l2.configure(text="")

l1.bind("<Enter>", handle_enter)
l1.bind("<Leave>", handle_leave)

root.mainloop()
