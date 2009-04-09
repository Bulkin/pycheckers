class Checkers:
    FREE = 0
    WH = 1
    BL = 2
    WHK = -1
    BLK = -2

    def __init__(self):
        self.array = {}

        self.countWH = 0
        self.countBL = 0
        for i in range(8):
            for ii in range(8):
                if not (i+ii) % 2:
                    continue
                if i < 3:
                    self.array[(ii,i)] = Checkers.WH
                    self.countWH+=1
                elif i < 5:
                    self.array[(ii,i)] = Checkers.FREE
                else:
                    self.array[(ii,i)] = Checkers.BL
                    self.countBL+=1
                    
        self.turn = Checkers.BL
        # test
        self.array[(3,4)] = self.WHK
        self.array[(4,3)] = self.WHK
        self.countWH += 2

        self.m = []
        self.turn = self.BL

        self.__checkBoard()
        
    def checkTile(self, x, y):
        return self.array[(x,y)]
    
    def __getDiag(self, x, y, inc):
        a = []
        if (y + inc) >= 0:
            if (x - 1) >= 0:
                a.append((x-1,y+inc))
            elif (x + 1) < 8:
                a.append((x+1,y+inc))
            else:
                return []
        return a

    def __checkBoard(self):
        self.m = []
        self.noeat = True
        for i in self.array:
            self.__findMoves(i)
        #debug
        print self.m

    def __findMoves(self, piece):
        if abs(self.array[piece]) != self.turn:
            return
        # piece coordinates
        x = piece[0]
        y = piece[1]
        # is white's turn
        wh = abs(self.array[piece]) == self.WH
        # is king
        k = self.array[piece] < 0
        
        index = len(self.m)

        for i in [-1,1]:
            # men can't move backwards
            if not k:
                if y + i < 0 or y + i > 7:
                    continue
                if wh and i == -1:
                    continue
                if not wh and i == 1:
                    continue
                
            for ii in [-1,1]:
                # out of bounds
                if x + ii < 0 or x + ii > 7:
                    continue
                
                # free spot ahead
                if self.array[(x+ii,y+i)] == self.FREE and self.noeat:
                    if index == len(self.m):
                        self.m.append([piece])
                    self.m[index].append((x+ii,y+i))
                # enemy piece ahead
                elif (abs(self.array[(x+ii,y+i)]) == self.WH) != wh:
                    # out of bounds
                    if (x + ii*2 < 0) or (x + ii*2 > 7):
                        continue
                    if (y + i*2 < 0) or (y + i*2 > 7):
                        continue
                    
                    if (self.array[(x+ii*2, y+i*2)]) == self.FREE:
                        if self.noeat:
                            self.noeat = False
                            self.m = []
                            index = 0
                        if index == len(self.m):
                            self.m.append([piece])
                        self.m[index].append((x+ii*2, y+i*2))
                        return self.m[index]
        return None

    def getSelected(self):
        for i in self.m:
            if i[0] == self.selected:
                return i
        return [self.selected]

    def setSelected(self, piece):
        x = piece[0]
        y = piece[1]
        if not (x + y) % 2:
            return None
        if abs(self.array[(x,y)]) != self.turn:
            return None
        self.selected = (x, y)
        return (x, y)



    def move(self, moves, target):
        src = moves[0]
        dest = target
        
        if self.noeat:
            self.array[dest] = self.array[src]
            self.array[src] = self.FREE
            self.turn = self.turn % 2 + 1
            self.__checkBoard()
        else:
            dx = dest[0] - src[0]
            dy = dest[1] - src[1]
            enemy = (src[0]+dx/2,src[1]+dy/2)
            self.array[enemy] = self.FREE
            if self.turn == self.BL:
                self.countWH-=1
            else:
                self.countBL-=1
            self.array[dest] = self.array[src]
            self.array[src] = self.FREE
            self.m = []
            if not self.__findMoves(dest):
                self.turn = self.turn % 2 + 1
                self.__checkBoard()
        # king
        if dest[1] == 0 or dest[1] == 7:
            self.array[dest] *= -abs(self.array[dest])
        return dest
        
