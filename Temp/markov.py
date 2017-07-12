from urllib.request import urlopen
from random import randint
def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum
def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word
def buildWordDict(text):
    #{word_a : {word_b : 2, word_c : 1, word_d : 1},
    # word_e : {word_b : 5, word_d : 2},...}
    
    #Remove newlines and quotes
    text = text.replace("\n", " ");
    text = text.replace("\"", "");
    #Make sure punctuation marks are treated as their own "words,"
    #so that they will be included in the Markov chain
    punctuation = [',','.',';',':']
    for symbol in punctuation:
        text = text.replace(symbol, " "+symbol+" ");
    words = text.split(" ")
    #Filter out empty words
    words = [word for word in words if word != ""]
    wordDict = {}
    for i in range(1, len(words)):
        if words[i-1] not in wordDict:
        #Create a new dictionary for this word
            wordDict[words[i-1]] = {}
        if words[i] not in wordDict[words[i-1]]:
            wordDict[words[i-1]][words[i]] = 0
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[
    i]] + 1
    return wordDict
text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt")
.read(), 'utf-8')
wordDict = buildWordDict(text)
#Generate a Markov chain of length 100
length = 100
chain = ""
currentWord = "I"
for i in range(0, length):
    chain += currentWord+" "
    currentWord = retrieveRandomWord(wordDict[currentWord])
print(chain)