import nltk

##filenName = input("File?")
fileName = "WSJ_POS_CORPUS_FOR_STUDENTS/WSJ_02-21.POS"

readFile = open(fileName)
lines = readFile.readlines()

POS_dict = {}
State_dict = {}



def dictionaryFiller(lines, POS_dict, State_dict):

    for line in lines:
        line = line.lower()
        line = line.strip()
        i = line.split("\t")
        if len(i)!=2:
            continue

        word = i[0]
        token = i[1]
        if token in POS_dict:
                if word in POS_dict[token]:
                    freq = POS_dict[token][word]
                    freq+=1
                    POS_dict[token][word] = freq
                    POS_dict[token]["total"] += 1
                else:
                    POS_dict[token][word]=1   
                    POS_dict[token]["total"] += 1         
        else: 
            POS_dict[token]= {}
            POS_dict[token][word] = 1
            POS_dict[token]["total"] = 1
    State_dict["End_Sent"]={}
    State_dict["End_Sent"]["Begin_Sent"]= 0

    prev = "Begin_Sent"
    for line in lines:
        line = line.lower()
        line = line.strip()
        i = line.split("\t")
        if len(i)!=2:
            token = "End_Sent"
        else:
            token = i[1]

        if prev in State_dict:
            if token in State_dict[prev]:
                freq = State_dict[prev][token]
                freq+=1
                State_dict[prev][token] = freq
                State_dict[prev]["total"] += 1
            else:
                State_dict[prev][token]=1
                State_dict[prev]["total"] += 1
                
        else:
            State_dict[prev]={}
            State_dict[prev][token] = 1
            State_dict[prev]["total"] = 1
        prev = token
        ## automatically connects end_sent to begin_sent
        if (prev=="End_Sent"):
            freq = State_dict[prev]["Begin_Sent"]
            freq += 1
            State_dict[prev]["Begin_Sent"] = freq
            if "total" in State_dict[prev]:
                State_dict[prev]["total"] += 1
            else:
                State_dict[prev]["total"] = 1
            prev="Begin_Sent"
    

# transforms frequencies into probabilities
def probFinder(POS_dict,State_dict):
    for pos in POS_dict.keys():
        for key in POS_dict[pos].keys():
            if key!="total":
                freq = POS_dict[pos][key]
                POS_dict[pos][key] = (freq/ POS_dict[pos]["total"])
    for state in State_dict.keys():
        for key in State_dict[state].keys():
            if key!="total":
                freq = State_dict[state][key]
                State_dict[state][key] = (freq/ State_dict[state]["total"])

#Viterbi: prev likelihood*
# prob that prev is a state* prob that prev state transitions to current state * prob that given current state, word is current word

def Viterbi(lines, emiss, trans):
    
    lines = lines.strip()

    speech = emiss.key()


dictionaryFiller(lines, POS_dict, State_dict)

probFinder(POS_dict,State_dict)

print((POS_dict["dt"]["the"]))