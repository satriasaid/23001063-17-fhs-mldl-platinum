import re, sqlite3
import pandas as pd
from flask import Flask, jsonify, request
from flasgger import Swagger, LazyString, LazyJSONEncoder, swag_from

class CustomFlaskAppWithEncoder(Flask):
    json_provider_class = LazyJSONEncoder

app = CustomFlaskAppWithEncoder(__name__)

swagger_template = dict(
    info = {
        'title' : LazyString(lambda: 'API untuk Analisis Sentimen'),
        'version' : LazyString(lambda: '1.0.0'),
        'description' : LazyString(lambda: 'Membuat API untuk Analisis Sentimen')
    },
    host = LazyString(lambda: request.host),
)

swagger_config = {
    'headers' : [],
    'specs' : [
        {
            "endpoint" : "docs",
            "route" : "/docs.json",
        }
    ],
    "static_url_path" : "/flasgger_static",
    "swagger_ui": True,
    "specs_route" : "/docs/",
}
swagger = Swagger(app, template = swagger_template, config = swagger_config)

# Endpoint testing dengan hello world
@app.route('/', methods=['GET'])
def hello_world():
    json_response = {
        '3. status_code': 200,
        '1. description' : "Please visit: ",
        '2. data' : "http://127.0.0.1:5000/docs/",
    }
    response_data = jsonify(json_response)
    return response_data

# proses Neural Network untuk data mula-mula 

# 1. loading initial data
df = pd.read_csv("train_preprocess.tsv", sep='\t', names=["tweet", "sentiment"])
df_proc = df.copy()

# 2. melakukan cleaning pada initial data
def cleaning(data):
    data = data.replace(r'(\\x\S+)','',regex=True).astype('str')
    data = data.replace(r'((\s{2}))',' ',regex=True).astype('str')
    data = data.replace(r'(\\n)',' ',regex=True).astype('str')
    data = data.replace(r'(?:RT\W+)',' ',regex=True).astype('str')
    data = data.replace(r'(?:USER\W+)',' ',regex=True).astype('str')
    data = data.replace(r'(?:USER)',' ',regex=True).astype('str')
    data = data.replace(r'(?:https:)\S+',' ',regex=True).astype('str')
    data = data.replace(r'(?:http)\S+',' ',regex=True).astype('str')
    data = data.replace(r'(?:https)\S+',' ',regex=True).astype('str')
    data = data.replace(r'(?:URL)',' ',regex=True).astype('str')
    data = data.replace(r'[^0-9A-Za-z]',' ',regex=True).astype('str')
    cleanTwList = data.to_list()
    cleanTwList = [x.strip(' ') for x in cleanTwList] #menghilangkan spasi yang tidak penting
    cleanTwList = [re.sub(r'\s+',' ',x) for x in cleanTwList] #menghilangkan spasi yang berlebihan
    data = cleanTwList
    return data

temp_col = cleaning(df_proc['tweet'])
df_proc['tweet'] = temp_col

df_alay = pd.read_csv("/external_source/kbba.txt", sep='\t', names=['alay','normal'])
df_sw = pd.read_csv("/external_source/stopword.txt", sep='\t', names=['stopword'])
df_neg = pd.read_csv("/external_resource/negation_combi.txt", sep='\t', names=['negate'])

alay_list = df_alay['alay'].to_list()
normal_list = df_alay['normal'].to_list()
sw_list = df_sw['stopword'].to_list()
neg_list = df_neg['negate'].to_list()

for swli in sw_list:
    if swli in neg_list:
        sw_list.remove(swli)
        
sw_list.append('nya')

def txt_dealay(datafr):
    data = datafr.str.lower()
    for i in range(len(alay_list)):
        normal = data.replace(r'\b'+ alay_list[i] + r'\b',normal_list[i],regex=True).astype('str')
        i += 1
        data = normal
    return data

def txt_sw(datafr):
    data = datafr.str.lower()
    for i in range(len(sw_list)):
        normal = data.replace(r'\b'+ sw_list[i] + r'\b','',regex=True).astype('str')
        i += 1
        data = normal
    return data

df_proc['norm'] = txt_dealay(df_proc['tweet'])
df_proc['norm'] = txt_sw(df_proc['norm'])
df_proc['norm'] = cleaning(df_proc['norm'])
df_proc[['tweet','norm','sentiment']]
    
# 3. Melakukan Feature Extraction untuk Neural Network


# Endpoint 1 untuk Neural Network menerima teks

# Endpoint 2 untuk Neural Network menerima file

# Endpoint 3 untuk LSTM menerima teks

# Endpoint 4 untuk LSTM menerima file

if __name__ == '__main__':
    app.run()