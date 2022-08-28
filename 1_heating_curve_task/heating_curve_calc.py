# -*- coding: utf-8 -*-

from mathhandler.Bezier import Bezier
from mathhandler.MathUtils import MathUtils
import common
import math

"""
t1 : -50
t2 : -41
t3 : t4 - dt4
t4 :
t5 : t4 + dt4
t6 : t6 - dt7
t7 : 47

m : l35曲线近似看成直线，l35的斜率是l56斜率的m倍，默认m = 2

l12 : 实际曲线，数据来源：实验曲线
l23 ：实际曲线， 创建新曲线
l35 ：实际曲线， 贝塞尔曲线
l56: 实际曲线， 数据来源：l67曲线的延伸
l67: 实际曲线，数据来源：试验曲线

Xt = [0,t1,t2,t3,t4,t5,t6,t7]

y7 : f(t7)
y6 : f(t6)
k67 : (y7-y6)/(t7-t6)
k56 : k67
y5 : y6 - k56 * (t6 - t5)
y4 : 根据l35来计算，l35为贝塞尔曲线
y3 : y5 - m * k56 * (t5-t3)
y2 : y3 - k23 * (t3-t2)
y1 : f(new_t1)
    (dy)/(dy2) = (dx)/(dx2)
    y_new = y_old - dy
"""


# l67_pts: [t6, ...]
def calc_l67_pts(Index, X, Y):
    l67_pts = []

    t6_index = Index[6]
    for pt_index in range(t6_index, len(X)):
        pt = [X[pt_index], Y[pt_index]]
        l67_pts.append(pt)

    return l67_pts


# l56_pts: [st5, et5) + [et5, t6)
def calc_l56_pts(Index, X, Y, Xt, k56, interval):
    # 分为两部分，第一部分需要推断并插入部分数据，第二部分，是实际的数据
    l_5_to_5half_pts = []

    # 插入数据 (st5, t5half]
    sxt5 = Xt[5]

    xt5half = X[Index[5]]
    yt5half = Y[Index[5]]

    i = 0
    while True:
        xt = xt5half - i * interval
        if xt >= sxt5:
            yt = yt5half + k56 * (xt - xt5half)
            pt = [xt, yt]
            l_5_to_5half_pts.append(pt)
            i += 1
        else:
            break

    l_5_to_5half_pts.reverse()

    # 实际数据 (t5half, t6)
    l_5half_to_6_pts = []
    for i in range(Index[5] + 1, Index[6]):
        pt = [X[i], Y[i]]
        l_5half_to_6_pts.append(pt)

    # 两段线之间做光滑处理（通过贝塞尔方式）
    l_5_to_5half_pts, l_5half_to_6_pts, l56_bezier_ctl_pts = common.SplitTwoCurve(l_5_to_5half_pts,
                                                                                  l_5half_to_6_pts)
    l56_bezier_pts = make_bezier_pts_by_interval(l56_bezier_ctl_pts, interval)

    return l_5_to_5half_pts, l_5half_to_6_pts, l56_bezier_pts


# l35_pts: [t3, t5)
def calc_l35_pts(pt3, pt5, k23, interval):
    # 计算bezier控制点信息
    ctl_pt3, ctl_pt5 = MathUtils.get_ctl_pts_by_By_parallel_line(pt3, pt5, k23)

    # 打印bezier控制点信息
    bezier_ctl_pts = [pt3, ctl_pt3, ctl_pt5, pt5]

    bezier_insert_pts = make_bezier_pts_by_interval(bezier_ctl_pts, interval)

    # 打印bezier曲线的插入点
    # BazelCurve.PrintOut_InsertPt(bezier_insert_pts)

    l35_pts = bezier_insert_pts

    return l35_pts


# l23_pts:(t2, t3)
def calc_l23_pts(Xt, Yt, ctl_pt3, k23, interval):
    l23_pts = []

    xt2 = Xt[2]
    xt3 = ctl_pt3[0]
    yt3 = ctl_pt3[1]

    i = 1  # (t2, t3)，不包括t3，所以i从1开始
    while True:
        xt = xt3 - i * interval
        if xt >= xt2:
            yt = yt3 + k23 * (xt - xt3)
            pt = [xt, yt]
            l23_pts.append(pt)
            i += 1
        else:
            break

    l23_pts.reverse()
    return l23_pts

    # yt2 = yt
    pass


