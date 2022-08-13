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
