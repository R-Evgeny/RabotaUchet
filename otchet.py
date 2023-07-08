import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import sqlite3 as sq


table1 = tkinter.Tk()
table1.title("Учет работы1")
table1.geometry('1250x700+30+30')
table1.config(bg="#06283D")

def next1():

    for widget in obj.winfo_children():
        widget.destroy()

    SD = start_date.get()
    ED = end_date.get()
    N = Name.get()

    with sq.connect('work_db.db') as con:
        global zp
        cur = con.cursor()
        cur.execute(
            f'SELECT date_todo, name, rabota.product, rabota.type_of_work, rabota.quantity, price FROM rabota '
            f'JOIN product ON rabota.product=product.product AND rabota.type_of_work=product.type_of_work AND '
            f'name="{N}" AND date_todo BETWEEN "{SD}" AND "{ED}"')
        search_items = cur.fetchall()
        print(len(search_items))
        zp = 0
        for search_item in search_items:
            summ = float(search_item[-2] * float(search_item[-1]))
            z = float("%.2f" % summ)
            zp += z
        Label(table1, text=f'{zp}', width=18, font='arial 25').place(x=25, y=25)

    heads = ['date_todo', 'name', 'product', 'type_of_work', 'quantity', 'price']
    table = tkinter.ttk.Treeview(obj, show='headings')
    table['columns'] = heads

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')

    for row in search_items:
        table.insert('', tkinter.END, values=row)

    table.pack(expand=tkinter.YES, fill=tkinter.BOTH)

obj = LabelFrame(table1, text="Отчет ЗП")
obj.place(x=25, y=100, width=1200, height=570)



Label(table1, text="Дата начала периода", font='arial 10').place(x=400, y=25)
start_date = StringVar()
DE1 = DateEntry(table1, textvariable=start_date, font='arial 10', date_pattern='YYYY/mm/dd').place(x=400, y=50)

Label(table1, text="Дата окончания периода", font='arial 10').place(x=600, y=25)
end_date = StringVar()
DE2 = DateEntry(table1, textvariable=end_date, font='arial 10', date_pattern='YYYY/mm/dd').place(x=600, y=50)

Label(table1, text="Имя работника", font='arial 10').place(x=800, y=25)
with sq.connect('work_db.db') as con:
    cur = con.cursor()
    cur.execute(f"SELECT name FROM workers")
    name = cur.fetchall()
Name = Combobox(table1, values=name, font='Roboto 10', width=12, state='r')
Name.place(x=800, y=50)
Name.set('Имя')

Button(table1, text='NEXT', width=5, height=1, font='arial 15 bold', bg='lightblue', command=next1).place(x=1000, y=28)






table1.mainloop()