def calc_l12_pts(Xt, Yt, X, Y, Index, k23, l12_ctl_pt3, interval):
    l12_pts = []
    # 先做偏置，让X[0]=27从-50开始
    off = X[0] - Xt[1]
    for i in range(Index[1], Index[2] + 1):  # [t1, t2]闭区间，所以Index[2] + 1
        xt = X[i] - off
        yt = Y[i]
        pt = [xt, yt]
        l12_pts.append(pt)

    # 寻找索引
    pos = -1
    l12_ctl_pt1 = None
    # 更新y值
    ydt2 = l12_pts[Index[2]][1] - Yt[2]
    xdt2 = l12_pts[Index[2]][0] - l12_pts[Index[1]][0]
    for i in range(Index[1], Index[2] + 1):
        xt = l12_pts[i][0]
        xdt = xt - l12_pts[0][0]
        if xdt == 0.0:
            ydt = ydt2 / (Index[2] - Index[1]) * (i - Index[1])
        else:
            ydt = xdt / xdt2 * ydt2
        yt = l12_pts[i][1] - ydt

        tmp_yt = l12_ctl_pt3[1] + k23 * (xt - l12_ctl_pt3[0])
        if yt > tmp_yt:
            pos = i
            l12_ctl_pt1 = [xt, tmp_yt]
            break
        else:
            l12_pts[i][1] = yt

    l1_1half_pts = l12_pts[0:pos]

    l12_ctl_pt2x = l12_ctl_pt1[0] + 3 / 4 * (l12_ctl_pt3[0] - l12_ctl_pt1[0])
    l12_ctl_pt2y = l12_ctl_pt1[1] + 3 / 4 * (l12_ctl_pt3[1] - l12_ctl_pt1[1])
    l12_ctl_pt2 = [l12_ctl_pt2x, l12_ctl_pt2y]

    tmpx = l12_ctl_pt1[0] + 1 / 4 * (l12_ctl_pt3[0] - l12_ctl_pt1[0])
    tmpy = l12_ctl_pt1[1] + 1 / 8 * (l12_ctl_pt3[1] - l12_ctl_pt1[1])

    tmp = [tmpx, tmpy]

    l12_ctl_pts = l1_1half_pts[-3:-1]
    l12_ctl_pts.extend([l12_ctl_pt1, tmp, l12_ctl_pt2, l12_ctl_pt3])

    l1_1half_pts = l1_1half_pts[0:-3]

    l12_bezier_pts = make_bezier_pts_by_interval(l12_ctl_pts, interval)

    return l1_1half_pts, l12_bezier_pts


def make_bezier_pts_by_interval(bezier_ctl_pts, interval):
    if len(bezier_ctl_pts) == 0:
        return []

    scale = interval / (bezier_ctl_pts[-1][0] - bezier_ctl_pts[0][0]) / 2
    T = Bezier.get_bezier_T_by_scale(scale)

    bezier = Bezier(bezier_ctl_pts)
    bezier_insert_pts = bezier.get_bezier_pts(T)

    return bezier_insert_pts


