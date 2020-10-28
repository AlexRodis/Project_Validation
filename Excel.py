from openpyxl import load_workbook
from collections import namedtuple


def get_analytes(workbook=None):
    wb = load_workbook(workbook)
    ws = wb.active
    this = [x[0] for x in ws.iter_rows(min_col=3, max_col=3, min_row=2, values_only=True)]
    return this


def get_areas(workbook = None, method = None):
    P = namedtuple("AnalyteValue", "Analyte,Area,Method")
    wb = load_workbook(workbook)
    ws = wb.active
    return [ P(Analyte=x[0],Area=x[7], Method = method) for x in ws.iter_rows(min_col =3, max_col=10, min_row=2, values_only = True) ]
