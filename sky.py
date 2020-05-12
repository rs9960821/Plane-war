#sky.py
# -*- coding:utf-8 -*-
import images
from tkinter import *

class GameList:
    def __init__(self):
        self.__objs = []

    def append(self, obj):
        # "把需要觸發鍵盤鼠標事件的地像加入到列表的末尾"
        self.__objs.append(obj)
    
    def remove(self, obj):
        for i, o in enumerate(self.__objs):
            if o is obj:
                del self.__objs[i]
                return

    def get_objs(self):
        return self.__objs        
    
    def clear(self):
        self.__objs.clear()
class EventObject:
    '''事件對像類，此類的子類對象將存放於事件列表中待觸發相應的事件'''
    def on_key_down(self, event):
        '''處理按鍵按下'''

    def on_key_up(self, event):
        '''處理按鍵抬起'''

    def on_mouse_down(self, event):
        '''處理鼠標左鍵按鍵按下'''
    
    def on_mouse_up(self, event):
        '''處理鼠標左鍵按鍵抬起'''

    def on_mouse_move(self, event):
        '''處理鼠標左鍵按下的同時移動'''

class EventList(GameList):
    '''事件列表類，此列表保存需要處理鍵盤事件和鼠標事件的類'''
    def __init__(self):
        super(EventList, self).__init__()

    def on_key_down(self, event):
        '''處理按鍵按下'''
        for obj in reversed(self.get_objs()):
            if obj.on_key_down(event):
                return

    def on_key_up(self, event):
        '''處理按鍵抬起'''
        for obj in reversed(self.get_objs()):
            if obj.on_key_up(event):
                return

    def on_mouse_down(self, event):
        '''處理鼠標左鍵按鍵按下'''
        for obj in reversed(self.get_objs()):
            if obj.on_mouse_down(event):
                return
    
    def on_mouse_up(self, event):
        '''處理鼠標左鍵按鍵抬起'''
        for obj in reversed(self.get_objs()):
            if obj.on_mouse_up(event):
                return

    def on_mouse_move(self, event):
        '''處理鼠標左鍵按下的同時移動'''
        for obj in reversed(self.get_objs()):
            if obj.on_mouse_move(event):
                return

class TimerList(GameList):
    def on_timer(self):
        for obj in self.get_objs():
            if obj.on_timer():
                return True

    def append_head(self, obj):
        # "把觸發事件對象插放在頭部位置"
        lst = self.get_objs()
        lst.insert(0, obj)

class Background:
    '''此類用於描述背景對象'''
    def __init__(self, canvas, speed=1):
        self.__image = images.load_image("background.png")
        self.__canvas = canvas
        self.__speed = speed
        self.__image_height = image_height = self.__image.height()
        self.__images_pos = [[0, 0], [0, -image_height]]
        self.__images_id = [self.__canvas.create_image(*pos,image=self.__image,anchor="nw") for pos in self.__images_pos]
    def on_timer(self):
        '''刷新背景'''
        for pos in self.__images_pos:
            pos[1] += self.__speed
            if pos[1] > self.__image_height:
                pos[1] -= self.__image_height * 2
        for i, pos in enumerate(self.__images_pos):
            self.__canvas.coords(self.__images_id[i], *pos)

class PauseButton(EventObject):
    '''此類用於描述暫停控件'''   

    def __init__(self, canvas, callback=None):
        self.__image_pause = images.load_image("game_pause_nor.png")
        self.__canvas = canvas
        self.__click_cb = callback
        self.__size = (self.__image_pause.width(), self.__image_pause.height())  # 寬和高(元組)
        self.__pos = (self.__image_pause.width() * .75, self.__image_pause.height() * .75)
        self.__images_id = self.__canvas.create_image(self.__pos,image=self.__image_pause)

    def on_key_down(self, event):
        '''處理按鍵按下'''
        if event.keysym == 'p':
            if self.__click_cb:
                self.__click_cb()
                return True

    def is_touch(self, x, y):
        if y > self.__pos[1] + self.__size[1] / 2:
            return False
        if x < self.__pos[0] - self.__size[0] / 2:
            return False
        if x > self.__pos[0] + self.__size[0] / 2:
            return False
        if y < self.__pos[1] - self.__size[1] / 2:
            return False
        return True

    def on_mouse_down(self, event):
        '''處理鼠標左鍵按鍵按下'''
        if event.num == 1 and self.is_touch(event.x, event.y):
            if self.__click_cb:
                self.__click_cb()
                return True
