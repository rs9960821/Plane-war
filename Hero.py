#Hero.py
# -*- coding:utf-8 -*-
import images
from FlyingObject import *
from Bullet import Bullet
from sky import *

class HeroPlaneImageManager:
    '''此對象負責處理圖片切換，但並不關心圖片位置'''
    def __init__(self, canvas, image_id, images, position=None):
        self.__canvas = canvas  # 畫布
        self.__image_id = image_id  # 圖片ID
        self.__images = images  # 要切換的圖
        self.__position = position

        self.__accelerator = False  # 加速狀態(默認不加速)
        self.__will_accelerator = False  # 下次更新時要轉換的狀態狀態
        if position:
            canvas.coords(image_id, *position)

    def set_acelerator(self, will=True):
        '''設置加速狀態'''
        self.__will_accelerator = will  # 設置即要觸發指令

    def draw(self, position):
        '''
        更新圖片，並刷新圖片及更新圖片位置
        args 如果不為空，則記錄當前的新位置
        '''
        if self.__accelerator != self.__will_accelerator:  # 狀態有所變量
            # 需發重新設置圖片
            if self.__will_accelerator:
                self.__canvas.itemconfigure(
                    self.__image_id, image=self.__images[1])
            else:
                self.__canvas.itemconfigure(
                    self.__image_id, image=self.__images[0])
            self.__accelerator = self.__will_accelerator  # 狀態切換完畢
        if self.__position != position:
            self.__canvas.coords(self.__image_id, *position)
            self.__position = position









