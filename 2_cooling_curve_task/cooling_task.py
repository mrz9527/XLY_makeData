import copy

import PlotCurve
from excelhandler.readexcel import ReadExcel
from excelhandler.writeexcel import WriteExcel
import common
from pltplot.pltplot import PltPlot
import matplotlib.pyplot as plt
import cooling_curve_calc


def get_excel_config():
    """
    获取label单元格坐标、起始x的单元格坐标，起始y的单元格坐标
        excel中单元格，行从1开始，列从A开始。单元格坐标（行从0开始，列从0开始）
    :return:
    """
    # 给出label单元格坐标，起始x单元格坐标，起始y单元格坐标
    label_cell_rows = [5, 5, 5, 5, 5]
    label_cell_col_names = ['B', 'D', 'F', 'H', 'J']

    startx_cell_rows = [6, 6, 6, 6, 6]
    startx_cell_col_names = [chr(ord(char) - 1) for char in label_cell_col_names]

    starty_cell_rows = startx_cell_rows
    starty_cell_col_names = label_cell_col_names

    label_cell_coords = []
    startx_cell_coords = []
    starty_cell_coords = []

    for i in range(len(label_cell_col_names)):
        label_cell_coord = [label_cell_rows[i] - 1, ReadExcel.from_col_name_to_col_index(label_cell_col_names[i])]
        startx_cell_coord = [startx_cell_rows[i] - 1,
                             ReadExcel.from_col_name_to_col_index(startx_cell_col_names[i])]
        starty_cell_coord = [starty_cell_rows[i] - 1,
                             ReadExcel.from_col_name_to_col_index(starty_cell_col_names[i])]

        label_cell_coords.append(label_cell_coord)
        startx_cell_coords.append(startx_cell_coord)
        starty_cell_coords.append(starty_cell_coord)

    return label_cell_coords, startx_cell_coords, starty_cell_coords


def get_curve_param_config():  # 预配置数据信息
    # 10, 21, 22, 23, 24
    # 因为曲线的横坐标是从高到低画的，所以x的坐标递减
    Xt0 = [31.0, 31.0, 31.0, 31.0, 31.0]
    Xdt0 = [3.0, 3.0, 3.0, 3.0, 3.0]
    Xt3 = [-8.6, -32.3, -15.6, -15.4, -6.3]
    Xdt32 = [9.0, 7.0, 7.0, 7.0, 7.0]
    Xdt34 = [29.0, 7.0, 7.0, 29.0, 7.0]
    Xt5 = [-50.0, -50.0, -50.0, -50.0, -50.0]
    M12 = [1.0, 1.0, 1.0, 1.0, 1.0]
    M45 = [1.0, 1.0, 1.0, 10.0, 1.0]
    M24 = [-100.0, 150.0, 170.0, -40.0, -40.0]

    curve_num = len(Xt0)

    Xt1 = [Xt0[i] - Xdt0[i] for i in range(curve_num)]
    Xt2 = [Xt3[i] + Xdt32[i] for i in range(curve_num)]
    Xt4 = [Xt3[i] - Xdt34[i] for i in range(curve_num)]

    # for l24 参数，l24用两段bezier曲线拼接
    # bezier1: p0, p1, p2
    # bezier2: p2, p3, p4, p5
    L24_scale1 = [0.3, 0.2, 0.2, 0.2, 0.2]  # p1.x = p0.x + (p3.x - p0.x) * L24_scale1
    L24_scale2 = [0.1, 0.5, 0.5, 0.5, 0.5]  # p2.x = p3.x - (p3.x - p0.x) * L24_scale2
    # L24_ctlPt[i][0]为高度(p1.y - p4.y)百分比。p2.y = p1.y - (p1.y - p4.y) * L24_ctlPt[i][0]
    # L24_ctlPt[i][1]为(p1.y - p2.y)的百分比。 p2.x = p1.x + (p1.y - p2.y) * L24_ctlPt[i][1]
    L24_ctlPt = [[0.2, 0.5], [0.2, 0.1], [0.2, 0.1], [0.2, 0.3], [0.2, 0.1]]

    curve_params = []
    Xts = []

    for i in range(curve_num):
        xt0 = Xt0[i]
        xt1 = Xt1[i]
        xt2 = Xt2[i]
        xt3 = Xt3[i]
        xt4 = Xt4[i]
        xt5 = Xt5[i]

        xdt0 = Xdt0[i]
        xdt32 = Xdt32[i]
        xdt34 = Xdt34[i]

        m12 = M12[i]
        m45 = M45[i]
        m24 = M24[i]

        Xt1 = [Xt0[i] - Xdt0[i] for i in range(curve_num)]
        Xt2 = [Xt3[i] + Xdt32[i] for i in range(curve_num)]
        Xt4 = [Xt3[i] - Xdt34[i] for i in range(curve_num)]

        # 检测xt2是否合理
        if xt2 >= xt1:
            xdt32 = 1 / 3 * (xt1 - xt3)
            xt2 = xt3 + xdt32

        # 检测xt4是否合理
        if xt4 <= xt5:
            xdt34 = 1 / 3 * (xt3 - xt5)
            xt4 = xt3 - xdt34

        curve_param = [xdt0, xdt32, xdt34, m12, m24, m45]
        Xt = [xt0, xt1, xt2, xt3, xt4, xt5]

        curve_params.append(curve_param)
        Xts.append(Xt)

    L24_params = []
    for i in range(curve_num):
        l24_scale1 = L24_scale1[i]
        l24_scale2 = L24_scale2[i]
        l24_ctlPt = L24_ctlPt[i]
        l24_param = [l24_scale1, l24_scale2, l24_ctlPt]
        L24_params.append(l24_param)

    return curve_params, Xts, L24_params