class ResumeWidet(EventObject):
    '''此類用於描述臨停窗口'''
    # 此窗口的狀態:
    # NORMAL = 1 # 顯示狀態
    # DESTROY = 2 # 銷毀狀態
    def __init__(self, canvas, resume_cb=None, destroy_cb=None):
        # 設置顯示狀態
        self.__image = images.load_image("pause.gif")
        self.__canvas = canvas
        self.__image_id = self.__canvas.create_image(canvas.width() / 2, canvas.height() / 2,image=self.__image)                                                     
        self.__resume_cb = resume_cb
        self.__destroy_cb = destroy_cb
        self.__destroy_count = 75
    def resume(self):
        if self.__resume_cb:
            self.__resume_cb()
        self.__canvas.delete(self.__image_id)
        self.__image_id = self.__canvas.create_text(self.__canvas.width() / 2,self.__canvas.height() / 2,
                                             text="3",font=("標楷體", 200), fill='yellow')
                                             
    def on_key_down(self, event):
        '''處理按鍵按下'''
        if event.keysym == 'r':
            self.resume()
        return True

    def on_mouse_down(self, event):
        '''處理鼠標左鍵按鍵按下'''
        if event.num == 1:
            self.resume()
        return True

    def on_timer(self):
        self.__destroy_count -= 1
        if self.__destroy_count % 25 == 0:
            n = self.__destroy_count // 25
            self.__canvas.itemconfigure(self.__image_id, text=str(n))
        if self.__destroy_count <= 0:
            self.__canvas.delete(self.__image_id)
            if self.__destroy_cb:
                self.__destroy_cb()
        return True
class StartWindow(EventObject):
    """此類用於實現開始窗口對象"""
    # 此窗口的狀態:
    NORMAL = 1  # 顯示狀態
    DESTROY = 2  # 銷毀狀態

    def __init__(self, canvas, start_callback=None, destroy=None):
        self.__images = [images.load_image("start2.gif")]
        self.__status = self.NORMAL  # 設置顯示狀態
        self.__canvas = canvas
        self.__start_fn = start_callback
        self.__destroy_cb = destroy
        # 畫布尺寸
        self.__pos = [self.__canvas.width() / 2, self.__canvas.height() / 2 + 3]

        # 設置飛機的初始圖片
        self.__image_id = canvas.create_image(self.__pos, image=self.__images[0])
        self.__start_id = canvas.create_image(self.__pos[0], self.__pos[1] + 20, image=self.__images[0])            
    def move(self, offset):
        '''根據偏移量移動，當超出範圍時較正位置'''
        self.__pos[0] += offset[0]
        self.__pos[1] += offset[1]

    def start_game(self):
        self.__start_fn()
        self.__status = self.DESTROY

    def on_key_down(self, event):
        '''處理按鍵按下'''
        if event.keysym == 'space':
            self.start_game()
            return True

    def on_mouse_down(self, event):
        '''處理鼠標左鍵按鍵按下'''
        if event.num == 1:
            self.start_game()
            return True

    def on_timer(self):
        self.move((0, -20))
        self.__canvas.coords(self.__image_id, self.__pos)
        self.__canvas.coords(
            self.__start_id, self.__pos[0], self.__pos[1] + 20)
        # 調試用
        if self.__pos[1] < -500 and self.__destroy_cb:
            self.__canvas.delete(self.__image_id)
            self.__canvas.delete(self.__start_id)
            self.__destroy_cb(self)
class PlaneLabel:
    '''此類用於描述飛機個數的圖片控件'''
   
    def __init__(self, canvas, count=0):
        self.__image = images.load_image("plane_count.gif")
        self.__canvas = canvas
        image = self.__image
        self.__pos = position = (
            image.width() * 0.75, canvas.height() - image.height() * 0.75)
        self.__images_id = self.__canvas.create_image(position,
                                                      image=self.__image)
        self.__size = size = (image.width(), image.height())  # 寬和高(元組)

        self.count=count
        self.__font_id = canvas.create_text(position[0],
                                            position[1]+20,
                                            text=self.__get_str(self.count),
                                            font=("標楷體", 18),
                                            fill='#FF0000')

    def set_count(self, count):
        self.count=count
        self.__canvas.itemconfigure(self.__font_id, text=self.__get_str(self.count))
        self.__canvas.tag_raise(self.__images_id)
        self.__canvas.tag_raise(self.__font_id)
    def __get_str(self, n):
        return "x" + str(n)
class ScoreLabel:
    '''此類用於描述得到條'''
    def __init__(self, canvas):
        self.__canvas = canvas
        self.__pos = position = (canvas.width()*4/5, 630)
        text = self.__get_str(0)
        self.__font_id = canvas.create_text(position,text=text,font=("標楷體", 30),fill='#FF0000')


    def set_score(self, s):
        self.__canvas.itemconfigure(self.__font_id, text=self.__get_str(s))

    # @staticmethod
    def __get_str(self,n):
        return "得分:" + str(n)
#https://www.runoob.com/python/python-tk-canvas.html
class SkyCanvas(Canvas):
    '''遊戲天空畫布類
    此類用於創建空戰地圖畫布對象，此畫布用於顯示飛機對象，子彈對像等
    '''
    def __init__(self, parent, *args, **kwargs):
        super(SkyCanvas, self).__init__(parent, *args, **kwargs)
        # 畫布尺寸
        self.__width = kwargs.get('width', 100)
        self.__height = kwargs.get('height', 100)

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def top(self):
        return 0

    def bottom(self):
        return self.__height

    def left(self):
        return 0

    def right(self):
        return self.__width
    