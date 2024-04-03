import random
from rlcard.games.doudizhu.utils import CARD_TYPE
import json
import openai
import copy
from .promptt import create_next_prompt, create_root_prompt, create_value_one_prompt, create_value_two_prompt, create_value_three_prompt

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



def get_value(hand_cards, played_cards):
    prompt_f=create_value_one_prompt(hand_cards, played_cards)
    response=get_completion(prompt_f)
    print(response)
    json_start=response.find('{')
    json_end=response.find('}')
    json_str=response[json_start:json_end+1]
    value_a=json.loads(json_str)
    num=value_a["value"]

    prompt_f=create_value_two_prompt(hand_cards, played_cards)
    response=get_completion(prompt_f)    
    json_start=response.find('{')
    json_end=response.find('}')
    json_str=response[json_start:json_end+1]
    print(json_str)
    value_a=json.loads(json_str)
    num +=value_a["value"]

    prompt_f=create_value_three_prompt(hand_cards, played_cards)
    response=get_completion(prompt_f)
    json_start=response.find('{')
    json_end=response.find('}')
    json_str=response[json_start:json_end+1]
    print(json_str)
    value_a=json.loads(json_str)
    num +=value_a["value"]

    return num



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
            prompt_f=create_root_prompt(hand_cards, legal_act)
            response=get_completion(prompt_f)

            # get three possible actions
            json_start=response.find('{')
            json_end=response.find('}')
            json_str=response[json_start:json_end+1]
            print(json_str)
            action=json.loads(json_str)
            act=action["cards"]
            highest_num=-100
            final_act=[]

            for i, ac in enumerate(act):
                tem_act=copy.deepcopy(ac)
                for j, c in enumerate(tem_act):
                    tem_act[j]=RealCard2EnvCard[c]
                scale=get_value(hand_cards, ac)
                if scale>highest_num:
                    highest_num=scale
                    final_act=tem_act
            print(final_act)

        else:
            prompt_f=create_next_prompt(hand_cards, last_move, legal_act)
            response=get_completion(prompt_f)
            print(response)

            json_start=response.find('{')
            json_end=response.find('}')
            json_str=response[json_start:json_end+1]
            action=json.loads(json_str)
            if action["pass"]==True :
                act=[]
                return act
            
            act=action["cards"]
            highest_num=-100
            final_act=[]

            for i, ac in enumerate(act):
                tem_act=copy.deepcopy(ac)
                for j, c in enumerate(tem_act):
                    tem_act[j]=RealCard2EnvCard[c]
                scale=get_value(hand_cards, ac)
                if scale>highest_num:
                    final_act=tem_act
                    highest_num=scale
            print(final_act)

        print(final_act)
        return final_act
    
