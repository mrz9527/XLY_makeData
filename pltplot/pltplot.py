# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt


class PltPlot():
    @staticmethod
    def plt_vline(X, ymin, ymax, label, color):
        plt.vlines(X, ymin=ymin, ymax=ymax, label=label, color=color)

    @staticmethod
    def plt_plot(X, Y, color):
        plt.plot(X, Y, color=color)

    @staticmethod
    def plt_show():
        plt.show()

    @staticmethod
    def plt_legend(label_names):
        # 设置图例
        plt.legend(label_names)