def curve_process(X, Y, curve_param, Xt, l24_param):
    xdt0, xdt32, xdt34, m12, m24, m45 = curve_param
    xt0, xt1, xt2, xt3, xt4, xt5 = Xt

    # 计算关键点坐标信息
    Xt, Yt, curve_param, Index, K = cooling_curve_calc.calc_import_pts(X, Y, curve_param, Xt)

    # 计算横坐标间距和基准百分比
    intervalx = common.GetInterval(Xt[0], Xt[1], Index[0], Index[1])

    # 计算l01
    l01_pts = cooling_curve_calc.calc_l01_pts(Index, X, Y)

    # 计算l12
    l12_pts = cooling_curve_calc.calc_l12_pts(curve_param, Xt, Yt, K, intervalx)

    # 计算l24
    # l24_pts = cooling_curve_calc.calc_l24_pts(l12_pts, Xt, Yt, K)
    l24_pts = cooling_curve_calc.calc_l24_pts_ext(l12_pts, Xt, Yt, K, l24_param)

    # 计算l45
    l45_pts = cooling_curve_calc.calc_l45_pts(Xt, Yt, curve_param, K, intervalx)

    l_pts = cooling_curve_calc.merge(l01_pts, l12_pts, l24_pts, l45_pts)

    new_X = [pt[0] for pt in l_pts]
    new_Y = [pt[1] for pt in l_pts]
    curve = [new_X, new_Y]

    return curve


def read_pt(read_excel: ReadExcel, x_cell_coord: list, y_cell_coord: list):
    x = read_excel.get_cell_value(x_cell_coord)
    y = read_excel.get_cell_value(y_cell_coord)
    if type(x) == str:
        if x == "":
            return None
        else:
            x = float(x)
    if type(y) == str:
        if y == "":
            return None
        else:
            y = float(y)

    return [x, y]


# , , startx_cell_coord, starty_cell_coord, row_count
## 从指定sheet的第Xcell个单元格开始，竖直读x坐标，从第Ycell个单元格开始，竖着读y坐标
def read_curve_data(read_excel: ReadExcel, label_cell_coord: list, startx_cell_coord, starty_cell_coord, row_count):
    label_name = read_excel.get_cell_value(label_cell_coord)

    X = []
    Y = []

    startx_cell_coordx = startx_cell_coord[0]
    x_cell_coordy = startx_cell_coord[1]
    y_cell_coordy = starty_cell_coord[1]
    for cell_coordx in range(startx_cell_coordx, row_count):
        x_cell_coord = [cell_coordx, x_cell_coordy]
        y_cell_coord = [cell_coordx, y_cell_coordy]
        xy = read_pt(read_excel, x_cell_coord, y_cell_coord)
        if xy == None:
            continue

        X.append(xy[0])
        Y.append(xy[1])

    return label_name, X, Y


