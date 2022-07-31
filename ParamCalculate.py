# -*- coding: utf-8 -*-


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
k56 : k67
y5 : y6 - k56 * (t6 - t5)
y4 : 根据l35来计算，l35为贝塞尔曲线
y3 : y5 - m * k56 * (t5-t3)
y2 : y3 - k23 * (t3-t2)
y1 : f(new_t1)
"""


def CalculateKeyPt(X: list, Y: list, Xt: list, m):
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
    Yt[7] = Y[Index[7]]

    # 计算t6对应的索引Index[6]
    lastIndex = Index[7] - 1
    for curIndex in range(lastIndex, -1, -1):
        if Xt[6] > X[curIndex]:
            if Xt[6] <= X[curIndex + 1]:
                Index[6] = curIndex + 1
                break

    # 计算t6对应的y6 = Yt[6]
    Yt[6] = Y[Index[6]]

    # 计算k67
    k67 = (Yt[7] - Yt[6]) / (Xt[7] - Xt[6])
    # 计算k56 = k67
    k56 = k67

    # 计算t5对应的y5 = Yt[5]
    Yt[5] = Yt[6] - k56 * (Xt[6] - Xt[5])

    # 计算y3 = Yt[3]
    Yt[3] = Yt[5] - m * k56 * (Xt[5] - Xt[3])

    # 计算y2 = Yt[2]
    k23 = k56
    Yt[2] = Yt[3] - k23 * (Xt[3] - Xt[2])

    # 计算y1 = Yt[1]
    Yt[1] = Y[0]

    # 计算Index[1]
    Index[1] = 0

    # 计算t2对应的索引Index[2]
    xdt12 = Xt[2] - Xt[1] # Xt为输出数据中对应的关键点坐标
    tmpXt2 = X[0] + xdt12

    lastIndex = Index[6] - 1
    for curIndex in range(lastIndex, -1, -1):
        if tmpXt2 > X[curIndex]:
            if tmpXt2 <= X[curIndex + 1]:
                Index[2] = curIndex + 1
                break

    Index[5] = Index[2] + 1

    return Index, Yt, k23, k56


def GetIntervalAndScale(ex, sx, eIndex, sIndex):
    interval = (ex - sx) / (eIndex - sIndex)
    scale = interval / (ex - sx)
    return interval, scale


def PrintOut_CalculateKeyPt(Index, Xt, Yt, k23, k56):
    print("打印关键坐标计算信息...")
    for index in range(len(Index)):
        print(f"index[{index}] = {Index[index]}")

    for xt in range(len(Xt)):
        print(f"xt[{xt}] = {Xt[xt]}")

    for yt in range(len(Yt)):
        print(f"yt[{yt}] = {Yt[yt]}")

    print(f"k23 = {k23}, k56 = {k56}")


def PrintOut_GetIntervalAndScale(interval, scale):
    print("打印间距和基准百分比...")
    print(f"interval : {interval}  scale : {scale}")
