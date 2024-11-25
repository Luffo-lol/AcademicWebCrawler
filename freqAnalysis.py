from collections import Counter
import re

def urlAnalysis(fileName):
    usefulRaw = []  # Keeps track of visited sites
    with open(fileName, 'r') as file:  # Load previously visited URLs
        for line in file:
            usefulRaw.append(line.strip())

    usefulRaw.sort()

    profileKeywords = [
    "staff",
    "people"
    ]

    blacklistedWords = {
        
    }

    #Sorst sites in seperates sets to properly perform freqency analysis on unique urls to prevent intersite differences in url formating
    sortedRaw = []
    i = 1
    setOfSites = [usefulRaw[i]] 
    while i < len(usefulRaw):
        path = re.sub(r"https?://", "", usefulRaw[i]).split("/")
        if path[0] in setOfSites[0]:
            setOfSites.append(usefulRaw[i])
        else:
            sortedRaw.append(setOfSites)
            setOfSites = []
            setOfSites.append(usefulRaw[i])
        i += 1

    processed = []
    for set in sortedRaw: 
        wordFreq = freqAnalysis(set)
        mostCommonKey = ""
        for word in wordFreq:
            if word in profileKeywords:
                mostCommonKey = word
                break
        if mostCommonKey != "":
            for url in set:
                if mostCommonKey in url:
                    processed.append(url)

    for url in processed:
        print(url)

def freqAnalysis(set):
    words = []
    
    # Extract words from URLs
    for url in set:
        # Remove protocol and split by slashes
        path = re.sub(r"https?://", "", url).split("/")
        # Split path components into words
        for component in path:
            words.extend(re.split(r"[-_]", component))  # Split by dashes and underscores

    # Count word frequencies
    word_counts = Counter(word.lower() for word in words if word.isalpha())  # Keep only alphabetic words
    return word_counts



urlAnalysis('sites/usefulWebsites1.txt')