from kivy.config import Config
Config.set('graphics', 'width', '900')
Config.set('graphics', 'height', '400')

import random
from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ObjectProperty, StringProperty
from kivy.graphics import Line
from kivy.properties import Clock
from kivy.core.window import Window 
from kivy.lang import Builder
from kivy import platform
from kivy.uix.relativelayout import  RelativeLayout
from kivy.graphics import Color, Quad, Triangle
from kivy.core.audio import SoundLoader

Builder.load_file('menu.kv')

class AsosiyYuz(RelativeLayout):
    from keybordmobile import keyboard_closed, on_keyboard_down, on_keyboard_up, on_touch_down, on_touch_up 
    from transforms import transform, transform_2D, transform_3D
    chiziq_x =NumericProperty(0)
    chiziq_y =NumericProperty(0)
    main_menu = ObjectProperty()
    menu_title = StringProperty("G   A   L   A   X   Y")
    button_text = StringProperty("START")
    score_text = StringProperty("0")
    
    
    vertical_chiziq = []
    chiziq_orasi_x = 0.3
    chiziq_soni_x = 20

    horizontal_chiziq = []
    chiziq_orasi_y = 0.1
    chiziq_soni_y = 15

    animation_down = 0
    SPEED = 0.4  

    animation_down_x = 0
    SPEED_X = 2

    x_tomon_tezlik = 0 

 #   NUMBER_TILES = 1
 #   number_tiles_list = []
    tile_chiziqlar_soni = 20
    tile = []
    tile_coordinates = []

    plane = None
    plane_eni = 0.13
    plane_boyi = 0.045
    plane_bottom = 0.04

    plane_coordinates = [(0, 0), (0, 0), (0, 0)]

    loop_y = 0

    gameover_holat = False

    on_start = False
    
    galaxy_music = None
    gameover_music = None

    def __init__(self,**kwargs):
        super(AsosiyYuz,self).__init__(**kwargs)
        self.init_sound()
        self.init_vertical_chiziq()
        self.init_horizontal_chiziq()
        self.init__tiles()
        self.init_plane()
        self.oldindan_chiziq_chiqarish()
        self.generate_tile_coordinates()
        if self.bu_desktop:
            self._keyboard = Window.request_keyboard(self.keyboard_closed, self)
            self._keyboard.bind(on_key_down=self.on_keyboard_down)
            self._keyboard.bind(on_key_up=self.on_keyboard_up)
            Clock.schedule_interval(self.update, 1/90)
    def init_plane(self):
        with self.canvas:
            Color(0,0,0)
            self.plane = Triangle()

    def update_plane(self):
        center_x = self.width/2
        plane_bottom_size = self.plane_bottom * self.height
        plane_eni = self.plane_eni * self.width/2
        plane_boyi = self.plane_boyi * self.height

        self.plane_coordinates[0] = (center_x - plane_eni, plane_bottom_size)
        self.plane_coordinates[1] = (center_x, plane_bottom_size+plane_boyi)
        self.plane_coordinates[2] = (center_x + plane_eni, plane_bottom_size)

        x1, y1 = self.transform(*self.plane_coordinates[0])
        x2, y2 = self.transform(*self.plane_coordinates[1])
        x3, y3 = self.transform(*self.plane_coordinates[2])
        self.plane.points = [x1, y1, x2, y2, x3, y3]

    def init_sound(self):
        self.galaxy_music = SoundLoader.load('sound/galaxy.mp3')
        self.gameover_music = SoundLoader.load('sound/gameover.wav')
        
        self.galaxy_music.volume = 1
        self.gameover_music.volume = 0.25
            
    def restart_game(self):
        self.animation_down = 0
        self.animation_down_x = 0
        self.x_tomon_tezlik = 0
        self.loop_y = 0
        self.score_text = str(self.loop_y)
        
        self.tile_coordinates = []
        self.oldindan_chiziq_chiqarish()
        self.generate_tile_coordinates()
        self.gameover_holat = False

    def on_size(self, *args):
        # print("eni: " + str(self.width) + "bo'yi " + str(self.height))
        self.chiziq_x = self.width / 2
        self.chiziq_y = self.height * 0.75

    def oldindan_chiziq_chiqarish(self):
        for i in range(0, 10):
            self.tile_coordinates.append((0, i))
            
    def check_tile_side(self):
        for i in range(0, len(self.tile_coordinates)):
            ti_x, ti_y = self.tile_coordinates[i]
            if ti_y > self.loop_y + 1:
                return False
            if self.check_side(ti_x, ti_y):
                return True
        return False
 
    def check_side(self, ti_x, ti_y):
        xmin, ymin = self.get_tile_cordinates(ti_x, ti_y)
        xmax, ymax = self.get_tile_cordinates(ti_x+1, ti_y+1)
        for i in range(0, 3):
            px, py = self.plane_coordinates[i]
            if xmin <= px<= xmax and ymin <= py <= ymax:
                return True
        return False

    def init_vertical_chiziq(self):
        with self.canvas:
            for i in range(0, self.chiziq_soni_x):
                self.vertical_chiziq.append(Line())

    def init_horizontal_chiziq(self):
        with self.canvas:
            for i in range(0, self.chiziq_soni_y):
                self.horizontal_chiziq.append(Line())

    def get_line_x_from_index(self, index):
        orta_x = self.chiziq_x
        ora = self.chiziq_orasi_x * self.width
        joylashuv = index - 0.5
        line_x = orta_x + ora*joylashuv + self.animation_down_x
        return line_x

    def get_line_y_from_index(self, index):
        spacing_y = self.chiziq_orasi_y*self.height
        line_x = index*spacing_y-self.animation_down
        return line_x


    def get_tile_cordinates(self, ti_x, ti_y):
        ti_y = ti_y - self.loop_y
        x = self.get_line_x_from_index(ti_x)
        y = self.get_line_y_from_index(ti_y)
        return x, y

    def update_tiles(self):
        for i in range(0, self.tile_chiziqlar_soni):
            tile = self.tile[i]    
            tile_coordinates = self.tile_coordinates[i]
            xmin, ymin = self.get_tile_cordinates(tile_coordinates[0], tile_coordinates[1])
            xmax, ymax = self.get_tile_cordinates(tile_coordinates[0]+ 1, tile_coordinates[1] + 1)

            x1, y1 = self.transform(xmin, ymin)
            x2, y2 = self.transform(xmin, ymax)
            x3, y3 = self.transform(xmax, ymax)
            x4, y4 = self.transform(xmax, ymin)

            tile.points = [x1, y1, x2, y2, x3, y3, x4, y4]

    def update_vertical_chiziq(self):
        start_index = -int(self.chiziq_soni_x/2)+1

        for i in range(start_index, start_index+self.chiziq_soni_x):
            line_x = self.get_line_x_from_index(i)
            x1, y1 = self.transform(line_x, 0)
            x2, y2 = self.transform(line_x, self.height)
            self.vertical_chiziq[i].points = (x1, y1, x2, y2)
           

    def update_horizontal_chiziq(self):
        start_index = -int(self.chiziq_soni_x/2)+1
        end_index = start_index+self.chiziq_soni_x-1

        xmin = self.get_line_x_from_index(start_index)
        xmax = self.get_line_x_from_index(end_index)  

        for i in range(0,self.chiziq_soni_y):
            line_y = self.get_line_y_from_index(i)
            x1, y1 = self.transform(xmin, line_y)
            x2, y2 = self.transform(xmax, line_y)
            self.horizontal_chiziq[i].points = (x1, y1, x2, y2)

    def init__tiles(self):
        with self.canvas:
            Color(1, 1, 0)
            for i in range(0, self.tile_chiziqlar_soni):
                self.tile.append(Quad())
    def generate_tile_coordinates(self):
        last_x = 0
        last_y = 0
        for i in range(len(self.tile_coordinates)-1, -1, -1):
            if self.tile_coordinates[i][1] < self.loop_y:
                del self.tile_coordinates[i]

        if len(self.tile_coordinates) > 0:
            last_cordinates = self.tile_coordinates[-1]
            last_x = last_cordinates[0]
            last_y = last_cordinates[1] + 1
        for i in range(len(self.tile_coordinates), self.tile_chiziqlar_soni):
            randoms = random.randint(0, 2)
            start_index = -int(self.chiziq_soni_x/2)+1
            end_index = start_index+self.chiziq_soni_x-1
            if last_x <= start_index:
                randoms = 1
            if last_x >= end_index:
                randoms = 2
            self.tile_coordinates.append((last_x, last_y))
            if randoms == 1:
                last_x += 1
                self.tile_coordinates.append((last_x, last_y))
                last_y += 1
                self.tile_coordinates.append((last_x, last_y))
            if randoms == 2:
                last_x -= 1
                self.tile_coordinates.append((last_x, last_y))
                last_y += 1
                self.tile_coordinates.append((last_x, last_y))
            last_y +=1

    def bu_desktop(self):
        if platform in("win", "macosx", "linux"):
            return True
        return False

    def update(self, dt):
        time_frame = dt*90
        self.update_vertical_chiziq()
        self.update_horizontal_chiziq()
        self.update_tiles()
        self.update_plane()
        self.generate_tile_coordinates()
        if not self.gameover_holat and self.on_start:
            asosiy_speed = self.SPEED * self.height / 100
            self.animation_down += asosiy_speed*time_frame
        
            spacing_y = self.chiziq_orasi_y*self.height
            if self.animation_down >= spacing_y:
                self.animation_down = 0
                self.loop_y += 1
                self.score_text = str(self.loop_y)

            speed_x = self.x_tomon_tezlik * self.width / 100
            self.animation_down_x += speed_x*time_frame

        if not self.check_tile_side() and not self.gameover_holat:
            self.gameover_holat = True
            # self.SPEED = 0
            self.menu_title = "G  A  M  E   O  V  E  R"
            self.button_text = "RESTART"
            self.main_menu.opacity = 1
            self.galaxy_music.stop()
            self.gameover_music.play()
            print("oxshadi")

    def on_click_start(self):
        self.galaxy_music.play()
        self.gameover_music.stop()
        self.on_start = True
        self.main_menu.opacity = 0
        self.restart_game()
        print("oxshadi")

        
class GalaxyApp(App):
    pass

GalaxyApp().run()