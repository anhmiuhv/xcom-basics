class Soldier:
    def __init__(self, coords=(0,0), mobility=5, health = 1000, aim=65):
        self.coords = coords
        self.health = health
        self.mobility = mobility
        self.aim = aim
        
    def set_image(self, image):
        self.image = image