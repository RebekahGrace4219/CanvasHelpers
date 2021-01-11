#Notes
#Rebekah - I used generic place holders for the pronouns, I need to go back and recheck what the actual pronoun names are
#Rebekah - I want to make a func that will create randomized data sets of the appropriate size to test on
#At current operation this code does not run
#It also does not take triples into account in order for it to be simpler- a prototype to edit when it is finished


#!/usr/bin/env python3
from canvasapi import Canvas
import pprint
import pandas as pd
from studentClass import Student

#Get the right class 
API_URL = "https://canvas.ucdavis.edu/"
API_KEY = "Key_Goes_Here"

#Macros that will have to change to the appropriate class and survey number
CLASS_ID = 1599
QUIZ_ID = 108761

#Get the class data from canvas
canvas = Canvas(API_URL, API_KEY)
canvasClass = canvas.get_course(CLASS_ID)  

# Get the right quiz and creating a Pandas dataFrame from the generated csv
quiz = canvasClass.get_quiz(QUIZ_ID)
studentReport = quiz.create_report("student_analysis")
url = studentReport.file["url"]
studentData = pd.read_csv(url)


#Create lists to sort students into
nonBinaryCare = []
womanCare = []
manCare = []
nonBinaryDontCare = []
womanDontCare = []
maleDontCare = []
allDontCare = []
didNotTakeSurvey = []


#Fill the dictionary and the student lists
dictSt = {}
for index, row in studentData.iterrows():

    #name and id
    tempStudent = Student(row['name'], row['id'])

    #pronouns that the student prefers
    tempStudent.pronouns = row[studentData.columns.str.contains('1085146')].item()

    #preferSame is True if the student would like to share their group with someone of the same gender
    if row[studentData.columns.str.contains('1085148')].item() == "If possible, I would prefer another person with the same pronouns as me.":
        tempStudent.preferSame = True
    else:
        tempStudent.preferSame = False

    #meeting times - Sun - Sat, Midnight-4, 4-8, 8-noon, etc  [0][0] is sunday at midnight to 4 time slot

    #asynch (2), synch (1), no pref (0)- how the student would like to meet

    #contact pref - Discord, Phone, Email, Canvas - 2 = yes, 1 = no preference, 0 = not comfortable

    #contact info - [DiscordHandle, PhoneNumber, personal@email.com]

    #prefer leader- True if they prefer to be the leader, false otherwise

    #country - Country of Origin

    #preferCountry - True if they would like to have a groupmate from the same country

    #languages - Preferred language

    #preferlanguage - True if they would like to share a group with someone from the same country

    #Preferred stuff to do - the drop downs and free response


    #Add the student to the dictionary of all students
    dictSt['id'] = tempStudent
    
    if tempStudent.pronouns == "They/them" or tempStudent.pronouns == "Not included":
        if tempStudent.preferSame:
            #If student is nonbinary and does care about their groups' gender, place them in that list
            nonBinaryCare.insert(dict['id'])
        else:
            #If student is nonbinary and does not care about their groups' gender, place them in that list and the full dont care list
            nonBinaryDontCare.insert(dict['id'])
            allDontCare.insert(dict['id'])
    elif tempStudent.pronouns == "She/her":
        if tempStudent.preferSame:
            #If student is a woman and does care about their groups' gender, place them in that list
            womanCare.insert(dict['id'])
        else:
            #If student is a woman and does not care about their groups' gender, place them in that list and the full dont care list
            womanDontCare.insert(dict['id'])
            allDontCare.insert(dict['id'])
    elif tempStudent.pronouns == "He/him/his":
        if tempStudent.preferSame:
            #If student is a man and does care about their groups' gender, place them in that list
            manCare.insert(dict['id'])
        else:
            #If student is a man and does not care about their groups' gender, place them in that list and the full dont care list
            manDontCare.insert(dict['id'])
            allDontCare.insert(dict['id'])
    elif tempStudent.pronouns == "Prefer not to say":
        #A student who prefers not to say is automatically in the full dont care list because their gender cannot be matched
        allDontCare.insert(dict['id'])
    else:
        print( "Error: inelibe response to sorting people by pronoun")
        
  

# update student dictionary to include people who did not take, as well as list composed of students who did not take the test
# the class and add default emails to all students
for user in canvasClass.get_users(enrollment_type=['student']):
    if user.id not in dictSt:
        temp = Student(user.id, user.name, user.email)
        dictSt[user.id] = temp
        didNotTakeSurvey.append(temp)
    else:
        dictSt[user.id].schoolEmail = user.email

#############################################################################################################################################################
#AT this point all students are in at least one of 8 lists, and we begin pairing up the students who care the partner of their gender within their own group#
#############################################################################################################################################################
        
#lists of pairs of students who match up together
matchListCare(nonBinaryCare, nonBinaryDontCare, allDontCare, pairs, didNotTakeSurvey)
matchListCare(womanCare, womanDontCare, allDontCare, pairs, didNotTakeSurvey)
matchListCare(manCare, manDontCare, allDontCare, pairs, didNotTakeSurvey)
matchListDontCare(allDontCare, pairs, didNotTakeSurvey)

#At this point, they are all pairs or in didNotTakeSurvey
for match1 in Pairs:
    for match2 in Pairs:
        if validQuad(match1, match2):
            Quad.score = scoreQuad(match1, match2)
            
            
            


