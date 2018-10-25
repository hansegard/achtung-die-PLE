from gym_achtung.envs.achtungdiekurve import AchtungDieKurve
WINWIDTH = 720  # width of the program's window, in pixels
WINHEIGHT = 576  # height in pixels

class AchtungDieKurveBigGrid(AchtungDieKurve):
    def __init__(self):
        self.winwidth = WINWIDTH
        self.winheight = WINHEIGHT
        super().__init__()
