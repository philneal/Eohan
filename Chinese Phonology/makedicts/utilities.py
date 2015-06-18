# Routine for converting glyphs into codepoints:
# gets round the problem of Windows narrow build.
# Windows Python assumes 16 bit reg assumes 16-bit
# registers and cannot handle Unicode above U+FFFF.
def hexStringToBin(s):
    return bin(int(repr(s)[3:-1],16))[2:]

def binStringToHex(s):
    # '11110000' -> '80' -> '0x8d' -> '8d'
    #print hex(int(s,2))[2:]
    return hex(int(s,2))[2:]
  
def lineToCodepoints(line):
    l = []
    while len(line) > 0:
        nextByte = hexStringToBin(line[0])
        line = line[1:]
        firstBit = nextByte[0]
        nextByte = nextByte[1:]
        if firstBit == "0":
            codepoint = binStringToHex(nextByte)
        elif firstBit == "1":
            while nextByte[0] == "1":
                nextByte = nextByte[1:] + hexStringToBin(line[0])[2:]
                line = line[1:]
            codepoint = binStringToHex(nextByte)
            codepoint = codepoint.upper()
        l.append(u"U+" + codepoint)
    return l

# A prettyprint routine for debugging output
def pp(arg):
    if isinstance(arg,list):
        if arg == []:
            return u"[]"
        else:
            myStr = u"["
            for item in arg:
                myStr += pp(item)
                myStr += u", "
            myStr = myStr[:-2]
            myStr += u"]"
            return myStr
    elif isinstance(arg,dict):
        if arg == {}:
            return u"{}"
        else:
            myStr = u"{"
            for key in arg.keys():
                myStr += pp(key)
                myStr += u": "
                myStr += pp(arg[key])
                myStr += u", "
            myStr = myStr[:-2]
            myStr += u"}"
            return myStr
    elif not isinstance(arg,basestring):
        return str(arg)
    else:
        return arg

# a prettyprint routine for debugging output
def pp(arg):
    if isinstance(arg,list):
        if arg == []:
            return u"[]"
        else:
            myStr = u"["
            for item in arg:
                myStr += pp(item)
                myStr += u", "
            myStr = myStr[:-2]
            myStr += u"]"
            return myStr
    elif isinstance(arg,dict):
        if arg == {}:
            return u"{}"
        else:
            myStr = u"{"
            for key in arg.keys():
                myStr += pp(key)
                myStr += u": "
                myStr += pp(arg[key])
                myStr += u", "
            myStr = myStr[:-2]
            myStr += u"}"
            return myStr
    elif not isinstance(arg,basestring):
        return str(arg)
    else:
        return arg
