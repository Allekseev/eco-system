import random
import auto


height = 150
width = 150
plantMutChance = 0
plantGrowTime = 10
plantOldTime = 100
plantSpreadTime = 30    # время на размножение травы
plantFood = 3    # питательность травы
animalFood = 35    # питательность при поедании жертвы
animalBirth = 75
animalHunger = 5    # чем выше тем реже животное голодает
animalOld = 100    # количество циклов до старения (животное начинает быстрее голодать)
animalDisappear = 200    # время до исчезновения трупа min 1
animalUpgrade = 25
animalCorrect = 0
animalMut = 0
animalChange = 10
babyCost = 25
globalGen = 1
period = plantOldTime * 3
time = 0
plantTime = []
for q in range(period):
    plantTime.append([])


class Grass:

    def __init__(self, x, y):
        self.name = 'seed'
        self.dead = False
        self.x = x
        self.y = y
        self.mut = Berry
        self.grow = 0
        self.die = (time + random.randint(plantOldTime, plantOldTime*2)) % period
        self.seed = 0
        self.food = plantFood
        self.nex = (time + random.randint(plantGrowTime + 1, plantSpreadTime)) % period
        self.neighborhood = []
        self.green = (plantGrowTime + time) % period
        plantTime[self.green].append(self)
        plantTime[self.nex].append(self)
        plantTime[self.die].append(self)
        for i in range(x - 1, x + 2):
            for j in range(y - 1, y + 2):
                if i != self.x or j != self.y:
                    self.neighborhood.append((i % height, j % width))

    def turn(self, dirt):
        old = ()
        new = ()
        if time == self.green:
            self.name = 'grass'
            return False
        if time == self.die:
            old = (self, )
            return old, new
        if time == self.nex:
            self.nex = (time + random.randint(1, plantSpreadTime)) % period
            plantTime[self.nex].append(self)
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
        print(self.name, time, self.green, self.nex, self.die)
        print('grass error')
        return False


class Berry:

    def __init__(self, x, y):
        self.name = 'seed'
        self.dead = False
        self.x = x
        self.y = y
        self.mut = Grass
        self.grow = 0
        self.die = (time + random.randint(plantOldTime, plantOldTime*2)) % period
        self.nex = (plantGrowTime * 2 + time) % period
        self.seed = 0
        self.food = plantFood * 2
        self.green = (plantGrowTime + time) % period
        plantTime[self.green].append(self)
        plantTime[self.nex].append(self)
        plantTime[self.die].append(self)

    def turn(self, dirt):
        old = ()
        new = ()
        if time == self.nex:
            self.seed += 1
            if self.seed < 5:
                self.nex = (plantGrowTime * 2 + time) % period
                plantTime[self.nex].append(self)
        if time == self.green:
            self.name = 'berry'
        if time == self.die:
            old = (self, )
            return old, new
        return False


