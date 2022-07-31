# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


def DrawCurve(pts, color):
    ptxs = []
    ptys = []

    for pt in pts:
        ptxs.append(pt[0])
        ptys.append(pt[1])

    plt.plot(ptxs, ptys, color=color)
    # plt.show()


def Show():
    plt.show()


def DrawMultiCurve(lines, colors):
    n = len(lines)
    for i in range(n):
        DrawCurve(lines[i], colors[i])

