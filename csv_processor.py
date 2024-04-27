import time
from icecream import ic

import pandas as pd


from helpers import extract_dicts_from_string
from llm_analysis import LLMAnalyzer

class CSVProcessor:
    def __init__(self, filename):
        self.filename = filename

    async def read_and_print_csv(self):
        df = pd.read_csv(self.filename)
        failed =[]
        for index, row in df.iterrows():
            try:
                # if(row['LLM Equivalence Evaluation (Response)'] == ""):
                response = await self.process_row(index, row)
                df.at[index, 'LLM Equivalence Evaluation (Response)'] = response["eval_res"]
                df.at[index, 'Time taken to complete the request'] = response["resp_time"]
            except Exception as e:
                ic(e)
                failed.append(row['Index'])
            # break
        df.to_csv(self.filename, index=False)
        ic("Complete")
        ic("Failed",failed)

    async def process_row(self, index, row):

        # print(f"internal_index [DO NOT CHANGE]: {row['internal_index [DO NOT CHANGE]']}")

        print(f"Index: {row['Index']}")
        # print(f"DialogID Hash: {row['DialogID Hash']}")
        # print(f"UserID Hash: {row['UserID Hash']}")
        # print(f"Conversation History: {row['Conversation History']}")
        # print(f"User Response: {row['User Response']}")
        # print(f"Human Evaluation: {row['Human Evaluation']}")
        # print(f"LLM Equivalence Evaluation (Response): {row['LLM Equivalence Evaluation (Response)']}")
        # print(f"Time taken to complete the request: {row['Time taken to complete the request']}")

        content = self.create_content(conversation=row['Conversation History'],userResponse=row['User Response'])
        llm_analysis = LLMAnalyzer()
        start_time = time.time()
        response = await llm_analysis.create_api(content)
        end_time = time.time()
        difference = str(round(end_time-start_time,2))
        ic(difference)
        response_dict = llm_analysis.clean_response_data(response)
        if response_dict:
            eval_res= "EQUIVALENT"
        else:
            eval_res= "NOT_EQUIVALENT"
        out= {
            "eval_res": eval_res,
            "resp_time":difference
        }
        return out
        # ic(response_dict)

    def last_bot_question(self,last_conversation):
        last_question = last_conversation.get("bot")
        return last_question

    def create_content(self,conversation,userResponse):
        try:
            data = eval(conversation)
        except:
            data = extract_dicts_from_string(conversation)
    
        bot_last_question = self.last_bot_question(data[-1])

        content= f"You will be provided with the following information:1. [CONVERSATION]: {data}2. [BOT_LAST_QUESTION]:{bot_last_question} 3. [USER_ANSWER]: {userResponse}.Your task is to evaluate whether the [USER ANSWER] is mathematically equivalent to the bot's last question [BOT_LAST_QUESTION] in based on the context of the [CONVERSATION].The output should be in the following JSON format within code blocks:json {{'rationale': 'A concise, brief reasoning for your decision on whether the user\'s answer is equivalent or not to the bot\'s last question.','equivalent': true/false}}To complete this task, follow these steps:1. Carefully review the [CONVERSATION] array and identify the context.2. Analyze the [BOT_LAST_QUESTION] and understand the meaning of the question and what the bot expects.2. Analyze the [USER_ANSWER] and determine if it is mathematically equivalent to the bot's last question [BOT_LAST_QUESTION].3. Provide a concise, brief reasoning for your decision in the 'rationale' key, explaining why the user's answer is equivalent or not equivalent to the bot's last question.. Based on your reasoning, set the 'equivalent' key to true if the [USER ANSWER] is mathematically equivalent to the bot's last question, or false otherwise.5. Ensure that your response strictly follows the provided JSON schema.Please ensure that your response strictly follows the provided JSON schema, with the 'rationale' key providing a concise, brief reasoning for your decision, and the 'equivalent' key indicating whether the user's answer is equivalent (true) or not equivalent (false) to the bot's last question."
        return content
