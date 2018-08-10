# -*- coding: utf-8 -*-

import difflib

class ColorDiff( object ):
    
    def __init__(self):
        self.colors = {
            "default" : {"ansi": "\033[39m", "css":"#000" },
            "red"     : {"ansi": "\033[31m", "css":"#651e1d" },
            "green"   : {"ansi": "\033[32m", "css":"#567b24" },
            "yellow"  : {"ansi": "\033[33m", "css":"#cc9900" },
            "blue"    : {"ansi": "\033[34m", "css":"#246281" },
        }
    
    def paintColorString(self, mode, color, inString ):
        if mode == "ansi":
            return self.colors[color]["ansi"] + inString + self.colors["default"]["ansi"]
        else:
            return "<span style='color:{0}'>{1}</span>".format(self.colors[color]["css"], inString)

    def colorDiff(self, colorMode, text, n_text):
        """
        https://stackoverflow.com/questions/10775029/finding-differences-between-strings
        """
        seqm = difflib.SequenceMatcher(None, text, n_text)
        output_orig = []
        output_new = []
        for opcode, a0, a1, b0, b1 in seqm.get_opcodes():
            orig_seq = seqm.a[a0:a1]
            new_seq = seqm.b[b0:b1]
            if opcode == 'equal':
                output_orig.append(orig_seq)
                output_new.append(orig_seq)
            elif opcode == 'insert':
                output_new.append( self.paintColorString( colorMode, "green", new_seq ) )
            elif opcode == 'delete':
                output_orig.append( self.paintColorString( colorMode, "red", orig_seq ) )
            elif opcode == 'replace':
                output_new.append( self.paintColorString( colorMode, "yellow", new_seq ) )
                output_orig.append( self.paintColorString( colorMode, "yellow", orig_seq ) )
        return ''.join(output_orig), ''.join(output_new)