class Animal:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.age = 1
        self.teeth = False
        self.diet = ['berry', 'corpse']
        self.name = 'animal'
        self.gen = 1
        self.family = set()
        self.family.add(1)
        self.rgb = [0, 0, 200]
        self.speed = 1
        self.hear = 2    # дальность обзора животных
        self.vision = 0
        self.hungerCount = 1
        self.seed = 0
        self.stomach = animalBirth
        self.food = animalFood
        self.maxFood = 100
        self.eyes = ()
        self.see = set()
        self.baby = 0
        self.auto = auto.Auto(self)
        if random.randint(0, 1):
            self.eyes = (random.choice((-1, 1)), 0)
        else:
            self.eyes = (0, random.choice((-1, 1)))

    def look(self, point):
        if (self.x - 1) % height == point[0]:
            self.eyes = (-1, 0)
        elif (self.x + 1) % height == point[0]:
            self.eyes = (1, 0)
        elif (self.y - 1) % width == point[1]:
            self.eyes = (0, -1)
        elif (self.y + 1) % width == point[1]:
            self.eyes = (0, 1)

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
        res.auto.matrix = self.auto.matrix
        res.auto.nodes = self.auto.nodes
        res.gen = self.gen
        res.family = self.family
        res.rgb = self.rgb
        r = random.randint(1, 100)
        if r <= animalCorrect:
            res.auto.rudiments = []
            for i in range(len(self.auto.rudiments)):
                res.auto.rudiments.append(1)
            res.correct()
        elif r <= animalCorrect + animalMut:
            res.auto.rudiments = self.auto.rudiments
            res.mut(self.gen)
        else:
            res.auto.rudiments = []
            for i in range(len(self.auto.rudiments)):
                res.auto.rudiments.append(self.auto.rudiments[i] + 1)
        self.family.add(res.gen)
        return res

    def correct(self):    # мутации отключены
        matrix = self.auto.matrix
        self.auto.matrix = []
        pos = 0
        if random.randint(0, 2):
            cor = random.randint(0, self.auto.size - 1)
            for line in matrix:
                newLine = []
                for arrow in line:
                    if cor == pos:
                        if arrow[0][0]:
                            if random.randint(0, 1):
                                newLine.append(
                                    ((arrow[0][0], random.randint(arrow[0][1] // 2, arrow[0][1] + arrow[0][1] // 2)),
                                     arrow[1]))
                            else:
                                newLine.append(((0, 0), arrow[1]))
                        else:
                            r = random.randint(1, len(self.auto.arrows) - 1)
                            newLine.append(((r, random.randint(1, auto.weights[r])), arrow[1]))
                    else:
                        newLine.append(arrow)
                    pos += 1
                self.auto.matrix.append(newLine)
        else:
            cor = random.randint(0, len(matrix) - 1)
            for line in matrix:
                newLine = []
                if cor == pos:
                    r = []
                    for i in range(len(line)):
                        r.append(i)
                    random.shuffle(r)
                    for i in r:
                        newLine.append(line[i])
                else:
                    newLine = line.copy()
                self.auto.matrix.append(newLine)

    def mut(self, gen):    # мутации отключены
        matrix = self.auto.matrix
        reserveMatrix = self.auto.matrix
        reserveNodes = self.auto.nodes
        randy = random.randint(0, 2)
        if randy:
            change = random.randint(1, min(self.auto.size - 1, animalChange // 2))
        else:
            change = 0
        self.auto.matrix = []
        al = []
        for i in range(self.auto.size):
            al.append(i)
        changes = []
        for i in range(change):
            r = random.choice(al)
            changes.append(r)
            al.remove(r)
        pos = 0
        for i in range(len(matrix)):
            newLine = []
            for arrow in matrix[i]:
                if pos not in changes and self.auto.rudiments[i] <= 5:
                    newLine.append(arrow)
                pos += 1
            self.auto.matrix.append(newLine)
        using = set()
        unusing = set()
        nextUsing = set()
        nextUsing.add(0)
        while nextUsing:
            using = using.union(nextUsing)
            newUsing = nextUsing
            nextUsing = set()
            for u in newUsing:
                if not self.auto.matrix[u]:
                    unusing.add(u)
                for arrow in self.auto.matrix[u]:
                    if arrow[1] not in using:
                        nextUsing.add(arrow[1])
        using = using.difference(unusing)
        oldNum = {}
        pos = -1
        nodes = []
        for i in range(len(self.auto.nodes)):
            if i in using:
                nodes.append(self.auto.nodes[i])
                pos += 1
                oldNum[i] = pos
                line = self.auto.matrix[i].copy()
                for arrow in self.auto.matrix[i]:
                    if arrow[1] not in using:
                        line.remove(arrow)
                self.auto.matrix[i] = line
        self.auto.nodes = nodes
        matrix = self.auto.matrix
        self.auto.matrix = []
        for i in range(len(matrix)):
            if i in using:
                self.auto.matrix.append([])
                for arrow in matrix[i]:
                    self.auto.matrix[len(self.auto.matrix) - 1].append((arrow[0], oldNum[arrow[1]]))
        if not self.auto.matrix or not self.auto.matrix[0] or not self.auto.matrix[0]:
            self.auto.matrix = reserveMatrix
            self.auto.nodes = reserveNodes
        if randy != 1:
            zeroIn = False
            change = random.randint(1, animalChange)
            newNodesPos = [random.randint(0, len(self.auto.matrix))]
            newNodesIn = []
            zeroLocked = not newNodesPos[0]
            newNodesIn.append(not newNodesPos[0])
            newNodesOut = [False]
            newArrows = []
            size = 1
            for i in range(len(self.auto.matrix)):
                size += len(self.auto.matrix[i]) + 1
                if i:
                    for arrow in self.auto.matrix[i]:
                        if not arrow[1]:
                            zeroIn = True
            while change:
                change -= 1
                arrowIn = [random.randint(0, 1)]
                if arrowIn[0]:
                    arrowIn.append(random.randint(0, len(newNodesPos) - 1))
                else:
                    arrowIn.append(random.randint(0, len(self.auto.matrix) - 1))
                arrowOut = [random.randint(0, 1)]
                if arrowOut[0]:
                    arrowOut.append(random.randint(0, len(newNodesPos) - 1))
                else:
                    arrowOut.append(random.randint(0, len(self.auto.matrix) - 1))
                if arrowOut[0] == 0 and arrowOut[1] == 0 and not (arrowIn[0] == 0 and arrowIn[1] == 0):
                    zeroIn = True
                if arrowOut[0] == 1:
                    newNodesOut[arrowOut[1]] = True
                if arrowIn[0] == 1 and not (arrowOut[0] == 1 and arrowIn[1] == arrowOut[1]):
                    newNodesIn[arrowIn[1]] = True
                newArrows.append((arrowIn, arrowOut))
                if (newNodesPos[len(newNodesPos) - 1] and newNodesIn[len(newNodesIn) - 1]) \
                        or (not newNodesPos[len(newNodesPos) - 1] and newNodesOut[len(newNodesOut) - 1]):
                    ne = random.randint(0 + zeroLocked, len(self.auto.matrix) + len(newNodesPos))
                    while ne in newNodesPos:
                        ne = (1 + ne) % (len(self.auto.matrix) + len(newNodesPos) + 1)
                        if zeroLocked and not ne:
                            ne += 1
                    if not ne:
                        zeroLocked = True
                    newNodesPos.append(ne)
                    newNodesIn.append(not newNodesPos[len(newNodesPos) - 1])
                    newNodesOut.append(False)
            if not newNodesIn[-1] and not newNodesOut[-1]:
                newNodesPos.pop()
                newNodesIn.pop()
                newNodesOut.pop()
            if not zeroIn and zeroLocked:
                arrowOut = [0, 0]
                arrowIn = [random.randint(0, 1)]
                if arrowIn[0]:
                    arrowIn.append(random.randint(0, len(newNodesPos) - 1))
                else:
                    arrowIn.append(random.randint(0, len(self.auto.matrix) - 1))   # 0/1
                newArrows.append((arrowIn, arrowOut))
            for i in range(len(newNodesPos)):
                if not newNodesIn[i]:
                    arrowIn = [1, i]
                    arrowOut = [0, random.randint(0, len(self.auto.matrix) - 1)]
                    newArrows.append((arrowIn, arrowOut))
                if not newNodesOut[i]:
                    arrowOut = [1, i]
                    arrowIn = [0, random.randint(0, len(self.auto.matrix) - 1)]
                    newArrows.append((arrowIn, arrowOut))
            oldNodesPos = []
            oldPointer = 0
            newPointer = 0
            newNodesSort = newNodesPos.copy()
            newNodesSort.sort()
            al = len(self.auto.matrix) + len(newNodesPos)
            matrix = []
            nodes = []
            for i in range(al):
                if newPointer < len(newNodesPos) and newNodesSort[newPointer] == i:
                    matrix.append([])
                    nodes.append(random.randint(0, len(self.auto.funcs) - 1))
                    newPointer += 1
                else:
                    matrix.append([])
                    nodes.append(self.auto.nodes[oldPointer])
                    oldNodesPos.append(i)
                    oldPointer += 1
            for i in range(len(oldNodesPos)):
                for line in self.auto.matrix[i]:
                    matrix[oldNodesPos[i]].append((line[0], oldNodesPos[line[1]]))
            #print()
            for arrow in newArrows:
                #print(arrow)
                if arrow[0][0]:
                    arrowIn = newNodesPos[arrow[0][1]]
                else:
                    arrowIn = oldNodesPos[arrow[0][1]]
                if arrow[1][0]:
                    arrowOut = newNodesPos[arrow[1][1]]
                else:
                    arrowOut = oldNodesPos[arrow[1][1]]
                if random.randint(0, 2):
                    condition = (0, 0)
                else:
                    r = random.randint(1, len(self.auto.arrows) - 1)
                    condition = (r, random.randint(1, auto.weights[r]))
                matrix[arrowOut].insert(random.randint(0, len(matrix[arrowOut])), (condition, arrowIn))
            self.auto.matrix = matrix
            self.auto.nodes = nodes
            #if not flag:
                #print(newNodesPos, oldNodesPos, self.auto.nodes)
                #for line in self.auto.matrix:
                    #print(line)
        self.auto.size = 0
        for el in self.auto.matrix:
            self.auto.size += len(el)
        global globalGen
        self.gen = globalGen
        globalGen += 1
        self.family = set()
        self.family.add(self.gen)
        self.family.add(gen)
        self.rgb = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.auto.rudiments = []
        for i in range(len(self.auto.nodes)):
            self.auto.rudiments.append(1)

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
            return (), new
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
        self.plants = set()
        self.animals = []
        self.herbivores = []
        self.dec = 0
        self.last = 1
        for i in range(height):
            line = []
            for j in range(width):
                if random.randint(1, 100) <= 10:    # примерный процент травы в начале
                    grass = Grass(i, j)
                    self.plants.add(grass)
                    line.append(grass)
                else:
                    line.append(False)
            self.dirt.append(line)
        for i in range(height):
            line = []
            for j in range(width):
                if (i or j) and random.randint(1, 100) <= 1:    # примерный процент клеток с животными в начале
                    if random.randint(1, 100) <= 9:    # примерный процент хищников в начале
                        self.animals.append(Animal(i, j))
                        self.animals[len(self.animals) - 1].gen = 0
                        self.animals[len(self.animals) - 1].family = set()
                        self.animals[len(self.animals) - 1].family.add(0)
                        self.animals[len(self.animals) - 1].rgb = [0, 0, 100]
                        self.animals[len(self.animals) - 1].auto.nodes = auto.predatorNodes
                    else:
                        self.animals.append(Animal(i, j))
                    line.append(self.animals[len(self.animals) - 1])
                else:
                    line.append(False)
            self.field.append(line)

    def turn(self):
        global time
        plantTime[time] = []
        time = (time + 1) % period
        for plant in plantTime[time]:
            if not plant.dead:
                end = plant.turn(self.dirt)
                if end:
                    old, new = end
                    for o in old:
                        try:
                            self.plants.remove(o)
                        except KeyError:
                            print(o.name, o.x, o.y, time, o.green, o.nex, o.die)
                        self.dirt[o.x][o.y] = False
                        o.dead = True
                    for n in new:
                        self.plants.add(n)
                        self.dirt[n.x][n.y] = n

        newAnimals = self.animals.copy()
        sta = {-1: 0, 0: 0, 1: 0}    # словарь для подсчёта животных
        for animal in self.animals:
            if not time % 10:    # подсчёт количества животных каждую десятую итерацию
                if animal.gen in sta:    # -1 : труп, 0 : хищник, 1 : травоядный
                    sta[animal.gen] += 1
                else:
                    sta[animal.gen] = 1
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
                        o.dead = True
                        self.plants.remove(o)
                        self.dirt[o.x][o.y] = False
                for n in new:
                    if n.name == 'seed':
                        self.plants.add(n)
                        self.dirt[n.x][n.y] = n
                    else:
                        newAnimals.insert(0, n)
                        self.field[n.x][n.y] = n
        self.animals = newAnimals
        if not time % 10:    # вывод количества животных каждую десятую итерацию
            self.dec += 1
            print(self.dec, "; хищники", sta[0], "; травоядные", sta[1], "; трупы", sta[-1])
