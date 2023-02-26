import random
import auto


height = 100
width = 100
plantNewChance = 5
plantDieChance = 10
plantMutChance = 1
plantGrowTime = 10
plantOldTime = 100
plantFood = 6
animalBirth = 75
animalHunger = 3
animalOld = 100
animalDisappear = 100
babyCost = 25


class Grass:

    def __init__(self, x, y):
        self.name = 'seed'
        self.x = x
        self.y = y
        self.mut = Berry
        self.grow = 0
        self.age = 0
        self.seed = 0
        self.food = plantFood
        self.neighborhood = []
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i != self.x or j != self.y:
                    self.neighborhood.append((i % height, j % width))

    def turn(self, dirt):
        old = ()
        new = ()
        self.age += 1
        if self.age == plantGrowTime:
            self.name = 'grass'
        if self.age <= plantGrowTime:
            return False
        if self.age >= plantOldTime and random.randint(1, 100) <= plantDieChance:
            old = (self, )
            return old, new
        if random.randint(1, 100) <= plantNewChance:
            pos = []
            for n in self.neighborhood:
                if not dirt[n[0]][n[1]]:
                    pos.append(n)
            if pos:
                r = random.choice(pos)
                if random.randint(1, 100) <= plantMutChance:
                    new = (self.mut(r[0], r[1]), )
                    return old, new
                new = (Grass(r[0], r[1]), )
                return old, new
        return False


class Berry:

    def __init__(self, x, y):
        self.name = 'seed'
        self.x = x
        self.y = y
        self.mut = Grass
        self.grow = 0
        self.age = 0
        self.seed = 0
        self.food = plantFood

    def turn(self, dirt):
        old = ()
        new = ()
        self.age += 1
        self.seed = max(0, min(5, self.age // (100 // plantNewChance) - 1))
        if self.age == plantGrowTime:
            self.name = 'berry'
        if self.age >= plantOldTime and random.randint(1, 100) <= plantDieChance:
            old = (self, )
            return old, new
        return False


class Animal:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 1
        self.teeth = 'standard'
        self.diet = ['berry', 'grass']
        self.name = 'animal'
        self.gen = 0
        self.speed = 1
        self.hear = 1
        self.vision = 0
        self.hungerCount = 1
        self.seed = 0
        self.stomach = animalBirth
        self.food = 50
        self.maxFood = 100
        self.eyes = []
        self.see = set()
        self.baby = 0
        self.auto = auto.Auto(self)
        if random.randint(0, 1):
            self.eyes = [random.choice((-1, 1)), 0]
        else:
            self.eyes = [0, random.choice((-1, 1))]

    def look(self, point):
        if (self.x - 1) % height == point[0]:
            self.eyes = [-1, 0]
        elif (self.x + 1) % height == point[0]:
            self.eyes = [1, 0]
        elif (self.y - 1) % width == point[1]:
            self.eyes = [0, -1]
        elif (self.y + 1) % width == point[1]:
            self.eyes = [0, 1]

    def eat(self, dish):
        food = dish.food
        if self.baby:
            food //= 2
            self.baby += food
        self.stomach += food
        while self.stomach > self.maxFood:
            self.stomach -= 5
            self.maxFood += 1
        self.look((dish.x, dish.y))
        return dish

    def born(self):
        self.baby = 0
        res = Animal((self.x + self.eyes[0] * -1) % height, (self.y + self.eyes[1] * -1) % width)
        res.diet = self.diet
        res.gen = self.gen
        return res

    def turn(self, dirt, field):
        self.age += 1
        if self.name == 'corpse':
            if self.age == animalDisappear:
                return (self, ), ()
            return (), ()
        self.auto.old = ()
        new = []
        if not self.age % animalOld:
            self.hungerCount += 1
        if not self.age % animalHunger:
            self.stomach -= self.hungerCount + bool(self.baby)
            if self.seed and not dirt[self.x][self.y]:
                self.seed -= 1
                if random.randint(1, 100) <= plantMutChance:
                    new.append(Grass(self.x, self.y))
                else:
                    new.append(Berry(self.x, self.y))
        if self.stomach < 1:
            self.name = 'corpse'
            self.gen = -1
            self.age = 0
            self.stomach = 0
            return (), ()
        self.see.clear()
        for i in range(self.x - self.hear, self.x + self.hear + 1):
            for j in range(self.y - self.hear, self.y + self.hear + 1):
                self.see.add((i % height, j % width))
        old = self.auto.turn(dirt, field)
        if self.baby >= animalBirth:
            new.append(self.born())
        return old, new


class Control:

    def __init__(self):
        self.dirt = []
        self.field = []
        self.plants = []
        self.animals = []
        for i in range(height):
            line = []
            for j in range(width):
                if random.randint(1, 100) <= 2:
                    self.plants.append(Grass(i, j))
                    line.append(self.plants[len(self.plants) - 1])
                else:
                    line.append(False)
            self.dirt.append(line)
        for i in range(height):
            line = []
            for j in range(width):
                if (i or j) and random.randint(1, 100) <= 1:
                    if random.randint(1, 100) <= 25:
                        self.animals.append(Animal(i, j))
                        self.animals[len(self.animals) - 1].gen = 1
                        self.animals[len(self.animals) - 1].diet = ['corpse', 'animal']
                    else:
                        self.animals.append(Animal(i, j))
                    line.append(self.animals[len(self.animals) - 1])
                else:
                    line.append(False)
            self.field.append(line)

    def turn(self):
        newPlants = self.plants.copy()
        for plant in self.plants:
            end = plant.turn(self.dirt)
            if end:
                old, new = end
                for o in old:
                    newPlants.remove(o)
                    self.dirt[o.x][o.y] = False
                for n in new:
                    newPlants.insert(0, n)
                    self.dirt[n.x][n.y] = n
        self.plants = newPlants

        newAnimals = self.animals.copy()
        for animal in self.animals:
            end = animal.turn(self.dirt, self.field)
            if end:
                old, new = end
                for o in old:
                    if o.name == 'animal' or o.name == 'corpse':
                        o.name = 'corpse'
                        o.gen = -1
                        if o in newAnimals:
                            newAnimals.remove(o)
                        self.field[o.x][o.y] = False
                    else:
                        self.plants.remove(o)
                        self.dirt[o.x][o.y] = False
                for n in new:
                    if n.name == 'seed':
                        self.plants.insert(0, n)
                        self.dirt[n.x][n.y] = n
                    else:
                        newAnimals.insert(0, n)
                        self.field[n.x][n.y] = n
        self.animals = newAnimals