def calc_import_pts(X: list, Y: list, Xt: list, m35, m56):
    Yt = [0 for i in range(len(Xt))]  # 列表，记录Xt对应的纵坐标
    Index = [0 for i in range(len(Xt))]

    k23 = 0.0
    k56 = 0.0
    k67 = 0.0

    # 计算t7对应的索引Index[7]
    lastIndex = len(X) - 1
    for curIndex in range(lastIndex, -1, -1):
        if Xt[7] > X[curIndex]:
            Index[7] = curIndex
            break

    # 计算t7对应的y7 = Yt[7]
    Xt[7] = X[Index[7]]  # 更新Xt[7]，之前的Xt[7]是计算得来的，现在的Xt[7]是实际的
    Yt[7] = Y[Index[7]]

    # 计算t6对应的索引Index[6]
    lastIndex = Index[7] - 1
    for curIndex in range(lastIndex, -1, -1):
        if Xt[6] > X[curIndex]:
            if Xt[6] <= X[curIndex + 1]:
                Index[6] = curIndex + 1
                break

    # 计算t6对应的y6 = Yt[6]
    Xt[6] = X[Index[6]]  # 更新Xt[6]，之前的Xt[6]是计算得来的，现在的Xt[6]是实际的
    Yt[6] = Y[Index[6]]

    # 计算k67
    k67 = (Yt[7] - Yt[6]) / (Xt[7] - Xt[6])
    # 计算k56 = k67
    k56 = m56 * k67

    # 寻找理论值Xt[2]对应实际Xt[2]的横坐标tmpx2, tmpx2也是xt_5.5的位置， 以5度作为误差
    tmpx2 = X[0]
    tmpIndex2 = 0

    # cos5degree = math.cos(5 * math.pi / 180)  # 5度对应的余弦值 cos(5 * pi / 180)
    cos1degree = math.cos(1 * math.pi / 180)  # 5度对应的余弦值 cos(5 * pi / 180)
    ntimes = 0
    maxtimes = 2
    vector67 = [Yt[7] - Yt[6], Xt[7] - Xt[6]]
    vector67_length = math.sqrt(vector67[0] ** 2 + vector67[1] ** 2)
    lastIndex = Index[6] - 1
    for curIndex in range(lastIndex, -1, -1):
        vector = [Y[curIndex + 1] - Y[curIndex], X[curIndex + 1] - X[curIndex]]
        vector_length = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        cos = (vector67[0] * vector[0] + vector67[1] * vector[1]) / vector67_length / vector_length
        if cos < cos1degree:
            if ntimes == 0:
                tmpx2 = X[curIndex]
                tmpIndex2 = curIndex
            ntimes += 1
            if ntimes >= maxtimes:  # 存在连续5次较大误差，认为找到了
                break
        else:
            ntimes = 0

    if (ntimes < maxtimes):
        print(f"[error]没有找到{maxtimes}次较大误差（大于5度）, ntimes = {ntimes}")
    else:
        print(f"找到{maxtimes}次较大误差（大于5度)")

    # plt.vlines(tmpx2, ymin=0, ymax=50, label="xxxxx", color="#777777")

    if (tmpx2 - X[0]) >= (Xt[3] - Xt[1]):
        print("(tmpx2 - X[0]) >= (Xt[3] - Xt[1])，进行修正")
        tmpx2 = (Xt[3] - Xt[1]) / 2 + X[0]
        for curIndex in range(lastIndex, -1, -1):
            if X[curIndex] < tmpx2:
                tmpIndex2 = curIndex
                tmpx2 = X[curIndex]
                break

    tmpy2 = Y[tmpIndex2]
    xdt12 = tmpx2 - X[0]
    Xt[2] = Xt[1] + xdt12
    Index[2] = tmpIndex2

    """
    y7 : f(t7)
    y6 : f(t6)
    k67 : (y7-y6)/(t7-t6)
    k56 : m56 * k67
    y5 : y6 - k56 * (t6 - t5)
    y4 : 根据l35来计算，l35为贝塞尔曲线
    y3 : y5 - m * k56 * (t5-t3)
    y2 : y3 - k23 * (t3-t2)
    y1 : f(new_t1)
    """
    # 计算t5对应的y5 = Yt[5]
    # Yt[5] = Yt[5.5] - k5_5.5 * (Xt[5.5] - Xt[5])
    t5half = [tmpx2, tmpy2]
    Yt[5] = t5half[1] - k56 * (t5half[0] - Xt[5])

    # 计算y3 = Yt[3]
    Yt[3] = Yt[5] - m35 * k56 * (Xt[5] - Xt[3])

    # 计算y2 = Yt[2]
    k23 = k56
    Yt[2] = Yt[3] - k23 * (Xt[3] - Xt[2])

    # 计算y1 = Yt[1]
    Yt[1] = Y[0]

    # 计算Index[1]
    Index[1] = 0

    Index[5] = Index[2] + 1

    return Index, Xt, Yt, k23, k56, xdt12
