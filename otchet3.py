import tkinter
from tkinter import *
from tkinter.ttk import Combobox
import sqlite3 as sq


table3 = tkinter.Tk()
table3.title("Изменение названий и цен")
table3.geometry('800x250+50+50')
table3.config(bg='#06283D')

def next1():
    global Prod

    Prod = Product.get()
    Prod = Prod[1:-1]
    global Tipe_of_work
    with sq.connect('uchet_rabot.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT type_of_work FROM product WHERE product = '{Prod}'")
        tipe_of_work = cur.fetchall()
        tipe_of_work.sort()
    Label(table3, text="Вид работы", font='arial 10').place(x=500, y=25)
    Tipe_of_work = Combobox(table3, values=tipe_of_work, font='Roboto 10', width=40, state='r')
    Tipe_of_work.place(x=400, y=50)
    Tipe_of_work.set('Вид работы')

def next2():
    global prod
    global tipe_o
    global pri
    global TOW_old
    P = Product.get()
    P = P[1:-1]
    TOW_old = Tipe_of_work.get()
    TOW_old = TOW_old[1:-1]

    prod = StringVar()
    entry_product = Entry(table3, textvariable=prod, width=50)
    entry_product.pack(pady=20, )
    entry_product.place(x=30, y=100)
    prod.set(P)

    tipe_o = StringVar()
    entry_type_of_work = Entry(table3,textvariable=tipe_o, width=50)
    entry_type_of_work.pack(pady=20, )
    entry_type_of_work.place(x=400, y=100)
    tipe_o.set(TOW_old)

    with sq.connect('uchet_rabot.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT price FROM product WHERE product = '{P}' AND type_of_work = '{TOW_old}'")
        price = cur.fetchall()

    pri = StringVar()
    entry_price = Entry(table3, textvariable=pri, width=10)
    entry_price.pack(pady=10, )
    entry_price.place(x=720, y=100)
    pri.set(price)

def next3():
    P = prod.get()          #Новое название продукта
    TOW = tipe_o.get()      #Новое название типа работы
    TOW_o = TOW_old         #Старое название типа работы
    Pri = pri.get()         #Новая цена
    PO = Prod               #Старое название продукта
    with sq.connect('uchet_rabot.db') as con:
        cur = con.cursor()
        cur.execute(f"UPDATE product SET product = '{P}' WHERE product = '{PO}'")
        cur.execute(f"UPDATE product SET type_of_work = '{TOW}' WHERE product = '{P}' AND type_of_work = '{TOW_o}'")
        cur.execute(f"UPDATE product SET price = '{Pri}' WHERE product = '{P}' AND type_of_work = '{TOW}'")
        cur.execute(f"UPDATE rabota SET product = '{P}' WHERE product = '{PO}'")
        cur.execute(f"UPDATE rabota SET type_of_work = '{TOW}' WHERE product = '{P}' AND type_of_work = '{TOW_o}'")

Label(table3, text="Название изделия", font='arial 10').place(x=100, y=25)
with sq.connect('uchet_rabot.db') as con:
    cur = con.cursor()
    cur.execute(f"SELECT product FROM product")
    product = cur.fetchall()
    product[:] = list(set(product))
    product.sort()
Product = Combobox(table3, values=product, font='Roboto 10', width=40, state='r')
Product.place(x=30, y=50)
Product.set('Название изделия')

Button(table3,text='>>>>',width=4,height=1,font='arial 10 bold',bg='lightblue',command=next1).place(x=340,y=45)

Button(table3,text='NEXT',width=4,height=1,font='arial 10 bold',bg='lightblue',command=next2).place(x=720,y=45)

Button(table3,text='Сохранить изменения',width=20,height=1,font='arial 20 bold',bg='lightblue',command=next3).place(x=200,y=150)

table3.mainloop()