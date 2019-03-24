def dis(massge,Key):
    massge=''.join(filter(lambda x: x if((x>='a'and x<='z')or (x>='A'and x<='Z')or x=='{' or x=='}' or x==':' or x=='['or x==']'or x==','or x=='\''or x=='"') else '',massge.upper()))
    Key=''.join(filter(lambda x: x if((x>='a'and x<='z')or (x>='A'and x<='Z')) else '',Key.upper()))
    LenKey=len(Key)
    Cipmassge=""
    i=0
    for x in massge:
	    if x>='A' and x<='Z':
        	Cipmassge=Cipmassge+chr((((ord(x)-ord('A'))-(ord(Key[i%LenKey])-ord('A')))%26)+ord('A'))
        	i=i+1
	    else:
		    Cipmassge=Cipmassge+x
    return Cipmassge


