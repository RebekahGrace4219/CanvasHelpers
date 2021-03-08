"""This function makes a course wide "announcement" that's actually a discussion topic
    takes in the course number (int),
          the title of the "announcement"/discussion topic (str)
          the message of the "announcement"/discussion topic (str)
          and the API KEY (str)
"""
# Import the canvas class
from canvasapi import Canvas

def makeAnnouncement(course, title: str, msg: str): #couse should be a couse object
    course.create_discussion_topic(title = title, message = msg, is_announcement = False) #if you are testing, you can set to false
    return