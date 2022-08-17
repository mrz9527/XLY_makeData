# -*- coding: utf-8 -*-

"""
对于可变序列(list、dict)，下列操作都是浅拷贝：
    使用数据类型本身的构造器
    对于可变的序列，还可以通过切片操作符 : 来完成浅拷贝 (dict不支持切片slice)
    Python 还提供了对应的函数 copy.copy() 函数，适用于任何数据类型

对于不可变序列(str、tuple)，只有深拷贝，包括:
    使用数据类型本身的构造器
    使用切片
    使用copy.copy()函数

对于可变序列(list、dict),深拷贝的方式:
    dest = copy.deepcopy(src)

python中赋值语句总是建立对象的引用值，而不是复制对象

python函数参数传递，是通过赋值的方式，所以形参是实参的引用
在函数体内，
    如果给形参赋新值，相当于形参是新值的引用，此时形参不在指向原实参对象
    如果参数是可变序列，并且给形参的某一个元素赋值，相当于直接操作实参


"""

from test_str import test_str
from test_tuple import test_tuple
from test_list import test_list
from test_dict import test_dict
from test_set import test_set, test_set_func_param

if __name__ == "__main__":
    print(__doc__)

    test_str()
    test_tuple()
    test_list()
    test_dict()
    test_set()
