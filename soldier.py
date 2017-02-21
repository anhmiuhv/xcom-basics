class Weapon:
    def __init__(self, name, minDamage, maxDamage, magSize, rangeMod):
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.magSize = magSize
        self.ammo = magSize
        self.rangeMod = rangeMod

class Soldier:
    def __init__(self, name, weapon, coords=(0,0), mobility = 5, health = 5, aim = 65):
        self.name = name
        self.weapon = weapon
        self.coords = coords
        self.health = health
        self.mobility = mobility
        self.aim = aim

    def set_image(self, image):
        self.image = image
