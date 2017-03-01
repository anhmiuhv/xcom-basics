class Weapon:
    def __init__(self, name, minDamage, maxDamage, magSize, rangeMod, critChance = 10, critDamage = 2, heavy = False):
        self.minDamage = minDamage
        self.maxDamage = maxDamage
        self.magSize = magSize
        self.ammo = magSize
        self.rangeMod = rangeMod
        self.name = name
        self.critChance = critChance
        self.critDamage = critDamage
        self.heavy = heavy

class Soldier:
    def __init__(self, name, weapon, coords=(0,0), mobility = 4, health = 5, aim = 65, defense = 0, dodge = 10, side = 0):
        self.name = name
        self.weapon = weapon
        self.coords = coords
        self.health = health
        self.maxhealth = health
        self.mobility = mobility
        self.aim = aim
        self.defense = defense
        self.dodge = dodge
        self.side = side
        self.actionPoints = 2

    def set_image(self, image):
        self.image = image
        
    def isDying(self):
        return self.health / self.maxhealth < 0.3
     
    def __eq__(self, a):
        if a == None:
            return False
        return self.name == a.name
