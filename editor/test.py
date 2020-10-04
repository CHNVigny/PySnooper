import pysnooper
import editor
import tkinter as tk
import json


def hello(name):
    print("hello, {name}".format(name=name))

@pysnooper.snoop()
def wrapper(function, *args, **kws):
    eval(function)(*args, **kws)

# @pysnooper.snoop()
# def test():
#     n = int(input("输入功能："))
#     if n == 1:
#         function = input("函数")
#         name = input("参数：")
#         name_list = name.split(',')
#         wrapper(function, *name_list)

@pysnooper.snoop()
def editortest():
    master = tk.Tk()
    pt = editor.PyText(master)
    master.mainloop()
    master.quit()

#editortest()

#test()
# list = []
#
# def record_checkpoint(list, kwargs):
#     list.append(kwargs)
#
# kwargs = {"1":"1", "2":"2"}
# record_checkpoint(list, kwargs)
# print(list)

@pysnooper.snoop()
def pop_test():
    list = [1, 2, 3, 4, 5]
    num = 6
    remove = 1
    CONTINUE = 1
    print("initial list: {}".format(list))
    while CONTINUE:
        if remove in list:
            list.remove(remove)
            list.append(num)
            remove += 1
            num += 1
            print(list)
            CONTINUE = int(input("continue?"))
        else:
            print("no remove: {}".format(remove))
            break

@pysnooper.snoop()
def json_test():
    """
    字典的键必须用双引号，字典的值随意。字典字符串化必须用单引号。
    """
    dict_obj = {"1": 1, "2": 2}
    dict_str = '{"1": 1, "2": 2}'
    dict_obj1 = {}
    dict_obj1["1"] = 1
    dict_obj1["2"] = 2
    print(dict_obj1 == dict_obj)
    str = json.dumps(dict_obj)
    print(str == dict_str)
    obj = json.loads(dict_str)
    print(dict_obj == obj)
    print(dict_obj["1"])


#json_test()

#判断字典中某个键是否存在
arr = {"int":"整数","float":"浮点","str":"字符串","list":"列表","tuple":"元组","dict":"字典","set":"集合"}
# #使用 in 方法
# if "int" in arr:
#     print("存在")
# if "float" in arr.keys():
#     print("存在")
# #判断键不存在
# if "floats" not in arr:
#     print("不存在")
# if "floats" not in arr:
#     print("不存在")

# class A():
#     def __init__(self):
#         print("a")
#
# class B():
#     def __init__(self):
#         self.A = A()
#
# b = B()

path = r"C:\Users\94519\Desktop\checkpoint.txt"
# try:
#     f1 = open(path,"w",encoding="utf-8")
#     count = 20
#     while count:
#         f1.write(str(count) + "\n")
#         count -= 1
# finally:
#     if f1:   #打开失败时f1对象还未创建就不用关闭了
#         f1.close()

file = open(path,'r')
done = 0
while not done:
    aLine = file.readline()
    if(aLine != ''):
        print (aLine)
    else:
        done = 1
file.close() #关闭文件