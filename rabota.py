import tkinter
from tkinter import *
from tkinter import messagebox
from datetime import date
from tkinter.ttk import Combobox
from tkcalendar import DateEntry, Calendar
import sqlite3 as sq
import subprocess


background = "#06283D"
framebg = "#EDEDED"
framefg = "#06283D"


def clear():
    DOW.set('')
    Name.set('')
    Product.set('')
    Quantity.set('')

def next():
    Prod = Product.get()
    Prod = Prod[1:-1]
    global Tipe_of_work
    with sq.connect('work_db.db') as con:
        cur = con.cursor()
        cur.execute(f"SELECT type_of_work FROM product WHERE product = '{Prod}'")
        tipe_of_work = cur.fetchall()
        tipe_of_work.sort()
    Label(root, text="Вид работы", font='arial 10').place(x=875, y=25)
    Tipe_of_work = Combobox(root, values=tipe_of_work, font='Roboto 10', width=40, state='r')
    Tipe_of_work.place(x=745, y=50)
    Tipe_of_work.set('Вид работы')

def save():
    DC = Date.get()
    DT = DOW.get()
    N = Name.get()
    P = Product.get()
    P = P[1:-1]
    try:
        T = Tipe_of_work.get()
        T = T[1:-1]
    except:
        messagebox.showerror('Ошибка', "Не все данные внесены")
    Q = Quantity.get()
    if DC=='' or DT=='' or N=='Имя' or P=='Название изделия' or T=='' or Q=='':
        messagebox.showerror('Ошибка', "Не все данные внесены")
    else:
        with sq.connect('work_db.db') as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO rabota (date_create, date_todo, name, product, type_of_work, quantity) VALUES ('{DC}','{DT}','{N}','{P}','{T}','{Q}')")
            cur.execute(f"UPDATE product SET quantity = quantity - {Q} WHERE product = '{P}' AND type_of_work = '{T}'")

        messagebox.showinfo('info','Все данные сохранены')

        clear()

def incoming():
    DC = Date.get()
    DT = DOW.get()
    P = Product.get()
    P = P[1:-1]
    Q = Quantity.get()

    if DC=='' or DT=='' or P=='Название изделия' or Q=='':
        messagebox.showerror('Ошибка', "Не все данные внесены")
    else:
        with sq.connect('work_db.db') as con:
            cur = con.cursor()
            cur.execute(f"INSERT INTO rabota (date_create, date_todo, product, incoming) VALUES ('{DC}','{DT}','{P}','{Q}')")
            cur.execute(f"UPDATE product SET quantity = quantity + {Q} WHERE product = '{P}'")

        messagebox.showinfo('info', 'Все данные сохранены')

        clear()

def root1():
    subprocess.call(['py', 'C:\Python\RabotaUchet\otchet.py'])

def root2():
    subprocess.call(['py', 'C:\Python\RabotaUchet\otchet1.py'])

root = Tk()
root.title("Учет работы")
root.geometry('1250x700+2+2')
root.config(bg=background)

Label(root, text='EMail: rudevgeny@gmail.com', width=5, height=1, bg=framebg, anchor='e').pack(side=TOP, fill=X)

######Ввод выполненой работы#####

Label(root, text='Дата записи', font='arial 10').place(x=13, y=25)
Date = StringVar()
today = date.today()
d1 = today.strftime("%d/%m/%Y")
date_entry = Entry(root, textvariable=Date, width=9, font="arial 12")
date_entry.place(x=10, y=50)
Date.set(d1)

Label(root, text="Дата выполнения", font='arial 10').place(x=118, y=25)
# DOW = StringVar()
# dow_entry = Entry(root, textvariable=DOW, width=9, font="arial 12")
# dow_entry.place(x=130, y=50)
DOW = StringVar()
DE = DateEntry(root,textvariable=DOW, font='arial 10', date_pattern='YYYY/mm/dd').place(x=120,y=50)

Label(root, text="Имя работника", font='arial 10').place(x=256, y=25)
with sq.connect('work_db.db') as con:
    cur = con.cursor()
    cur.execute(f"SELECT name FROM workers")
    name = cur.fetchall()
Name = Combobox(root, values=name, font='Roboto 10', width=12, state='r')
Name.place(x=250, y=50)
Name.set('Имя')

Label(root, text="Название изделия", font='arial 10').place(x=460, y=25)
with sq.connect('work_db.db') as con:
    cur = con.cursor()
    cur.execute(f"SELECT product FROM product")
    product = cur.fetchall()
    product[:] = list(set(product))
    product.sort()
Product = Combobox(root, values=product, font='Roboto 10', width=40, state='r')
Product.place(x=378, y=50)
Product.set('Название изделия')

Button(root,text='NEXT',width=4,height=1,font='arial 10 bold',bg='lightblue',command=next).place(x=692,y=47)

Label(root, text="Кол-во", font='arial 10').place(x=1082, y=25)
Quantity = StringVar()
dow_entry = Entry(root, textvariable=Quantity, width=9, font="arial 12")
dow_entry.place(x=1065, y=50)

Button(root,text='Сохранить',width=9,height=2,font='arial 10 bold',bg='lightblue',command=save).place(x=1161,y=33)

#####ВВод приходов#####

Button(root,text='Приход',width=9,height=2,font='arial 10 bold',bg='lightblue',command=incoming).place(x=1161,y=85)

Button(root,text='З/П',width=9,height=2,font='arial 10 bold',bg='lightblue',command=root1).place(x=1161,y=180)

Button(root,text='Приходы',width=9,height=2,font='arial 10 bold',bg='lightblue',command=root2).place(x=900,y=180)





root.mainloop()