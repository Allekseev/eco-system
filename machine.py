import random
import auto


height = 100
width = 100
plantNewChance = 10
plantDieChance = 10
plantMutChance = 1
plantGrowTime = 10
plantOldTime = 100
plantFood = 4
animalBirth = 75
animalHunger = 2
animalOld = 100
babyCost = 25


class Grass:

    def __init__(self, x, y):
        self.name = 'seed'
        self.x = x
        self.y = y
        self.mut = Berry
        self.grow = 0
        self.age = 0
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
        self.food = plantFood

    def turn(self, dirt):
        old = ()
        new = ()
        self.age += 1
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
        self.speed = 1
        self.hear = 1
        self.vision = 0
        self.hungerCount = 1
        self.food = animalBirth
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
        self.food += food
        while self.food > self.maxFood:
            self.food -= 5
            self.maxFood += 1
        self.look((dish.x, dish.y))
        return dish

    def turn(self, dirt, field):
        self.age += 1
        new = False
        if not self.age % animalOld:
            self.hungerCount += 1
        if not self.age % animalHunger:
            self.food -= self.hungerCount + bool(self.baby)
        if self.food < 1:
            return self, False
        for i in range(self.x - self.hear, self.x + self.hear + 1):
            for j in range(self.y - self.hear, self.y + self.hear + 1):
                self.see.add((i % height, j % width))
        old = self.auto.turn(dirt, field)
        if self.baby >= animalBirth:
            new = Animal((self.x + self.eyes[0] * -1) % height, (self.y + self.eyes[1] * -1) % width)
            self.baby = 0
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
                if random.randint(1, 100) == 100:
                    print('0')
                    self.plants.append(Grass(i, j))
                    line.append(self.plants[len(self.plants) - 1])
                else:
                    line.append(False)
            self.dirt.append(line)
        for i in range(height):
            line = []
            for j in range(width):
                line.append(False)
            self.field.append(line)
        self.animals.append(Animal(50, 50))
        self.field[50][50] = self.animals[0]

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
                if old:
                    if old.name == 'animal':
                        newAnimals.remove(old)
                        self.field[old.x][old.y] = False
                    else:
                        self.plants.remove(old)
                        self.dirt[old.x][old.y] = False
                if new:
                    newAnimals.insert(0, new)
                    self.field[new.x][new.y] = new
        self.animals = newAnimals
