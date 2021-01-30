
from canvasapi import Canvas
import pandas as pd
from parseStudent import parse
from parseStudent import parseEmails
from makeGroups import makeGroups
from checkVaildGroup import invalidGroupDict
#from sendEmail import sendMessage
#from groupFile import formGroups


#Get the right class 
API_URL = "https://canvas.ucdavis.edu/"
API_KEY = "api_key_here"

#Macros that will have to change to the appropriate class and survey number
CLASS_ID = 1
QUIZ_ID = 1
className = "ECS 154A or ECS 050"
studyGroupNumber = 2

#Get the class data from canvas
canvas = Canvas(API_URL, API_KEY)
canvasClass = canvas.get_course(CLASS_ID)  

# Get the right quiz
quiz = canvasClass.get_quiz(QUIZ_ID)
studentReport = quiz.create_report("student_analysis")
reportProgress = None

# URL of canvas progress object from studentReport
reportProgressURL = studentReport.progress_url

# parse so only the process id remains
reportProgressID = reportProgressURL.removeprefix('https://canvas.ucdavis.edu/api/v1/progress/')
​
# wait for student report to finish generating while the process has not completed or failed 
while reportProgress != 'completed' and reportProgress != 'failed':
       reportProgressObj = canvas.get_progress(reportProgressID)
       reportProgress = reportProgressObj.workflow_state
       print(reportProgress)
studentReportN = quiz.create_report("student_analysis")
url = studentReportN.file["url"]
studentData = pd.read_csv(url)

#Parse the student data of those that took the survey
dictStudentTakeSurvey = parse(studentData, canvasClass)

#Finds out who did not take survey (also updates the entire class with their school emails)
dictStudentDidNotTakeSurvey = parseEmails(dictStudentTakeSurvey, canvasClass)

#Find the people who were matchedBefore, place it into a dict 
matchedBefore = invalidGroupDict(canvasClass)

#Create the groups:
groups = makeGroups(dictStudentTakeSurvey, dictStudentDidNotTakeSurvey, matchedBefore)

#Now that groups are matched, send emails and form groups
#formGroups(groups)
#sendMessage(groups, className, studyGroupNumber)
