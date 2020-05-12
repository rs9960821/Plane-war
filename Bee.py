# Bee.py
import images
from FlyingObject import *

class EnemyPlane2(AerocraftBee):
    '''敵機類2'''
    

    def __init__(self, canvas, destroy_cb=None):
        self.__images = [
        images.load_image('enemy2.png'),
        images.load_image('enemy2_down1.png'),
        images.load_image('enemy2_down2.png'),
        images.load_image('enemy2_down3.png'),
        images.load_image('enemy2_down4.png'),
        images.load_image('enemy2_down5.png'),
        images.load_image('enemy2_down8.png'),
        images.load_image('enemy2_down9.png')
    ]
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 5))