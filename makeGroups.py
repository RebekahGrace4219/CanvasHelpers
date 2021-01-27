from preferenceLists import preferenceSymmetricalSort
from preferenceLists import preferenceAsymmetricalSort
from matching.games import StableMarriage
from matching.games import StableRoommates
import random
from checkValidGroup import isValidGroup


def removeImpossibleTwo(game: dict, matchDict: dict, students: dict, pairs: list):
    #create an empty list to store all the removed students
    extraStudents = []

    #I can't change the dict size while its going, so I need to record all the keys to take out in the iteration
    keysToTakeOut = []
    
    for pair in pairs:
        for key in game:
            flag = False
            if int(pair[0].idNum) == int(str(key)):
                flag = True
        if not flag:
            extraStudents.append(pair)

    for key in game:
        #only want to make a list of both students if they exist
        tempList = [0] * 4
        student1 = students[int(str(key))]
        student2 = students[int(str(game[key]))]

        for pair in pairs:
            flag1 = False
            flag2 = False
            if student1 in pair:
                flag1 = True
                tempList[0] = pair[0]
                tempList[1] = pair[1]
            if student2 in pair:
                flag2 = True
                tempList[2] = pair[0]
                tempList[3] = pair[1]
            if flag1 and flag2:
                break
        
        #If the two people cannot be in the group, then we are going to remove the first person
        if not(isValidGroup(matchDict, tempList)):
            #Delete both people from the list and move them into extraStudents
            keysToTakeOut.append(key)
            

    for key in keysToTakeOut:
        #Need to add back both students in the pair
        for pair in pairs:
            #Find the pair that corresponds to this key
            #Should probably make pair into a dictionary later
            if int(str(key)) == pair[0].idNum:
                extraStudents.append(pair)
                break
        game.pop(key)

    return extraStudents
    
def moveStudentsTwo(ans: dict, quads: list, students: dict, pairs: list):
    #Keep a list of all the used keys so we don't add a pair twice
    usedKeys = []
    print("Length ans: " +str(len(ans)) + "Length pairs: " +str(len(quads)))

    #Make student-student if matchType is OneByOne
    for key in ans:
        thisStudentKey = int(str(key))
        otherStudentKey = int(str(ans[key]))

        #Don't add a pair if its reverse was already added
        if not (otherStudentKey in usedKeys):
            usedKeys.append(thisStudentKey)
            #Find the appropriate pairs
            tempList = [0] * 4
            student1 = students[thisStudentKey]
            student2 = students[otherStudentKey]
            for pair in pairs:
                flag1 = False
                flag2 = False
                if student1 in pair:
                    flag1 = True
                    tempList[0] = pair[0]
                    tempList[1] = pair[1]
                if student2 in pair:
                    flag2 = True
                    tempList[2] = pair[0]
                    tempList[3] = pair[1]
                if flag1 and flag2:
                    break

            #Add the set of two students to the quad list
            quads.append(tempList)
    print("Length pairs: " +str(len(quads)))
    return quads

#There are some options from game that we cannot actually use, so we need to take them out of game, and return the unused students to make the next run as extra students
#game: a list of student's with another student's id as the key- these are "good" matches
#matchedDict: a dictionary of student id matches to check who has matched before
#I need the full list of students 
def removeImpossibleOne(game: dict, matchDict: dict, students: dict):
    #create an empty list to store all the removed students
    extraStudents = []

    #I can't change the dict size while its going, so I need to record all the keys to take out in the iteration
    keysToTakeOut = []

    for studentKey in students:
        flag = False
        for key in game:
            if int(str(key)) == studentKey:
                flag = True
                break
        
        if not flag:
            extraStudents.append(students[studentKey])

    for key in game:
        #only want to make a list of both students if they exist
        listStudents = [students[int(str(key))], students[int(str(game[key]))]]

        #If the two people cannot be in the group, then we are going to remove the first person
        if not(isValidGroup(matchDict, listStudents)):
            #Delete both people from the list and move them into extraStudents
            keysToTakeOut.append(key)
            continue

    
    #For each key to take out, add that student to extraStudents
    for key in keysToTakeOut:
        extraStudents.append(students[int(str(key))])
        game.pop(key)

    return extraStudents      

#Move the now correct student pairs into the actual pairs   
def moveStudentsOne(ans: dict, pairs: list, students: dict):
    #Keep a list of all the used keys so we don't add a pair twice

    
    usedKeys = []

    #Make student-student if matchType is OneByOne
    
    for key in ans:
        thisStudentKey = int(str(key))
        otherStudentKey = int(str(ans[key]))

        #Don't add a pair if its reverse was already added
        if not (otherStudentKey in usedKeys):
            usedKeys.append(thisStudentKey)
            pairs.append([students[thisStudentKey], students[otherStudentKey]])

    
    return

