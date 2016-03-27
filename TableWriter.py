import shutil
import os
import subprocess
import sys
import math

from errors import FatalError

class TableWriter(object):
    def __init__(self):
        self.width = shutil.get_terminal_size().columns
        self.rows = []
        self.data = []
        self.colConf = []
        self.rowConf = []
        self.colNum = 0
        self.border_vert = " │ "
        self.border_hor = "─"#" "#
        self.border_inter = "┼"#"│"#
        self.empty_char = " " #"•"
        self.hasHeader = False
        self.colors = {
            "default"    : "\033[39m",
            "red"         : "\033[31m",
            "green"     : "\033[32m",
            "yellow"     : "\033[33m",
            "blue"         : "\033[34m"
        }
        self.headerContentFormat = "\033[1m" # bold text
        self.borderFormat = "\033[0m" # reset all
        self.hasColor = self.guessColorEnabled()
        
    def guessColorEnabled(self):
        r1 = os.isatty( sys.stdout.fileno() )
        if r1 == False:
            return False
        r2 = int( subprocess.check_output( ["tput","colors"] ).decode())
        return ( r1 and r2 > 0 )
        
    def setColorOutput(self, value ):
        r = self.guessColorEnabled()
        self.hasColor = (value and r)        
    
    def getConf(self, i, j, name):
        """ i: row, j:col, name:configNameString"""
        e = self.data[i][j]
        if name in e and e[name] != None:
            return e[name]
        elif name in self.rowConf[i] and self.rowConf[i] != None:
            return self.rowConf[i][ name ]
        elif name in self.colConf[j] and self.colConf[j] != None:
            return self.colConf[j][ name ]
        elif name in e:
            return e[name] # None
        else:
            raise TypeError( "unknown config id string" )
    
    def setConf(self, i, j, name, value):
        """ i:rowIdx, j:colIdx, name:configID, i=None:allRows, j=None:allCols"""
        if i == None and j == None:
            raise TypeError( "i and j cannot be None at the same time" )
        if i == None:
            self.colConf[j][ name ] = value
        elif j == None:
            self.rowConf[i][ name ] = value
        else:
            self.data[i][j][ name ] = value
        
    def getDefaultConf(self, data):
        return {"data":data, "color":None, "wrap":None,"heading":None} # colspan?
    def getDefaultColConf(self):
        return {"color":None, "wrap":None,"heading":None}
    def getDefaultRowConf(self):
        return {"color":None, "wrap":True,"heading":None}
    
    def appendRow(self, row ):
        r = []
        # copy element data
        for e in row:
            r.append( self.getDefaultConf(e) )
        # grow colConf to new col count
        if len(r) > len(self.colConf):
            for i in range( len(r)-self.colNum ):
                self.colConf.append( self.getDefaultColConf() )
        # append to data and add new config defaults
        self.data.append( r )
        self.rowConf.append( self.getDefaultRowConf() )
            
    def wrapText( self, text, startIndex ,maxWidth ):
        if startIndex >= len(text):
            raise IndexError( "invalid start index" )
        words = text[startIndex:].split(" ")
        i=0
        for w in words:
            if i+len(w)+1 <= maxWidth:
                i += (len(w)+1)
                continue
            elif len(w) >= maxWidth:
                i = maxWidth
            else:
                continue
        return startIndex + i
    
    def print_borderline(self, colMaxWidth ):
        border = ""
        if self.hasColor:
            border += self.borderFormat + self.colors["default"]
        border += math.floor(len(self.border_vert)/2)*" "+self.border_inter
        for i in range( len(self.colConf) ):
            border += self.border_hor*(colMaxWidth[i]+len(self.border_vert)-1)
            border += self.border_inter
        print( border )
        
    
    def print(self):
        avgs = []
        maxs = []
        # init 
        for i in range( len(self.colConf) ):
            avgs.append( 0 )
            maxs.append( 0 )
        # sum element length for all cols
        for row in self.data:
            for i in range(len(row)):
                contLen = len(row[i]["data"])
                avgs[i] += contLen
                if maxs[i] < contLen:
                    maxs[i] = contLen
        # get average content length per col
        s =0
        for i in range( len(self.colConf) ):
            avgs[i] = avgs[i] / len( self.data )
            if self.colConf[i]["wrap"] == False:
                avgs[i] = maxs[i]
            else:
                s += avgs[i] # do not add no-wrap cells

        # get the remaining space to distribute to wrapping cols
        flexWidth = self.width-len(self.border_vert)
        for i in range( len(self.colConf) ):            
            if self.colConf[i]["wrap"] == False:
                flexWidth -= maxs[i]
                flexWidth -= len(self.border_vert)
        if (flexWidth - self.colNum*len(self.border_vert)) <= 0 :
            raise FatalError( "Terminal is not wide enough to view this table" )        

        # finally distribute the available term width to all cols
        colMaxWidth = []
        for i in range( len(self.colConf) ):
            if self.colConf[i]["wrap"] == False:
                colMaxWidth.append( maxs[i] ) 
            else:
                per = (avgs[i]/s)*flexWidth
                colMaxWidth.append( math.floor( per )-len(self.border_vert) )
                # if average*width < 1char => column cannot be negative width
                if colMaxWidth[-1] <= 0:
                    colMaxWidth[-1] = 1
                    s += 1
        
        self.print_borderline(colMaxWidth)
        rowCount = 0
        for row in self.data:
            # init list of indices up to where cell content has been printed
            rowIdx = []
            for i in range( len(self.colConf) ):
                rowIdx.append(0)            
            # print lines while cells have data
            data = True
            while data == True:
                line = ""
                # add leftmost border
                if self.hasColor:
                    line = self.colors["default"] 
                line += self.border_vert
                t = True
                # print cell content for this line
                for i in range( len(row) ):
                    # set the right color
                    color = self.getConf( rowCount, i, "color" )
                    head  = self.getConf( rowCount, i, "heading" )
                    # set cell content color
                    if self.hasColor and color != None and color in self.colors:
                        line += self.colors[ color ]
                    # set bold for heading cells
                    if self.hasColor and head == True:
                        line += self.headerContentFormat 
                    if rowIdx[i] < len( row[i]["data"] ):
                        # if there is data in the cell row[i]
                        b = rowIdx[i] # start index of new content
                        rowIdx[i] = self.wrapText( row[i]["data"], rowIdx[i], colMaxWidth[i] )
                        e = rowIdx[i] # end index of new content
                        line += row[i]["data"][b:e].ljust( colMaxWidth[i], self.empty_char )
                    else:
                        line += (self.empty_char*colMaxWidth[i])
                    # add cell border 
                    if self.hasColor:
                        line += self.borderFormat + self.colors["default"] 
                    line += self.border_vert
                    if rowIdx[i] < len( row[i]["data"] ):
                        t = False # there is still content to distribute in this cell
                if t == True:
                    # t has not been touched by any cell of this row, 
                    # so all cells have been completely printed
                    data = False
                print(line)
            self.print_borderline(colMaxWidth)
            rowCount += 1
