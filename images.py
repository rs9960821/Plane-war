# -*- coding:utf-8 -*-


import os
from tkinter import *

paths = ['./images']
def load_image(filename):
    '''根據給定的文件名自動找開圖片資源返回。
    如果沒有找天圖片資源則會返回None
    '''
    for pth in paths:
        path1 = os.path.join(pth, filename)
        if os.path.exists(path1):
            return PhotoImage(file=path1)





    