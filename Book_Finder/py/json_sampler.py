import sys
import json
import pandas as pd
import re
import os
import pickle
import datetime


# Save an object as a pickle file; a compressed version
def save_as_pkl(object, path):
    pickle.dump(object, open(path, "wb"))


# Load an object from a pickle file
def load_pkl(path):
    obj = pickle.load(open(path, "rb"))
    return obj

# Merging both array halves for mergesort.
def merge(l1, l2):
    pointerL = 0
    pointerR = 0
    merged = []

    # While both of the half arrays still have entries
    # to process, add the lower element to the merged
    # array.
    while pointerL < len(l1) and pointerR < len(l2):
        if l1[pointerL] < l2[pointerR]:
            merged += [l1[pointerL]]
            pointerL += 1
        else:
            merged += [l2[pointerR]]
            pointerR += 1

    # When one of the arrays has had all of its values
    # added to the merged list, add the remaining elements
    # from the other list to the output.
    if pointerL == len(l1):
        merged += l2[pointerR:]
    else:
        merged += l1[pointerL:]

    return merged

# Mergesort implementation, used for handling the large
# dataset.

# Divide the array to be sorted into halves recursively,
# then merge the resultant halves.
def mergeSort(l):
    left = l[:len(l) // 2]
    right = l[len(l) // 2:]

    if len(l) == 1:
        return l

    return merge(mergeSort(left), mergeSort(right))


# Insert into the sorted list while keeping it sorted.
def listInsert(l, target):
    # Edge cases:
    if len(l) == 0:
        l.append(target)
        return l

    # Find the closest element in the array to the target value
    index = binarySearch(l, target[0])

    # If the target is in the array already, increment the corresponding
    # counters to maintain word occurence values.
    if l[index][0] == target[0]:
        innerInd = binarySearch(l[index][1], target[1][0][0])
        l[index][2] += 1
        if l[index][1][innerInd][0] == target[1][0][0]:
            l[index][1][innerInd][2] += 1
        else:
            if l[index][1][innerInd][0] > target[1][0][0]:
                l[index][1].insert(innerInd, target[1][0])
            else:
                l[index][1].insert(innerInd + 1, target[1][0])

    # If the target is not already in the array, we need insert it
    # into the appropriate position by comparing it with the 
    # closest returned index. 
    else:
        if l[index] > target:
            l.insert(index, target)
        else:
            l.insert(index + 1, target)

    return l

# Searching for a target value in an array in Log(N) time.
# Standard binary search implementation.
def binarySearch(l, target):
    length = len(l)
    low = 0
    mid = length // 2
    hi = length
    # Convert the target string to lower case. 
    target = target.lower()

    # Handling simple Integers/Strings
    try:
        # While the low-value pointer is less than the
        # current mid pointer
        while low < mid:

            #If we find the target, simply return the index
            if l[mid] == target:
                return mid

            # If the value pointed to is less than the target,
            # increase the low pointer and increase the mid
            # pointer
            elif l[mid] < target:
                low = mid
                mid = (mid + hi) // 2

            # Otherwise, lower the hi pointer and decrease the
            # mid pointer.
            else:
                hi = mid
                mid = (mid + low) // 2


    # Handling Tuples
    # See the above code for a description.
    except TypeError:
        while low < mid:
            if l[mid][0] == target:
                return mid
            elif l[mid][0] < target:
                low = mid
                mid = (mid + hi) // 2
            else:
                hi = mid
                mid = (mid + low) // 2

    # Returns closest target if no match exists
    return mid


def takeSecond(elem):
    return elem[2]

# Takes in the input data, process it into useful 
# sorted forms, and outputs word occurence statistics
# for the books in the dataset.
def mainMethod(word):
    asinIndices = []
    asinCounts = {}
    reviewerIndices = []
    data = []
    wordList = []
    topItems = {}

	# Don't extract data unless it has not yet been extracted
    if not os.path.isfile("pickles/data.pkl"):
        linesParsed = 0
        with open('data/reviews_Books_5.json') as f:
            for line in f:
                lineDict = json.loads(line)
                data.append(lineDict)
                asinIndices.append((lineDict['asin'], linesParsed))
                reviewerIndices.append((lineDict['reviewerID']))
                linesParsed += 1

				# Take only the first 100,000 rows of the data
                if linesParsed > 100000:
                    break

        sortedAsins = mergeSort(asinIndices)
        sortedRID = mergeSort(reviewerIndices)

		# Counting the number of reviews for each asin.
		# Used to compute % of reviews which use a keyword.
        for index in sortedAsins:
            if index[0] not in asinCounts:
                asinCounts[index[0]] = 0
            else:
                asinCounts[index[0]] += 1

		# Save objects as pickle files
        save_as_pkl(data, 'pickles/data.pkl')
        save_as_pkl(sortedAsins, 'pickles/sortedAsins.pkl')
        save_as_pkl(sortedRID, 'pickles/sortedRID.pkl')
        save_as_pkl(asinCounts, 'pickles/asinCounts.pkl')
    
    else:
		# Load pickle files into objects
        data = load_pkl("pickles/data.pkl")
        sortedAsins = load_pkl("pickles/sortedAsins.pkl")
        sortedRID = load_pkl("pickles/sortedRID.pkl")
        asinCounts = load_pkl("pickles/asinCounts.pkl")

	# Computing the list of keywords is a heavy computation,
	# if the pickle file exists, don't bother recomputing.
    if not os.path.isfile("pickles/wordList.pkl"):
        total = len(data)
        count = 1
        startTime = datetime.datetime.now()
        totalTime = 0
        for review in data:
            # Processing progress output
            if count % 5000 == 0:
                print("{0:.2f}% complete".format(count/total * 100))
                endTime = datetime.datetime.now()
                elapsedS = (endTime - startTime).total_seconds()
                estimate = elapsedS * (total/count)
                totalTime += elapsedS
                print("Elapsed time in last section: ",elapsedS)
                print()

                startTime = endTime
            asin = review['asin']
            asinCount = asinCounts[asin]
            if 'reviewText' not in review.keys():
                continue           
            reviewText = review['reviewText'].lower()
            reviewText = re.sub(r'[^\w\s]','',reviewText)
            reviewText = reviewText.split()
            wordSet = set(reviewText) # Don't want to count multiple occurrences in same review
            for word in wordSet:
                newVal = [word, [[asin, asinCount, 1]], 1]
                wordList = listInsert(wordList, newVal)

                # Keeping the list of most used words for each book
                if asin in topItems:
                    if word in topItems[asin]:
                        topItems[asin][word] += 1
                    else:
                        topItems[asin][word] = 1
                else:
                    topItems[asin] = {word:1}
            count += 1

        save_as_pkl(wordList, 'pickles/wordList.pkl')
        save_as_pkl(topItems, 'pickles/topItems.pkl')

        print("Total time elapsed: ", totalTime)


    else:
        wordList = load_pkl("pickles/wordList.pkl")

    wordUses = []
    words = []

    ## STRUCTURE OF WORDLIST:
    # [['word1', [['asin1', totalReviewsInAsin1, occurrences of word1 in asin1],
    #			 ['asin2', totalReviewsInAsin2, occurrences of word2 in asin2],
    #			 [...],
    #			  ]
    #  ['word2', [...]],
    #  [ ... ],
    #  ['wordn']]

    ind = binarySearch(wordList, word)
    sum = 0
    v = wordList[ind]

    # sort 2nd index element which is appeared times.
    v[1].sort(key=takeSecond, reverse=True)
    index = 0
    for occurrence in v[1]:
        if index < 10:
            print("\tUsed in reviews for book " + str(occurrence[0]) + " " + str(occurrence[2]) + " times.")
        sum += occurrence[2]
        index += 1

# Call the main method when json_sampler is run.
if __name__ == '__main__':
    word = sys.argv[1]
    mainMethod(word)
