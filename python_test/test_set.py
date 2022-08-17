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
"""

import copy


def test_set_construct():
    print("test_set_construct:\tset2 = set(set1)")
    set1 = {1, 2, 3}
    set2 = set(set1)
    print("set1 == set2 ?", set1 == set2)
    print("set1 is set2 ?", set1 is set2)
    print("")


def test_set_copy():
    print("test_set_copy:\tset2 = copy.copy(set1)")
    set1 = {1, 2, 3}
    set2 = copy.copy(set1)
    print("set1 == set2 ?", set1 == set2)
    print("set1 is set2 ?", set1 is set2)
    print("")


def test_set_slice():
    print("test_set_slice:\tset2 = set1[:]")
    print("set不支持切片slice")
    print("")


def test_set_assignment():
    print("test_set_assignment:\tset2 = set1")
    set1 = {1, 2, 3}
    set2 = set1

    print(f"set1 == set2 ?", set2 == set2)
    print(f"set1 is set2 ?", set1 is set2)
    print("赋值只是把原对象的引用给到新对象")
    print("")


def test_set_item_assignment():
    print(f"test_set_item_assignment: ")
    print("# set1[1] = 5     # 编译报错, set不支持下标")
    print("# a = set1[1]     # 编译报错, set不支持下标")
    print("")


def test_set_other():
    print(f"test_set_other:")
    set1 = {1, 2, 3}
    set2 = {1, 2, 3}

    print("set1 = [1, 2, 3]")
    print("set2 = [1, 2, 3]")
    print(f"set1 == set2 ?", set1 == set2)
    print(f"set1 is set2 ?", set1 is set2)
    print("因为set是可变序列，所以set1和set2为两块内存")
    print("")


def test_set():
    print("测试set的浅拷贝和深拷贝")
    test_set_construct()
    test_set_copy()
    test_set_slice()
    test_set_assignment()
    test_set_item_assignment()
    test_set_other()
    print("结论，set的构造、切片、copy，都是浅拷贝")

    print("测试set参数传递")
    set1 = {8, 9, 10}
    print("id(set1) = ", id(set1))
    print(f"set1 = {set1}")
    print("test_set_func_param(set1)")
    test_set_func_param(set1)
    print("id(set1) = ", id(set1))
    print(f"set1 = {set1}")
    print("----------------------------------\n")


def test_set_func_param(set1: set):
    set1.add(5)

if __name__ == "__main__":
    print(__doc__)
    test_set()
