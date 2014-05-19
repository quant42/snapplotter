#! /usr/bin/env python

#
# This is a snap2 file reader 
#

# consts
AA_ONE_LETTER = [ "A", "R", "N", "D", "C", "Q", "E", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V" ]

import re, datetime, time, sys

class Matrix():
    
    """ This class is for reading in any snap2 (matrix) files in python """
    
    def __init__(self, filename):
        
        """ Parse a snap2 output file """
        
        # some patterns
        pattern1 = re.compile("(.)(\d*)(.)\s*=>\s*(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *(\d*) (\d*) *\\| *sum *= *(-?\d*)")
        pattern2 = re.compile("(.)(\d*)(.)\s*([^\s]*)\s*(\d*)\s*(\d*)%")
        
        # the matrix to readin
        self.matrix = []
        
        # a helper function to get the column, by the position
        def getColumn(matrix, pos, aaFrom):
            for column in reversed(matrix):
                if column.pos == pos:
                    return column
            column = MatrixColumn(pos, aaFrom)
            matrix.append(column)
            return column
        
        # ok, read in all snap2 lines
        try:
            with open(filename, "r") as f:
                for line in f:
                    line = line.strip()
                    match1 = pattern1.match(line)
                    if match1:
                        # ok, we found a line containing network results
                        col = getColumn(self.matrix, int(match1.group(2)), match1.group(1))
                        cell = col.getCellByAaTo(match1.group(3))
                        for i in range(0, 10):
                             cell.networks[ i ] = [ int(match1.group(4 + 2 * i)), int(match1.group(5 + 2 * i)) ]
                        cell.networkSum = int(match1.group(24))
                        # skip the next pattern matching search etc.
                        continue
                    match2 = pattern2.match(line)
                    if match2:
                        # ok, we found a line containing simple results
                        col = getColumn(self.matrix, int(match2.group(2)), match2.group(1))
                        cell = col.getCellByAaTo(match2.group(3))
                        cell.description = match2.group(4)
                        cell.relIndex = int(match2.group(5))
                        cell.accuracy = int(match2.group(6))
                        continue
                    print("Unexpected line: \"{}\"".format(line))
        except Exception as e:
            ts = datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')
            if sys.version_info >= (3, 0):
                print("[ERR READING SNAP2FILE {}] {} on line {}".format( ts, str(e), sys.exc_info()[2] ))
            else:
                print("[ERR READING SNAP2FILE {}] {} on line {}".format( ts, str(e), sys.exc_traceback.tb_lineno ))
            exit(1)
        
        # sort the matrix by position
        self.matrix.sort(key=lambda x: x.pos)
    
    def __len__(self):
        
        return len(self.matrix)
    
    def __iter__(self):
        
        return self.matrix.__iter__()
    
    def __getitem__(self, key):
        
        # slice object:
        if isinstance( key, slice ):
            arr = []
            key = slice(key.start, key.stop, 1 if not key.step else key.step)
            for column in self.matrix:
                if column.pos >= key.start and column.pos < key.stop and (column.pos - key.start) % key.step == 0:
                    arr.append(column)
                elif column.pos > key.stop:
                    break
            return arr
        # ok, index
        if isinstance( key, int ):
            for column in self.matrix:
                if column.pos == key:
                    return column
                elif column.pos > key:
                    break
            raise IndexError("Index \"{}\" out of range! (Maxval: \"{}\")".format(key, len(self)))
        raise TypeError("Invalid argument type.")
    
    def toSequence(self):
       
       """ Returns the primary sequence of a snap matrix """
       result = ""
       for c in self.matrix:
           result = result + c.aaFrom
       return result

class MatrixColumn():
    
    """ This class represents a single line in the matrix """
    
    def __init__(self, pos, aaFrom):
        
        self.aaFrom = aaFrom
        self.pos = pos
        self.column = [ MatrixCell() for i in range(0, 20) ]
    
    def getCellByAaTo(self, aminoAcid):
        
        return self.column[ AA_ONE_LETTER.index(aminoAcid.upper()) ]
    
    def __iter__(self):
        
        return self.column.__iter__()
    
    def __getitem__(self, key):
        
        return self.column[key]

class MatrixCell():
    
    """ This class represents a single cell of the snap2 matrix results """
    
    def __init__(self):
        
        self.networks = [ [ float('inf'), float('inf') ] for i in range(0, 10) ]
        self.networkSum = float('inf')
        self.description = "unknown"
        self.relIndex = float('inf')
        self.accuracy = float('inf')
