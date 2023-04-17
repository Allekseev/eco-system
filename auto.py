import machine
import random

left = {(-1, 0): (0, 1), (1, 0): (0, -1), (0, -1): (-1, 0), (0, 1): (1, 0)}
right = {(-1, 0): (0, -1), (1, 0): (0, 1), (0, -1): (1, 0), (0, 1): (-1, 0)}
omnivorousMatrix = [
            [((1, 90), 1), ((0, 0), 2), ((0, 0), 3), ((0, 0), 4), ((0, 0), 5)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 0)],
        ]
omnivorousNodes = [0, 4, 2, 3, 1, 5]
travelerMatrix = [
            [((0, 0), 1)],
            [((0, 0), 2)],
            [((1, 90), 3), ((0, 0), 4), ((0, 0), 5), ((0, 0), 6), ((0, 0), 7), ((0, 0), 8)],
            [((0, 0), 2)],
            [((0, 0), 2)],
            [((0, 0), 2)],
            [((0, 0), 2)],
            [((0, 0), 2)],
            [((0, 0), 2)]
        ]
herbivorousNodes = [0, 7, 0, 4, 2, 3, 1, 5, 10]
predatorNodes = [0, 6, 0, 4, 2, 3, 1, 5, 10]
lazyCowMatrix = [
            [((0, 0), 1), ((1, 90), 2), ((0, 0), 3), ((0, 0), 4), ((0, 0), 5)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 0)]
        ]
lazyCowNodes = [0, 7, 4, 2, 3, 1]
weights = {1: 100, 2: 100, 3: 5, 4: 5, 5: 5, 6: 5}


def distance(p1, p2):
    return min(abs(p1[0] - p2[0]), machine.height - 1 - abs(p1[0] - p2[0])) \
           + min(abs(p1[1] - p2[1]), machine.width - 1 - abs(p1[1] - p2[1]))


