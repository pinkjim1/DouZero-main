import pickle


with open('eval_data.pkl','rb') as f:
    data=pickle.load(f)

print(data)