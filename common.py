# -*- coding: utf-8 -*-

def GetInterval(ex, sx, eIndex, sIndex):
    interval = (ex - sx) / (eIndex - sIndex)
    return interval


def SplitScale(count, base):
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