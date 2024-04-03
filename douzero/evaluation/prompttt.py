def create_root_prompt(a, b):
    root_prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. It is now your turn to play cards. Your current task is to play cards based on your hand, \
with the ultimate goal of winning the game. You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "legal action": array, \
    "cards": array \
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
I will give you "hand cards" and "legal action" as input, and you should choose three actions from "legal action" parts and show them in "cards" part. If there are less than three possible actions on "legal action" parts, show all of them in "cards" part.  \
Any other actions not in "legal action" is illegal.
You should consider Which action can finish your hand cards more quickly? which action has big cards and small cards? For example, if you have double "3" and double "2", which means you can play double "3" first and in the next turn play double "2" which are most likely unmatched by your opponents, so you can get first move advantage. \
Here are some tips, it might be a good idea to start from small cards like ["3", "3"] or ["4"].
You should also try not to break straight cards, because it is likely unmatched by your opponents. But if it is necessary, you can split it. \
You should figure out the cards you want to play. \
here are some examples of your response: \
input: hand cards:["3", "5", "5", "A"], \
legal action: [["3"], ["5"], ["A"], ["5", "5"]], 
reponse: {{ 
    "hand cards":["3", "5", "5", "A"], \
    "legal action": [["3"], ["5"], ["A"], ["5", "5"]], \
    "cards":[["3"], ["5, 5"], ["A"]]
}}
input: hand cards:["4", "5", "6", "7", "8", "2"], \
legal action:[["4"],["5"], ["6"], ["7"], ["8"], ["2"], ["4", "5", "6", "7", "8"]], \
reponse:{{
    "hand cards":["4", "5", "6", "7", "8", "2"], \
    "legal action": [["4"], ["5"], ["6"], ["7"], ["8"], ["2"], ["4", "5", "6", "7", "8"]], \
    "cards":[["4"],  ["4", "5", "6", "7", "8"], ["2"]]
}}
input:hand cards:{a}, \
legal action:{b}, \
reponse: 
"""
    return root_prompt



def create_next_prompt(a, b, c):
    next_prompt=f"""
