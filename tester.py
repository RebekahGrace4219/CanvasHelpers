from studentClass import Student

import time
import scoringFunc
from matchingFunc import matchInternational
from matchingFunc import matchActivity
from matchingFunc import matchMeetingTimeSpecific
from matchingFunc import matchTime
from matchingFunc import matchLead
from matchingFunc import matchGender
from matchingFunc import matchLanguage
from matchingFunc import matchSkill
from canvasapi import Canvas
import pandas as pd
from parseStudent import parse
from parseStudent import parseEmails
from checkValidGroup import invalidGroupDict
from checkValidGroup import isValidGroup
from makeGroups import makeGroups
#from sendEmail import sendMessage
#from groupFile import formGroups


#Get the right class 
API_URL = "canvas url"
API_KEY = "key"

#Macros that will have to change to the appropriate class and survey number
CLASS_ID = classid
QUIZ_ID = quizid
className = "className"
studyGroupNumber = 3

#Get the class data from canvas
canvas = Canvas(API_URL, API_KEY)
canvasClass = canvas.get_course(CLASS_ID)  

# Get the right quiz and creating a Pandas dataFrame from the generated csv
quiz = canvasClass.get_quiz(QUIZ_ID)
studentReport = quiz.create_report("student_analysis")
#time.sleep(120)
url = studentReport.file["url"]
studentData = pd.read_csv(url)


#Parse the student data of those that took the survey
dictStudentTakeSurvey = parse(studentData, canvasClass)

#Finds out who did not take survey (also updates the entire class with their school emails)
dictStudentDidNotTakeSurvey = parseEmails(dictStudentTakeSurvey, canvasClass)


#Find the people who were matchedBefore, place it into a dict 
matchedBefore = invalidGroupDict(canvas, CLASS_ID)

makeGroups(dictStudentTakeSurvey, dictStudentDidNotTakeSurvey, matchedBefore)

print("finish")
