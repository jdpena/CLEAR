# XXX A. XXX. Distribution is unlimited.

# XXX supported XXXnder XXX of XXX for 
# XXX and XXX under XXX Contract No. XXX-15-D-XXX. Any opinions,
# findings, XXX 
# of the author(s) XXX the XXX 
# XXX of XXX for XXX and XXX.

# © 2023 XXX.

# XXX.XXX-11 Patent Rights - XXX (May 2014)

# The software/XXX-Is basis

# XXX.S. XXX with Unlimited Rights, as defined in XXX Part 
# XXX.XXX-XXX or 7014 (Feb 2014). Notwithstanding any copyright notice, 
# U.S. XXX rights in this work are defined by XXX XXX.XXX-XXX or 
# XXX XXX.XXX-7014 as detailed above. Use of this work other than as specifically
# XXX XXX.S. XXX may violate any copyrights that exist in this work.

class Output():

    def __init__(self, objects) -> None:
        self.target = None
        if not len(objects) : return
        self.objects = objects
   

    def getOutputString(self) :
        if self.objects == None : return None
        outputString = ""

        for i in self.objects :
            if not outputString == "" :
                  outputString += '&'
                  
            outputString += "{},{},{}".format(i.label, i.midPoint[0],i.midPoint[1])
            for j in i.sub_objects :
                 outputString += "; {},{},{}".format(j.label, j.midPoint[0], j.midPoint[1])
        return outputString
     
    def percentDif(self, x, y) :
            return abs((x - y)/((x+y)/2))