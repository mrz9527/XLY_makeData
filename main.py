import PlotCurve
import ReadExcel
import ParamCalculate

import MakePts

import matplotlib.pyplot as plt


def OneProcess(sheet, labelCell, Xcell, Ycell, rowCount, xdt34=7.0, xdt45=7.0, xt7=48.0, xdt7=0.5, xt1=-50.0, xt4=-6.3,
               m35=2, m56=0.4):
    # 读取X、Y坐标和标签label
    label, X, Y = ReadExcel.ReadXY(sheet, labelCell, Xcell, Ycell, rowCount)

    # 设置t1~t6、dt4
    Xt, m35, m56 = ParamCalculate.SetConfig(xdt34, xdt45, xt7, xdt7, xt1, xt4, m35, m56)

    # 计算关键点坐标信息
    Index, Xt, Yt, k23, k56, xdt12 = ParamCalculate.CalculateKeyPt(X, Y, Xt, m35, m56)

    # 打印关键点坐标信息
    ParamCalculate.PrintOut_CalculateKeyPt(Index, Xt, Yt, k23, k56)

    # 计算横坐标间距和基准百分比
    intervalx = ParamCalculate.GetInterval(Xt[7], Xt[6], Index[7], Index[6])
    # 打印横坐标间距和基准百分比
    ParamCalculate.PrintOut_GetInterval(intervalx)

    # 计算l67
    l67_pts = MakePts.calc_l67_pts(Index, X, Y)

    # 计算l56
    # 基于已有数据来造数据，已有数据曲线上，只有l12和l56(可能没有，或者只有一部分数据曲线）和l67
    # 所以基于已有数据,l12的t2的index2，和l56(部分曲线数据）的t5的index5相等
    l_5_to_5half_pts, l_5half_to_6_pts, l56_bezier_pts = MakePts.calc_l56_pts(Index, X, Y, Xt, k56, intervalx)

    # 计算l35贝塞尔曲线上的数据
    pt3 = [Xt[3], Yt[3]]
    pt5 = l_5_to_5half_pts[0]
    l35_pts = MakePts.calc_l35_pts(pt3, pt5, k23, intervalx)

    # 计算l23曲线上的数据
    l23_pts = MakePts.calc_l23_pts(Xt, Yt, l35_pts[0], k23, intervalx)

    # 计算l12曲线上的数据
    l12_ctl_pt3 = l23_pts[0]
    l1_1half_pts, l12_bezier_pts = MakePts.calc_l12_pts_ex(Xt, Yt, X, Y, Index, k23, l12_ctl_pt3, intervalx)

    # 所有曲线
    l_pts = []
    l_pts.extend(l1_1half_pts)
    l_pts.extend(l12_bezier_pts)
    l_pts.extend(l23_pts)
    l_pts.extend(l35_pts)
    l_pts.extend(l_5_to_5half_pts)
    l_pts.extend(l56_bezier_pts)
    l_pts.extend(l_5half_to_6_pts)
    l_pts.extend(l67_pts)

    return l_pts, label, X, Y


def GetRowColInfo():
    # 给出数据文件路径
    dataFilePath = "data.xlsx"
    # 获取workbook
    workbook = ReadExcel.GetWorkbook(dataFilePath)
    # 获取sheet
    sheet = ReadExcel.GetSheet(workbook, 0)
    # 获取行列数
    rowCount, colCount = ReadExcel.GetRowColCountFromSheet(sheet)

    # 给出label单元格坐标，起始x单元格坐标，起始y单元格坐标
    labelCellRow = [5, 5, 5, 5, 5]
    labelCellColStr = ['F', 'H', 'J', 'L', 'N']

    ptCellXRow = [7, 7, 7, 7, 7]
    ptCellXColStr = labelCellColStr

    ptCellYRow = ptCellXRow
    ptCellYColStr = [chr(ord(char) + 1) for char in labelCellColStr]

    labelCells = []
    ptCellXs = []
    ptCellYs = []

    for i in range(len(labelCellRow)):
        labelCell = [labelCellRow[i] - 1, ReadExcel.GetColNumberByColName(labelCellColStr[i]) - 1]
        ptCellX = [ptCellXRow[i] - 1, ReadExcel.GetColNumberByColName(ptCellXColStr[i]) - 1]
        ptCellY = [ptCellYRow[i] - 1, ReadExcel.GetColNumberByColName(ptCellYColStr[i]) - 1]

        labelCells.append(labelCell)
        ptCellXs.append(ptCellX)
        ptCellYs.append(ptCellY)

    return sheet, rowCount, labelCells, ptCellXs, ptCellYs

def Process():
    # # 给出数据文件路径
    # dataFilePath = "data.xlsx"
    # # 获取workbook
    # workbook = ReadExcel.GetWorkbook(dataFilePath)
    # # 获取sheet
    # sheet = ReadExcel.GetSheet(workbook, 0)
    # # 获取行列数
    # rowCount, colCount = ReadExcel.GetRowColCountFromSheet(sheet)
    #
    # # 给出label单元格坐标，起始x单元格坐标，起始y单元格坐标
    # labelCellRow = [5, 5, 5, 5, 5]
    # labelCellColStr = ['F', 'H', 'J', 'L', 'N']
    #
    # PtCellXRow = [7, 7, 7, 7, 7]
    # PtCellXColStr = labelCellColStr
    #
    # PtCellYRow = PtCellXRow
    # PtCellYColStr = [chr(ord(char) + 1) for char in labelCellColStr]
    #
    # Xcell = [6, 5]
    # Ycell = [6, 6]

    sheet, rowCount, labelCells, ptCellXs, ptCellYs = GetRowColInfo()

    # Xt4 = [-6.3, xxxxxxx]
    Xt4 = [-8.6, -32.3, -15.6, -15.4, -6.3]
    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777"] # "#00FFFF", "#00334455", "#7722FF"

    legends = []

    # 遍历5条曲线
    for i in range(len(labelCells)):
        labelCell = labelCells[i]
        Xcell = ptCellXs[i]
        Ycell = ptCellYs[i]
        xt4 = Xt4[i]
        color = colors[i]

        l_pts, label, X, Y = OneProcess(sheet, labelCell, Xcell, Ycell, rowCount, xdt34=7.0, xdt45=7.0, xt7=48.0, xdt7=0.5,
                                  xt1=-50.0, xt4=-6.3, m35=2, m56=0.4)

        legends.append(label)
        if i == 0:
            PlotCurve.DrawCurve(l_pts, color)
        # plt.plot(X, Y)

    plt.legend(legends)
    PlotCurve.Show()


if __name__ == '__main__':
    Process()
