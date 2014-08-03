# Python implementation of QNAP's encoding function
# Converted from http://eu1.qnap.com/Storage/SDK/get_sid.js

ezEncodeChars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'

def ezEncode(str):
    out = ''
    length = len(str)

    i = 0
    while i < length:
        c1 = ord(str[i]) & 0xff
        i += 1
        if i == length:
            out += ezEncodeChars[c1 >> 2]
            out += ezEncodeChars[(c1 & 0x3) << 4]
            out += '=='
            break
        c2 = ord(str[i])
        i += 1
        if i == length:
            out += ezEncodeChars[c1 >> 2]
            out += ezEncodeChars[((c1 & 0x3) << 4) | ((c2 & 0xF0) >> 4)]
            out += ezEncodeChars[(c2 & 0xF) << 2]
            out += '='
            break
        c3 = ord(str[i])
        i += 1
        out += ezEncodeChars[c1 >> 2]
        out += ezEncodeChars[((c1 & 0x3)<< 4) | ((c2 & 0xF0) >> 4)]
        out += ezEncodeChars[((c2 & 0xF) << 2) | ((c3 & 0xC0) >> 6)]
        out += ezEncodeChars[c3 & 0x3F]

    return out
