import tkinter as tk

import click

root = tk.Tk()
root.title("Hilem Nur Erdem")
root.geometry("800x800")
#root.configure(bg="white")  # Arka plan pastel yeşili

root.columnconfigure((0,1,2,3,4,5,6,7,8,9,10), weight = 1)
root.rowconfigure((0,1,2,3,4,5,6,7,8,9,10), weight = 1)

label = tk.Label(root, text="HOŞ GELDİNİZZZ!!!", font=("Arial", 14, "bold"))
label.grid(row = 3, column = 5, sticky = 'sn')

label1 = tk.Label(root,text="Kullanıcı adı:",  font=("Arial", 12))
label1.grid(row=4,column=5, sticky='s')
entry1 = tk.Entry(root)
entry1.grid(row=4, column=6)

label2 = tk.Label(root,text="Şifre:",  font=("Arial", 12))
label2.grid(row=5,column=5, sticky='s')
entry2 = tk.Entry(root)
entry2.grid(row=5, column=6)

def giris_kontrol():
    username = entry1.get()
    password = entry2.get()
    print(f"Kullanıcı Adı: {username}, Şifre: {password}")

login_button = tk.Button(root, text="Giriş", command=giris_kontrol, font=("Arial", 12))
login_button.grid(row=6, column=5, columnspan=2, pady=10)

root.mainloop()

root1 = tk.Tk()

label = tk.Label(root1, text="Lütfen yapmak istediğiniz işlemi seçiniz...")
label.grid()
root1.mainloop()





