# -*- coding: utf-8 -*-

import copy


class Bezier():
    def __init__(self, ctl_pts: list):
        self.ctl_pts = ctl_pts

    def get_bezier_pt(self, t) -> list:
        """
        根据t，计算bezier曲线上的点
        :param t: 比例值, [0,1]之间的一个浮点数
        :return: 返回pt:list
        """

        iter_ctl_pts = self.ctl_pts
        while len(iter_ctl_pts) > 1:
            iter_ctl_pts = Bezier.get_next_iter_ctl_pts(iter_ctl_pts, t)

        bezier_pt = iter_ctl_pts[0]

        return bezier_pt

    def get_bezier_pts(self, T: list) -> list:
        """
        根据t，计算bezier曲线上的点
        :param T: 递增的比例序列
        :return: 返回pt:list
        """

        bezier_pts = []
        for t in T:
            bezier_pt = self.get_bezier_pt(t)
            bezier_pts.append(bezier_pt)
        return bezier_pts

        iter_ctl_pts = self.ctl_pts
        while len(iter_ctl_pts) > 1:
            iter_ctl_pts = Bezier.get_next_iter_ctl_pts(iter_ctl_pts, t)

        return iter_ctl_pts[0]

    @staticmethod
    def get_next_iter_ctl_pts(ctl_pts: list, t) -> list:
        count = len(ctl_pts)
        if count <= 1:
            return ctl_pts

        iter_ctl_pts = []
        for pos in range(count - 1):
            x = (1 - t) * ctl_pts[pos][0] + t * ctl_pts[pos + 1][0]
            y = (1 - t) * ctl_pts[pos][1] + t * ctl_pts[pos + 1][1]
            pt = [x, y]
            iter_ctl_pts.append(pt)

        return iter_ctl_pts

    @staticmethod
    def get_bezier_T_by_scale(scale):
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
