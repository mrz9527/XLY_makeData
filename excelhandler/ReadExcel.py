# -*- coding: utf-8 -*-
import xlrd
from mathhandler import MathUtils


class ReadExcel():
    def __init__(self, filepath):
        self.filepath = filepath

    def open_workbook(self):
        self.workbook = xlrd.open_workbook(self.filepath)

    def get_sheet_by_index(self, index=0):
        self.sheet = self.workbook.sheet_by_index(index)

    def get_sheet_by_name(self, name="sheet"):
        self.sheet = self.workbook.sheet_by_name(name)

    def get_cell_value(self, row: int, col: int):
        """

        :param row: 从0开始
        :param col: 从0开始
        :return:
        """
        return self.sheet.cell_value(row, col)

    def get_cell_value(self, cell_coord: list):
        return self.sheet.cell_value(cell_coord[0], cell_coord[1])

    def get_row_count(self):
        row_count = self.sheet.nrows
        return row_count

    def get_col_count(self):
        col_count = self.sheet.ncols
        return col_count

    @staticmethod
    def from_col_name_to_col_index(col_name):  # col_index从0开始
        col_index = 0
        for i, j in enumerate(col_name[::-1]):
            col_index += (ord(j) - ord('A') + 1) * 26 ** i

        col_index = col_index - 1

        return col_index

    @staticmethod
    def from_col_index_to_col_name(col_index):
        indexs = MathUtils.MathUtils.dec_to(26, col_index)
        index_str = ReadExcel.indexs_to_str(indexs)
        return index_str

    @staticmethod
    def indexs_to_str(indexs: list):
        """
        给定索引号和索引地图，找到对应的字符串
        :param indexs:
        :param index_map:
        :return:
        """

        index_map = [chr(ord('A') + i) for i in range(26)]
        res = ""

        len_indexs = len(indexs)
        for i in range(len_indexs):
            index = indexs[i]
            ch = index_map[index]
            if i < len_indexs - 1:
                ch = chr(ord(ch) - 1)  # 关键点: -1
            res = res + ch

        return res
