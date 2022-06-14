# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import random
import sqlite3
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

def get_from_database(course_name):
   print("function: " + course_name)
   conn = sqlite3.connect("courses.db")
   cursor = conn.cursor()

   words = course_name.split()
   searchstr = "%"
   for word in words:
      searchstr += word + "%"
   
   print(searchstr)

   cursor.execute("SELECT * FROM courses WHERE UPPER(title) LIKE ?", (searchstr.upper(),))
   data_row = cursor.fetchall()
   if len(list(data_row)) < 1:
      return None
   else:
      return random.sample(data_row, 1)[0]


class ActionCourseInfo(Action):

    def name(self) -> Text:
       return "action_course_info"

    def run(self, dispatcher: CollectingDispatcher,
           tracker: Tracker,
           domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_course = next(tracker.get_latest_entity_values("course"), None)
        print(current_course)
            
        if not current_course:
            msg = f"Δεν έχω απάντηση."
            dispatcher.utter_message(text=msg)
            return []

        course_info = get_from_database(current_course)
        print(course_info)
        if course_info == None:
            dispatcher.utter_message('Δεν μπορώ να βρω πληροφορίες για αυτό το μάθημα.')
        else:
            dispatcher.utter_message(f'Όνομα: {course_info[1]} \nECTS: {course_info[2]} \nΤύπος: {course_info[3]} \nΠεριεχόμενο: {course_info[4]}')


