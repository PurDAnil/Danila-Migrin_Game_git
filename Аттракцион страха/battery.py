from blitter import Blitter


class Battery:
    def __init__(self, app):
        self.app = app
        self.charge = 100
        self.batt = Blitter(self.app, '', [660, 65], [150, 200], cp=self.app.cam.all_blit, text_size=20, color='green')

    def update(self):
        if self.charge > 0:
            self.charge -= self.app.clock.tick(60) / (500 - self.app.player.camera * 100)
            self.batt.change(str(round(self.charge)) + '%', color='green')
        elif self.app.player.camera:
            self.app.cam.change_cam(0)
        else:
            [i.hide() for i in self.app.cam.plansh]
