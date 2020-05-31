import numpy as np
import pandas as pd
import sqlite3
from flask import Flask, render_template, request
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
app = Flask(__name__)
df = pd.read_csv("https://sebkaz.github.io/teaching/PrzetwarzanieDanych/data/polish_names.csv")
def string_number(string):
    return int(string == 'm')

def last_a(string):
    return int(string[-1] == 'a')

def length(string):
    return int(len(string))

df['target'] = df['gender'].map(string_number)

df['last_a'] = df['name'].map(last_a)

df['len_name'] = df['name'].map(length)

y = df['target'].values
X = df[['len_name','last_a']].values

model2 = LogisticRegression()
model2.fit(X,y)
y_pred_lr = model2.predict(X)
accuracy_score(y, y_pred_lr)
dd = np.array([[length("Tomasz"), last_a("Tomasz")]])
test_prediction = model2.predict(dd)

@app.route('/', methods=['GET','POST'])
def check_gender():
    
    
    insert_name = ' '
    if request.method == 'POST':
        insert_name = request.form['name']
    
    if (insert_name == ' '):
        return render_template('index.html')
    if (insert_name == ''):
        return render_template('index.html', blad='Something gonna wrong, please enter again your name')
        
    if (model2.predict(np.array([[length(insert_name), last_a(insert_name)]])) == 0):
        conn = sqlite3.connect('project.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS names
                 (id_proc INTEGER PRIMARY KEY AUTOINCREMENT, name text , gender text)''')
        c.execute("INSERT INTO names (name, gender) VALUES (?,?)",(insert_name,'Woman'))
        conn.commit()        
        return render_template('index.html', user=insert_name, gender='Woman')    
    if (model2.predict(np.array([[length(insert_name), last_a(insert_name)]])) == 1):
        conn = sqlite3.connect('project.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS names
                 (id_proc INTEGER PRIMARY KEY AUTOINCREMENT, name text , gender text)''')
        c.execute("INSERT INTO names (name, gender) VALUES (?,?)",(insert_name,'Man'))
        conn.commit()        
        return render_template('index.html', user=insert_name, gender='Man')
    else:
        return render_template('index.html', blad='Something gone wrong, please enter your name again')

if __name__ == "__main__":
    app.run(host='0.0.0.0')
    