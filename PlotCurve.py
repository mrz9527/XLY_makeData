# -*- coding: utf-8 -*-


from pltplot.pltplot import PltPlot


def DrawCurve(pts, color):
    ptxs = []
    ptys = []

    for pt in pts:
        ptxs.append(pt[0])
        ptys.append(pt[1])

    PltPlot.plt_plot(ptxs, ptys, color=color)


def DrawVlines(Xt, yrange: list, Color, Label):
    for i in range(0, len(Color)):
        PltPlot.plt_vline(Xt[i], ymin=yrange[0], ymax=yrange[1], label=Label[i], color=Color[i])


def Show():
    PltPlot.plt_show()

def legend(label_names):
    PltPlot.plt_legend(label_names)
