from gym_achtung.envs.achtungdiekurve import AchtungDieKurve
WINWIDTH = 400  # width of the program's window, in pixels
WINHEIGHT = 400  # height in pixels

class AchtungDieKurveSmallGrid(AchtungDieKurve):
    def __init__(self):
        self.winwidth = WINWIDTH
        self.winheight = WINHEIGHT
        super().__init__()
