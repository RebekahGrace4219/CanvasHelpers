from canvasapi import Canvas
import pprint
import csv
import time
from canvasapi.quiz import Quiz
import pandas as pd
from pandas.core.accessor import register_series_accessor
from studentClass import Student
from parseStudent import parse, parseEmails, parsePartnerQuiz
import cProfile, pstats

def retrieveCSVfromCanvas(quiz:Quiz, canvasAPIAccess:Canvas) :
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
              print(reportProgress)
       studentReportN = quiz.create_report("student_analysis")
       url = studentReportN.file["url"]
       studentData = pd.read_csv(url)

       return studentData



 #Get the right class 
start_time = time.time()
if __name__=='__main__':
       profiler = cProfile.Profile()
       profiler.enable()
       API_URL = "https://canvas.ucdavis.edu/"
       API_KEY = ""
       #Macros that will have to change to the appropriate class and survey number
       CLASS_ID = 546554
       QUIZ_ID = 111034
       QUIZ_ID2 = 115402

       #Get the class data from canvas
       canvas = Canvas(API_URL, API_KEY)
       canvasClass = canvas.get_course(CLASS_ID)  

       # Get the right quiz and creating a Pandas dataFrame from the generated csv
       quiz = canvasClass.get_quiz(QUIZ_ID)
       studentData = retrieveCSVfromCanvas(quiz, canvas)
       var = parse(studentData, canvasClass)
       profiler.disable()
       missingStudents = parseEmails(var,canvasClass)
       quiz2 = canvasClass.get_quiz(QUIZ_ID2)
       partnerQuizData = retrieveCSVfromCanvas(quiz2, canvas)
       parsePartnerQuiz(partnerQuizData ,canvasClass, var, missingStudents)
       
       '''
       for key in var:
              print(var[key])
              '''
       for key in var:
              print(var[key].partnerEmail)
              print(var[key].partner)
       for key in missingStudents:
              print(missingStudents[key].partnerEmail)
              print(missingStudents[key].partner)

       print("--- %s seconds ---" % (time.time() - start_time))
       stats = pstats.Stats(profiler).sort_stats('cumtime')
       stats.print_stats(25)
