#Bullet.py
import images
from FlyingObject import *

class Bullet(Arm):
    def __init__(self, canvas, position, destroy_cb=None):
        self.__images = [images.load_image("bullet.png")]
        self.__canvas = canvas
        self.image = self.__images[0]
        # 先算寬和高
        self.size = (self.image.width(), self.image.height())
        self.__image_id = canvas.create_image(position, image=self.image)
        self.__destroy_cb = destroy_cb
        super().__init__(position=position, size=self.size, speed=(0, -20))
        # 圖片管理器
        self.__image_manager = FlyingImageManager(canvas,self.__image_id,position)                                            
        
    def set_destroy(self):
        '''設置為擊中銷毀狀態'''
        self.__canvas.delete(self.__image_id)
        if self.__destroy_cb:
            self.__destroy_cb(self)
   
    def on_timer(self):
        self.move()
        self.__image_manager.draw(self.pos())
        if self.pos()[1] <10:
            self.set_destroy()
