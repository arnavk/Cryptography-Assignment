import math
import random

dictionary = {}

def decrypt(ciphertext, key):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	plaintext = ""
	for c in ciphertext:
		if c.isalpha():
			plaintext = plaintext + alphabet[key.index(c)]
		else:
			plaintext = plaintext + c;
	return plaintext

def initializeDictionary():
	global dictionary
	for line in open ('count.txt'):
		parts = line.split();
		dictionary[parts[0]] = parts[1]
		

def getScore (ciphertext, key):
	global dictionary
	decryptedText = decrypt(ciphertext, key)
	# print decryptedText
	trigramMap = {}
	trigramList = []
	for i in range(0, len(decryptedText) - 2):
		if decryptedText[i:i+3].isalpha():
			trigramList.append(decryptedText[i:i+3])
	
	trigramSet = set(trigramList)
	# print trigramList

	for trigram in trigramList:
		trigramMap[trigram] = trigramList.count(trigram)

	score = 0

	for trigram in trigramSet:
		# print trigram + ":"
		# print trigramMap[trigram]
		# print dictionary[trigram]
		# print math.log(float(dictionary[trigram]), 2)
		score = score + ( trigramMap[trigram] * math.log(float(dictionary[trigram]), 2))

	return score

def getProbableKey(ciphertext):
	frequencyMap = {}
	alphabet = 'abcdefghijklmnopqrstuvwxyz'
	letters = set(ciphertext)
	maxCount = 0
	for letter in letters:
		if letter.isalpha():
			frequencyMap[letter] = ciphertext.count(letter)
			if frequencyMap[letter] > maxCount:
				maxCount = frequencyMap[letter]
	frequencyList = []
	for letter in frequencyMap.keys():
		count = frequencyMap[letter]
		num = ''
		for i in range(len(str(count)), len(str(maxCount))):
			num = num + '0'
		num = num + str(count) + '|' + letter
		frequencyList.append(num)
	# print frequencyList
	frequencyList.sort(reverse = True)
	
	sortedLetters = ''
	for entry in frequencyList:
		sortedLetters = sortedLetters + entry[-1:]

	# print sortedLetters
	normalDistribution = 'etaoinshrdlcumwfygpbvkxjqz'

	key = ''
	for c in alphabet:
		key = key + sortedLetters[normalDistribution.index(c)]

	# print key

	return key

def solve(ciphertext, numberOfTrials, numberOfSwaps, mode):
	initializeDictionary()
	negativeInfinity = - float ('inf')
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	bestKey = alphabet
	bestScore = negativeInfinity
	probableKey = getProbableKey(ciphertext)
	for i in range(0, numberOfTrials):
		print ('Working: ' + str(i*100.0/numberOfTrials) + '% completed')
		key = ''
		if mode == 0:
			key = ''.join(random.sample(alphabet, len(alphabet)))
		else:
			key = probableKey

		bestTrialScore = negativeInfinity

		for j  in range (0, numberOfSwaps):

			randInt1 = random.randint(0, 25)
			randInt2 = randInt1
			while (randInt2 == randInt1):
				randInt2 = random.randint(0,25)
			
			if randInt1 > randInt2:
				temp = randInt1
				randInt1 = randInt2
				randInt2 = temp

			newKey = key[0:randInt1] + key[randInt2] + key[randInt1+1:randInt2] + key[randInt1] + key[randInt2+1:len(key)] # make this mutate newKey
			score = getScore(ciphertext, newKey)
			if score > bestTrialScore:
				key = newKey
				bestTrialScore = score

			print ('Working: ' + str(j*100.0/numberOfSwaps) + '% of swaps completed')

		if bestTrialScore > bestScore:
			bestKey = key
			bestScore = bestTrialScore

	print 'Key: ' + bestKey
	print decrypt(ciphertext, bestKey)		
# analyse.solve ("", 15, 1000)

def decryptFile(filename):
	with open(filename, 'r') as content_file:
		content = content_file.read()
		solve (content, 5, 1000, 1)
		solve (content, 15, 1000, 0)

def test (filename):
	with open(filename, 'r') as content_file:
		content = content_file.read()
		getProbableKey(content)


# vmshjlobyaxcqzneupdrgfiktw