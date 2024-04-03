import random
from rlcard.games.doudizhu.utils import CARD_TYPE
import json
import openai
import copy

EnvCard2RealCard = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7',
                    8: '8', 9: '9', 10: '10', 11: 'J', 12: 'Q',
                    13: 'K', 14: 'A', 17: '2', 20: 'Black_joker', 30: 'Red_joker'}
RealCard2EnvCard = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
                    '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12,
                    'K': 13, 'A': 14, '2': 17, 'Black_joker': 20, 'Red_joker': 30}

INDEX = {'3': 0, '4': 1, '5': 2, '6': 3, '7': 4,
         '8': 5, '9': 6, 'T': 7, 'J': 8, 'Q': 9,
         'K': 10, 'A': 11, '2': 12, 'Black_joker': 13, 'Red_joker': 14}


openai.api_key= ""

def get_completion(prompt, model="gpt-4"):
    messages=[{"role":"user", "content":prompt}]
    response=openai.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0,
    )
    return response.choices[0].message.content



class GptAgent():

    def __init__(self,position):
        self.name = 'Gpt'
        self.position=position

    def act(self, infoset):

        hand_cards = infoset.player_hand_cards
        for i, c in enumerate(hand_cards):
            hand_cards[i] = EnvCard2RealCard[c]

            # Last move
        last_move = infoset.last_move.copy()
        for i, c in enumerate(last_move):
            last_move[i] = EnvCard2RealCard[c]

            # Last two moves
        last_two_cards = infoset.last_two_moves
        for i in range(2):
            for j, c in enumerate(last_two_cards[i]):
                last_two_cards[i][j] = EnvCard2RealCard[c]

            # Last pid
        last_pid = infoset.last_pid


            #legal actions
        legal_act=copy.deepcopy(infoset.legal_actions)
        for i, cards_com in enumerate(legal_act):
            for j, c in enumerate(cards_com):
                legal_act[i][j]=EnvCard2RealCard[c]
        

        if last_pid==self.position:
            prompt=f"""
Your main task is to complete a game of Fight the Landlord (a popular Chinese card game). \
In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. It is now your turn to play cards. Your current task is to play cards based on your hand, \
with the ultimate goal of winning the game.  You should only respond in the json format as described below \
{{
    "hand cards": array, \
    "legal action": array, \
    "single":array, \
    "double":array, \
    "Triple":array, \
    "Triple with one":array, \
    "Triple with two":array, \
    "Bomb":array, \
    "Bomb with one":array, \
    "Bomb with two":array, \
    "straight":array, \
    "double straight":array, \
    "triple straight":array, \
    "analysis":"analysis", \
    "reasoning": "reasoning", \
    "cards": array
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
From "single" to "triple straight" are divided from "legal action", which means any other arrays not in "legal action" is illegal. Below are your hand cards delimited by triple backticks \
``` {hand_cards}```  Below are the legal action you can play \
```{legal_act}```  \
In analysis, you should consider Which combination can be played to finish the hand more quickly? which combination has big cards and small cards? For example, if you have double "3" and double "2", which means you can play double "3" first and in the next turn play double "2" which are most likely unmatched by your opponents, so you can get first move advantage. \
In reasoning part you should figure out the cards you want to play, and you can only get one solution. If you can't decide which choices are better, just choose random one \
here is an example of your response: \
{{ 
    "hand cards":["3", "5", "5", "A"], \
    "legal action": [["3"], ["5"], ["A"], ["5", "5"]], \
    "single":[["3"], ["5"], ["A"]], \
    "double":["5", "5"], \
    "Triple":[], \
    "Triple with one":[], \
    "Triple with two":[], \
    "Bomb":[], \
    "Bomb with one":[], \
    "Bomb with two":[], \
    "straight":[], \
    "double straight":[], \
    "triple straight":[], \
    "analysis": "it need at least three turns to finish this game. if you play ["3"], ["5","5"], ["A"], it is the quickest way to end the game",  \
    "reasoning":"if you play ["3"], your opponent can only play single card and you can play ["A"] which is most likely unmatched by your opponents becuase it is big card", \
    "cards":["3"]
}}

you should only output only one json solution. After that you can't output anything else. 
            """
            response=get_completion(prompt)
            print(response)
            json_start=response.find('{')
            json_end=response.find('}')
            json_str=response[json_start:json_end+1]
            print(json_str)
            action=json.loads(json_str)
            act=action["cards"]
            for i, c in enumerate(act):
                act[i] = RealCard2EnvCard[c]
        else:
            prompt=f"""
Your primary task is to complete a game of Dou Di Zhu (Fight the Landlord).In this game, the person who finishes playing all their cards wins. So, your task is to play all the cards in your hand as quickly as possible. You are currently \
in the phase of playing cards. Based on the cards played by others, you need to determine whether \
you can play cards that beat theirs and whether you should play those cards. Your ultimate goal is \
to win the entire game.  You should only respond in json format as described below \
{{
    "hand cards": array,
    "opponent cards" :array,
    "legal action": array,
    "analysis":"analysis",
    "reasoning": "reasoning",
    "cards": array,
    "pass": boolean
    }}
In this json response, you should only use double quote. Single quote is illegal and should not appear in your response. \
Below are your hand cards delimited by triple backticks \
``` {hand_cards}```  2. Below are the legal action you can play \
```{legal_act}``` 3.  Below are your hand cards \
the cards played by the opponent are following \
```{last_move}``` You can only choose actions from "legal action" part, and if there are no legal action, skip this turn, and value of "pass" would be "true" ; if there are, speculate on your subsequent playing strategy after \
playing these cards, and judge whether this strategy can lead to victory, and value of "pass" would be "false".  Finally, decide whether \
to play the cards. You can only play cards choosing from "legal action" part. show your analysis. here is an example:
{{
    "hand cards": ["3", "4", "A", "2", "2"],
    "opponent cards" :["5"],
    "legal action": [["A"], ["2"], ["2"]],
    "reasoning": "you can play "A", "2", "2" to beat your opponents, but "2" may be used as double in the next turn. so "A" might be better", 
    "cards": ["A"],
    "pass": false
}}
you should only output only one json solution, after that you can't output anything else. If you do not want to play any cards, the value of "pass" would be "true", otherwise it would be false.
            """
            response=get_completion(prompt)
            print(response)
            json_start=response.find('{')
            json_end=response.find('}')
            json_str=response[json_start:json_end+1]
            action=json.loads(json_str)
            if action["pass"]==True :
                act=[]
                return act
            act=action["cards"]
            for i, c in enumerate(act):
                act[i] = RealCard2EnvCard[c]

        print(act)
        return act
