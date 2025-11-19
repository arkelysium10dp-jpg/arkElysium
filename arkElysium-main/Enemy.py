from Object import Hitbox, Object

"""
hp = max_hp
sp = max_sp
defence: int
resistance: float
speed: float
dmg: int
atk_speed: int
dmg_type: 0/1/2 'PHYSICAL' / 'ARTS' / 'TRUE'
dmg_area: Hitbox
direction: 0/1/2/3 (right, up, left, down)
state: ?
path: Path

"""


class EnemyObject(Object):
    def __init__(self, hp, defence, resistance, speed, dmg, atk_speed, dmg_type,
                 dmg_area, direction, state, path,
                 surface, x, y, anim=None, script=lambda a: None, hitbox: Hitbox = None):
        super().__init__(surface, x, y, anim, script, hitbox)
        self.max_hp = hp
        self.hp = hp
        self.defence = defence
        self.resistance = resistance
        self.speed = speed
        self.dmg = dmg
        self.atk_speed = atk_speed
        self.dmg_type = dmg_type
        self.dmg_area = dmg_area
        self.direction = direction
        self.state = state
        self.path = path

    def collided(self, colliding_object):
        if self.hitbox.triggered(colliding_object.xy):
            print("COLLIDED")
            return

    def on_place(self, x, y):
        self.xy = x, y

    def on_tick(self):
        self.path.move(self.speed)
        return

    def is_area(self, x, y):
        return

    def on_collision(self, collision_object):
        return

    def attacked(self, attacker, dmg_type, dmg):
        match dmg_type:
            case "ARTS":
                self.hp -= dmg / self.resistance
            case "PHYSICAL":
                if (dmg - self.defence) > 0:
                    real_dmg = (dmg - self.defence)
                else:
                    real_dmg = dmg*0.03
                self.hp -= real_dmg
            case "TRUE":
                self.hp -= dmg
        if self.hp < 0:
            self.on_death(attacker)

    def attack(self, attacking_object):
        attacking_object.attacked(self, self.dmg_type, self.dmg)

    def on_death(self, attacker):
        return
