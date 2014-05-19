#! /usr/bin/env python

import re

# ok, an msa plotter
class MsaReader:
    
    """ A class for plotting msa files! """
    
    def __init__(self, fileName):
        
        """ Parse an msa by a file """
        
        self.fileName = fileName
        pattern = re.compile("^([^ ]*) *(.*)$")
        
        self.identifiers = []
        self.aligns = []
        
        fasta, firstLine = False, True
        
        with open(fileName, "r") as f:
            for line in f:
                if firstLine and line.startswith(">"):
                    fasta = True
                line = line.strip()
                # check wheather to parse fasta or my own format?
                # parse fasta
                if fasta:
                    if line.startswith(">"):
                        self.identifiers.append(line[1:].strip())
                        self.aligns.append("")
                    else:
                        self.aligns[-1] = self.aligns[-1] + line
                # parse my own format
                else:
                    if line.startswith("#") or line.startswith("/") or line.startswith("'") or line == "":
                        continue
                    match = pattern.match(line)
                    if match:
                        self.identifiers.append(match.group(1))
                        self.aligns.append(match.group(2))
            firstLine = False
        
        # check
        if len(self.aligns) < 1:
            raise Exception("No sequence found in this alignment!")
        length = len(self.aligns[0])
        self.length = length
        for l in self.aligns:
            if len(l) != length:
                raise Exception("MSA format error! Sequences have different lengths!")
