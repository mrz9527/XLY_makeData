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


def test_str_construct():
    print("test_str_construct:\tdest_str = str(src_str)")
    src_str = 'operation'
    dest_str = str(src_str)
    print("src_str == dest_str ?", src_str == dest_str)
    print("src_str is dest_str ?", src_str is dest_str)
    print("")


def test_str_copy():
    print("test_str_copy:\tdest_str = copy.copy(src_str)")
    src_str = 'operation'
    dest_str = copy.copy(src_str)
    print("src_str == dest_str ?", src_str == dest_str)
    print("src_str is dest_str ?", src_str is dest_str)
    print("")


def test_str_slice():
    print("test_str_slice:\tdest_str = src_str[:]")
    src_str = 'operation'
    dest_str = src_str[:]
    print("src_str == dest_str ?", src_str == dest_str)
    print("src_str is dest_str ?", src_str is dest_str)
    print("")


def test_str_assignment():
    print("test_str_assignment:\tstr2 = str1")
    str1 = 'zhangsan'
    str2 = str1

    print(f"str1 == str2 ?", str1 == str2)
    print(f"str1 is str2 ?", str1 is str2)
    print("赋值只是把原对象的引用给到新对象")
    print("")


def test_str_item_assignment():
    name = "zhangsan"
    print(f"test_str_item_assignment: name = {name}")
    print(f"name[1] = {name[1]}")
    print("# name[1] = 'G'     # 编译报错，因为str是不可变对象，不支持item assignment")
    print("")


def test_str_other():
    print(f"test_str_other:")
    str1 = 'zhangsan'
    str2 = 'zhangsan'

    print("str1 = 'zhangsan'")
    print("str2 = 'zhangsan'")
    print(f"str1 == str2 ?", str1 == str2)
    print(f"str1 is str2 ?", str1 is str2)
    print("因为str是不可变序列，所以str1和str2指向同一块内存")
    print("")

def test_str():
    print("测试字符串的浅拷贝和深拷贝")
    test_str_construct()
    test_str_copy()
    test_str_slice()
    test_str_assignment()
    test_str_item_assignment()
    test_str_other()
    print("结论，字符串的构造、切片、copy，都是深拷贝")
    print("----------------------------------\n")


if __name__ == "__main__":
    print(__doc__)
    test_str()