import BazelCurve
import PlotCurve
import ReadExcel
import ParamCalculate

import MakePts


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
    # Xt, m = ParamCalculate.SetConfig(xdt34=4.0, xdt45=4.0, xt7=47.0, xdt7=3.0, xt1=-50.0, xt4=-6.3, m=2)
    Xt, m35, m56 = ParamCalculate.SetConfig(xdt34=4.0, xdt45=4.0, xt7=48.0, xdt7=0.5, xt1=-50.0, xt4=-6.3, m35=2,
                                            m56=0.4)

    # 计算关键点坐标信息
    Index, Xt, Yt, k23, k56, xdt12 = ParamCalculate.CalculateKeyPt(X, Y, Xt, m35, m56)
    # Index, Yt, k23, k56 = ParamCalculate.CalculateKeyPt(X, Y, Xt, m)
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

    ctl_ptx3 = pt3[0] - (pt3[0] - Xt[2]) / 4
    ctl_pty3 = pt3[1] + k23 * (ctl_ptx3 - pt3[0])
    ctl_pt3 = [ctl_ptx3, ctl_pty3]
    # ctl_ptx3, pt3, l_5_to_5half_pts, k23, interval

    # l35_pts, l_5_to_5half_pts = MakePts.calc_l35_pts_ex(ctl_pt3, pt3, l_5_to_5half_pts, k23, intervalx)
    l35_pts = MakePts.calc_l35_pts(pt3, pt5, k23, intervalx)

    # 计算l23曲线上的数据
    # l23_pts = MakePts.calc_l23_pts(Xt, Yt, ctl_pt3, k23, intervalx)
    l23_pts = MakePts.calc_l23_pts(Xt, Yt, l35_pts[0], k23, intervalx)

    # 计算l12曲线上的数据
    l12_pts = MakePts.calc_l12_pts(Xt, Yt, X, Y, Index)

    print(f"l12: ({l12_pts[0][0]}, {l12_pts[-1][0]})")
    print(f"l23: ({l23_pts[0][0]}, {l23_pts[-1][0]})")

    print(f"l35: ({l35_pts[0][0]}, {l35_pts[-1][0]})")
    print(f"l_5_5.5: ({l_5_to_5half_pts[0][0]}, {l_5_to_5half_pts[-1][0]})")
    print(f"l_5.5_6: ({l_5half_to_6_pts[0][0]}, {l_5half_to_6_pts[-1][0]})")
    print(f"l67: ({l67_pts[0][0]}, {l67_pts[-1][0]})")

    print(f"Xt = {Xt}")
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
    # for pt in l_5_to_5half_pts:
    #     l_pts.append(pt)
    #
    # for pt in l_5half_to_6_pts:
    #     l_pts.append(pt)
    #
    # for pt in l67_pts:
    #     l_pts.append(pt)
    #
    # PlotCurve.DrawCurve(l_pts, "#054E9F")

    # src_pts = []
    # for i in range(len(X)):
    #     pt = [X[i], Y[i]]
    #     src_pts.append(pt)
    #
    # PlotCurve.DrawCurve(src_pts, "#556677")

    lines = [l12_pts, l23_pts, l35_pts, l_5_to_5half_pts, l56_bezier_pts, l_5half_to_6_pts, l67_pts]
    linecolors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777", "#00FFFF", "#00334455"]
    PlotCurve.DrawMultiCurve(lines, linecolors)

    # vlinecolors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#00FFFF", "#FF00FF", "#FFFF00"]
    # vlinelabels = ["t1", "t2", "t3", "t4", "t5", "t6", "t7"]
    # PlotCurve.DrawVlines(Xt[1:], [15, 35], vlinecolors, vlinelabels)
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


import matplotlib.pyplot as plt
import numpy as np


def TestBezier():
    k = 1.0
    sp = [5.0, 5.0]
    ep = [50.0, 100.0]

    x1 = np.linspace(-50.0, sp[0], 50)
    y1 = x1

    x2 = np.linspace(ep[0], 100.0, 50)
    y2 = x2 + 50.0
    plt.plot(x1, y1)
    plt.plot(x2, y2)

    bezier_insert_pts = MakePts.calc_l35_pts(sp, ep, k, 0.02)

    PlotCurve.DrawCurve(bezier_insert_pts, "red")
    PlotCurve.Show()


if __name__ == '__main__':
    Process()