def read_data(filepath, label_cell_coords, startx_cell_coords, starty_cell_coords):
    # 获取workbook、sheet、row_count
    read_excel = ReadExcel(filepath)
    read_excel.open_workbook()
    read_excel.get_sheet_by_index(0)
    row_count = read_excel.get_row_count()

    # 读取曲线的label和曲线的坐标轨迹
    label_names = []
    curves = []
    curve_count = len(label_cell_coords)
    for i in range(curve_count):
        label_cell_coord = label_cell_coords[i]
        startx_cell_coord = startx_cell_coords[i]
        starty_cell_coord = starty_cell_coords[i]

        label, X, Y = read_curve_data(read_excel, label_cell_coord, startx_cell_coord, starty_cell_coord, row_count)
        curve = [X, Y]

        label_names.append(label)
        curves.append(curve)

    return label_names, curves


def save_label_data(write_excel: WriteExcel, label_cell_coord, label_name):
    write_excel.set_cell_value(row=label_cell_coord[0], col=label_cell_coord[1], value=label_name)


def save_curve_data(write_excel: WriteExcel, startx_cell_coord, starty_cell_coord, curve: list):
    startx_cell_coordx = startx_cell_coord[0] + 1
    x_cell_coordy = startx_cell_coord[1] + 1
    y_cell_coordy = starty_cell_coord[1] + 1

    pt_count = len(curve[0])
    for pt_index in range(pt_count):
        pt_x = curve[0][pt_index]
        pt_y = curve[1][pt_index]

        cell_coordx = pt_index + startx_cell_coordx
        write_excel.set_cell_value(cell_coordx, x_cell_coordy, pt_x)
        write_excel.set_cell_value(cell_coordx, y_cell_coordy, pt_y)


def save_data(filepath, label_cell_coords, label_names, startx_cell_coords, starty_cell_coords, curves):
    # 构建WriteExcel
    write_excel = WriteExcel(filepath)
    write_excel.open_workbook()
    write_excel.create_sheet("new sheet")

    curve_count = len(curves)
    for i in range(curve_count):
        save_label_data(write_excel=write_excel, label_cell_coord=label_cell_coords[i], label_name=label_names[i])
        save_curve_data(write_excel=write_excel, startx_cell_coord=startx_cell_coords[i],
                        starty_cell_coord=starty_cell_coords[i], curve=curves[i])

    write_excel.save()


def plot_curves(curves, colors, label_names):
    # 绘制5条曲线
    curve_count = len(curves)

    for i in range(curve_count):
        curve = curves[i]
        color = colors[i]
        PltPlot.plt_plot(curve[0], curve[1], color=color)

    # 设置图例
    PlotCurve.legend(label_names)

    plt.gca().invert_xaxis()  # 用于反转x轴

    # 显示曲线
    PlotCurve.Show()


def main_process():
    # 设置excel文件
    filepath = "2_cooling_curve_task.xlsx"

    # 获取excel基本配置信息
    label_cell_coords, startx_cell_coords, starty_cell_coords = get_excel_config()

    # 提取excel中5条曲线坐标轨迹
    label_names, curves = read_data(filepath, label_cell_coords, startx_cell_coords, starty_cell_coords)

    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777"]

    # plot_curves(curves, colors, label_names)

    # 获取曲线的参数配置
    curve_params, Xts, L24_params = get_curve_param_config()

    new_curves = []

    # 遍历并处理5条曲线
    curve_count = len(curves)
    for i in range(curve_count):
        X = curves[i][0]
        Y = curves[i][1]
        curve_param = curve_params[i]
        Xt = Xts[i]
        l24_param = L24_params[i]

        new_curve = curve_process(X, Y, curve_param, Xt, l24_param)

        new_curves.append(new_curve)

    # 绘制并显示5条曲线
    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777"]
    plot_curves(new_curves, colors, label_names)

    save_filepath = "new_" + filepath
    save_data(save_filepath, label_cell_coords, label_names, startx_cell_coords, starty_cell_coords, new_curves)


if __name__ == '__main__':
    print("2_cooling_curve_task")
    main_process()
