import random
PlainText_File = open("PlainText.txt","r")
PlainText = PlainText_File.read()

key_File = open("key.txt","r")
key = key_File.read()
Sbox = []
initial = []
final = []
def generateSBox() :
	for i in range (0,8):
		newSBox = []
		for j in range(0,4):
			linebox=[]
			while len(linebox) != 16 :
				x=random.randint(0,15)
				if x not in linebox :
					linebox.append(x)
			newSBox.append(linebox)
		Sbox.append(newSBox)
generateSBox()
def Eight (text) :
	if len(text)==8 :
		return text
	else :
		return Eight('0'+text)


def makeBinary (text):
	binary = ""
	for i in text  :
		asciiChar = ord(i)
		unequalBinary = bin(asciiChar)[2:]
		EightBitsBinary=Eight(unequalBinary)
		binary=binary+EightBitsBinary    	
	return binary



key56 = ""

for i in range(0,8) :
	temp_key = key [i*8:i*8+7]
	key56 += temp_key

def makeSequence(arr) :
	global final,initial
	if arr == "0" and initial !=[]:
		return initial
	elif arr=="1" and final != []:
		return final
	else :
		seqList=[]
		while len(seqList)<64:
			x=random.randint(0,63)
			if x not in seqList:
				seqList.append(x)
			else :
				continue
		if arr == '0' :
			initial = seqList
		else :
			final = seqList
		return seqList
def initialPermutation (key,PlainText):
	sequence = makeSequence('0')
	text1 = ""
	for i in range(0,64):
		oneChar = PlainText[sequence[i]]
		text1+=oneChar

	return text1[0:32],text1[32:],sequence

def expandRight(text) :
	right48 = ""
	for i in range (0,8) :
		FourBitStr =  text[i*4:i*4+4]
		prevBlock = ((i+7)%8)
		nextBlock = ((i+1)%8)
		prevBit = text[prevBlock*4+3]
		nextBit = text[nextBlock*4]
		SixBits = prevBit+FourBitStr+nextBit
		right48+=SixBits
	return right48


def XOR (text1,text2):
	if len(text1) == len(text2) :
		op = ""
		for i in range(0,len(text1)):
			if (text1[i]==text2[i]):
				op+='0'
			else :
				op+='1'
		return op

def binaryToDecimal(binaryNum) :
	RevbinaryNum = binaryNum[::-1]
	j=1
	decNum = 0
	for i in range(0,len(binaryNum)):
		x=j*int(RevbinaryNum[i])
		j*=2
		decNum += x
	return decNum

def SBoxOperations (text,Snum) :
	row = text[0] + text[5]
	col = text[1:5]
	rowDec = binaryToDecimal(row)
	colDec = binaryToDecimal(col)
	block = Sbox[Snum]
	value = block[rowDec][colDec]
	valueBinary = bin(value)
	valueBinary = valueBinary[2:]
	while len (valueBinary) != 4 :
		valueBinary = '0' + valueBinary
	return valueBinary

def rounds (left,right,key56,roundNo) :
	Op_Left = right
	right_48bit = expandRight(right)
	manglerOp = XOR(right_48bit,keyBox[roundNo-1])
	mangler32=""
	for i in range (0,8) :
		seq6 = manglerOp[i*6:i*6+6]
		seq4 = SBoxOperations(seq6,i)
		mangler32+=seq4
	Op_right = XOR(left,mangler32)
	return Op_Left,Op_right
# TODO: 
bitsShift = [1,2,9,16]

def RotateLeft(text):
	text1=text[1:]
	text2=text[0]
	return text1+text2
keyBox=[]
keySequenceBox=[]

def Generate48KeySequence  (keyLR) :

	keySeq =[]
	key_48 = ""
	while len(keySeq) != 48:
		i=random.randint(0,55)
		if i not in keySeq :
			keySeq.append(i)
	for j in keySeq :
		key_48+=keyLR[j]
	return keySeq,key_48

def keyGeneration (keyL,keyR,i) :
	global keyBox , keySequenceBox
	if i>16:
		return 
	else :
		keyL = RotateLeft(keyL)
		keyR = RotateLeft(keyR)
		if i not in bitsShift :
			keyL = RotateLeft(keyL)
			keyR = RotateLeft(keyR)
		keySeq,key_48 = Generate48KeySequence(keyL+keyR)
		keyBox.append(key_48)
		keySequenceBox.append(keySeq)
		keyGeneration(keyL,keyR,i+1)

def FinalPermutation(text) :
	sequenceFinal = makeSequence('1')
	finalOp=""
	for i in range (0,64):
		x=text[sequenceFinal[i]]
		finalOp+=x 
	return finalOp,sequenceFinal

def printArray (arr) :
	for i in arr :
		print(i)

def encryption (key,PlainText) :
	left,right,initialsequence = initialPermutation (key,PlainText)
	for count in range (1,17):
	 	left,right = rounds(left,right,key56,count)
		
	
	finalOp,finalSequence = FinalPermutation(left+right)
	return initialsequence,finalSequence,finalOp


keyGeneration(key56[0:28],key56[28:],1)
inputText = ""
cipherOp=""
for i in PlainText :
	binaryPlainText = str(makeBinary(i))
	inputText+=binaryPlainText 
	if len(inputText) == 64 :
		initialsequence,finalSequence,cipher=encryption(key56,inputText)
		cipherOp += cipher
		inputText = ""

if len(inputText) > 0 and len(inputText) < 64 :
	while len(inputText) !=64 :
		inputText += makeBinary(chr(0))

	initialsequence,finalSequence,cipher=encryption(key56,inputText)
	cipherOp+=cipher

def printSingleArray (arr) :
	for i in range(0,len(arr)):
		if i%8  != 0 or i==0:
			print(arr[i],end=" ")
		else :
			print(i)
print(f"PlainText - {PlainText}")
print("Initial Permutation\n["  )
printSingleArray(initialsequence)
print("]\n")
print("Final Permutation\n[")
printSingleArray(finalSequence)
print("]\n")

for i in range(0,8) :
	print(f"\nS Box {i+1} \n")
	printArray(Sbox[i])
print("\n\nCipher Text -",cipherOp,len(cipherOp))
		
opFile = open("CipherText.txt","w")
opFile.write(cipherOp)
opFile.close()
PlainText_File.close()
key_File.close()


