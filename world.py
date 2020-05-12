#world.py
# -*- coding:utf-8 -*-
from tkinter import *
import random
import images
from Airplane import *
from Bee import *
from BigAirplane import *
from sky import *
from Hero import *


class MainApp:
    def main(self):
        self.__root=Tk()
        self.__root.title("飛機大戰")
        self.__canvas=SkyCanvas(self.__root,width=480,height=720)
        self.__canvas.pack()
        self.__timer_list=TimerList()
        #創建背景
        self.create_backgound()
        #創建生命
        self.__life_count = 3
        self.__plane_label=PlaneLabel(self.__canvas,\
            count=self.__life_count)
        #創建得分
        self.__score=0
        self.__score_label=ScoreLabel(self.__canvas)
        #刷新時間
        self.__timer_interval=40 #(40毫秒)
        #調高遊戲難度
        self.__tick_count=0
        #創建按鍵列表
        
                # #創建按鈕
        
        self.__pause_btn=PauseButton(self.__canvas,callback=self.pause_game)
        self.__event_list=EventList()
        self.__event_list.append(self.__pause_btn)
        ##創建英雄機
        self.create_new_hero()
        ##創建敵人
        self.__enemy_list=GameList()
        self.__enemy_listhp=GameList()
        self.__enemy_listtwo=GameList()
        self.__random_list=[EnemyPlane1]*10+[EnemyPlane2]*3+\
        [EnemyPlane3]+[EnemyPlane1_2]*2
        self.__min_list_len=len(self.__random_list)
        self.__random_list.extend([None]*500)
        # #遊戲開始
        # self.start_timer()
        #按鍵控制
        self.__root.bind('<Key>',lambda event:
            self.__event_list.on_key_down(event)) 
        self.__root.bind('<KeyRelease>',lambda event:
            self.__event_list.on_key_up(event)) 
        self.__root.bind('<Button>',lambda event:
            self.__event_list.on_mouse_down(event))
        self.__root.bind('<Motion>',lambda event:
            self.__event_list.on_mouse_move(event))
        self.__root.bind('<ButtonRelease>',lambda event:
            self.__event_list.on_mouse_up(event))
        #創建遊戲開始畫面
        self.__start_window=StartWindow(self.__canvas,start_callback=
        	self.start_game,destroy=self.destroy_object)
        self.__event_list.append(self.__start_window)

        
        self.__root.mainloop()
					
    def create_backgound(self):
        self.__background = Background(self.__canvas)
        self.__timer_list.append(self.__background)

    def create_new_hero(self):
        self.__hero_plane = hero_plane = HeroPlane(self.__canvas, destroy_cb=self.hero_crush)            
        self.__event_list.append(hero_plane)
        self.__timer_list.append(hero_plane)
        self.__life_count -= 1
        self.__plane_label.set_count(self.__life_count)

    def destroy_object(self, obj):
        """刪除對象"""
        
        self.__enemy_listhp.remove(obj)
        
        self.__enemy_listtwo.remove(obj)
        self.__enemy_list.remove(obj)
        
        self.__timer_list.remove(obj)
        self.__event_list.remove(obj) 
        
    def start_game(self):
        self.__timer_list.append(self.__start_window)
        self.__event_list.remove(self.__start_window)
        del self.__start_window  
        self.start_timer()  

    def random_enemys(self):
        r=random.randint(0,len(self.__random_list)-1)
        plane =self.__random_list[r]
        
        if plane:

            if 9< r < 13:
                ep = plane(self.__canvas, destroy_cb=self.destroy_object)
                self.__timer_list.append(ep)
                self.__enemy_listhp.append(ep)

            elif r==13:
                ep = plane(self.__canvas, destroy_cb=self.destroy_object)
                self.__timer_list.append(ep)
                self.__enemy_listtwo.append(ep)
            else:
                ep = plane(self.__canvas, destroy_cb=self.destroy_object)
                self.__timer_list.append(ep)
                self.__enemy_list.append(ep)

    def hero_crush(self, obj):
        #'''飛機墜落'''
        # print('''飛機墜落''')

        self.destroy_object(self.__hero_plane)

        self.__hero_plane = None

        if self.__life_count > 0:
            self.create_new_hero()
            # print("剩餘生命數為:", self.__life_count)
        else:
            self.game_over()         

    def game_over(self):
        self.stop_timer()
        self.__event_list.clear()
        self.__timer_list.clear()
        self.__enemy_list.clear()
        self.__enemy_listhp.clear()
        self.__enemy_listtwo.clear()
        self.__image = images.load_image("gameover.gif")
        self.__images_id = self.__canvas.create_image(self.__canvas.width() / 2, self.__canvas.height() / 2,
                                                      image=self.__image)
        
        print("遊戲結束")

    def pause_game(self):
        # print("遊戲已暫暫停....")
        self.stop_timer()
        
        self.resume_widget = ResumeWidet(self.__canvas, resume_cb=self.begin_resume_game, destroy_cb=self.resume_game)
        self.__event_list.append(self.resume_widget)
        
    def begin_resume_game(self):
        '''開始恢復遊戲進入恢復倒計時'''
        # print("遊戲開始恢復!!!!!")
        self.__event_list.remove(self.resume_widget)
        self.__timer_list.append_head(self.resume_widget)
        self.start_timer()
        
    def resume_game(self):
        '''已恢復，正式開戰'''
        # print("遊戲已恢復!!!!!")
        self.__timer_list.remove(self.resume_widget)
        del self.resume_widget
        
    def increase_score(self, score):
        self.__score += score
        if score:
            self.__score_label.set_score(self.__score)
    def increase_life(self, life):
        self.__life_count += life
        if life:
            self.__plane_label.set_count(self.__life_count)
    def on_timer(self):
        # 再次啟動定時器
        self.timer_id = self.__canvas.after(self.__timer_interval, self.on_timer)  
        # 讓定時器重複啟動
        self.on_timer_tick()
        self.__tick_count += 1
        if self.__tick_count == 25:
            self.__tick_count = 0
            self.on_timer_levelup()
    def start_timer(self):
        # print("已啟動定時器")
        self.timer_id = self.__canvas.after(self.__timer_interval, self.on_timer)

    def stop_timer(self):
        # 取消定時器
        self.__canvas.after_cancel(self.timer_id)  
        # print("定時器已取消!")

    def on_timer_tick(self):
        '''定時器觸發時調用此方法'''
        # 刷新背景圖
        if self.__timer_list.on_timer():
            return
        # 隨機生成敵機
        self.random_enemys()
        # 檢測飛機得分及飛機是否飛機被摧毀
        if self.__hero_plane:
            score = self.__hero_plane.check_attack(self.__enemy_list.get_objs())
            self.increase_score(score)
            score2 = self.__hero_plane.check_attack(self.__enemy_listhp.get_objs())
            self.increase_life(score2)
            self.increase_score(score2)
            score3 = self.__hero_plane.check_attack(self.__enemy_listtwo.get_objs())
            self.__hero_plane.firetwo+=score3*20
            self.increase_score(score3)
    def on_timer_levelup(self):
        '''定時器每秒鐘調用一次此方法''' #刪掉尾巴None,已增加遊戲難度
        if len(self.__random_list) > self.__min_list_len:
            self.__random_list.pop()


if __name__ == '__main__':
    app = MainApp()
    app.main()