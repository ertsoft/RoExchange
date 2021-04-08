import tkinter as tk
from PIL import ImageTk, Image
import math
from datetime import datetime


class Clock(tk.Canvas):
    def __init__(self, parent, highlightthickness, width, height, img):
        tk.Canvas.__init__(self, parent, highlightthickness=highlightthickness)

        self.width = width
        self.height = height
        self.configure(width=self.width, height=self.height)

        self.img = Image.open(img)
        self.image = ImageTk.PhotoImage(self.img.resize((300, 300), Image.ANTIALIAS))
        self.create_image(0, 0, image=self.image, anchor='nw')

        self.sec_old = self.create_line((150, 150), (200, 40), width=2, fill='black')
        self.update_sec(1)

        self.now = datetime.now()
        real_hour = int(self.now.strftime('%I'))
        """ the hours line must be at the real_hour that have (init_x, init_y) coordinates """
        h_angle = (3 - real_hour) * 30 if real_hour < 3 else 360 - (real_hour - 3) * 30
        init_x_for_hour = 150 + 70 * math.cos(h_angle * math.pi / 180)  # init_x != center_x     # init_y != center_y
        if 9 >= real_hour >= 3:
            init_y_for_hour = math.sqrt(70 ** 2 - (init_x_for_hour - 150) ** 2) + 150
        else:
            init_y_for_hour = abs(math.sqrt(70 ** 2 - (init_x_for_hour - 150) ** 2) - 150)
        self.h_old = self.create_line((150, 150), (init_x_for_hour, init_y_for_hour), width=7)
        self.update_h()

        real_min = int(self.now.strftime('%M'))
        m_angle = (15 - real_min) * 6 if 15 >= real_min >= 1 else 360 - (real_min - 15) * 6
        init_x_for_min = 150 + 120 * math.cos(m_angle * math.pi / 180)

        if 45 >= real_min >= 15:
            init_y_for_min = math.sqrt(120 ** 2 - (init_x_for_min - 150) ** 2) + 150
        else:
            init_y_for_min = abs(math.sqrt(120 ** 2 - (init_x_for_min - 150) ** 2) - 150)
        self.m_old = self.create_line((150, 150), (init_x_for_min, init_y_for_min), width=6)
        self.update_min()

    def update_sec(self, i):
        def del_sec():
            self.delete(self.sec_old)
            self.after(1000, del_sec)

        del_sec()

        angle_in_radians = i * 6 * math.pi / 180
        line_length = 121
        center_x = 150
        center_y = 150
        x_end = center_x + line_length * math.cos(angle_in_radians)
        y_end = center_y + line_length * math.sin(angle_in_radians)
        sec_new = self.create_line((150, 150), (x_end, y_end), width=2)
        if i < 61:
            i += 1
            self.after(1000, lambda: self.update_sec(i))
        else:
            i = 1
            self.after(1000, lambda: self.update_sec(i))

        self.sec_old = sec_new

    def update_h(self):
        def del_h():
            self.delete(self.h_old)
            self.after(3600000, del_h)

        del_h()

        real_time = datetime.now()
        hour = int(real_time.strftime('%I'))

        angle_in_radians = (3 - hour) * 30 if hour < 3 else 360 - (hour - 3) * 30
        x_end = 150 + 70 * math.cos(angle_in_radians * math.pi / 180)
        if 9 >= hour >= 3:
            y_end = math.sqrt(70 ** 2 - (x_end - 150) ** 2) + 150
        else:
            y_end = abs(math.sqrt(70 ** 2 - (x_end - 150) ** 2) - 150)
        h_new = self.create_line((150, 150), (x_end, y_end), width=7)

        self.after(3600000, self.update_h)

        self.h_old = h_new

    def update_min(self):
        def del_m():
            self.delete(self.m_old)
            self.after(60000, del_m)

        del_m()

        real_time = datetime.now()
        mins = int(real_time.strftime('%M'))
        ang = (15 - mins) * 6 if 15 >= mins >= 1 else 360 - (mins - 15) * 6
        x_end = 150 + 120 * math.cos(ang * math.pi / 180)
        if 45 >= mins >= 15:
            y_end = math.sqrt(120 ** 2 - (x_end - 150) ** 2) + 150
        else:
            y_end = abs(math.sqrt(120 ** 2 - (x_end - 150) ** 2) - 150)
        m_new = self.create_line((150, 150), (x_end, y_end), width=6)

        self.after(60000, self.update_min)

        self.m_old = m_new

