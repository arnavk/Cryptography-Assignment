import math
import random

dictionary = {}
quick = 1
full = 2

# This method deciphers a ciphertext for a particular key
def decrypt(ciphertext, key):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	plaintext = ""
	for c in ciphertext:
		if c.isalpha():
			plaintext = plaintext + alphabet[key.index(c)] # deciphering only alphabetic characters
		else:
			plaintext = plaintext + c; # punctuation marks/other non-alphabetic characters get copied verbatim
	return plaintext

def initializeDictionary():
	global dictionary
	# reading information from the file with trigram probabilites and saving it in the dictionary
	for line in open ('count.txt'):
		parts = line.split();
		dictionary[parts[0]] = parts[1]
		

def getScore (ciphertext, key):
	# evaluates the score of the key. For more information on the formula, read the attached document.

	global dictionary
	decryptedText = decrypt(ciphertext, key)

	trigramMap = {}
	trigramList = []
	for i in range(0, len(decryptedText) - 2):
		if decryptedText[i:i+3].isalpha():
			trigramList.append(decryptedText[i:i+3])
	
	trigramSet = set(trigramList)

	for trigram in trigramList:
		trigramMap[trigram] = trigramList.count(trigram)

	score = 0

	for trigram in trigramSet:
		score = score + ( trigramMap[trigram] * math.log(float(dictionary[trigram]), 2))

	return score

def getProbableKey(ciphertext):
	# performing analysis and returing a "probable key". This is found by sorting the alphabet appearing in the cipher text in descending order and matching it against the statistical probability of the alphabet in english.
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

	frequencyList.sort(reverse = True)
	
	sortedLetters = ''
	for entry in frequencyList:
		sortedLetters = sortedLetters + entry[-1:]

	normalDistribution = 'etaoinshrdlcumwfygpbvkxjqz'

	key = ''
	for c in alphabet:
		key = key + sortedLetters[normalDistribution.index(c)]

	return key

def solve(ciphertext, numberOfTrials, numberOfSwaps, mode):
	# For a detailed explanation on this alorithm, please refer to the attached documentation.
	global quick, full
	initializeDictionary()
	negativeInfinity = - float ('inf')
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	bestKey = alphabet
	bestScore = negativeInfinity
	probableKey = getProbableKey(ciphertext)
	for i in range(0, numberOfTrials):
		print ('Working: ' + str(i*100.0/numberOfTrials) + '% completed')
		key = ''
		if mode == quick:
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

def decryptFile(filename):
	global quick,  full
	with open(filename, 'r') as content_file:
		content = content_file.read()
		solve (content, 5, 1000, quick)
		solve (content, 15, 1000, full)
