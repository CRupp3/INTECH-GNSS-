def nmeaChecksum(sz):
    length = len(sz)
    i = 0
    cs = 0
    if sz[0] == '$':
        i += 1
    while i < length and sz[i]:
        cs ^= ord(sz[i])
        i += 1
    return format(cs, '02x')


#string = '$DT @'
#length = len(string)
#checksum = nmeaChecksum(string)
#print(length)
#print('Checksum: ', checksum)

#checksumHex = hex(checksum)
#print('Checksum hex: ', )