class Auto:

    def __init__(self, animal):
        self.body = animal
        self.posNode = 0
        self.matrix = travelerMatrix
        self.size = 11
        self.steps = 1
        self.point = ()
        self.old = ()
        self.new = False
        self.counter = 0
        self.funcs = (self.transitoin0, self.closestFoodPoint1, self.eatPoint2, self.goPoint3, self.pregnancy4,
                      self.goUp5, self.killTeeth6, self.veganTeeth7, self.hearUpgrade8, self.speedUpgrade9,
                      self.turnLeft10, self.turnRight11)
        self.arrows = (self.simple0, self.foodMoreTest1, self.foodLessTest2, self.speedMoreTest3, self.speedLessTest4,
                       self.hearMoreTest5, self.hearLessTest6)
        self.nodes = herbivorousNodes
        self.rudiments = []
        for i in range(len(self.nodes)):
            self.rudiments.append(1)

    def turn(self, dirt, field):
        self.steps = self.body.speed
        self.old = ()
        arrow = 0
        tries = 0
        while tries < 10:
            self.rudiments[self.posNode] = 0
            tries += not arrow
            if arrow >= len(self.matrix[self.posNode]):
                return self.old
            if self.arrows[self.matrix[self.posNode][arrow][0][0]](self.matrix[self.posNode][arrow][0][1]):
                res = self.funcs[self.nodes[self.matrix[self.posNode][arrow][1]]](dirt, field)
                if res == -1:
                    arrow += 1
                else:
                    self.posNode = self.matrix[self.posNode][arrow][1]
                    if res == 0:
                        arrow = 0
                    else:
                        return self.old
            else:
                arrow += 1
        return self.old

    def transitoin0(self, dirt, field):
        return 0

    def closestFoodPoint1(self, dirt, field):
        resPoint = ()
        for point in self.body.see:
            if (dirt[point[0]][point[1]] and dirt[point[0]][point[1]].name in self.body.diet) or \
                    (field[point[0]][point[1]] and (field[point[0]][point[1]].gen not in self.body.family or field[point[0]][point[1]].name == 'corpse') and field[point[0]][point[1]].name in self.body.diet):
                if resPoint:
                    if distance((self.body.x, self.body.y), point) < distance((self.body.x, self.body.y), resPoint):
                        resPoint = point
                else:
                    resPoint = point
        if resPoint:
            self.point = resPoint
            return 0
        self.point = ()    # спорно
        return -1

    def eatPoint2(self, dirt, field):
        if not self.point:
            return -1
        for point in (dirt[self.point[0]][self.point[1]], field[self.point[0]][self.point[1]]):
            if not point:
                continue
            if distance((point.x, point.y), (self.body.x, self.body.y)) < 2:
                self.point = ()
                if not point or point.name not in self.body.diet:
                    continue
                self.body.seed += point.seed
                self.old = (self.body.eat(point),)
                return 1
        return -1

    def goPoint3(self, dirt, field):
        if not self.point or distance((self.point[0], self.point[1]), (self.body.x, self.body.y)) < 2:
            return -1
        flag = False
        while self.steps and distance((self.point[0], self.point[1]), (self.body.x, self.body.y)) > 0:
            pos = []
            d = self.body.x - self.point[0]
            if d > machine.height//2 or 0 > d > -machine.height//2:
                pos.append(((self.body.x + 1) % machine.height, self.body.y))
            elif d:
                pos.append(((self.body.x - 1) % machine.height, self.body.y))
            d = self.body.y - self.point[1]
            if d > machine.width//2 or 0 > d > -machine.width//2:
                pos.append((self.body.x, (self.body.y + 1) % machine.width))
            elif d:
                pos.append((self.body.x, (self.body.y - 1) % machine.width))
            res = []
            for point in pos:
                if not field[point[0]][point[1]]:
                    res.append(point)
            if len(res) == 0:
                if flag:
                    return 1
                else:
                    self.point = ()
                    return -1
            point = random.choice(res)
            self.body.look(point)
            field[self.body.x][self.body.y] = False
            self.body.x = point[0]
            self.body.y = point[1]
            field[self.body.x][self.body.y] = self.body
            self.steps -= 1
            flag = True
        return 1

    def pregnancy4(self, dirt, field):
        if self.body.baby or self.body.stomach < machine.babyCost:
            return -1
        self.body.stomach -= machine.babyCost
        self.body.baby = 1
        return 1

    def goUp5(self, dirt, field):
        if field[(self.body.x + self.body.eyes[0]) % machine.height][(self.body.y + self.body.eyes[1]) % machine.width]:
            return -1
        while self.steps and not field[(self.body.x + self.body.eyes[0]) % machine.height][(self.body.y + self.body.eyes[1]) % machine.width]:
            field[self.body.x][self.body.y] = False
            self.body.x = (self.body.x + self.body.eyes[0]) % machine.height
            self.body.y = (self.body.y + self.body.eyes[1]) % machine.width
            field[self.body.x][self.body.y] = self.body
            self.steps -= 1
        return 1

    def killTeeth6(self, dirt, field):
        if self.body.teeth or self.body.stomach <= machine.animalUpgrade:
            return -1
        #print('OMG')
        self.body.stomach -= machine.animalUpgrade
        self.body.teeth = True
        self.body.diet = ['corpse', 'animal']
        return 1

    def veganTeeth7(self, dirt, field):
        if self.body.teeth or self.body.stomach <= machine.animalUpgrade:
            return -1
        #print('omg')
        self.body.stomach -= machine.animalUpgrade
        self.body.teeth = True
        self.body.diet = ['grass', 'berry']
        return 1

    def hearUpgrade8(self, dirt, field):
        if self.body.stomach <= machine.animalUpgrade:
            return -1
        self.body.stomach -= machine.animalUpgrade
        self.body.hungerCount += 1
        self.body.hear += 1
        return 1

    def speedUpgrade9(self, dirt, field):
        if self.body.stomach <= machine.animalUpgrade:
            return -1
        self.body.stomach -= machine.animalUpgrade
        self.body.hungerCount += 1
        self.body.speed += 1
        return 1

    def turnLeft10(self, dirt, field):
        self.steps -= 1
        self.body.eyes = left[self.body.eyes]
        return not self.steps

    def turnRight11(self, dirt, field):
        self.steps -= 1
        self.body.eyes = right[self.body.eyes]
        return not self.steps

    def simple0(self, c):
        return True

    def foodMoreTest1(self, c):
        return self.body.stomach > c

    def foodLessTest2(self, c):
        return self.body.stomach < c

    def speedMoreTest3(self, c):
        return self.body.speed > c

    def speedLessTest4(self, c):
        return self.body.speed < c

    def hearMoreTest5(self, c):
        return self.body.hear > c

    def hearLessTest6(self, c):
        return self.body.hear < c
