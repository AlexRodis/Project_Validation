from openpyxl import load_workbook
import os


def get_analytes(workbook=None):
    wb = load_workbook(workbook)
    ws = wb.active
    return [x[0] for x in ws.iter_rows(min_col=3, max_col=3, min_row=2, values_only=True)]

# os.chdir(r'H:\Pesticides Honey\Results\GC\Method Validation\Excel Exports')
# workbook = os.listdir()[1]
# print(get_analytes(workbook=workbook))
