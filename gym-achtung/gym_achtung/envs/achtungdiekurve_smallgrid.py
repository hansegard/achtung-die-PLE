from gym_achtung.envs.achtungdiekurve import AchtungDieKurve
WINWIDTH = 300  # width of the program's window, in pixels
WINHEIGHT = 300  # height in pixels

class AchtungDieKurveSmallGrid(AchtungDieKurve):
    def __init__(self):
        self.winwidth = WINWIDTH
        self.winheight = WINHEIGHT
        super().__init__()
