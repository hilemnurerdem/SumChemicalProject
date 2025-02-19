import tkinter as tk
from tkinter import ttk
window = tk.Tk()
window.title('Grid')
window.geometry('500x500')

label1 = ttk.Label(window, text='Label 1 ', background='red')
label2 = ttk.Label(window, text='Label 2 ', background='blue')
label3 = ttk.Label(window, text='Label 3 ', background='green')
label4 = ttk.Label(window, text='Label 4 ', background='yellow')
button1 = ttk.Button(window, test='Button 1 ')
button2 = ttk.Button(window, test='Button 2 ')

entry = ttk.Entry(window)

window.columnconfigure((0,1,2), weigth = 1)
window.columnconfigure(3, weigth = 1)
window.columnconfigure(4, weigth = 1)

label1.grid(row = 0, column = 0, sticky = 'e')
label2.grid(row = 0, column = 1, sticky = 'w')

window.mainloop()





