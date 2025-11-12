from Object import Hitbox, Object


"""

hp = max_hp
sp = max_sp
defence: int
resistance: float
dmg: int
atk_speed: int
dmg_area: Hitbox
direction: 0/1/2/3 (right, up, left, down)
type_sp: 'PASSIVE' / 'OFFENSIVE'
dmg_type: 0/1/2 'PHYSICAL' / 'ARTS' / 'TRUE'
init_sp: int


"""

class OperatorObject(Object):
    def __init__(self, hp: int, sp: int, type_sp, defence: int, resistance: float, dmg: int, atk_speed: int, dmg_type,
                 dmg_area, direction,
                 surface, x, y,  anim = None, script = lambda a: None, hitbox: Hitbox = None, init_sp=0):
        super().__init__(surface, x, y, anim, script, hitbox)
        self.max_hp = hp
        self.hp = hp
        self.max_sp = sp
        self.sp = init_sp
        self.type_sp = type_sp
        self.defence = defence
        self.resistance = resistance
        self.dmg = dmg
        self.atk_speed = atk_speed
        self.dmg_type = dmg_type
        self.dmg_area = dmg_area
        self.direction = direction

    def on_place(self, x, y):
        self.xy = x,y

    def is_area(self, x, y):
        return

    def on_collision(self, colliding_object):
        if self.hitbox.triggered(colliding_object.xy):
            print("OPERATOR COLLIDED")
            return

    def attacked(self, attacker, dmg_type, dmg):
        match dmg_type:
            case "ARTS":
                self.hp -= dmg / self.resistance
            case "PHYSICAL":
                if (dmg - self.defence) > 0:
                    self.hp -= (dmg - self.defence)
            case "TRUE":
                self.hp -= dmg
        if self.hp <= 0:
            self.on_death(attacker)

    def attack(self, attacking_object):
        if self.type_sp == "OFFENSIVE":
            self.sp += 1
        attacking_object.attacked(self, self.dmg_type, self.dmg)

    def on_death(self, attacker):
        return
