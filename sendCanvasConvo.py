"""This file is for sending the canvas conversation for each group (python3)
    last line is: sendConvo(canvas, course_number, group_list, study_group_number)
    canvas is a canvas objects
    group_list should be a list of list of student objects
    course_number is the number of the course
    study_group_number is the number of that week's study group (1-5)
    """

# import system variables
# in order to send the messages, need canvas api keyjupyter
# i put the api key in environment variables


# Import the canvas class
from canvasapi import Canvas

from studentClass import Student

# need getBody to create the body of the message
from createMessageBody import getBody


def getStudentIds(student_list: list):
    """
    takes in a list of student objects
    returns back a list of strings where each string is a student's ID
    """
    student_ids = []
    for student in student_list:
        student_ids.append(str(student.idNum))
    return student_ids

def getStudentLastNames(student_list: list):
    """Takes in the list of student objects
    gets the last names of everyone
    return a string of everyones last names with underscores separating
    """
    student_names = " _"
    for student in student_list:
        student_names += student.lastName + "_"
    return student_names

def uploadTable(canvas):
    """
    upload the table.txt to the "conversation attachments" folder
    return back the id of the table to be attached
    """
    curr_user = canvas.get_current_user()

    folders = curr_user.get_folders()
    folder_id = 0
    for i in folders:
        if i.name == "conversation attachments":
            folder_id = i.id
    folder = curr_user.get_folder(folder_id)

    did_upload = folder.upload('table.txt')
    
    return did_upload[1]['id']

def makeGroupAndMsg(canvas: Canvas, course_number: int, group_list: list, study_group_number: str):
    """
    Takes in the list of groups and 1) makes every group in canvas 2) creates the corresponding group msg
    and returns a dictionary of groups and its matching message
    """
    course = canvas.get_course(course_number)
    
    course_name = course.name
    category_name = "Study Groups " + study_group_number
    #make the study group category
    curr_group_category = course.create_group_category(name=category_name, self_signup=None)

    group_info_dict = {}
    for group in range(len(group_list)):

        members = getStudentIds(group_list[group])
        last_names = getStudentLastNames(group_list[group])
        group_name = "Study Group " + study_group_number + ":" + last_names
        #make the group
        curr_group = curr_group_category.create_group(name=group_name)
        #edit the group
        curr_group.edit(members=members)

        body = getBody(group_list[group])
        #make the conversation

        group_info_dict[body] = [group,members, group_name]
    return group_info_dict


def sendConvo(canvas: Canvas, course_number: int, group_info_dict: dict, study_group_number: str):
    """
    takes in a dictionary of message to group
    send the message to the appropriate group in canvas
    """
    course = canvas.get_course(course_number)
    
    course_name = course.name
    category_name = "Study Groups " + study_group_number

    for group in group_info_dict:

        members = group_info_dict[group][1]
        group_name = group_info_dict[group][2]

        table_id = [uploadTable(canvas)]
        canvas.create_conversation(recipients=members, body=group, subject = group_name, attachment_ids = table_id, force_new = True)
    return



