#!/usr/bin/env python3
# yuhun.py
"""
组队御魂副本
仅支持进行中的组队副本
"""

import time
import pyautogui

from . import window
from .function import Function
from mysignal import global_ms as ms

'''
组队界面-协战队伍
xiezhanduiwu.png
挑战按钮
tiaozhan.png
队员2
passenger_2.png
队员3
passenger_3.png
对局进行中
fighting.png
御魂副本结算按钮
yuhun_victory.png
'''


class YuHun(Function):
    """组队御魂副本"""

    def __init__(self):
        self.picpath = 'yuhun'  # 图片路径
        self.m = 0  # 当前次数
        self.n = None  # 总次数
        self.flag_driver = False  # 是否为司机（默认否）
        self.flag_passengers = 2  # 组队人数
        self.flag_passenger_2 = False  # 队员2就位
        self.flag_passenger_3 = False  # 队员3就位
        self.flag_driver_start = False  # 司机待机
        self.flag_fighting = False  # 是否进行中对局（默认否）

    def title(self):
        """场景"""
        flag_title = True  # 场景提示
        while 1:
            if self.judge_scene(f'{self.picpath}/xiezhanduiwu.png', '[SCENE] 组队御魂准备中'):
                self.flag_driver_start = True
                return True
            elif self.judge_scene(f'{self.picpath}/fighting.png', '[SCENE] 组队御魂进行中'):
                self.flag_fighting = True
                return True
            elif flag_title:
                flag_title = False
                ms.text_print_update.emit('[WARN] 请检查游戏场景')

    def finish(self):
        """结算"""
        while 1:
            x, y = self.get_coor_info_picture(f'{self.picpath}/yuhun_victory.png')
            if x != 0 and y != 0:
                ms.text_print_update.emit('结算中')
                break
        self.random_sleep(2, 4)
        x, y = self.random_finish_left_right(False)
        while 1:
            pyautogui.moveTo(x + window.window_left, y + window.window_top, duration=0.25)
            pyautogui.doubleClick()
            if self.result():
                while 1:
                    self.random_sleep(1, 2)
                    pyautogui.click()
                    self.random_sleep(1, 2)
                    x, y = self.get_coor_info_picture('victory.png')
                    if x == 0 or y == 0:
                        break
                break
            self.random_sleep(0, 1)

    def run(self, n: int, flag_driver: bool = False, flag_passengers: int = 2):
        """
        :param n: 次数
        :param flag_driver: 是否司机（默认否）
        :param flag_passengers: 人数（默认2人）
        """
        x: int
        y: int
        self.flag_driver = flag_driver
        self.flag_passengers = flag_passengers
        time.sleep(2)
        self.n = n
        time_progarm = self.TimeProgram()  # 程序计时
        time_progarm.start()
        if self.title():
            ms.text_num_update.emit(f'0/{self.n}')
            while self.m < self.n:
                self.flag_passenger_2 = False
                self.flag_passenger_3 = False
                # 司机
                if self.flag_driver and self.flag_driver_start:
                    ms.text_print_update.emit('等待队员')
                    # 队员2就位
                    while 1:
                        x, y = self.get_coor_info_picture(f'{self.picpath}/passenger_2.png')
                        if x == 0 and y == 0:
                            self.flag_passenger_2 = True
                            ms.text_print_update.emit('队员2就位')
                            break
                    # 是否3人组队
                    if self.flag_passengers == 3:
                        while 1:
                            x, y = self.get_coor_info_picture(f'{self.picpath}/passenger_3.png')
                            if x == 0 and y == 0:
                                self.flag_passenger_3 = True
                                ms.text_print_update.emit('队员3就位')
                                break
                    # 开始挑战
                    self.judge_click(f'{self.picpath}/tiaozhan.png', dura=0.25)
                    ms.text_print_update.emit('开始')
                if not self.flag_fighting:
                    self.judge_click(f'{self.picpath}/fighting.png', False)
                    self.flag_fighting = False
                    ms.text_print_update.emit('对局进行中')
                self.finish()
                self.m += 1
                ms.text_num_update.emit(f'{self.m}/{self.n}')
                time.sleep(2)
        text = f"已完成 组队御魂副本{self.m}次"
        time_progarm.end()
        text = text + " " + time_progarm.print()
        ms.text_print_update.emit(text)
        # 启用按钮
        ms.is_fighting_update.emit(False)
