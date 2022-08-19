# -*- coding: utf-8 -*-

class MathUtils():
    @staticmethod
    def dec_to(jinzhi: int, number: int):
        """
        进制转换，将十进制正整数转化为任意进制
        :param jinzhi: 指定进制
        :param number: 带转换的原始数据
        :return: 返回一个整数序列，用于保存余数
        """

        if jinzhi <= 0 or number < 0:
            print(f"jinzhi <= 0 or number < 0, jinzhi = {jinzhi}, number = {number}")

        res = []
        while number != 0:
            mod = number % jinzhi
            number = number // jinzhi
            res.append(mod)

        res.reverse()

        if len(res) == 0:
            res.append(0)

        return res

    @staticmethod
    def get_ctl_pts_by_By_parallel_line(pt1: list, pt2: list, k):
        """
        给定两条平行线上两点，计算两个控制点
        :param pt1: 平行线上点
        :param pt2: 另一条平行线上点
        :param k: 平行线的斜率
        :return: 返回两个控制点
        """
        mid_ptx = (pt1[0] + pt2[0]) / 2
        mid_pty = (pt1[1] + pt2[1]) / 2

        ctl_pt1x = (mid_pty - pt1[1] + mid_ptx / k + k * pt1[0]) * k / (k ** 2 + 1)
        ctl_pt1y = pt1[1] + k * (ctl_pt1x - pt1[0])

        ctl_pt1 = [ctl_pt1x, ctl_pt1y]

        ctl_pt2x = (mid_pty - pt2[1] + mid_ptx / k + k * pt2[0]) * k / (k ** 2 + 1)
        ctl_pt2y = pt2[1] + k * (ctl_pt2x - pt2[0])

        ctl_pt2 = [ctl_pt2x, ctl_pt2y]

        return ctl_pt1, ctl_pt2
