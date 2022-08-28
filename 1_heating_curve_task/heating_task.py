import PlotCurve
from excelhandler.readexcel import ReadExcel
from excelhandler.writeexcel import WriteExcel
import common
import heating_curve_calc


def get_excel_config():
    """
    获取label单元格坐标、起始x的单元格坐标，起始y的单元格坐标
        excel中单元格，行从1开始，列从A开始。单元格坐标（行从0开始，列从0开始）
    :return:
    """
    # 给出label单元格坐标，起始x单元格坐标，起始y单元格坐标
    label_cell_rows = [5, 5, 5, 5, 5]
    label_cell_col_names = ['F', 'H', 'J', 'L', 'N']

    startx_cell_rows = [7, 7, 7, 7, 7]
    startx_cell_col_names = label_cell_col_names

    starty_cell_rows = startx_cell_rows
    starty_cell_col_names = [chr(ord(char) + 1) for char in label_cell_col_names]

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

    Xt4 = [-8.6, -32.3, -15.6, -15.4, -6.3]
    Xt7 = [48, 48, 48, 48, 48]

    Xdt34 = [7.0, 7.0, 7.0, 7.0, 7.0]
    Xdt45 = [7.0, 7.0, 7.0, 7.0, 7.0]
    Xdt7 = [0.5, 0.5, 0.5, 0.5, 0.5]
    Xt1 = [-50.0, -50.0, -50.0, -50.0, -50.0]
    M35 = [8, 4, 8, 4, 8]
    M56 = [0.4, 0.2, 0.2, 0.2, 0.2]

    curve_params = []
    Xts = []
    count = len(Xt4)
    for i in range(count):
        xdt34 = Xdt34[i]
        xdt45 = Xdt45[i]
        xdt7 = Xdt7[i]
        xt1 = Xt1[i]
        m35 = M35[i]
        m56 = M56[i]

        xt4 = Xt4[i]
        xt7 = Xt7[i]

        xt6 = xt7 - xdt7

        xt3 = xt4 - xdt34
        xt5 = xt4 + xdt45

        if xt5 >= xt6:
            xdt45 = 1 / 3 * (xt6 - xt4)
            xt5 = xt4 + xdt45

        curve_param = [xt4, xt7, xdt34, xdt45, xdt7, xt1, m35, m56, xt6, xt3, xt5]
        Xt = [0, xt1, 0, xt3, xt4, xt5, xt6, xt7]

        curve_params.append(curve_param)
        Xts.append(Xt)

    return curve_params, Xts


def curve_process(X, Y, curve_param, Xt):
    xt4, xt7, xdt34, xdt45, xdt7, xt1, m35, m56, xt6, xt3, xt5 = curve_param

    # 计算关键点坐标信息
    Index, Xt, Yt, k23, k56, xdt12 = heating_curve_calc.calc_import_pts(X, Y, Xt, m35, m56)

    # 打印关键点坐标信息
    # ParamCalculate.PrintOut_CalculateKeyPt(Index, Xt, Yt, k23, k56)

    # 计算横坐标间距和基准百分比
    intervalx = common.GetInterval(Xt[7], Xt[6], Index[7], Index[6])

    # 计算l67
    l67_pts = heating_curve_calc.calc_l67_pts(Index, X, Y)

    # 计算l56
    # 基于已有数据来造数据，已有数据曲线上，只有l12和l56(可能没有，或者只有一部分数据曲线）和l67
    # 所以基于已有数据,l12的t2的index2，和l56(部分曲线数据）的t5的index5相等
    l_5_to_5half_pts, l_5half_to_6_pts, l56_bezier_pts = heating_curve_calc.calc_l56_pts(Index, X, Y, Xt, k56, intervalx)

    # 计算l35贝塞尔曲线上的数据
    pt3 = [Xt[3], Yt[3]]
    pt5 = l_5_to_5half_pts[0]
    l35_pts = heating_curve_calc.calc_l35_pts(pt3, pt5, k23, intervalx)

    # 计算l23曲线上的数据
    l23_pts = heating_curve_calc.calc_l23_pts(Xt, Yt, l35_pts[0], k23, intervalx)

    # 计算l12曲线上的数据
    l12_ctl_pt3 = l23_pts[0]
    l1_1half_pts, l12_bezier_pts = heating_curve_calc.calc_l12_pts(Xt, Yt, X, Y, Index, k23, l12_ctl_pt3, intervalx)

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

    return l_pts, Xt, Yt


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
    startx_cell_coordx = startx_cell_coord[0]
    x_cell_coordy = startx_cell_coord[1]
    y_cell_coordy = starty_cell_coord[1]

    pt_count = len(curve)
    for pt_index in range(pt_count):
        pt_x = curve[pt_index][0]
        pt_y = curve[pt_index][1]

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

    pass


def plot_curves(curves, colors, label_names):
    # 绘制5条曲线
    curve_count = len(curves)
    for i in range(curve_count):
        curve = curves[i]
        color = colors[i]
        PlotCurve.DrawCurve(curve, color)

    # 设置图例
    PlotCurve.legend(label_names)

    # 显示曲线
    PlotCurve.Show()


def main_process():
    # 设置excel文件
    filepath = "1_heating_curve_task.xlsx"

    # 获取excel基本配置信息
    label_cell_coords, startx_cell_coords, starty_cell_coords = get_excel_config()

    # 提取excel中5条曲线坐标轨迹
    label_names, curves = read_data(filepath, label_cell_coords, startx_cell_coords, starty_cell_coords)

    # 获取曲线的参数配置
    curve_params, Xts = get_curve_param_config()

    new_curves = []

    # 遍历并处理5条曲线
    curve_count = len(curves)
    for i in range(curve_count):
        X = curves[i][0]
        Y = curves[i][1]
        curve_param = curve_params[i]
        Xt = Xts[i]

        new_curve, Xt, Yt = curve_process(X, Y, curve_param, Xt)

        new_curves.append(new_curve)

    save_filepath = "new_" + filepath
    save_data(save_filepath, label_cell_coords, label_names, startx_cell_coords, starty_cell_coords, new_curves)

    # 绘制并显示5条曲线
    colors = ["#000000", "#FF0000", "#00FF00", "#0000FF", "#777777"]
    plot_curves(new_curves, colors, label_names)


if __name__ == '__main__':
    print("1_heating_curve_task")
    main_process()
