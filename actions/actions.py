# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


# import openpyxl
import pandas as pd
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-medium")
model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-medium")
model_engine = "microsoft/DialoGPT-medium"

class ActionGetStudentID(Action):
    def name(self) -> Text:
        return "action_get_student_id"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Open the excel file and select the worksheet
        # workbook = openpyxl.load_workbook('student_database.xlsx')
        # worksheet = workbook.active
        data = pd.read_excel('student_database.xlsx', sheet_name='Sheet1')

        # Get the student name from the tracker
        student_name = tracker.get_slot("first_name") + " " + tracker.get_slot("last_name")

        # Search for the student ID in the database
        for i in range(len(data["Student Name"])):
            if data["Student Name"][i] == student_name:
                student_id = data["Student ID"][i]
                break

        # Send the student ID to the user
        dispatcher.utter_message("Your student ID is {}.".format(student_id))
        
        
        # prompt = f"Your student ID is {student_id}."
        # Generate a casual response using the DialoGPT-medium model
        # response = openai.Completion.create(engine=model.encode('utf-8'), prompt=prompt.encode('utf-8'), max_tokens=100)["choices"][0]["text"]
        # response = openai.Completion.create(engine=model_engine, prompt=prompt, max_tokens=100)["choices"][0]["text"]
        # dispatcher.utter_message(response)

                
        # input_ids = tokenizer.encode(prompt, return_tensors='pt').input_ids
        # output_ids = model.generate(input_ids=input_ids, max_length=100, do_sample=True)
        # response = tokenizer.decode(output_ids[0], skip_special_tokens=True)       
        # dispatcher.utter_message(response)



        # # get user input from tracker
        # user_input = tracker.latest_message.get('text')

        # # encode the new user input, add the eos_token and return a tensor in Pytorch
        # new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # # append the new user input tokens to the chat history
        # chat_history_ids = tracker.get_slot("chat_history_ids")
        # bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids

        # # generated a response while limiting the total chat history to 1000 tokens
        # chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, temperature=0.7)

        # # update chat history slot
        # tracker.slots["chat_history_ids"] = chat_history_ids

        # # pretty print last ouput tokens from bot
        # bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # # send bot response to user
        # dispatcher.utter_message(text=bot_response)

        return []



class SubmitCovidTestResultsAction(Action):

    def name(self) -> Text:
        return "action_submit_covid_test_results"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the student details and test results from slots
        student_id = tracker.get_slot("student_id")
        student_name = tracker.get_slot("first_name") + " " + tracker.get_slot("last_name")
        covid_status = tracker.get_slot("covid_status")
        test_type = tracker.get_slot("covid_test_type")

        # Load the student database
        data = pd.read_excel('student_database.xlsx', sheet_name='Sheet1')

        # Check if the student record already exists
        if student_id in data["Student ID"].values:
            data.loc[data["Student ID"] == student_id, ["Covid Status", "Covid Test Type"]] = [covid_status, test_type]
        else:
            data = data.append({"Student Name": student_name, "Student ID": student_id,  "Covid Status": covid_status, 
                                "Covid Test Type": test_type}, ignore_index=True)

        # Save the updated student database
        data.to_excel("student_database.xlsx", sheet_name='Sheet1', index=False)

        # Send a confirmation message to the user
        dispatcher.utter_message(text="Thank you for submitting your COVID-19 test results. Your status has been updated.")

        return []


class ActionGenerateResponse(Action):
    def name(self):
        return "action_generate_response"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the latest user message
        user_input = tracker.latest_message.get('text')

        # # encode the user's input and generate a response
        # input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')
        # bot_output = model.generate(input_ids, max_length=1000, top_k=100)
        # # pad_token_id=tokenizer.eos_token_id
        # # decode the bot's output and send it to the user
        # bot_response = tokenizer.decode(bot_output[0], skip_special_tokens=True, padding_side='left')
        # dispatcher.utter_message(bot_response)

        # Generate a response.
        response = model.generate(
            input_ids=tokenizer.encode(user_input, return_tensors="pt"),
            do_sample=True,
            temperature=0.7,
            max_length=100,
            top_p=0.9,
            repetition_penalty=1.0,
            no_repeat_ngram_size=3,
            eos_token_id=tokenizer.eos_token_id,
        )

        # Decode the response.
        response = tokenizer.decode(response[0], skip_special_tokens=True)

        # Send the response to the user.
        dispatcher.utter_message(response)

        return []
    

class ActionChat(Action):

    def name(self) -> Text:
        return "action_chat"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # get user input from tracker
        user_input = tracker.latest_message['text']

        # encode the new user input, add the eos_token and return a tensor in Pytorch
        new_user_input_ids = tokenizer.encode(user_input + tokenizer.eos_token, return_tensors='pt')

        # append the new user input tokens to the chat history
        chat_history_ids = tracker.get_slot("chat_history_ids")
        bot_input_ids = torch.cat([chat_history_ids, new_user_input_ids], dim=-1) if chat_history_ids is not None else new_user_input_ids

        # generated a response while limiting the total chat history to 1000 tokens
        chat_history_ids = model.generate(bot_input_ids, max_length=1000, pad_token_id=tokenizer.eos_token_id, temperature=0.7, do_sample=True)

        # update chat history slot
        tracker.slots["chat_history_ids"] = chat_history_ids

        # pretty print last ouput tokens from bot
        bot_response = tokenizer.decode(chat_history_ids[:, bot_input_ids.shape[-1]:][0], skip_special_tokens=True)
        
        # send bot response to user
        dispatcher.utter_message(text=bot_response)

        return []