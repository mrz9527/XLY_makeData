# -*- coding: utf-8 -*-

import math
import matplotlib.pyplot as plt


"""
直线l1和l2平行，l1上一点pt1和l2上一点pt2之间构造2个控制点ctl_pt1和ctl_pt2
(pt1，ctl_pt1, ctl_pt2, pt2)，共四个点，构造贝塞尔曲线
"""


def CalcTwoControlPtByParallelLine(pt1: list, pt2: list, k):
    mid_ptx = (pt1[0] + pt2[0]) / 2
    mid_pty = (pt1[1] + pt2[1]) / 2

    ctl_pt1x = (mid_pty - pt1[1] + mid_ptx / k + k * pt1[0]) * k / (k ** 2 + 1)
    ctl_pt1y = pt1[1] + k * (ctl_pt1x - pt1[0])

    ctl_pt1 = [ctl_pt1x, ctl_pt1y]

    ctl_pt2x = (mid_pty - pt2[1] + mid_ptx / k + k * pt2[0]) * k / (k ** 2 + 1)
    ctl_pt2y = pt2[1] + k * (ctl_pt2x - pt2[0])

    ctl_pt2 = [ctl_pt2x, ctl_pt2y]

    return ctl_pt1, ctl_pt2


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
k56 : m56 * k67
y5 : y6 - k56 * (t6 - t5)
y4 : 根据l35来计算，l35为贝塞尔曲线
y3 : y5 - m * k56 * (t5-t3)
y2 : y3 - k23 * (t3-t2)
y1 : f(new_t1)
"""


def CalculateKeyPt(X: list, Y: list, Xt: list, m35, m56):
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
        tmpx2 = (Xt[3] - Xt[1])/2 + X[0]
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


def GetInterval(ex, sx, eIndex, sIndex):
    interval = (ex - sx) / (eIndex - sIndex)
    return interval


def PrintOut_CalculateKeyPt(Index, Xt, Yt, k23, k56):
    print("打印关键坐标计算信息...")
    for index in range(len(Index)):
        print(f"index[{index}] = {Index[index]}")

    for xt in range(len(Xt)):
        print(f"xt[{xt}] = {Xt[xt]}")

    for yt in range(len(Yt)):
        print(f"yt[{yt}] = {Yt[yt]}")

    print(f"k23 = {k23}, k56 = {k56}")


def PrintOut_GetInterval(interval):
    print("打印间距和基准百分比...")
    print(f"interval : {interval}")


def SplitScale(count, base):
    split_scale = 0.0
    if count / 8 > base:
        split_scale = 4 * base / count
    elif count / 4 > base:  # 至少4倍基本个数，取四分之一
        split_scale = 1 / 4
    elif count / 2 > base:  # 至少2倍基本个数，取二分之一
        split_scale = 1 / 2
    else:  # 否则全选
        split_scale = 0.75

    return split_scale


def SplitTwoCurve(l1_pts, l2_pts, base_count=10):
    if len(l1_pts) == 0:
        return [], l2_pts, []
    if len(l2_pts) == 0:
        return l1_pts, [], []

    scale1 = SplitScale(len(l1_pts), base_count)
    scale2 = SplitScale(len(l2_pts), base_count)

    index1 = len(l1_pts) * (1 - scale1)
    index2 = len(l2_pts) * scale2

    index1 = int(index1)
    index2 = int(index2)

    # 构造3阶（4个点）的贝塞尔曲线控制点
    l12_bezier_ctl_pts = []
    l12_bezier_ctl_pts.append(l1_pts[index1])
    l12_bezier_ctl_pts.append(l1_pts[-1])
    l12_bezier_ctl_pts.append(l2_pts[0])
    l12_bezier_ctl_pts.append(l2_pts[index2])

    l1_pts = l1_pts[0:index1]
    l2_pts = l2_pts[index2:-1]

    return l1_pts, l2_pts, l12_bezier_ctl_pts
