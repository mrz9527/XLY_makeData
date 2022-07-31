# -*- coding: utf-8 -*-
import xlrd

def PrintXY(X, Y):
    for index in range(len(X)):
        print(f" {index}. ({X[index]}, {Y[index]})")


def GetWorkbook(dataFilePath: str):
    workbook = xlrd.open_workbook(dataFilePath)
    return workbook


# 获取sheet
def GetSheet(workbook: xlrd.book.Book, index):
    sheet = workbook.sheet_by_index(index)
    return sheet


# 获取sheet的行列数
def GetRowColCountFromSheet(sheet: xlrd.sheet.Sheet):
    rowCount = sheet.nrows
    colCount = sheet.ncols
    return rowCount, colCount


## 从指定sheet的第Xcell个单元格开始，竖直读x坐标，从第Ycell个单元格开始，竖着读y坐标
def ReadXY(sheet: xlrd.sheet.Sheet, labelCell: list, Xcell, Ycell, rowCount):
    label = sheet.cell_value(labelCell[0], labelCell[1])

    X = []
    Y = []

    sRow = Xcell[0]
    xCol = Xcell[1]
    yCol = Ycell[1]
    for rowIndex in range(sRow, rowCount):
        x = sheet.cell_value(rowIndex, xCol)
        y = sheet.cell_value(rowIndex, yCol)
        X.append(x)
        Y.append(y)
    return label, X, Y