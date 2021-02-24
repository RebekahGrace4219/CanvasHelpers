
from canvasapi import Canvas
import pandas as pd
from parseStudent import parse
from parseStudent import parseEmails
from makeGroups import makeGroups
from checkValidGroup import invalidGroupDict
from analyzeCode import gradeGroups
from sendCanvasConvo import sendConvo

#Get the right class 
API_URL = "https://canvas.ucdavis.edu/"
API_KEY = "3438~5oDYLD2x3ncXItqCASsXHVkBWdLjHBTjajxEhuQCNHmiXmuaTQp7TGMJtLriQDDc"

#Macros that will have to change to the appropriate class and survey number
CLASS_ID = 516271
QUIZ_ID = 111035
className = "ECS 154A"
studyGroupNumber = "3"

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

# wait for student report to finish generating while the process has not completed or failed 
while reportProgress != 'completed' and reportProgress != 'failed':
       reportProgressObj = canvas.get_progress(reportProgressID)
       reportProgress = reportProgressObj.workflow_state

studentReportN = quiz.create_report("student_analysis")
url = studentReportN.file["url"]
studentData = pd.read_csv(url)

#Parse the student data of those that took the survey
dictStudentTakeSurvey = parse(studentData, canvasClass, CLASS_ID)

#Finds out who did not take survey (also updates the entire class with their school emails)
dictStudentDidNotTakeSurvey = parseEmails(dictStudentTakeSurvey, canvasClass)

#Find the people who were matchedBefore, place it into a dict 
matchedBefore = invalidGroupDict(canvas, CLASS_ID)


#Find the first three groups
group_cat_list = canvasClass.get_group_categories()

#List of group sets and then the actual students

userIds = []
#Now make the groups of other students
for studyGroupSet in group_cat_list:
    group_list = studyGroupSet.get_groups()
    listPerStudyGroupSet = []

    for group in group_list:
        users_list = group.get_users()
        tempGroup = []
        for user in users_list:
            tempGroup.append(user.id)
        
        listPerStudyGroupSet.append(tempGroup)
    
    userIds.append(listPerStudyGroupSet)


realGroups = []

for groupSet in userIds:
    tempGroupSet = []
    for group in groupSet:
        tempGroup = []
        for i in group:
            if i in dictStudentTakeSurvey:
                tempGroup.append(dictStudentTakeSurvey[i])
            elif i in dictStudentDidNotTakeSurvey:
                tempGroup.append(dictStudentDidNotTakeSurvey[i])
            else:
                print("Error")
        tempGroupSet.append(tempGroup)

    realGroups.append(tempGroupSet)

print(realGroups)

for real in realGroups:
    print("")
    gradeGroups(real, matchedBefore)