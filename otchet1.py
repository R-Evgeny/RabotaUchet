import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import sqlite3 as sq


table2 = tkinter.Tk()
table2.title("Приходы")
table2.geometry('1250x700+50+50')
table2.config(bg="#06283D")

def next2():

    for widget in obj2.winfo_children():
        widget.destroy()

    SD = start_date.get()
    ED = end_date.get()

    with sq.connect('uchet_rabot.db') as con:
        cur = con.cursor()
        cur.execute(
            f'SELECT date_todo, product, incoming FROM rabota WHERE incoming BETWEEN "1" AND "100000" AND date_todo BETWEEN "{SD}" AND "{ED}"')
        search_items = cur.fetchall()

    heads = ['date_todo', 'product', 'incoming']
    table = tkinter.ttk.Treeview(obj2, show='headings')
    table['columns'] = heads

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')

    for row in search_items:
        table.insert('', tkinter.END, values=row)

    table.pack(expand=tkinter.YES, fill=tkinter.BOTH)

obj2 = LabelFrame(table2, text="Отчет -Приходы-")
obj2.place(x=25, y=100, width=1200, height=570)



Label(table2, text="Дата начала периода", font='arial 10').place(x=300, y=25)
start_date = StringVar()
DE1 = DateEntry(table2, textvariable=start_date, font='arial 10', date_pattern='YYYY/mm/dd').place(x=300, y=50)

Label(table2, text="Дата окончания периода", font='arial 10').place(x=600, y=25)
end_date = StringVar()
DE2 = DateEntry(table2, textvariable=end_date, font='arial 10', date_pattern='YYYY/mm/dd').place(x=600, y=50)


Button(table2, text='NEXT', width=5, height=1, font='arial 15 bold', bg='lightblue', command=next2).place(x=1000, y=28)






table2.mainloop()