class HeroPlane(Arm):
    #"""此類是英雄飛機類,此類繼承自飛機對象，所有的飛機地像有相同的行為:移動、發射子彈等的對像是一個或多個同樣的英雄飛機""" 
    # 飛機的狀態:
    NORMAL = 1  # 正常飛行狀態
    DESTROY = 2  # 被擊中狀態，正在銷毀中

    def __init__(self, canvas, destroy_cb=None):
        self.__images = [
        images.load_image("hero2.png"),
        images.load_image("hero1.png"),
        images.load_image("hero_blowup_n1.png"),
        images.load_image("hero_blowup_n2.png"),
        images.load_image("hero_blowup_n3.png"),
        images.load_image("hero_blowup_n4.png"),
        images.load_image("hero_blowup_n5.png"),
        images.load_image("hero_blowup_n8.png"),
        images.load_image("hero_blowup_n9.png")
    ]
        self.__status = self.NORMAL  # 設置飛行狀態為正常飛行
        self.__canvas = canvas
        self.__destroy_cb = destroy_cb
        self.firetwo = 0
        image = self.__images[0]
        # self.old_image = self.new_image = self.__images[0]  # 設置當前顯示圖片

        # 畫布尺寸
        canvas_width = canvas.width()
        canvas_height = canvas.height()

        # 計算飛機能夠飛行的的上下左右邊緣
        self.__left_side = image.width()/2  # 左邊緣
        self.__right_side = canvas_width - image.width()/2  # 右邊緣
        self.__top_side = image.height()/2  # 上邊緣
        self.__bottom_side = canvas_height - image.height()/2  # 下邊緣

        # 把飛機的初始放在圖片的底部 (x坐標，y軸坐標)
        x = int(canvas_width / 2)
        y = int(canvas_height - image.height() / 2)
        pos = (x, y)
        size = (image.width(), image.height())
        super().__init__(position=pos, size=size)

        # 此集合用於存放用戶操作的按鍵或鼠標事件
        self.__key_evens = set()

        # 設置飛機的初始圖片
        self.__image_id = canvas.create_image(pos, image=image)

        # 正常飛行時採用正常飛行圖片管理器
        self.__image_manager = HeroPlaneImageManager(canvas,
                                                     self.__image_id,
                                                     self.__images[:2],
                                                     pos)
        # 鼠標的按下狀態
        self.__mouse_down = False

        # -----子彈相關----
        
        self.__bullet_list = TimerList()
        self.__bullet_interval = 7  # 每秒鐘2.8 發子彈(40X7=350毫秒 1 發子彈)
        self.__bullet_count = 0  # 子彈計數
        
    def destory_self(self):
        self.__image_manager = None
        self.__canvas.delete(self.__image_id)
        self.__bullet_list.clear()
        if self.__destroy_cb:
            self.__destroy_cb(self)

    def is_flying(self):
        '''判斷是否是正常飛行狀態'''
        return self.__status == self.NORMAL

    def is_destroy(self):
        '''判斷是否是擊中銷毀狀態'''
        return self.__status == self.DESTROY

    def set_destroy(self):
        '''設置為擊中銷毀狀態'''
        self.__status = self.DESTROY
        self.__image_manager = DestroyImageAnimate(
            self.__canvas, self.__image_id, self.__images[2:],
            callback=self.destory_self)

    def __adjust_pos(self, position):
        '''校正飛機的坐標，如果超出地圖，則修改正回來'''
        x, y = position
        if x < self.__left_side:
            x = self.__left_side
        if x > self.__right_side:
            x = self.__right_side
        if y < self.__top_side:
            y = self.__top_side
        if y > self.__bottom_side:
            y = self.__bottom_side
        super().set_position((x, y))

    def set_position(self, position):
        self.__adjust_pos(position)

    def move(self, offset):
        '''根據偏移量移動，當超出範圍時較正位置'''
        x, y = self.pos()
        x += offset[0]
        y += offset[1]
        self.__adjust_pos((x, y))
        
        try:
            if offset[1] < 0:
                
                self.__image_manager.set_acelerator()
            else:
                
                self.__image_manager.set_acelerator(False)
        except:
            pass
    def on_key_down(self, event):
        '''處理按鍵按下'''
        # 當有銨鍵按下,把按鍵加入到集合中記錄下來
        self.__key_evens.add(event.keysym.lower())

    def on_key_up(self, event):
        '''處理按鍵抬起'''
        # 當有銨鍵抬起,把按鍵從集合中移除
        self.__key_evens.discard(event.keysym.lower())

    def on_mouse_down(self, event):
        '''處理鼠標左鍵按鍵按下'''
        if event.num == 2:
            # self.set_destroy()
            self.fire()
            return
        if event.num != 1:
            return

        self.__mouse_down = True
        self.mouse_pos = (event.x, event.y)

    def on_mouse_up(self, event):
        '''處理鼠標左鍵按鍵抬起'''
        if event.num != 1:
            return
        self.__mouse_down = False
        if self.is_flying():
            self.__image_manager.set_acelerator(False)

    def on_mouse_move(self, event):
        '''處理鼠標左鍵按下的同時移動'''
        if not self.__mouse_down:
            return
        offset = (event.x - self.mouse_pos[0], event.y - self.mouse_pos[1])
        self.mouse_pos = (event.x, event.y)  # 用新位置替換舊位置
        self.move(offset)

    def process_key_event(self):
        '''檢查鍵盤狀態，計算飛機飛行移動位置'''
        if self.is_destroy():  # 如果飛機已被擊中，鍵槃無效
            return
        if self.__mouse_down:
            return

        assert self.is_flying()
        speed = 10
        self.__image_manager.set_acelerator(False)
        if 'a' in self.__key_evens or 'left' in self.__key_evens:
            self.move((-speed, 0))
        if 'd' in self.__key_evens or 'right' in self.__key_evens:
            self.move((speed, 0))
        if 'w' in self.__key_evens or 'up' in self.__key_evens:
            self.move((0, -speed))
            self.__image_manager.set_acelerator()
        if 's' in self.__key_evens or 'down' in self.__key_evens:
            self.move((0, speed))

    def fire(self):
        '''英雄飛機開火 '''
        x, y = self.pos()
        if not self.firetwo:
            # 單子彈位置(0, -60)
            pos = (x, y-60)
            b1 = Bullet(self.__canvas, position=pos,destroy_cb=self.__bullet_list.remove)
            self.__bullet_list.append(b1)
        else:
            # 雙子彈位置(-32, -18)和 (32, -18)
            pos1 = (x-14, y-18)
            pos2 = (x+14, y-18)
            b1 = Bullet(self.__canvas, position=pos1, destroy_cb=self.__bullet_list.remove)
            b2 = Bullet(self.__canvas, position=pos2, destroy_cb=self.__bullet_list.remove)
            
            self.__bullet_list.append(b2)
            self.__bullet_list.append(b1)
            
            self.firetwo-=1



    def check_attack(self, lst):
        '''此方法檢測英雄飛機及子彈是否打印敵機，以及是否與英雄飛機進行碰幢
        返回元組:
           第一個元素: 飛機是否幢True/False
           第二個元素: 本次得分
           return (False, 20) # 本次得到20飛機沒有被幢到
        '''
        score = 0
        # 檢查子彈是否打到敵機
        i = 0
        
        bullet_list = self.__bullet_list.get_objs()
        while i < len(bullet_list):
            bullet = bullet_list[i]
            for j, ep  in enumerate(lst):
                if bullet.is_touch(ep):
                    bullet.set_destroy()
                    del lst[j]
                    ep.set_destroy()
                    score += 1
                    break
            else:
                i += 1

        # 檢查飛機是否被幢
        for i, ep in enumerate(lst):
            if self.is_touch(ep):
                ep.set_destroy()
                self.set_destroy()
                del lst[i]
                break
        return score
    def on_timer(self):
        if self.is_flying():
            self.process_key_event()  # 先處理按鍵事件
            # --- begin處理子彈是否發射---------
            self.__bullet_count += 1
            if self.__bullet_count >= self.__bullet_interval:
                self.__bullet_count = 0
                self.fire()
            # --- end 處理子彈是否發射---------
            self.__image_manager.draw(self.int_position())
        elif self.is_destroy():
            if self.__image_manager:
                self.__image_manager.draw()
        self.__bullet_list.on_timer()
