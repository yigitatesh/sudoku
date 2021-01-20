import numpy as np
import random


### SUDOKU ###
class Sudoku(object):
    """Creates a sudoku object that can handle sudoku events.

    Initially creates a sudoku solution filled with digits."""
    def __init__(self):
        # keeps track to end sudoku creating process
        # set to False to kill the whole creating process 
        self.alive = True
        # keeps whether sudoku playboard created or not
        self.fullyCreated = False
        # sudoku board which will keep solution
        self.sudokuSol = np.zeros((3,3,3,3), dtype=int)
        # numbers which can be in sudoku
        self.numbers = [1,2,3,4,5,6,7,8,9]
        # create sudoku solution
        self.createSudokuSol()
        # sudoku board to try to solve each step and decide
        # whether it is solvable or not
        self.tryBoard = np.copy(self.sudokuSol) #sudoku
        # sudoku board which game will be played
        self.playBoard = np.copy(self.sudokuSol) #sudoku_game
        # if you want to reset board to initial sudoku game
        self.resetBoard = None

    ## kill the whole sudoku creating process
    def kill(self):
        self.alive = False

    # is full sudoku board valid
    @staticmethod
    def isSudokuValid(sudoku_brd):
        for i in range(3):
            for j in range(3):
                for k in range(3):
                    for l in range(3):
                        digit = sudoku_brd[i,j,k,l]
                        sudoku_brd[i,j,k,l] = 0
                        if (digit in sudoku_brd[i,:,k]) or (digit in sudoku_brd[:,j,:,l]) or (digit in sudoku_brd[i,j]):
                            return False
                        sudoku_brd[i,j,k,l] = digit
        return True

    ## are two sudoku boards same
    @staticmethod
    def areBoardsSame(board1, board2):
        return np.array_equal(board1, board2)

    ## remove a number from playboard and returns it's location
    def removeNumberReturnLocAndDigit(self, remove_count):
        count = 0
        while count < remove_count:
            a = random.randint(0,2)
            b = random.randint(0,2)
            c = random.randint(0,2)
            d = random.randint(0,2)
            digit = self.tryBoard[a,b,c,d]
            if digit != 0 and [a,b,c,d] not in self.removedNumbersList:
                self.tryBoard[a,b,c,d] = 0
                count += 1
        return digit, [a,b,c,d]

    ## update number lists of sudoku squares
    def updateNumberLists(self):
        for blk in range(3):
            for sqr in range(3):
                for row in range(3):
                    #look for all points
                    for col in range(3):
                        r = blk*3 + row%3
                        c = sqr*3 + col%3
                        if self.tryBoard[blk,sqr,row,col] == 0:
                            n = 0
                            while n<len(self.num_list[r][c]):
                                number = self.num_list[r][c][n]
                                if (number in self.tryBoard[blk,:,row]) or\
                                   (number in self.tryBoard[:,sqr,:,col]) or (number in self.tryBoard[blk,sqr]):
                                    del self.num_list[r][c][n]
                                else:
                                    n += 1
                        else:
                            self.num_list[r][c] = []

    ### checkings for use a solving technique or not ###
                            
    # are there points which can have only one digit
    # 0 3 2 
    # 1 4 8 -> 0 digit is a certain point, it can take 5 only.
    # 9 7 6
    @staticmethod
    def certainPoints(numberlist):
        for i in numberlist:
            for j in i:
                if len(j) == 1:
                    return True
        return False

    # are there points which must have one digit in a 3x3 square 
    # 0 1 2 | 0 0 0    first 0 seems it can take 3,5,7,9. but it must take 7.
    # 0 0 0 | 7 3 4 -> because it is the only point which can take 7 in that square. 
    # 4 6 8 | 5 1 2    other three 0's can't take 7 because of 7 in their row.
    @staticmethod
    def certainPointsInSquares(numberlist):
        for blk in range(3):
            for sqr in range(3):
                digit_count_list = [0 for d in range(9)]
                #look for squares
                for row in range(3):
                    #look for all points
                    for col in range(3):
                        r = blk*3 + row%3
                        c = sqr*3 + col%3
                        digitlist = numberlist[r][c]
                        for digit in digitlist:
                            digit_count_list[digit-1] += 1
                #check whether there are certain points
                if 1 in digit_count_list:
                    return True
        return False

    # are there points which must have one digit in a row
    # 0 1 5 | 0 4 6 | 2 0 3 |    
    # 8 0 4 | 0 0 0 | 0 0 0 |     first 0 seems it can take 7 or 8
    # 0 0 0 | 0 0 0 | 0 0 0 | ->  but it must take 7
    # ------|-------|-------|     because there is no place to take 7 in that row
    #         7
    #                   7
    @staticmethod
    def certainPointsInRows(numberlist):
        #look for rows
        for r in range(9):
            digit_count_list = [0 for d in range(9)]
            for c in range(9):
                digitlist = numberlist[r][c]
                for digit in digitlist:
                    digit_count_list[digit-1] += 1
            #check whether there are certain points
            if 1 in digit_count_list:
                return True
        return False

    # are there points which must have one digit in a column
    @staticmethod
    def certainPointsInCols(numberlist):
        #look for cols
        for c in range(9):
            digit_count_list = [0 for d in range(9)]
            for r in range(9):
                digitlist = numberlist[r][c]
                for digit in digitlist:
                    digit_count_list[digit-1] += 1
            #check whether there are certain points
            if 1 in digit_count_list:
                return True
        return False

    ### sudoku solving techniques ###

    # put digits to points which can take only one digit clearly
    def putOnlyDigits(self):
        for blk in range(3):
            for sqr in range(3):
                for row in range(3):
                    #look for all points
                    for col in range(3):
                        r = blk*3 + row%3
                        c = sqr*3 + col%3
                        if len(self.num_list[r][c]) == 1:
                            self.tryBoard[blk,sqr,row,col] = self.num_list[r][c][0]
                            self.num_list[r][c] = []

    # put digits to points which can take only one digit by looking 3x3 squares
    def putOnlyDigitsInSquares(self):
        for blk in range(3):
            for sqr in range(3):
                #keeps count of possible digits in a 3x3 square
                digit_count_list = [0 for d in range(9)]
                #keeps possible digits locations
                digit_locs = [[] for l in range(9)]
                #look for squares
                for row in range(3):
                    #look for all points
                    for col in range(3):
                        r = blk*3 + row%3
                        c = sqr*3 + col%3
                        digitlist = self.num_list[r][c]
                        for digit in digitlist:
                            digit_count_list[digit-1] += 1
                            if not digit_locs[digit-1]:
                                digit_locs[digit-1] = [blk,sqr,row,col]
                #update points by looking digit counts
                for i in range(9):
                    if digit_count_list[i] == 1:
                        location = digit_locs[i]
                        self.tryBoard[location[0],location[1],location[2],location[3]] = i+1

    # put digits to points which can take only one digit by looking rows
    def putOnlyDigitsInRows(self):
        #look for rows
        for r in range(9):
            #keeps count of possible digits in a 3x3 square
            digit_count_list = [0 for d in range(9)]
            #keeps possible digits locations
            digit_locs = [[] for l in range(9)]
            for c in range(9):
                blk = r//3
                sqr = c//3
                row = r%3
                col = c%3
                digitlist = self.num_list[r][c]
                for digit in digitlist:
                    digit_count_list[digit-1] += 1
                    if not digit_locs[digit-1]:
                        digit_locs[digit-1] = [blk,sqr,row,col]
            #update points by looking digit counts
            for i in range(9):
                if digit_count_list[i] == 1:
                    location = digit_locs[i]
                    self.tryBoard[location[0],location[1],location[2],location[3]] = i+1

    # put digits to points which can take only one digit by looking columns
    def putOnlyDigitsInCols(self):
        #look for cols
        for c in range(9):
            #keeps count of possible digits in a 3x3 square
            digit_count_list = [0 for d in range(9)]
            #keeps possible digits locations
            digit_locs = [[] for l in range(9)]
            for r in range(9):
                blk = r//3
                sqr = c//3
                row = r%3
                col = c%3
                digitlist = self.num_list[r][c]
                for digit in digitlist:
                    digit_count_list[digit-1] += 1
                    if not digit_locs[digit-1]:
                        digit_locs[digit-1] = [blk,sqr,row,col]
            #update points by looking digit counts
            for i in range(9):
                if digit_count_list[i] == 1:
                    location = digit_locs[i]
                    self.tryBoard[location[0],location[1],location[2],location[3]] = i+1

    
    ## create sudoku solution
    def createSudokuSol(self):
        self.trialLimit = 10
        self.trial = 0
        self.created = False
        while not self.created and self.alive:
            ## creating
            for blk in range(3):
                for sqr in range(3):
                    # look for 3x3 squares
                    while (True):
                        for row in range(3):
                            for col in range(3):
                                # create a num list for each square in sudoku
                                nums = self.numbers.copy()
                                n = 0
                                # update point's num list
                                while (n<len(nums)):
                                    #if number exists in the row, the column or the 3x3 square, remove it from the list
                                    if (nums[n] in self.sudokuSol[blk,:,row]) or\
                                       (nums[n] in self.sudokuSol[:,sqr,:,col]) or (nums[n] in self.sudokuSol[blk,sqr]):
                                        del nums[n]
                                    else:
                                        n+=1
                                if len(nums) == 0:
                                    self.sudokuSol[blk,sqr,row,col] = 0
                                else:
                                    self.sudokuSol[blk,sqr,row,col] = random.choice(nums)
                        #if 3x3 square is incorrect, recreate 3x3 square
                        if 0 in self.sudokuSol[blk,sqr]:
                            self.sudokuSol[blk,sqr] = 0
                            self.trial+=1
                        else:
                            self.trial = 0
                            break
                        #if trial limit exceed, recreate sudoku board
                        if self.trial >= self.trialLimit:
                            break
            ## check whether sudoku is correct or not
            if 0 in self.sudokuSol:
                self.sudokuSol[:,:,:,:] = 0
            else:
                self.created = True

    ## create sudoku playboard
    def createPlayBoard(self):
        """Creates a playboard by using sudoku solution named 'playBoard'"""
        self.removedNumbers = 0
        self.removedNumbersList = []
        self.maxRemoveCount = 53
        self.removeTrials = 0
        #self.maxRemoveTrials = 30

        self.fullyCreated = False
        while not self.fullyCreated and self.alive:
            self.tryBoard = np.copy(self.playBoard)
            #remove one number from tryBoard (assign it to 0)
            digit, digit_loc = self.removeNumberReturnLocAndDigit(1)
            self.removedNumbersList.append(digit_loc)
            #copy tryBoard
            #playBoard is board will be game if tryBoard can be solved
            self.playBoard = np.copy(self.tryBoard)
            #create lists of possible digits for every point
            self.num_list = [[self.numbers.copy() for i in range(9)] for j in range(9)]
            #check whether it is solvable or not
            #solve loop
            self.solve = False
            #trials
            self.solveTrial = 0
            self.maxSolveTrial = 20
            #count of solve techniques
            #self.count_look_only_digits = 0
            #self.count_look_squares = 0
            #self.count_look_rows = 0
            #self.count_look_cols = 0
            # solve current board (tryBoard)
            while not self.solve and self.alive:
                #update number lists of possible numbers for all points
                self.updateNumberLists()
                #check whether there are points which can take only 1 digit
                if self.certainPoints(self.num_list):
                    self.putOnlyDigits()
                    #self.count_look_only_digits += 1
                #check whether there are digits which can only be in one point in a 3x3 square 
                elif self.certainPointsInSquares(self.num_list):
                    self.putOnlyDigitsInSquares()
                    #self.count_look_squares += 1
                #check whether there are digits which can only be in one point in a row
                elif self.certainPointsInRows(self.num_list):
                    self.putOnlyDigitsInRows()
                    #self.count_look_rows += 1
                #check whether there are digits which can only be in one point in a column
                elif self.certainPointsInCols(self.num_list):
                    self.putOnlyDigitsInCols()
                    #self.count_look_cols += 1
                else:
                    self.solve = True
                self.solveTrial+=1
                #check whether sudoku is solved or not
                if not 0 in self.tryBoard:
                    self.solve = True
                elif self.solveTrial >= self.maxSolveTrial:
                    self.solve = True

            #it is solved or not
            if self.areBoardsSame(self.tryBoard, self.sudokuSol):
                self.removedNumbers += 1
                self.removedNumbersList = []
            else:
                self.playBoard[digit_loc[0],digit_loc[1],digit_loc[2],digit_loc[3]] = digit
                #self.removeTrials += 1

            #check removed numbers count
            if self.removedNumbers >= self.maxRemoveCount:
                self.fullyCreated = True
            if len(self.removedNumbersList) >= 81-self.removedNumbers:
                self.fullyCreated = True
##            if self.removeTrials >= self.maxRemoveTrials:
##                self.fullyCreated = True

        # keeps initial sudoku playboard
        self.resetBoard = np.copy(self.playBoard)

        #save sudoku solution and sudoku game
        #np.save("sudoku_sol", self.sudokuSol)
        #np.save("sudoku_game", self.playBoard)
