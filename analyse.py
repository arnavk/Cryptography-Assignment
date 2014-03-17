def decrypt(ciphertext, key):
	alphabet = "abcdefghijklmnopqrstuvwxyz"
	plaintext = ""
	for c in ciphertext:
		if c not in alphabet:
			plaintext = plaintext + c;
		else:
			plaintext = plaintext + alphabet[key.index(c)]
	return plaintext
