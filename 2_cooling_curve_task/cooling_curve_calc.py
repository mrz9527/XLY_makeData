# -*- coding: utf-8 -*-

from mathhandler.Bezier import Bezier
from mathhandler.MathUtils import MathUtils
import common


def calc_import_pts(X: list, Y: list, curve_param: list, Xt: list):
    xdt0, xdt32, xdt34, m12, m24, m45 = curve_param
    xt0, xt1, xt2, xt3, xt4, xt5 = Xt

    Yt = [0 for i in range(len(Xt))]  # 列表，记录Xt对应的纵坐标
    Index = [-1 for i in range(len(Xt))]

    K = [0 for i in range(len(Xt) - 1)]  # n个点，构成n-1条线段，有n-1条斜率

    # 计算xt0对应的索引Index[0]
    lastIndex = len(X) - 1
    for curIndex in range(lastIndex, -1, -1):
        if Xt[0] < X[curIndex]:
            Index[0] = curIndex
            break

    # 计算xt0对应的yt0 = Yt[0]
    Xt[0] = X[Index[0]]  # 更新Xt[0]，之前的Xt[0]是预设的或计算的，现在的Xt[0]是实际的
    Yt[0] = Y[Index[0]]

    # 计算xt1对应的索引Index[1]
    for curIndex in range(lastIndex, -1, -1):
        if Xt[1] < X[curIndex]:
            Index[1] = curIndex
            break

    # 计算xt1对应的yt1 = Yt[1]
    Xt[1] = X[Index[1]]  # 更新Xt[1]，之前的Xt[1]是预设的或计算的，现在的Xt[1]是实际的
    Yt[1] = Y[Index[1]]

    # 更新xdt0 = curve_param[0]
    curve_param[0] = Xt[0] - Xt[1]

    # 计算k01 = K[0]
    K[0] = (Yt[1] - Yt[0]) / (Xt[1] - Xt[0])
    # 计算k12
    K[1] = m12 * K[0]
    # 计算k24
    K[2] = m24 * K[1]
    K[3] = K[2]
    K[4] = m45 * K[0]

    return Xt, Yt, curve_param, Index, K


def calc_l01_pts(Index, X, Y):
    l01_pts = []

    t1_index = Index[1]

    for pt_index in range(0, t1_index + 1):
        pt = [X[pt_index], Y[pt_index]]
        l01_pts.append(pt)

    return l01_pts


def calc_l12_pts(curve_param: list, Xt: list, Yt: list, K: list, intervalx):
    l12_pts = []

    """
    y = k(x-xt1) + yt1. 区间[xt1, xt2]
    """
    xt1 = Xt[1]
    yt1 = Yt[1]

    xt2 = Xt[2]

    pt_count = (xt1 - xt2) / intervalx
    pt_count = int(pt_count) + 1

    for i in range(1, pt_count):
        x = xt1 - intervalx * i
        y = yt1 - K[0] * intervalx * i
        pt = [x, y]
        l12_pts.append(pt)

    # 更新xt2，yt2的值
    Xt[2] = l12_pts[-1][0]
    Yt[2] = l12_pts[-1][1]

    # 更新xdt32 = curve_param[1]
    curve_param[1] = Xt[2] - Xt[3]

    return l12_pts


def calc_l24_pts(l12_pts: list, Xt: list, Yt: list, K: list):
    Yt[4] = K[2] * (Xt[4] - Xt[2]) + Yt[2]
    start_pt = l12_pts[-1]
    end_pt = [Xt[4], Yt[4]]

    dx = end_pt[0] - start_pt[0]
    scale = 0.7

    # 控制点
    ctrl_pt1 = [start_pt[0] + dx * scale, 0]
    ctrl_pt2 = [end_pt[0] - dx * scale, 0]

    # ctrl_pt1Y = k12 * (ctrl_pt1X - start_pt[0]) + start_pt[1]
    ctrl_pt1[1] = K[1] * (ctrl_pt1[0] - start_pt[0]) + start_pt[1]

    # ctrl_pt2Y = K[4] * (ctrl_pt2X - end_pt[0]) + end_pt[1]
    ctrl_pt2[1] = K[4] * (ctrl_pt2[0] - end_pt[0]) + end_pt[1]

    # 更新起点和终点
    # new_startx = start_pt[0] - scale * dx
    # new_starty = K[1] * (new_startx - start_pt[0]) + start_pt[1]
    # new_start_pt = [new_startx, new_starty]
    #
    # new_endx = end_pt[0] + dx * scale
    # new_endy = K[4] * (new_endx - end_pt[0]) + end_pt[1]
    # new_end_pt = [new_endx, new_endy]
    #
    # bezier_pts = [new_start_pt, ctrl_pt1, ctrl_pt2, new_end_pt]

    bezier_pts = [start_pt, ctrl_pt1, ctrl_pt2, end_pt]

    interval = (l12_pts[-1][0] - l12_pts[0][0]) / len(l12_pts)
    scale = interval / (bezier_pts[-1][0] - bezier_pts[0][0]) / 2
    T = Bezier.get_bezier_T_by_scale(scale)

    bezier = Bezier(bezier_pts)
    l24_pts = bezier.get_bezier_pts(T)

    return l24_pts


