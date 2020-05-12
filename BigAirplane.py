#BigAirplane.py
import images
from FlyingObject import *

class EnemyPlane3(Aerocraft):
    '''敵機類3'''
    

    def __init__(self, canvas, destroy_cb=None):
        self.__images = [
        images.load_image('enemy3_n1.png'),
        images.load_image('enemy3_down1.png'),
        images.load_image('enemy3_down2.png'),
        images.load_image('enemy3_down3.png'),
        images.load_image("hero_blowup_n4.png"),
        images.load_image("hero_blowup_n5.png"),
        images.load_image("hero_blowup_n8.png"),
        images.load_image("hero_blowup_n9.png")

    ]
        super().__init__(canvas,
                         image=self.__images[0], destroy_images=self.__images[1:], destroy_cb=destroy_cb, speed=(0, 10))