Your primary task is to complete a game of Dou Di Zhu (Fight the Landlord).In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. You are currently \
in the phase of playing cards. Based on the cards played by others, you need to determine whether \
you can play cards that beat theirs and whether you should play those cards. Your ultimate goal is \
to win the entire game.  You should only respond in json format as described below \
{{
    "hand cards": array,
    "opponent cards" :array,
    "legal action": array,
    "cards": array,
    "pass": boolean
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
You can only choose actions from "legal action" part, and if there are no legal action, skip this turn, and value of "pass" would be "true" ; if there are, speculate on your subsequent playing strategy after \
playing these cards, and judge whether this strategy can lead to victory, and value of "pass" would be "false". you should choose three possible actions from "legal action" parts and show them in "cards" part. If there are less than three possible actions on "legal action" parts, show all of them in "cards" part.  \
Finally, decide whether \
to play the cards.  here is an example: \
input: hand cards:["3", "4", "A", "2", "2"], \
"opponent cards" :["5"], \
"legal action": [["A"], ["2"], ["2"]], \
{{
    "hand cards": ["3", "4", "A", "2", "2"],
    "opponent cards" :["5"],
    "legal action": [["A"], ["2"], ["2"]],
    "cards": [["A"], ["2"]],
    "pass": false
}}
input: hand cards:{a}, \
"opponent cards" :{b}, \
"legal action": {c}, \
            """
    return next_prompt


def create_value_one_prompt(a, b):
    value_prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. Your current task is to value the card on your hands and give a score of your cards.\
You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "played cards": array, \
    "reason": string, \
    "value": double \
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
I will give you "hand cards" and "played cards" as input, you are in a state that you have already played your cards, and you should value the cards on your hand after this action. \
The score you give should obey the following rule: Whether or not you have the bigger cards which are the same type with "played cards" in your hand. The reason why it is important is that you can use them to take back the first play advantage. The scores you give should be between 0-10. 0 means you dont have such cards, 10 means you have absolute biggest cards in your hand to take back the first play advantage. \
here are some examples of your response: \
input: hand cards:["3", "5", "5", "A"], \
played cards: [["3"]], 
reponse: {{ 
    "hand cards":["3", "5", "5", "A"], \
    "played cards": [["3"]], \
    "reason": "There is "A" in the hand, which is the same type card with "3", and it is pretty big. So I will give it 7."
    "value": 7.0
}}
input: hand cards:["4", "5", "6", "7", "8", "2"], \
played cards:[["4", "5", "6", "7", "8"]], \
reponse:{{
    "hand cards":["4", "5", "6", "7", "8", "2"], \
    "played cards": [["4", "5", "6", "7", "8"]], \
    "reason":"You don't have the same type of cards with ["4", "5", "6", "7", "8"] in your hands, so I will give it 0."
    "value": 0.0
}}
input: hand cards:["3"], \
played cards:[["3"]], \
reponse:{{
    "hand cards":["3"], \
    "played cards": [["3"]], \
    "reason": "After you played ["3"], you don't have any card in your hand. But you no any cards in your hand means that you have already win the game, so I will give it 10."
    "value": 10.0
}}
input:hand cards:{a}, \
played cards:{b}, \
reponse: 
"""
    return value_prompt


def create_value_two_prompt(a, b):
    value_prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. Your current task is to value the card on your hands and give a score of your cards.\
You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "played cards": array, \
    "reason": string, \
    "value": double \
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
I will give you "hand cards" and "played cards" as input, you are in a state that you have already played your cards, and you should value the cards on your hand after this action. \
The score you give should obey the following rule: How many times you still need to finish the cards on your hand. the scores you give should between 0-10, 0 means you need at least 13 times to play your cards, and 10 means you have already played all the cards on your hand. \
here are some examples of your response: \
input: hand cards:["3", "5", "5", "A"], \
played cards: [["3"]], 
reponse: {{ 
    "hand cards":["3", "5", "5", "A"], \
    "played cards": [["3"]], \
    "reason": "You can play ["5", "5"] and ["A"], so you need at least 2 times to finish the cards on your hand. I will give it 8."
    "value": 8.0
}}
input: hand cards:["4", "5", "6", "7", "8", "2"], \
played cards:[["4", "5", "6", "7", "8"]], \
reponse:{{
    "hand cards":["4", "5", "6", "7", "8", "2"], \
    "played cards": [["4", "5", "6", "7", "8"]], \
    "reason":"You only have ["2"] on your hands, so I will give it 9."
    "value": 9.0
}}
input: hand cards:["3"], \
played cards:[["3"]], \
reponse:{{
    "hand cards":["3"], \
    "played cards": [["3"]], \
    "reason": "After you played ["3"], you don't have any card in your hand. But you no any cards in your hand means that you have already win the game, so I will give it 10."
    "value": 10.0
}}
input:hand cards:{a}, \
played cards:{b}, \
reponse: 
"""
    return value_prompt



def create_value_three_prompt(a, b):
    value_prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. Your current task is to value the card on your hands and give a score of your cards.\
You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "played cards": array, \
    "reason": string, \
    "value": double \
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
I will give you "hand cards" and "played cards" as input, you are in a state that you have already played your cards, and you should value the cards on your hand after this action. \
The score you give should obey the following rule: How big the cards on your hands are. the scores you give should between 0-10, 0 means you need at least 13 times to play your cards, and 10 means you have already played all the cards on your hand. \
here are some examples of your response: \
input: hand cards:["3", "5", "5", "A"], \
played cards: [["3"]], 
reponse: {{ 
    "hand cards":["3", "5", "5", "A"], \
    "played cards": [["3"]], \
    "reason": "["5"] is small card but ["A"] is pretty big, so I will give it 6.0"
    "value": 6.0
}}
input: hand cards:["4", "5", "6", "7", "8", "2"], \
played cards:[["4", "5", "6", "7", "8"]], \
reponse:{{
    "hand cards":["4", "5", "6", "7", "8", "2"], \
    "played cards": [["4", "5", "6", "7", "8"]], \
    "reason":"You only have ["2"] on your hands, so I will give it 9."
    "value": 9.0
}}
input: hand cards:["3"], \
played cards:[["3"]], \
reponse:{{
    "hand cards":["3"], \
    "played cards": [["3"]], \
    "reason": "After you played ["3"], you don't have any card in your hand. But you no any cards in your hand means that you have already win the game, so I will give it 10."
    "value": 10.0
}}
input:hand cards:{a}, \
played cards:{b}, \
reponse: 
"""
    return value_prompt


def predict_prompt(a, b):
    value_prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. Your task is to predict your opponents' hands cards based on the cards already played and the cards on your hand.\
You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "played cards": array, \
    "opponent cards": array \
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
I will give you "hand cards" and "played cards" as input, and you should guess your opponents' hands cards. \
here are some examples of your response: \
input: hand cards:["3", "5", "5", "A"], \
played cards: [["3"]], 
reponse: {{ 
    "hand cards":["3", "5", "5", "A"], \
    "played cards": [["3"]], \
    "opponent cards":["3", "4", "2", "2"]
}}
input: hand cards:["4", "5", "6", "7", "8", "2"], \
played cards:[["4", "5", "6", "7", "8"]], \
reponse:{{
    "hand cards":["4", "5", "6", "7", "8", "2"], \
    "played cards": [["4", "5", "6", "7", "8"]], \
    "opponent cards":["7", "8", "9", "9"]
}}
input: hand cards:["3"], \
played cards:[["3"]], \
reponse:{{
    "hand cards":["3"], \
    "played cards": [["3"]], \
    "opponent cards":["7", "8"]
}}
input:hand cards:{a}, \
played cards:{b}, \
reponse: 
"""
    return value_prompt