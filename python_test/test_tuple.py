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


def test_tuple_construct():
    print("test_tuple_construct:\ttuple2 = tuple(tuple1)")
    tuple1 = (1, 2, 3)
    tuple2 = tuple(tuple1)
    print("tuple1 == tuple2 ?", tuple1 == tuple2)
    print("tuple1 is tuple2 ?", tuple1 is tuple2)
    print("")


def test_tuple_copy():
    print("test_tuple_copy:\ttuple2 = copy.copy(tuple1)")
    tuple1 = (1, 2, 3)
    tuple2 = copy.copy(tuple1)
    print("tuple1 == tuple2 ?", tuple1 == tuple2)
    print("tuple1 is tuple2 ?", tuple1 is tuple2)
    print("")


def test_tuple_slice():
    print("test_tuple_slice:\ttuple2 = tuple1[:]")
    tuple1 = (1, 2, 3)
    tuple2 = tuple1[:]
    print("tuple1 == tuple2 ?", tuple1 == tuple2)
    print("tuple1 is tuple2 ?", tuple1 is tuple2)
    print("")


def test_tuple_assignment():
    print("test_tuple_assignment:\ttuple2 = tuple1")
    tuple1 = (1, 2, 3)
    tuple2 = tuple1

    print(f"tuple1 == tuple2 ?", tuple2 == tuple2)
    print(f"tuple1 is tuple2 ?", tuple1 is tuple2)
    print("赋值只是把原对象的引用给到新对象")
    print("")


def test_tuple_item_assignment():
    tuple1 = (1, 2, 3)
    print(f"test_tuple_item_assignment: tuple1 = {tuple1}")
    print(f"tuple1[1] = {tuple1[1]}")
    print("# tuple1[1] = 5     # 编译报错，因为tuple是不可变对象，不支持item assignment")
    print("")


def test_tuple_other():
    print(f"test_tuple_other:")
    tuple1 = (1, 2, 3)
    tuple2 = (1, 2, 3)

    print("tuple1 = (1, 2, 3)")
    print("tuple2 = (1, 2, 3)")
    print(f"tuple1 == tuple2 ?", tuple1 == tuple2)
    print(f"tuple1 is tuple2 ?", tuple1 is tuple2)
    print("因为tuple是不可变序列，所以tuple1和tuple2指向同一块内存")
    print("")


def test_tuple():
    print("测试元组的浅拷贝和深拷贝")
    test_tuple_construct()
    test_tuple_copy()
    test_tuple_slice()
    test_tuple_assignment()
    test_tuple_item_assignment()
    test_tuple_other()
    print("结论，元组的构造、切片、copy，都是深拷贝")
    print("----------------------------------\n")


if __name__ == "__main__":
    print(__doc__)
    test_tuple()