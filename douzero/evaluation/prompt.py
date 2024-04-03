
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


def create_value_prompt(a, b):
    value_prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. Your current task is to value the card on your hands and give a score of your cards.\
You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "played cards": array, \
    "value": double \
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
I will give you "hand cards" and "played cards" as input, you are in a state that you have already played your cards, and you should value the cards on your hand after this action. \
The score you give should obey the following rule: 1. if you have bigger cards, you get higher scores. "3" is 0, "4" is 0.5, and "K"is 4.5,"A" is 5,  "2" is 5.5, "red_joker" is 6.5.  \
2. the less cards the better. If you have one card, minus 0.5 scores. For example, if you have 3 cards, then the total value minus 1.5 scores. 
3. if you have bigger cards you will get scores. For example, "played cards" is ["3"] and you have ["2"], then you get 2 scores. "played cards" is ["5", "5", "5", "3" , "4"] and you have ["8", "8", "8"], you get 2 scores. \
4. if after your playing, there are no cards on your hands, then you get 100.
5. When you calculate the scores, you only need calculated "hand cards" minus "played cards". For example, your hand cards is ["3", "5"], your played cards is ["3"], then you should only calculate ["5"] scores. \
here are some examples of your response: \
input: hand cards:["3", "5", "5", "A"], \
played cards: [["3"]], 
reponse: {{ 
    "hand cards":["3", "5", "5", "A"], \
    "played cards": [["3"]], \
    "value": 4.0
}}
input: hand cards:["4", "5", "6", "7", "8", "2"], \
played cards:[["4", "5", "6", "7", "8"]], \
reponse:{{
    "hand cards":["4", "5", "6", "7", "8", "2"], \
    "played cards": [["4", "5", "6", "7", "8"]], \
    "value": 4.5 
}}
input: hand cards:["3"], \
played cards:[["3"]], \
reponse:{{
    "hand cards":["3"], \
    "played cards": [["3"]], \
    "value": 100
}}
input:hand cards:{a}, \
played cards:{b}, \
reponse: 
"""
    return value_prompt
