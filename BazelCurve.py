# -*- coding: utf-8 -*-

def Bezier(control_pts, count, t):
    """
    首次调用时，count = len(control_pts)，每次迭代时，相当于控制点减1
    :param control_pts:
    :param count:
    :param t:
    :return:
    """
    if count <= 1:
        return

    for pos in range(count - 1):
        control_pts[pos][0] = (1 - t) * control_pts[pos][0] + t * control_pts[pos + 1][0]
        control_pts[pos][1] = (1 - t) * control_pts[pos][1] + t * control_pts[pos + 1][1]

    Bezier(control_pts, count - 1, t)


def PrintOut_Bezier(bezier_pts):
    print("打印bezier控制点信息...")
    for pt_index in range(len(bezier_pts)):
        print(f"{pt_index} ({bezier_pts[pt_index][0]},{bezier_pts[pt_index][1]})")


def InsertPtByT(bezier_ctl_pts, T):
    bezier_insert_pts = []
    for t in T:
        Bezier(bezier_ctl_pts, len(bezier_ctl_pts), t)
        bezier_insert_pts.append(bezier_ctl_pts[0].copy())
    return bezier_insert_pts


def InsertPtByInterval(bezier_ctl_pts, interval):
    if len(bezier_ctl_pts) == 0:
        return []

    scale = interval / (bezier_ctl_pts[-1][0] - bezier_ctl_pts[0][0]) / 2
    T = GetBezierParamT(scale)

    bezier_insert_pts = InsertPtByT(bezier_ctl_pts, T)
    return bezier_insert_pts


def PrintOut_InsertPt(bezier_insert_pts):
    print("打印bazel曲线的插入点")
    for pt_index in range(len(bezier_insert_pts)):
        print(f"{pt_index} ({bezier_insert_pts[pt_index][0]},{bezier_insert_pts[pt_index][1]})")


def GetBezierParamT(scale):
    T = []
    tmpN = 0
    while True:
        t = tmpN * scale
        if t < 1.0:
            T.append(t)
            tmpN += 1
        else:
            break
    return T
