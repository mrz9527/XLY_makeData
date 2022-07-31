import PlotCurve
import ReadExcel
import ParamCalculate

import MakePts


def SetConfig(xdt34=4.0, xdt45=4.0, xt7=47.0, xdt7=3.0, xt1=-50.0, xt2=-41.0, xt4=-6.3, m=2):
    xdt12 = xt2 - xt1
    xt3 = xt4 - xdt34
    xt5 = xt4 + xdt45
    xt6 = xt7 - xdt7

    Xt = [0, xt1, xt2, xt3, xt4, xt5, xt6, xt7]

    return Xt, m, xdt12


def Process():
    # 给出数据文件路径
    dataFilePath = "data.xlsx"
    # 获取workbook
    workbook = ReadExcel.GetWorkbook(dataFilePath)
    # 获取sheet
    sheet = ReadExcel.GetSheet(workbook, 0)
    # 获取行列数
    rowCount, colCount = ReadExcel.GetRowColCountFromSheet(sheet)

    # 给出label单元格坐标，起始x单元格坐标，起始y单元格坐标
    labelCell = [4, 5]
    Xcell = [6, 5]
    Ycell = [6, 6]

    # 读取X、Y坐标和标签label
    label, X, Y = ReadExcel.ReadXY(sheet, labelCell, Xcell, Ycell, rowCount)
    # 打印坐标
    # PrintXY(X, Y)

    # 设置t1~t6、dt4
    Xt, m, xdt12 = SetConfig(xdt34=4.0, xdt45=4.0, xt7=47.0, xdt7=3.0, xt1=-50.0, xt2=-41.0, xt4=-6.3, m=2)

    # 计算关键点坐标信息
    Index, Yt, k23, k56 = ParamCalculate.CalculateKeyPt(X, Y, Xt, m)
    # 打印关键点坐标信息
    ParamCalculate.PrintOut_CalculateKeyPt(Index, Xt, Yt, k23, k56)

    # 计算横坐标间距和基准百分比
    intervalx, scale = ParamCalculate.GetIntervalAndScale(Xt[7], Xt[6], Index[7], Index[6])
    # 打印横坐标间距和基准百分比
    ParamCalculate.PrintOut_GetIntervalAndScale(intervalx, scale)

    # 计算l67
    l67_pts = MakePts.calc_l67_pts(Index, X, Y)
    print(f"l67_pts 计算完成, len_67:{len(l67_pts)}")

    # 计算l56
    # 基于已有数据来造数据，已有数据曲线上，只有l12和l56(可能没有，或者只有一部分数据曲线）和l67
    # 所以基于已有数据,l12的t2的index2，和l56(部分曲线数据）的t5的index5相等
    l56_pts = MakePts.calc_l56_pts(Index, X, Y, Xt, k56, intervalx)
    print(f"l56_pts 计算完成, len_56:{len(l56_pts)}")

    # 计算l35贝塞尔曲线上的数据
    l35_pts = MakePts.calc_l35_pts(Xt, Yt, k23, scale)
    print(f"l35_pts 计算完成, len_35:{len(l35_pts)}")

    # 计算l23曲线上的数据
    l23_pts = MakePts.calc_l23_pts(Xt, Yt, k23, intervalx)

    # 计算l12曲线上的数据
    l12_pts = MakePts.calc_l12_pts(Xt, Yt, X, Y, Index)

    # # 所有曲线
    # l_pts = []
    # for pt in l12_pts:
    #     l_pts.append(pt)
    #
    # for pt in l23_pts:
    #     l_pts.append(pt)
    #
    # for pt in l35_pts:
    #     l_pts.append(pt)
    #
    # for pt in l56_pts:
    #     l_pts.append(pt)
    #
    # for pt in l67_pts:
    #     l_pts.append(pt)
    #
    # # PlotCurve.DrawCurve(l_pts, "#054E9F")


    lines = [l12_pts, l23_pts, l35_pts, l56_pts, l67_pts]
    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#00FFFF"]
    PlotCurve.DrawMultiCurve(lines, colors)
    PlotCurve.Show()

    # # 打印边界值看看
    # print("边界值:")
    # print(f"l67_pt6:{l67_pts[0][0]},{l67_pts[0][1]}")
    # len_l56 = len(l56_pts)
    # print(f"l56_pt6:{l56_pts[len_l56 - 1][0]},{l67_pts[len_l56 - 1][1]}")
    #
    # print(f"xt6,yt6:{Xt[6]},{Yt[6]}")
    #
    # print(f"l56_pt5:{l56_pts[0][0]},{l67_pts[0][1]}")
    # len_l35 = len(l35_pts)
    # print(f"l35_pt5:{l35_pts[len_l35 - 1][0]},{l35_pts[len_l35 - 1][1]}")
    #
    # print(f"xt5,yt5:{Xt[5]},{Yt[5]}")
    #
    # print(f"l35_pt3:{l35_pts[0][0]},{l35_pts[0][1]}")


if __name__ == '__main__':
    Process()
