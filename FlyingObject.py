#FlyingObject.py
# -*- coding:utf-8 -*-
import random 
from sky import * 
class Arm:
    '''此類是武器類的基類，用來檢測的碰幢條件等'''
    def __init__(self, position=None , size=(2, 2), speed=(0, 3)):
        if position is None:
            position = [0, 0]
        self.__pos = list(position)  # 中心點(列表)
        self.__size = size # 寬和高(元組)
        self.__speed = speed # 默認移動速度
        self.bee=random.randint(1,2)
    def set_position(self, position):
        self.__pos[:] = position

    def left(self):
        '''得到左邊的x坐標'''
        return self.__pos[0] - self.__size[0] / 2

    def right(self):
        '''得到右邊的x坐標'''
        return self.__pos[0] + self.__size[0] / 2

    def bottom(self):
        '''得到底邊的y坐標'''
        return self.__pos[1] + self.__size[1] / 2

    def top(self):
        '''得到頂邊的y坐標'''
        return self.__pos[1] - self.__size[1] / 2

    def get_size(self):
        '''得到飛行器的寬和高的元組: (寬, 高)'''
        return self.__size

    def width(self):
        '''返回飛行器的寬度'''
        return self.__size[0]

    def height(self):
        '''返回飛行器的高度'''
        return self.__size[1]

    def pos(self):
        '''返回飛行器的中心位置'''
        return self.__pos

    def int_position(self):
        '''返回飛行器的中心位置座標'''
        return (int(self.__pos[0]), int(self.__pos[1]))

    def move(self, offset=None):
        '''移動位置''' #直線移動
        if offset:
            self.__pos[0] += offset[0]
            self.__pos[1] += offset[1]
        else:
            self.__pos[0] += self.__speed[0]
            self.__pos[1] += self.__speed[1]
    def moveBee(self, offset=None):
        '''移動位置'''  #反彈移動
        
        if offset:
            self.__pos[0] += offset[0]
            self.__pos[1] += offset[1]
            
        else: 
            if self.__pos[0]>470:
                self.bee=1
            if self.__pos[0]<20:
                self.bee=0
            if self.bee==1:
                self.__pos[0] -= self.__speed[1]
                self.__pos[1] += self.__speed[1]
            else:
                self.__pos[0] += self.__speed[1]
                self.__pos[1] += self.__speed[1]

    def is_touch(self, other):
        '''檢測兩個物體是否碰撞。如果碰撞返回True,否則返回False'''
        if self.bottom() < other.top():
            return False
        if self.top() > other.bottom():
            return False
        if self.left() > other.right():
            return False
        if self.right() < other.left():
            return False
        return True

class FlyingImageManager:
    '''此類的對像只負責處理飛行過程中圖片及圖片的自動切換，但並不關心圖片位置'''
    def __init__(self, canvas, image_id, position=None):
        self.__canvas = canvas  # 画布
        self.__image_id = image_id  # 图片ID
        self.__position = list(position)
        
        if position:
            canvas.coords(image_id, *position)

    def draw(self, position=None):
        '''更新圖片，並刷新圖片及更新圖片位置
        args 如果不為空，則記錄當前的新位置
        '''
        if position is None:
            return
        if self.__position != position:
            self.__canvas.coords(self.__image_id, *position)
            self.__position[:] = position

class DestroyImageAnimate:
    '''此對象負責處理圖片切換，但並不關心圖片位置'''
    def __init__(self, canvas, image_id, images, *, tick_times=5, callback=None):
        self.__canvas = canvas  # 畫布
        self.__image_id = image_id  # 圖片ID
        self.__images = images  # 要切換的圖
        self.__tick_times = tick_times  # ticks 為切換圖片的時間／默認為10/25秒換一張片
        self.__callback = callback  # 圖片插放完比畢後觸發回調

        self.__position = None
        self.__image_index = 0  # 當前圖片的索引
        self.__canvas.itemconfigure(self.__image_id, image=images[0])
        self.__cur_ticks = 0

    def draw(self, position=None):
        '''
        更新圖片，並刷新圖片及更新圖片位置
        args 如果不為空，則記錄當前的新位置
        '''
        self.__cur_ticks += 1
        if self.__cur_ticks >= self.__tick_times:  # 需要更新圖片 或停止動畫
            self.__cur_ticks = 0
            self.__image_index += 1
            if self.__image_index >= len(self.__images):
                # 終止動畫
                if self.__callback:
                    self.__callback()
            else:
                # 更新畫面
                self.__canvas.itemconfigure(self.__image_id, image=self.__images[self.__image_index])

        if self.__position != position:
            self.__canvas.coords(self.__image_id, position)
            self.__position = position




class Aerocraft(Arm):
    '''此類是飛行器類的基類，用來檢測飛行器的碰撞條件等'''
    NORMAL = 1  # 正常飛行狀態
    DESTROY = 2  # 被擊中狀態，正在銷毀中
    def __init__(self, canvas, position=None, image=None, destroy_images=[], destroy_cb=None, **kwargs):
        self.__status = self.NORMAL  # 設置飛行狀態為正常飛行

        self.__canvas = canvas
        # 先算出飛機的寬和高
        size = (image.width(), image.height())
        if position is None:
            # 隨機指定飛機的位置
            x = random.randint(int(image.width() / 2), int(canvas.width() - image.width() / 2))
            y = -int(image.height() / 2)
            # 設置飛機的初始圖片
            position = [x, y]
        self.__image_id = canvas.create_image(position, image=image)
        self.__image = image
        self.__destroy_images = destroy_images
        self.__destroy_cb = destroy_cb

        # 把飛機的初始放在圖片的上部 (x坐標，y軸坐標)
        super().__init__(position=position, size=size, **kwargs)


        # 正常飛行時採用正常飛行圖片管理器
        self.__image_manager = FlyingImageManager(canvas,
                                                    self.__image_id,
                                                    position)
        
    def set_image_manager(self, image_manager):
        self.__image_manager = image_manager

    def get_image_manager(self):
        return self.__image_manager

    def get_image_id(self):
        return self.__image_id

    def is_flying(self):
        '''判斷是否是正常飛行狀態'''
        return self.__status == self.NORMAL

    def is_destroy(self):
        '''判斷是否是擊中銷毀狀態'''
        return self.__status == self.DESTROY
    def set_destroy(self):
        '''設置為擊中銷毀狀態'''
        self.__status = self.DESTROY
        self.__image_manager = DestroyImageAnimate(self.__canvas,
                                                    self.__image_id,
                                                    self.__destroy_images,
                                                    callback=self.destory_self)
    
    def destory_self(self):
        self.__canvas.delete(self.__image_id)
        self.__image_manager = None
        if self.__destroy_cb:
            self.__destroy_cb(self)
    
    def moving_now(self):
        return self.move()
    def on_timer(self):
        if self.is_flying():
            self.moving_now()
            self.__image_manager.draw(self.pos())
            
            # 銷毀飛機對象
            if self.pos()[1] > self.__canvas.height() + self.height() / 2:
                self.destory_self()
        elif self.is_destroy():
            if self.__image_manager:
                self.__image_manager.draw()
class AerocraftBee(Aerocraft):
    #另外一台敵機機類
    def moving_now(self):
        return self.moveBee()

