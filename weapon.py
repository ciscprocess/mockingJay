import random
from weaponInfo import weaponInfo


class Weapon:
    def __init__(self, self_type):
        # All weapons start w/ a base d, and
        # they gain or lose depending on what kind of weapon they're fighting against
        self.weapon_info = weaponInfo()
        self.type = self_type
        self.damage_cap = 0
        self.is_ranged = False
        self.range = 1
        self.damage = self.find_damage()
        self.self_constructed = False
        self.uses_left = 50

        self.set_ranged()
        self.damage_cap = self.weapon_info.weaponStrength(self.type)

    def __repr__(self):
        return '<Weapon>(' + str(self.type) + ', ' + str(self.damage) + ')'

    def find_damage(self):
        return random.randint(1, self.weapon_info.weaponStrength(self.type))

    def is_in_range(self, dist_to_target):
        if self.is_ranged and dist_to_target <= 1:
            in_range = False
        elif self.is_ranged and (dist_to_target > 1) and (dist_to_target < self.range):
            in_range = True
        elif (not self.is_ranged) and dist_to_target > 1:
            in_range = False
        elif (not self.is_ranged) and dist_to_target <= 1:
            in_range = True
        else:
            in_range = False

        return in_range

    def set_ranged(self):
        if self.type == 'bow':
            self.is_ranged = True
        elif self.type == 'slingshot':
            self.is_ranged = True
        elif self.type == 'blowgun':
            self.is_ranged = True
        else:
            self.is_ranged = False
        self.range = self.weapon_info.weaponRange(self.type)

    def get_ranged(self):
        return self.is_ranged

    #First is the weapon that we're looking for the damage for
    #Second it the weapon that it's fighting against
    def get_damage(self, wep_against):
        against = wep_against.type
        own_weapon = self.type
        damage = self.damage

        if not wep_against.is_ranged and not self.is_ranged:
            if own_weapon == 'spear':
                if against == 'none':
                    damage += 4
                elif against == 'axe' or against == 'sword' or against == 'dagger':
                    damage += 3
                else:
                    damage += -1
            elif own_weapon == 'axe':
                if against == 'none':
                    damage += 4
                elif against == 'sword' or against == 'dagger' or against == 'mace' or against == 'hammer':
                    damage += 3
                else:
                    damage += -1
            elif own_weapon == 'sword':
                if against == 'none':
                    damage += 4
                elif against == 'dagger' or against == 'mace' or against == 'hammer':
                    damage += 3
                else:
                    damage += -1
            elif own_weapon == 'dagger':
                if against == 'none':
                    damage += 4
                elif against == 'mace' or against == 'hammer' or against == 'trident':
                    damage += 3
                else:
                    damage += -1
            elif own_weapon == 'mace':
                if against == 'none':
                    damage += 4
                elif against == 'hammer' or against == 'trident' or against == 'spear':
                    damage += 3
                else:
                    damage += -1
            elif own_weapon == 'hammer':
                if against == 'none':
                    damage += 4
                elif against == 'trident' or against == 'spear':
                    damage += 3
                else:
                    damage += -1
            elif own_weapon == 'trident':
                if against == 'none':
                    damage += 4
                elif against == 'spear' or against == 'axe' or against == 'sword':
                    damage += 3
                else:
                    damage += -1
            else:
                damage += 0

        elif wep_against.is_ranged and not self.is_ranged:
            damage += 4

        elif (not wep_against.is_ranged) and self.is_ranged:
            damage -= 1

        elif wep_against.is_ranged and self.is_ranged:
            if own_weapon == 'slingshot':
                if against == 'none':
                    damage += 1
                elif against == 'blowgun':
                    damage += 2
                else:
                    damage += -1
            elif own_weapon == 'blowgun':
                if against == 'none':
                    damage += 1
                elif against == 'bow':
                    damage += 2
                else:
                    damage += -1
            elif own_weapon == 'bow':
                if against == 'none':
                    damage += 1
                elif against == 'slingshot':
                    damage += 2
                else:
                    damage -= 1
            else:
                damage += 0
        else:
            damage += 0

        return damage