def calc_l24_pts_ext(l12_pts: list, Xt: list, Yt: list, K: list, l24_param: list):
    l24_scale1, l24_scale2, l24_ctlPt = l24_param

    Yt[4] = K[2] * (Xt[4] - Xt[2]) + Yt[2]
    p0 = l12_pts[-1]
    p5 = [Xt[4], Yt[4]]

    dx = p5[0] - p0[0]
    dy = p5[1] - p0[1]

    # p1
    p1 = [p0[0] + dx * l24_scale1, 0]
    p1[1] = K[1] * (p1[0] - p0[0]) + p0[1]

    # p2
    # L24_ctlPt[i][0]为高度(p1.y - p4.y)百分比。p2.y = p1.y - (p1.y - p4.y) * L24_ctlPt[i][0]
    # L24_ctlPt[i][1]为(p1.y - p2.y)的百分比。 p2.x = p1.x + (p1.y - p2.y) * L24_ctlPt[i][1]
    p2 = [0, 0]
    p2[1] = p1[1] + dy * l24_ctlPt[0]
    p2[0] = p1[0] + (p2[1] - p1[1]) * l24_ctlPt[1]

    # bezier1
    bezier1_pts = [p0, p1, p2]

    # p3
    p3 = [0, 0]
    p3[0] = p2[0] + (p2[0] - p1[0]) * 1.5
    p3[1] = p2[1] + (p2[1] - p1[1]) * 1.5

    # p4
    p4 = [p5[0] - dx * l24_scale2, 0]
    p4[1] = K[4] * (p4[0] - p5[0]) + p5[1]

    # bezier2
    bezier2_pts = [p2, p3, p4, p5]

    interval = (l12_pts[-1][0] - l12_pts[0][0]) / len(l12_pts)

    scale1 = interval / (bezier1_pts[-1][0] - bezier1_pts[0][0]) / 2
    scale2 = interval / (bezier2_pts[-1][0] - bezier2_pts[0][0]) / 2

    T1 = Bezier.get_bezier_T_by_scale(scale1)
    T2 = Bezier.get_bezier_T_by_scale(scale2)

    bezier1 = Bezier(bezier1_pts)
    l24_pts_1 = bezier1.get_bezier_pts(T1)

    bezier2 = Bezier(bezier2_pts)
    l24_pts_2 = bezier2.get_bezier_pts(T2)

    l24_pts = []
    l24_pts.extend(l24_pts_1)
    l24_pts.extend(l24_pts_2)

    return l24_pts


def calc_l45_pts(Xt, Yt, curve_param, K, intervalx):
    l45_pts = []

    # y = k * (x - xt5) + yt5
    pt_count = (Xt[4] - Xt[5]) / intervalx
    pt_count = int(pt_count) + 1

    for i in range(1, pt_count):
        x = Xt[4] - intervalx * i
        y = Yt[4] + K[4] * intervalx * i
        pt = [x, y]
        l45_pts.append(pt)

    return l45_pts


def merge(l01_pts, l12_pts, l24_pts, l45_pts):
    # 所有曲线
    l_pts = []
    l_pts.extend(l01_pts)
    l_pts.extend(l12_pts)

    l24_left_pt = l24_pts[0]

    last_pos = len(l_pts) - 1
    pos = -1
    for i in range(last_pos, -1, -1):
        if l_pts[i][0] > l24_left_pt[0]:
            pos = i
            break

    if (pos > 0):
        l_pts = l_pts[0: pos + 1]

    l_pts.extend(l24_pts)

    l24_right_pt = l24_pts[-1]
    pos = -1
    for i in range(len(l45_pts)):
        if l45_pts[i][0] < l24_right_pt[0]:
            pos = i
            break

    if (pos > 0):
        l45_pts = l45_pts[pos:-1]

    l_pts.extend(l45_pts)

    return l_pts
