from NMEAChecksum import nmeaChecksum

def formatReadNewest():
	stringSansCheck = ('$MM R=N')
	checksum = nmeaChecksum(stringSansCheck)
	string = (stringSansCheck + '*' + checksum + "\n")
	return string
	