#Make pairs of student-student or studentPair-studentPair
def makePairs(students: dict, matchDict: dict):
    #Make a copy that won't change the orignal students
    extraStudents = []

    for student in students:
        extraStudents.append((students[student]))
        
    pairs = []

    #Control mechanisms for the loop: check if all the students have been paired, and that the list has not been 
    finished = False
    if len(extraStudents) == 0:
        finished = True
    
    i = 0
    #You don't want to loop too many times, but run five times at most to find good matches that have not matched before
    while(not finished and i < 5):
        preferenceList = preferenceSymmetricalSort(extraStudents, "OneByOne", matchDict)
        game = StableRoommates.create_from_dictionary(preferenceList)
        ans = game.solve()
        
        #remove the students who did not find matches out, delete them from the ans dict
        extraStudents = removeImpossibleOne(ans, matchDict, students)

        #Take the remaining, succesful students, and place them into pairs
        moveStudentsOne(ans, pairs, students)
        

        #Update your controls
        if len(extraStudents) == 0:
            finished = True

        i = i + 1

    #I have left this code in because we may come back to it, but right now the matching works so well the control hardly seems necessary 
    """
    Drop the matched before requirement in order to create more matches
    while(not finished and i < 10):
        preferenceList = preferenceSymmetricalSort(extraStudents, matchType)
        game = StableRoommates.create_from_dictionary(preferenceList)

        moveStudents(game)

        Update your controls
        if len(extraStudents) == 0:
            finished = True
        i = i + 1
    """

    #Match the rest of the students randomly and print that the matching sucked
    for index in range(0, len(extraStudents), 2):
        pairs.append([extraStudents[index], extraStudents[index+1]])
        print("Matching sucked, had to resort the randomness " +   str(index))
    extraStudents.clear()

    #Return the pairs list (list[Student, Student])
    return pairs

#We probaby want to fold this code in with make pairs eventually, but for now it's here
#students dict - a dictionary of all the students
#matchDict - a dictionary of all invalid matching
def makeQuads(students: dict, matchDict: dict, pairs: list):
    #Make a copy that won't change the orignal students
    extraStudents = []

    for pair in pairs:
        extraStudents.append(pair)
        
    quads = []

    #Control mechanisms for the loop: check if all the pairs been put into quads
    finished = False
    if len(extraStudents) == 0:
        finished = True
    i = 0
    
    #You don't want to loop too many times, but run five times at most to find good matches that have not matched before
    while(not finished and i < 5):
        preferenceList = preferenceSymmetricalSort(extraStudents, "TwoByTwo", matchDict)
        print("Length extraStudents = "+str(len(extraStudents)))
        print("preferenceList: "+ str(len(preferenceList)))
        game = StableRoommates.create_from_dictionary(preferenceList)
        ans = game.solve()

        #remove the students who did not find matches out, delete them from the ans dict
        extraStudents = removeImpossibleTwo(ans, matchDict, students, pairs, extraStudents)
        
        #Take the remaining, succesful students, and place them into pairs
        moveStudentsTwo(ans, quads, students, pairs)

        #Update your controls
        if len(extraStudents) == 0:
            finished = True
        i = i + 1

    print(len(quads))
    print(len(extraStudents))
    """
    place some extra code here to match people by happiness but drop match before requirement or somethinh maybe
    """
    for index in range(0, len(extraStudents), 2):
        quads.append([extraStudents[index], extraStudents[index+1]])
    extraStudents.clear()

    return quads

def minIndex(quads: list, matchedBefore: dict):
    index = 0
    minScore = scoreTwoByTwo([quads[0][0], quads[0][1]],  [quads[0][2], quads[0][3]], matchedBefore)

    for i in range(len(quads)):
        pair1 = [quads[i][0], quads[i][1]]
        pair2 = [quads[i][2], quads[i][3]]

        if scoreTwoByTwo(pair1, pairs2, matchedBefore) < minScore:
            minScore = scoreTwoByTwo(pair1, pairs2, matchedBefore)
            index = i

    return index


def cleanQuads(quads: list, singles: dict, numGroups: int, matchedBefore: dict):
    if len(quads) == numGroups:
        return 
    
    #In the case that there are too many quads, break up the least happy ones
    while(len(quads) > numGroups):
        index = findMinIndex(quads)
        removeQuad = quads[index]
        quads.remove(removeQuad)
        for person in removeQuad:
            single[person.numId] = person

    #This should not happen
    if len(quads) < numGroups:
        print("ERROR: the number of quads should match the number of needed groups")


    print("working on it")
    
#Take a list of the possible stuednts 
def makeGroups(singles: dict, extraStudents: dict, matchBefore: dict):

    #Calculate the number of needed groups
    lenClass = len(singles) + len(extraStudents)
    numGroups = lenClass//5

    i = 0 #temp

    #move students from extras to free singles until I have 4/5 the class and its divisible by 4
    while(len(singles) < numGroups*4 and len(extraStudents) > 0):
        student = extraStudents.popitem()
        singles[student[0]] = student[1]

    #People need to move between the two lists in order to make the students divisible by 4
    while(len(singles)%4 != 0):
        #If there are not enough students to move out of extra students, you gotta move some people who took the survey in
        if len(extraStudents) < len(singles)%4:
            student = singles.popitem()
            extraStudents[student[0]] = student[1]
        else:
            #Else you can just add extraStudents in to the singles list
            student = extraStudents.popitem()
            singles[student[0]] = student[1]
    
    index = 0
    singles1 = dict()
    singles2 = dict()

    for key in singles:
        index = index + 1
        if index%2 == 0:
            singles1[key] = singles[key]
        else:
            singles2[key] = singles[key]


    #Make the first set of pairs
    pairs1 = makePairs(singles1, matchBefore)
    pairs2 = makePairs(singles2, matchBefore)
    pairs = list()

    
    #Place the pairs together
    for i in range(len(pairs1)):
        pairs.append(pairs1[i])
    for i in range(len(pairs2)):    
        pairs.append(pairs2[i])

    print(len(pairs))

    #Make the pairs into quads
    quads = makeQuads(singles, matchBefore, pairs)
    print(len(quads))

    
    return 1

    


    
            

            


    
        
        
        
        

        
