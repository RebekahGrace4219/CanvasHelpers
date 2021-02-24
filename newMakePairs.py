
#Returns a list of [student, student] pairs or [student, student, student, student]
#students: a dictionary of all the students, called by id
#matchDict: a dictionary of all the students who have matched before
#studentsToMatch: a list of all students or student pairs to group
#matchType: a string to denote making pairs or quads
def makePairs(students: dict, matchDict: dict, studentsToMatch: list, matchType: str):
    #make an empty list of return 
    retPairs = []

    if len(studentsToMatch) == 0:
        finished = True
    index = 0

    while (len(studentsToMatch)!=0) and (index < 10):
        #Rank each set of students against eachother and have the matching program choose matches
        preferenceList = preferenceSymmetricalSort(studentsToMatch, matchType, matchDict)
        game = StableRoommates.create_from_dictionary(preferenceList)
        ans = game.solve()

        #Make Pairs of students
        if matchType == "TwoByTwo":
            studentsToMatch = removeImpossibleTwo(ans, matchDict, students, retPairs, studentsToMatch)
            moveStudentsTwo(ans, retPairs, students, studentsToMatch)
        elif matchType == "OneByOne":
            studentsToMatch = removeImpossibleOne(ans, matchDict, students, studentsToMatch)
            moveStudentsOne(ans, retPairs, students)

        #Update controls
        index = index + 1

    for index in range(5):
        listUsedIndexes = list()
        pairsToMake = list()
        for index1 in range(len(studentsToMatch)):
            for index2 in range(len(studentsToMatch)):
                if index1 != index2 and (index1 not in listUsedIndexes) and (index2 not in listUsedIndexes):
                    if isValidGroup(matchDict, [studentsToMatch[index1], studentsToMatch[index2]]):
                        listUsedIndexes.append(index1)
                        listUsedIndexes.append(index2)
                        pairsToMake.append([index1, index2])

        usedStudents = list()
        for pairToMake in pairsToMake:
            retPairs.append([studentsToMatch[pairToMake[0]], studentsToMatch[pairToMake[1]]])
            usedStudents.extend([studentsToMatch[pairToMake[0]], studentsToMatch[pairToMake[1]]])
        

        for student in usedStudents:
            studentsToMatch.remove(student)
    
    return retPairs


    
