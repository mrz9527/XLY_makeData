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


def test_dict_construct():
    print("test_dict_construct:\tdict2 = dict(dict1)")
    dict1 = {1: 'xiaoming', 2: 'xiahua', 3: 'xiaoli'}
    dict2 = dict(dict1)
    print("dict1 == dict2 ?", dict1 == dict2)
    print("dict1 is dict2 ?", dict1 is dict2)
    print("")


def test_dict_copy():
    print("test_dict_copy:\tdict2 = copy.copy(dict1)")
    dict1 = {1: 'xiaoming', 2: 'xiahua', 3: 'xiaoli'}
    dict2 = copy.copy(dict1)
    print("dict1 == dict2 ?", dict1 == dict2)
    print("dict1 is dict2 ?", dict1 is dict2)
    print("")


def test_dict_slice():
    print("test_dict_slice:\tdict2 = dict1[:]")
    print("dict不支持切片slice")
    print("")


def test_dict_assignment():
    print("test_dict_assignment:\tdict2 = dict1")
    dict1 = {1: 'xiaoming', 5: 'xiahua', 7: 'xiaoli'}
    dict2 = dict1

    print(f"dict1 == dict2 ?", dict2 == dict2)
    print(f"dict1 is dict2 ?", dict1 is dict2)
    print("赋值只是把原对象的引用给到新对象")
    print("")


def test_dict_item_assignment():
    dict1 = {1: 'xiaoming', 5: 'xiahua', 7: 'xiaoli'}
    print(f"test_dict_item_assignment: dict1 = {dict1}")
    dict1[5] = 'wangerxiao'
    print("dict1[5] = 'wangerxiao'")
    print(f"dict1[5] = {dict1[5]}")
    print("")


def test_dict_other():
    print(f"test_dict_other:")
    dict1 = {1: 'xiaoming', 5: 'xiahua', 7: 'xiaoli'}
    dict2 = {1: 'xiaoming', 5: 'xiahua', 7: 'xiaoli'}

    print("dict1 = {1: 'xiaoming', 5: 'xiahua', 7: 'xiaoli'}")
    print("dict2 = {1: 'xiaoming', 5: 'xiahua', 7: 'xiaoli'}")
    print(f"dict1 == dict2 ?", dict1 == dict2)
    print(f"dict1 is dict2 ?", dict1 is dict2)
    print("因为dict是可变序列，所以dict1和dict2指向同一块内存")


def test_dict():
    print("测试dict的浅拷贝和深拷贝")
    test_dict_construct()
    test_dict_copy()
    test_dict_slice()
    test_dict_assignment()
    test_dict_item_assignment()
    test_dict_other()
    print("结论，dict的构造、切片、copy，都是浅拷贝")
    print("----------------------------------\n")


if __name__ == "__main__":
    print(__doc__)
    test_dict()
