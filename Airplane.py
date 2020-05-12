# Airplane.py
# -*- coding:utf-8 -*-
import images
from FlyingObject import *

class EnemyPlane1(Aerocraft):
    '''敵機類1'''
    def __init__(self, canvas, destroy_cb=None):
        self.__images = [
        images.load_image('enemy1.png'),
        images.load_image('enemy1_down1.png'),
        images.load_image('enemy1_down2.png'),
        images.load_image('enemy1_down3.png'),
        images.load_image('enemy1_down4.png'),
        images.load_image('enemy1_down5.png'),
        images.load_image('enemy1_down8.png'),
        images.load_image('enemy1_down9.png')
    ]
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0,5))



class EnemyPlane1_2(Aerocraft):
    '''敵機類1'''
    def __init__(self, canvas, destroy_cb=None):
        self. __images = [
        images.load_image('enemy1.png'),
        images.load_image('enemy1_down1.png'),
        images.load_image('enemy1_down2.png'),
        images.load_image('enemy1_down3.png'),
        images.load_image('enemy1_down4.png'),
        images.load_image('enemy1_down5.png'),
        images.load_image('enemy1_down8.png'),
        images.load_image('enemy1_down9.png')
    ]
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 30))
