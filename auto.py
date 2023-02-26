import machine
import random


def distance(p1, p2):
    return min(abs(p1[0] - p2[0]), machine.height - 1 - abs(p1[0] - p2[0])) \
           + min(abs(p1[1] - p2[1]), machine.width - 1 - abs(p1[1] - p2[1]))


class Auto:

    def __init__(self, animal):
        self.body = animal
        self.posNode = 0
        self.matrix = [
            [((1, 90), 1), ((0, 0), 3), ((0, 0), 2)],
            [((0, 0), 0)],
            [((0, 0), 0)],
            [((0, 0), 4)],
            [((0, 0), 6), ((0, 0), 5), ((0, 0), 2)],
            [((0, 0), 4)],
            [((0, 0), 0)],
        ]
        self.point = ()
        self.old = ()
        self.new = False
        self.counter = 0
        self.funcs = (self.transitoin0, self.closestFoodPoint1, self.eatPoint2, self.goPoint3, self.pregnancy4, self.goUp5)
        self.arrows = (self.simple0, self.foodTest1)
        self.nodes = [self.funcs[0], self.funcs[4], self.funcs[5], self.funcs[1], self.funcs[0], self.funcs[3], self.funcs[2]]

    def turn(self, dirt, field):
        self.old = ()
        arrow = 0
        while True:
            if arrow >= len(self.matrix[self.posNode]):
                return self.old
            #print(self.posNode, arrow, self.body.food)
            if self.arrows[self.matrix[self.posNode][arrow][0][0]](self.matrix[self.posNode][arrow][0][1]):
                res = self.nodes[self.matrix[self.posNode][arrow][1]](dirt, field)
                if res == -1:
                    arrow += 1
                elif res == 0:
                    self.posNode = self.matrix[self.posNode][arrow][1]
                    arrow = 0
                else:
                    self.posNode = self.matrix[self.posNode][arrow][1]
                    return self.old
            else:
                arrow += 1

    def transitoin0(self, dirt, field):
        return 0

    def closestFoodPoint1(self, dirt, field):
        resPoint = ()
        for point in self.body.see:
            if (dirt[point[0]][point[1]] and dirt[point[0]][point[1]].name in self.body.diet) or \
                    (field[point[0]][point[1]] and (field[point[0]][point[1]].gen != self.body.gen or field[point[0]][point[1]].name == 'corpse') and field[point[0]][point[1]].name in self.body.diet):
                if resPoint:
                    if distance((self.body.x, self.body.y), point) < distance((self.body.x, self.body.y), resPoint):
                        resPoint = point
                else:
                    resPoint = point
        if resPoint:
            self.point = resPoint
            return 0
        return -1

    def eatPoint2(self, dirt, field):
        if not self.point:
            return -1
        for point in (dirt[self.point[0]][self.point[1]], field[self.point[0]][self.point[1]]):
            if not point:
                self.point = ()
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
        steps = self.body.speed
        while steps and distance((self.point[0], self.point[1]), (self.body.x, self.body.y)) > 0:
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
                if not field[point[1]][point[0]]:
                    res.append(point)
            if len(res) == 0:
                if steps == self.body.speed:
                    return -1
                else:
                    return 1
            point = random.choice(res)
            self.body.look(point)
            field[self.body.x][self.body.y] = False
            self.body.x = point[0]
            self.body.y = point[1]
            field[self.body.x][self.body.y] = self.body
            steps -= 1
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
        steps = self.body.speed
        while steps and not field[(self.body.x + self.body.eyes[0]) % machine.height][(self.body.y + self.body.eyes[1]) % machine.width]:
            field[self.body.x][self.body.y] = False
            self.body.x = (self.body.x + self.body.eyes[0]) % machine.height
            self.body.y = (self.body.y + self.body.eyes[1]) % machine.width
            field[self.body.x][self.body.y] = self.body
            steps -= 1
        return 1

    def simple0(self, c):
        return True

    def foodTest1(self, c):
        return self.body.stomach > c
