import nltk

def main():
    emissions = {}
    transitions = {}

    popData(emissions, transitions)

    calcProbs(emissions, transitions)

    viterbi('test.words', emissions, transitions)


def popData(emissions, transitions):
    # this function populates the emissions/transitions data from the WSJ_02-21.pos file
    wsj21File = open('WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.POS')

    lines = [l.rstrip('\n') for l in wsj21File]

    prevPos = 'begin_sentence'

    for i in range(len(lines)):
        line = lines[i]

        # prepare the words
        line = line.strip()
        words = line.split('\t')

        pos = ''
        word = ''

        # this if statement makes sure the 'words' array is well formed
        if len(words) != 2:
            # simulate beginning and ending of sentences for the sentence boundaries
            word = 'end_sentence'
            pos = 'end_sentence'
            recordTallies(emissions, transitions, pos, word, prevPos)
            prevPos = 'end_sentence'
            word = 'begin_sentence'
            pos = 'begin_sentence'
            recordTallies(emissions, transitions, pos, word, prevPos)
        else:
            # isolate the POS and the word
            word = words[0].lower()
            pos = words[1]
            recordTallies(emissions, transitions, pos, word, prevPos)

        prevPos = pos


def recordTallies(emissions, transitions, pos, word, prevPos):
    # calculate the emission probability first
    if pos not in emissions:
        emissions[pos] = {'RECORDED_TOTAL': 1}

    if word not in emissions[pos]:
        emissions[pos][word] = 1
    else:
        emissions[pos][word] += 1
        emissions[pos]['RECORDED_TOTAL'] += 1

    # next, calculate the transition probabilities
    if prevPos not in transitions:
        transitions[prevPos] = {'RECORDED_TOTAL': 1}

    if pos not in transitions[prevPos]:
        transitions[prevPos][pos] = 1
    else:
        transitions[prevPos][pos] += 1
        transitions[prevPos]['RECORDED_TOTAL'] += 1


def calcProbs(emissions, transitions):
    for pos in emissions.keys():
        for key in emissions[pos].keys():
            if key == 'RECORDED_TOTAL':
                continue
            emissions[pos][key] = emissions[pos][key] / \
                float(emissions[pos]['RECORDED_TOTAL'])

    for pos in transitions.keys():
        for key in transitions[pos].keys():
            if key == 'RECORDED_TOTAL':
                continue
            transitions[pos][key] = transitions[pos][key] / \
                float(transitions[pos]['RECORDED_TOTAL'])


def viterbi(fileName, emissions, transitions):
    file = open(fileName)

    lines = [l.strip() for l in file]

    POS = emissions.keys()
    NUM_POS = len(POS)
    BEGIN_INDEX = POS.index('begin_sentence')
    END_INDEX = POS.index('end_sentence')

    matrix = []
    firstColumn = [(float(0), 0)] * NUM_POS
    firstColumn[BEGIN_INDEX] = (float(1), 0)
    matrix.append(firstColumn)

    for line in lines:

        # this is the column that we will eventually push onto the matrix
        thisCol = [(float(0), 0)] * NUM_POS
        # this is the previous column in the matrix
        prevCol = matrix[len(matrix)-1]

        if len(line) == 0:
            line = 'end_sentence'

        for i in range(len(thisCol)):
            line = line.lower()
            # the current part of speech we want to test, for this line
            currentPos = POS[i]
            maxVal = float(0)
            maxIndex = 0

            for j in range(len(prevCol)):
                # the previous part of speech that we want to see if it transitioned into this one
                prevPos = POS[j]
                prevProb = prevCol[j][0]  # previous probability

                transProb = float(0)  # transition probability
                if currentPos in transitions[prevPos].keys():
                    transProb = transitions[prevPos][currentPos]

                wordProb = float(0)  # emission probability
                if line in emissions[currentPos].keys():
                    wordProb = emissions[currentPos][line]
                else:
                    wordProb = 0.001

                totalProb = wordProb * prevProb * transProb  # total probability

                if totalProb > maxVal:  # see if it's the maximum probability
                    maxVal = totalProb
                    maxIndex = j

            # write the max probability to this matrix cell
            thisCol[i] = (maxVal, maxIndex)

        matrix.append(thisCol)  # finally, append the column to the matrix

        # we also need to check if this is the end/beginning of sentence
        if line == 'end_sentence':
            nextCol = [(float(0), 0)] * NUM_POS
            nextCol[BEGIN_INDEX] = (float(1), END_INDEX)
            matrix.append(nextCol)

    # now, we have our matrix filled with viterbi results
    # now we start and the end and work our way backwards
    # find the most probable last element
    lastCol = matrix[len(matrix)-1]
    maxVal = (0, 0)
    maxIndex = 0
    for i in range(len(lastCol)):
        if lastCol[i][0] > maxVal[0]:
            maxVal = lastCol[i]
            maxIndex = i

    i = len(matrix)
    next = maxIndex
    res = []
    while i > 0:
        i -= 1
        res.append(POS[next])
        next = matrix[i][next][1]

    res.reverse()

    print(res)



main()
