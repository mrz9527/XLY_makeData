import BazelCurve
import PlotCurve
import ReadExcel
import ParamCalculate

import MakePts


def OneProcess(X, Y, xdt34=7.0, xdt45=7.0, xt7=48.0, xdt7=0.5, xt1=-50.0, xt4=-6.3, m35=2, m56=0.4):
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

    # print(f"l1_1half_pts = ({l1_1half_pts[0][0]},{l1_1half_pts[0][1]}), ({l1_1half_pts[-1][0]},{l1_1half_pts[-1][1]})")
    # print(
    #     f"l12_bezier_pts = ({l12_bezier_pts[0][0]},{l12_bezier_pts[0][1]}), ({l12_bezier_pts[-1][0]},{l12_bezier_pts[-1][1]})")
    # print(f"l23_pts = ({l23_pts[0][0]},{l23_pts[0][1]}), ({l23_pts[-1][0]},{l23_pts[-1][1]})")
    # print(f"l35_pts = ({l35_pts[0][0]},{l35_pts[0][1]}), ({l35_pts[-1][0]},{l35_pts[-1][1]})")
    # print(
    #     f"l_5_to_5half_pts = ({l_5_to_5half_pts[0][0]},{l_5_to_5half_pts[0][1]}), ({l_5_to_5half_pts[-1][0]},{l_5_to_5half_pts[-1][1]})")
    # print(
    #     f"l56_bezier_pts = ({l56_bezier_pts[0][0]},{l56_bezier_pts[0][1]}), ({l56_bezier_pts[-1][0]},{l56_bezier_pts[-1][1]})")
    # print(
    #     f"l_5half_to_6_pts = ({l_5half_to_6_pts[0][0]},{l_5half_to_6_pts[0][1]}), ({l_5half_to_6_pts[-1][0]},{l_5half_to_6_pts[-1][1]})")
    # print(f"l67_pts = ({l67_pts[0][0]},{l67_pts[0][1]}), ({l67_pts[-1][0]},{l67_pts[-1][1]})")
    #
    # print(f"Xt = {Xt}")

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

    PlotCurve.DrawCurve(l_pts, "#556677")

    # lines = [l1_1half_pts, l12_bezier_pts, l23_pts, l35_pts, l_5_to_5half_pts, l56_bezier_pts, l_5half_to_6_pts,
    #          l67_pts]
    # linecolors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777", "#00FFFF", "#00334455", "#7722FF"]
    # PlotCurve.DrawMultiCurve(lines, linecolors)
    PlotCurve.Show()


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

    # 设置t1~t6、dt4
    Xt, m35, m56 = ParamCalculate.SetConfig(xdt34=7.0, xdt45=7.0, xt7=48.0, xdt7=0.5, xt1=-50.0, xt4=-6.3, m35=2,
                                            m56=0.4)

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

    print(f"l1_1half_pts = ({l1_1half_pts[0][0]},{l1_1half_pts[0][1]}), ({l1_1half_pts[-1][0]},{l1_1half_pts[-1][1]})")
    print(
        f"l12_bezier_pts = ({l12_bezier_pts[0][0]},{l12_bezier_pts[0][1]}), ({l12_bezier_pts[-1][0]},{l12_bezier_pts[-1][1]})")
    print(f"l23_pts = ({l23_pts[0][0]},{l23_pts[0][1]}), ({l23_pts[-1][0]},{l23_pts[-1][1]})")
    print(f"l35_pts = ({l35_pts[0][0]},{l35_pts[0][1]}), ({l35_pts[-1][0]},{l35_pts[-1][1]})")
    print(
        f"l_5_to_5half_pts = ({l_5_to_5half_pts[0][0]},{l_5_to_5half_pts[0][1]}), ({l_5_to_5half_pts[-1][0]},{l_5_to_5half_pts[-1][1]})")
    print(
        f"l56_bezier_pts = ({l56_bezier_pts[0][0]},{l56_bezier_pts[0][1]}), ({l56_bezier_pts[-1][0]},{l56_bezier_pts[-1][1]})")
    print(
        f"l_5half_to_6_pts = ({l_5half_to_6_pts[0][0]},{l_5half_to_6_pts[0][1]}), ({l_5half_to_6_pts[-1][0]},{l_5half_to_6_pts[-1][1]})")
    print(f"l67_pts = ({l67_pts[0][0]},{l67_pts[0][1]}), ({l67_pts[-1][0]},{l67_pts[-1][1]})")

    print(f"Xt = {Xt}")

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

    PlotCurve.DrawCurve(l_pts, "#556677")

    # lines = [l1_1half_pts, l12_bezier_pts, l23_pts, l35_pts, l_5_to_5half_pts, l56_bezier_pts, l_5half_to_6_pts,
    #          l67_pts]
    # linecolors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777", "#00FFFF", "#00334455", "#7722FF"]
    # PlotCurve.DrawMultiCurve(lines, linecolors)
    PlotCurve.Show()


if __name__ == '__main__':
    Process()
