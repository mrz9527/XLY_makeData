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


def test_list_construct():
    print("test_list_construct:\tlist2 = list(list1)")
    list1 = [1, 2, 3]
    list2 = list(list1)
    print("list1 == list2 ?", list1 == list2)
    print("list1 is list2 ?", list1 is list2)
    print("")


def test_list_copy():
    print("test_list_copy:\tlist2 = copy.copy(list1)")
    list1 = [1, 2, 3]
    list2 = copy.copy(list1)
    print("list1 == list2 ?", list1 == list2)
    print("list1 is list2 ?", list1 is list2)
    print("")


def test_list_slice():
    print("test_list_slice:\tlist2 = list1[:]")
    list1 = [1, 2, 3]
    list2 = list1[:]
    print("list1 == list2 ?", list1 == list2)
    print("list1 is list2 ?", list1 is list2)
    print("")


def test_list_assignment():
    print("test_list_assignment:\tlist2 = list1")
    list1 = [1, 2, 3]
    list2 = list1

    print(f"list1 == list2 ?", list2 == list2)
    print(f"list1 is list2 ?", list1 is list2)
    print("赋值只是把原对象的引用给到新对象")
    print("")


def test_list_deepcopy_vs_shallowcopy():
    list1 = [[1, 2], (30, 40)]
    list2 = list(list1)
    list1.append(100)
    print("list1:", list1)
    print("list2:", list2)
    list1[0].append(3)
    print("list1:", list1)
    print("list2:", list2)
    list1[1] += (50, 60)
    print("list1:", list1)
    print("list2:", list2)


def test_list_item_assignment():
    list1 = [1, 2, 3]
    print(f"test_list_item_assignment: list1 = {list1}")
    list1[1] = 5
    print("list1[1] = 5")
    print(f"list1[1] = {list1[1]}")
    print("")


def test_list_other():
    print(f"test_list_other:")
    list1 = [1, 2, 3]
    list2 = [1, 2, 3]

    print("list1 = [1, 2, 3]")
    print("list2 = [1, 2, 3]")
    print(f"list1 == list2 ?", list1 == list2)
    print(f"list1 is list2 ?", list1 is list2)
    print("因为list是可变序列，所以list1和list2为两块内存")
    print("")


def test_list():
    print("测试list的浅拷贝和深拷贝")
    test_list_construct()
    test_list_copy()
    test_list_slice()
    test_list_assignment()
    test_list_item_assignment()
    test_list_other()
    print("结论，list的构造、切片、copy，都是浅拷贝")

    print("测试list参数传递")
    list1 = [8, 9, 10]
    print("id(list1) = ", id(list1))
    print(f"list1 = {list1}")
    print("test_list_func_param(list1)")
    test_list_func_param(list1)
    print("id(list1) = ", id(list1))
    print(f"list1 = {list1}")
    print("----------------------------------\n")


def test_list_func_param(list1: list):
    list1[0] = 100

if __name__ == "__main__":
    print(__doc__)
    test_list()
