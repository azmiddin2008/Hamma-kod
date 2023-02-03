from kivy.uix.relativelayout import RelativeLayout



def keyboard_closed(self):
    self._keyboard.unbind(on_key_down=self.on_keyboard_down)
    self._keyboard.unbind(on_key_up=self.on_keyboard_up)
    self._keyboard = None

def on_keyboard_down(self, keyboard, keycode, text, modifiers):
    if keycode[1] == 'left':
        self.x_tomon_tezlik = self.SPEED_X
    
    if keycode[1] == 'spacebar':
        self.on_click_start()
        
    if keycode[1] == 'alt':
        self.SPEED = 0
        self.SPEED_X = False
        
    if keycode[1] == 'shift':
        self.SPEED = 0.4

        
    elif keycode[1] == 'right':
        self.x_tomon_tezlik = -self.SPEED_X
    
    return True
def on_keyboard_up(self, keyboard, keycode):
    self.x_tomon_tezlik = 0

def on_touch_down(self, touch):
    if self.gameover_holat and self.on_start:
        if touch.x >= self.chiziq_x:
            self.x_tomon_tezlik = self.SPEED_X
        if touch.x <= self.chiziq_x:
            self.x_tomon_tezlik = -self.SPEED_X
    return super(RelativeLayout, self).on_touch_down(touch)

def on_touch_up(self, touch):
    self.x_tomon_tezlik = 0

