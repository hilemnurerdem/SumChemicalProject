import pyodbc
import tkinter as tk
from tkinter import ttk
from datetime import datetime

# 🔹 SQL Server bağlantısını kur
try:
    conn = pyodbc.connect(
        "DRIVER={ODBC Driver 17 for SQL Server};"
        "SERVER=Your_Server;"
        "DATABASE=Your_Database;"
        "UID=Your_Name;"
        "PWD=Your_Password;"               #Buradaki bilgilerin değişmesi gerek.
    )
    cursor = conn.cursor()
    print("✅ SQL Server bağlantısı başarılı!")
except Exception as e:
    print(f"❌ SQL Bağlantı Hatası: {e}")
    exit()

# 🔹 Tkinter ana pencereyi oluştur
root = tk.Tk()
root.title("ProcessHistories & ProcessParameters Viewer")
root.geometry("1000x600")

# 🔹 İş Emirlerini (WorkOrder) getir
try:
    cursor.execute("SELECT DISTINCT WorkOrder FROM ProcessHistories;")
    workorders = [str(row[0]) for row in cursor.fetchall()]
    print(f"🔍 İş Emirleri Yüklendi: {workorders}")
except Exception as e:
    print(f"❌ İş Emri Çekme Hatası: {e}")
    workorders = []

# 🔹 İş Emri seçme alanı
workorder_label = tk.Label(root, text="İş Emri Seç:")
workorder_label.pack(pady=5)
workorder_combo = ttk.Combobox(root, values=workorders)
workorder_combo.pack(pady=5)

# 🔹 ProcessHistories tablosunu görüntülemek için Treeview
tree_histories = ttk.Treeview(root, columns=("id", "WorkOrder", "Step", "StartTime", "EndTime"), show="headings")
tree_histories.heading("id", text="ID")
tree_histories.heading("WorkOrder", text="WorkOrder")
tree_histories.heading("Step", text="Step")
tree_histories.heading("StartTime", text="Start Time")
tree_histories.heading("EndTime", text="End Time")
tree_histories.pack(pady=10)

# 🔹 ProcessParameters tablosunu görüntülemek için Treeview
tree_parameters = ttk.Treeview(root, columns=("id", "Time", "PmTemperature", "PmWeight"), show="headings")
tree_parameters.heading("id", text="ID")
tree_parameters.heading("Time", text="Time")
tree_parameters.heading("PmTemperature", text="Pm Temperature")
tree_parameters.heading("PmWeight", text="Pm Weight")
tree_parameters.pack(pady=10)


# 🔹 İş Emrini Getir
def get_process_histories():
    selected_workorder = workorder_combo.get()
    if not selected_workorder:
        print("⚠️ İş emri seçilmedi!")
        return

    tree_histories.delete(*tree_histories.get_children())

    query = "SELECT id, WorkOrder, Step, StartTime, EndTime FROM ProcessHistories WHERE WorkOrder = ?;"

    try:
        cursor.execute(query, (selected_workorder,))
        rows = cursor.fetchall()
        print(f"📌 İş Emri Seçildi: {selected_workorder}")
        if not rows:
            print("❌ Hiç veri bulunamadı.")

        for row in rows:
            formatted_start = row[3].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[3], datetime) else row[3]
            formatted_end = row[4].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[4], datetime) else row[4]

            print(f"✅ ProcessHistories Verisi: {row[0]}, {row[1]}, {row[2]}, {formatted_start}, {formatted_end}")
            tree_histories.insert("", "end", values=(row[0], row[1], row[2], formatted_start, formatted_end))

    except Exception as e:
        print(f"❌ ProcessHistories Sorgu Hatası: {e}")


# 🔹 Seçilen Satırın StartTime ve EndTime Değerine Göre ProcessParameters Getir
def get_process_parameters(event):
    selected_item = tree_histories.selection()
    if not selected_item:
        print("⚠️ Tablo'dan satır seçilmedi!")
        return

    item = tree_histories.item(selected_item)["values"]
    if not item:
        print("⚠️ Seçilen satırda değer yok!")
        return

    start_time_str = item[3]  # StartTime sütunu
    end_time_str = item[4]  # EndTime sütunu

    try:
        # 🕒 Tarih formatlarını standart hale getir
        start_time = datetime.strptime(start_time_str, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.strptime(end_time_str, "%Y-%m-%d %H:%M:%S")

        # 🔹 SQL Server için string formatına dönüştür
        start_time_sql = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_sql = end_time.strftime('%Y-%m-%d %H:%M:%S')

        print(f"🎯 Seçilen StartTime: {start_time_sql}, EndTime: {end_time_sql}")
        print(f"🔍 Arama Yapılan Aralık: {start_time_sql} - {end_time_sql}")

        tree_parameters.delete(*tree_parameters.get_children())

        query = """
            SELECT id, Time, PmTemperature, PmWeight 
            FROM ProcessParameters 
            WHERE Time BETWEEN ? AND ?;
        """

        cursor.execute(query, (start_time_sql, end_time_sql))
        rows = cursor.fetchall()

        print(f"✅ Bulunan Satır Sayısı: {len(rows)}")
        if not rows:
            print("❌ Bu tarih aralığında veri yok!")

        for row in rows:
            formatted_time = row[1].strftime('%Y-%m-%d %H:%M:%S') if isinstance(row[1], datetime) else row[1]
            print(f"📊 ProcessParameters Verisi: {row[0]}, {formatted_time}, {row[2]}, {row[3]}")
            tree_parameters.insert("", "end", values=(row[0], formatted_time, row[2], row[3]))

    except ValueError as ve:
        print(f"❌ Tarih formatı hatalı: {start_time_str} → {end_time_str}, Hata: {ve}")
    except Exception as e:
        print(f"❌ ProcessParameters Sorgu Hatası: {e}")


# 🔹 Buton ve event bağlama

get_histories_button = tk.Button(root, text="İş Emrini Getir", command=get_process_histories)
get_histories_button.pack(pady=5)

tree_histories.bind("<<TreeviewSelect>>", get_process_parameters)

# 🔹 Uygulamayı çalıştır
root.mainloop()

# 🔹 Bağlantıyı kapat
conn.close()
 