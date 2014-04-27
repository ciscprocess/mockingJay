class weaponInfo:
    def __init__(self):
        self.bow = ['longStick', 'shortStick', 'vine', 'sharpStone', 'feather']
        self.slingshot= ['longGrass', 'pebbles']
        self.blowgun = ['reeds', 'feather', 'thorn']
        self.hammer = ['broadStone','shortStick']
        self.mace = ['sharpStone', 'thorn', 'shortStick']
        self.trident = ['longStick', 'shortStick', 'sharpStone']
        self.spear =  ['longStick', 'sharpStone']
        self.axe = ['broadStone', 'longStick', 'longGrass']
        self.sword = []
        self.dagger = ['sharpStone', 'longGrass']
        self.craftTypes = ['shortStick', 'longStick', 'sharpStone', 'broadStone', 'pebbles', 'feather', 'vine', 'reeds', 'longGrass', 'thorns']
        self.error = []


    def weaponStrength(self, type):
        if(type == 'bow'):
            strength = 6
        elif(type == 'slingshot'):
            strength = 3
        elif(type == 'blowgun'):
            strength = 3
        elif(type == 'hammer'):
            strength = 5
        elif(type == 'mace'):
            strength = 6
        elif(type == 'trident'):
            strength = 5
        elif(type == 'spear'):
            strength =  5
        elif(type == 'axe'):
            strength = 5
        elif(type == 'sword'):
            strength = 6
        elif(type == 'dagger'):
            strength = 4
        else:
            strength = 5

        return strength

    def weaponRange(self, type):
        if(type == 'bow'):
            range = 7
        elif(type == 'slingshot'):
            range = 5
        elif(type == 'blowgun'):
            range = 4
        else:
            range = 1
        return range

    def totalItemsToCraft(self, type):
        if(type == 'bow'):
            return self.bow
        elif(type == 'slingshot'):
            return self.slingshot
        elif(type == 'blowgun'):
            return self.blowgun
        elif(type == 'hammer'):
            return self.hammer
        elif(type == 'mace'):
            return self.mace
        elif(type == 'trident'):
            return self.trident
        elif(type == 'spear'):
            return self.spear
        elif(type == 'axe'):
            return self.axe
        elif(type == 'sword'):
            return self.sword
        elif(type == 'dagger'):
            return self.dagger
        else:
            return self.error

    def totalNumItemsToCraft(self, type):
        if(type == 'bow'):
            return len(self.bow)
        elif(type == 'slingshot'):
            return len(self.slingshot)
        elif(type == 'blowgun'):
            return len(self.blowgun)
        elif(type == 'hammer'):
            return len(self.hammer)
        elif(type == 'mace'):
            return len(self.mace)
        elif(type == 'trident'):
            return len(self.trident)
        elif(type == 'spear'):
            return len(self.spear)
        elif(type == 'axe'):
            return len(self.axe)
        elif(type == 'sword'):
            return len(self.sword)
        elif(type == 'dagger'):
            return len(self.dagger)
        else:
            return len(self.error)

    def canCraft(self, type, items):
        itemList = self.itemsToCraft(type)
        tribItems = items
        ans = False
        if(type == 'sword'):
            return False
        if(len(itemList) > len(tribItems)):
            ans = False
        else:
            matchedItems = 0
            for needed in itemList:
                for item in tribItems:
                    if item == needed:
                        matchedItems += 1
            if matchedItems >= len(itemList):
                ans = True
            else:
                ans = False
        return ans

    def itemsNeededToCraft(self, type, items):
        itemList = self.itemsToCraft(type)
        tribItems = items
        ans = []
        if(type == 'sword'):
            return []
        match = 0
        for needed in itemList:
            for item in tribItems:
                if item == needed:
                    match = 1
            if match == 0:
                ans.append(needed)
            else:
                match = 1
        return ans
