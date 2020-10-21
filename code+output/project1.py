import numpy as np
def caeser(plain,key):
    plain = plain.upper()
    cipher = str()
    for p in plain:
        cipher += chr(((ord(p) - ord('A') + key) % 26) + ord('A'))
    return cipher
def playfair(plain,key):
    key = key.upper()
    plain = str(plain).upper().replace("J","I")
    posdic = dict() # represent the order of each letter in the key matrix if it was 1D
    index = 0# the index of the current letter in the posdic
    letters = ""

    for k in key:
        if(k not in posdic):
            letters+=k
            posdic[k] = index
            index += 1

    for i in range(ord("A"),ord("Z") + 1):
        if(i == ord("J")):
            continue
        if(chr(i) not in posdic):
            posdic[chr(i)] = index
            letters+=chr(i)
            index += 1

    pairs = list()
    i = 0
    while i < len(plain):
        if i == len(plain) - 1: # only last letter left
            if(plain[i] == "X"): # if the single letter is x append z
                pairs.append(("X","z"))
            else: # if last letter not x append x
                pairs.append((plain[i],"X")) 
        elif plain[i] == plain[i+1]: # letter is same as next one
            pairs.append((plain[i],"X")) 
        else:
            pairs.append((plain[i],plain[i+1])) 
            i+=1
        i += 1

    def getitem(row,col):
        i = row * 5 + col
        return letters[i]
    def shiftright(row,col):
        return getitem(row,(col+1) % 5)
    def shiftdown(row,col):
        return getitem((row + 1) % 5,col)
    def encrypt(pair:tuple):
        row1 = posdic[pair[0]] // 5 # 0,1,2,3,4 will ll return 0 which is required
        col1 = posdic[pair[0]] % 5 # 0,5,10 all return 0 which is required
        row2 = posdic[pair[1]] // 5 # 0,1,2,3,4 will ll return 0 which is required
        col2 = posdic[pair[1]] % 5 # 0,5,10 all return 0 which is required
        ans = str()
        if row1 == row2:
            ans += shiftright(row1,col1)
            ans += shiftright(row2,col2)
        elif col1 == col2:
            ans += shiftdown(row1,col1)
            ans += shiftdown(row2,col2)
            pass
        else:
            ans += getitem(row1,col2)
            ans += getitem(row2,col1)
        return ans
    res = ""
    for i in pairs:
        res += encrypt(i)
    return res

def hill(plain, key, size):
    plain = plain.upper()
    plain += "X" * ((size-len(plain) % size) % size)
    pairs = list()
    for i in range(0,len(plain),size):
        tmplist = list()
        for j in range(0,size):
            tmplist.append(ord(plain[i + j]) - ord("A"))
        pairs.append(np.array(tmplist))
    ans = ""
    for i in range(0,pairs.__len__()):
        pairs[i] = np.dot(pairs[i], key)
        for i in pairs[i]:
            ans += chr((((i%26) + 26) % 26) + ord("A"))
    return ans
    
def vigenere(plain,key,mode):
    plain = plain.upper()
    key = key.upper()
    if(mode):#automode
        key += plain
    else:#repeat
        key = key * (len(plain) // len(key) + 1)
    ans = ""
    for i in range(0,len(plain)):
        ans += caeser(plain[i],ord(key[i]) - ord('A'))
    return ans


def vernam(plain,key="spartans"):
    xkey = list()
    for i in key:
        xkey.append(ord(i) - ord('A'))
    l = len(xkey)
    ans = ""
    for i in range(0,len(plain)):
        p = (ord(plain[i]) - ord('A')) ^ xkey[i % l]
        ans += chr(p + ord('A'))
    return ans


def readfile(filename):
    file = open(filename, "r")
    ans = []
    for p in file.readlines():
        ans.append(p.replace("\n",""))
    return ans
    

def writefile(filename, strlist):
    file = open(filename, "w")
    for st in strlist:
        file.write(st + "\n")


if __name__ == "__main__":

    plains = readfile("caesar_plain.txt") # Caeser
    keys = [3,6,12]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(caeser(p,k))
        ciphers.append("\n")
    writefile("caesar_cipher.txt", ciphers)

    plains = readfile("vigenere_plain.txt") # Vigenere
    keys = [("PIE",False), ("AETHER", True)]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k[0]) + ", mode: " + ("auto mode" if k[1] else "repeating mode"))
        for p in plains:
            ciphers.append(vigenere(p,k[0],k[1]))
        ciphers.append("\n")
    writefile("vigenere_cipher.txt", ciphers)
    
    plains = readfile("playfair_plain.txt") # playfair
    keys = [ "RATS", "ARCHANGEL"]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(playfair(p,k))
        ciphers.append("\n")
    writefile("playfair_cipher.txt", ciphers)

    plains = readfile("vernam_plain.txt") # vernam
    keys = ["SPARTANS"]
    ciphers = []
    for k in keys:
        ciphers.append("key: " + str(k))
        for p in plains:
            ciphers.append(vernam(p,k))
        ciphers.append("\n")
    writefile("vernam_cipher.txt", ciphers)

    plains = readfile("hill_plain_2x2.txt") # hill_2x2
    key = np.array([[5,17],[8,3]])
    ciphers = []
    for p in plains:
        ciphers.append(hill(p,key,2))
    writefile("hill_cipher_2x2.txt", ciphers)

    plains = readfile("hill_plain_3x3.txt") # hill_3x3
    key = np.array([[2,4,12],[9,1,6],[7,5,3]])
    ciphers = []
    for p in plains:
        ciphers.append(hill(p,key,3))
    writefile("hill_cipher_3x3.txt", ciphers)