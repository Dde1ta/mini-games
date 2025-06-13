



root = tk.Tk()
root.geometry("1800x1000+0+0")

frame = tk.Frame(root,height = 1000, width = 1800)
frame.pack()

main = Main(frame,1000,1800)

root.mainloop()