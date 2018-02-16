import xlwt, xlrd
from xlutils.copy import copy as xlcopy

source_filename = "all_base_gs1.xls"
destination_filename = "example_new.xls"

read_book = xlrd.open_workbook(source_filename, on_demand=True)  # Открываем исходный документ
worksheet = read_book.get_sheet(0)  # Читаем из первого листа
count = 0
while True:
    if worksheet.cell(count, 0).value == xlrd.empty_cell.value:
        break
    print(worksheet.row_values(count)[0])
    count += 1


write_book = xlcopy(read_book)  # Копируем таблицу в память, в неё мы ниже будем записывать
write_sheet = write_book.get_sheet(0)  # Будем записывать в первый лист
write_sheet.write(0, 0, worksheet.cell_value(0, 0) + 42)  # Прибавим к значению из ячейки "A1" число 42
write_book.save(destination_filename)  # Сохраняем таблицу