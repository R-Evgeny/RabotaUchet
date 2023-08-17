import tkinter
from tkinter import *
from tkinter.ttk import Combobox
from tkcalendar import DateEntry
import sqlite3 as sq


table2 = tkinter.Tk()
table2.title("Отчет по изделию")
table2.geometry('1250x700+50+50')
table2.config(bg='#06283D')


def next1():

    for widget in obj.winfo_children():
        widget.destroy()

    P = Product.get()
    P = P[1:-1]
    SD = start_date.get()
    ED = end_date.get()
    #print(P)
    with sq.connect('uchet_rabot.db') as con:
        cur = con.cursor()
        cur.execute(f'SELECT date_todo, name, product, type_of_work, quantity, incoming FROM rabota '
                    f'WHERE product = "{P}" AND date_todo BETWEEN "{SD}" AND "{ED}" ORDER BY type_of_work')
        search_items = cur.fetchall()
        incoming_item = 0
        incoming_quantity = 0
        for item in search_items:
            incoming = item[-1]
            quantity = item[-2]
            try:
                incoming_item += int(incoming)
            except:
                incoming_quantity += int(quantity)

        print(search_items)
        print(len(search_items))
        Label(table2, text=f'{incoming_item}', font='arial 15').place(x=950, y=35)
        Label(table2, text=f'{incoming_quantity}', font='arial 15').place(x=1100, y=35)

    heads = ['date_todo', 'name', 'product', 'type_of_work', 'quantity', 'incoming']
    table = tkinter.ttk.Treeview(obj, show='headings')
    table['columns'] = heads

    for header in heads:
        table.heading(header, text=header, anchor='center')
        table.column(header, anchor='center')

    for row in search_items:
        table.insert('', tkinter.END, values=row)

    table.pack(expand=tkinter.YES, fill=tkinter.BOTH)

obj = LabelFrame(table2, text="Отчет по изделию")
obj.place(x=25, y=100, width=1200, height=570)

Label(table2, text="Дата начала периода", font='arial 10').place(x=400, y=25)
start_date = StringVar()
DE1 = DateEntry(table2, textvariable=start_date, font='arial 10', date_pattern='YYYY/mm/dd').place(x=400, y=50)

Label(table2, text="Дата окончания периода", font='arial 10').place(x=600, y=25)
end_date = StringVar()
DE2 = DateEntry(table2, textvariable=end_date, font='arial 10', date_pattern='YYYY/mm/dd').place(x=600, y=50)

Label(table2, text="Изделие", font='arial 10').place(x=50, y=25)
with sq.connect('uchet_rabot.db') as con:
    cur = con.cursor()
    cur.execute(f"SELECT product FROM product")
    product = cur.fetchall()
    product[:] = list(set(product))
    product.sort()
Product = Combobox(table2, values=product, font='Roboto 10', width=40, state='r')
Product.place(x=50, y=50)
Product.set('Изделие')

Button(table2, text='NEXT', width=5, height=1, font='arial 15 bold', bg='lightblue', command=next1).place(x=800, y=28)










table2.mainloop()