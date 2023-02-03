from kivy.uix.relativelayout import RelativeLayout

class MainMenu(RelativeLayout):
    def on_touch_down(self, touch):
        if self.opacity == 0:
            return False
        return super().on_touch_down(touch)