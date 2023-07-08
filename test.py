import sqlite3 as sq
import openpyxl
import tqdm

# with sq.connect('work_db.db') as con:
#     cur = con.cursor()
#     cur.execute(f'SELECT date_todo, name, rabota.product, rabota.type_of_work, rabota.quantity, price FROM rabota JOIN product ON rabota.product=product.product AND rabota.type_of_work=product.type_of_work  AND name="Лена"')
#     items = cur.fetchall()
#     zp = 0
#     for item in items:
#         try:
#             summa = float(item[-2]) * float(item[-1])
#             zp += summa
#         except:
#             print(item)
#     print(zp)


# with sq.connect('work_db.db') as con:
#     cur = con.cursor()
#
#     book = openpyxl.open('import_price.xlsx', read_only=True)
#     sheet = book.active
#     for row in range(1, sheet.max_row + 1):
#         product = str(sheet[row][0].value)
#         type_of_work = str(sheet[row][1].value)
#         price = str(sheet[row][2].value)
#         cur.execute(f"UPDATE product SET price = {price} WHERE product = '{product}' AND type_of_work = '{type_of_work}'")

with sq.connect('work_db.db') as con:
    cur = con.cursor()

    book = openpyxl.open(r'123.xlsx', read_only=True)
    sheet = book.active
    for row in range(1, sheet.max_row + 1):
        date_create = str(sheet[row][0].value)
        date_todo = str(sheet[row][1].value)
        name = str(sheet[row][2].value)
        product = str(sheet[row][3].value)
        type_of_work = str(sheet[row][4].value)
        quantity = str(sheet[row][5].value)
        incoming = str(sheet[row][6].value)
        cur.execute(f"INSERT INTO rabota VALUES ('{date_create}','{date_todo}','{name}','{product}','{type_of_work}','{quantity}','{incoming}')")