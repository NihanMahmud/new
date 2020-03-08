
from flask import Flask 
from flask import render_template
from flask import request
from datetime import datetime as dt
import os
import re

now=dt.today()
info={}

app=Flask(__name__)
@app.route('/')
def main():
    return render_template('Mainpage.html')

@app.route('/NextPage',methods=['POST'])
def main2():
    username=request.form['Name'] 
    password=request.form['password']
    if username=='' or password=='':
        return render_template('Invalid.html')
    username=username.replace(' ','')
    if username in info.keys():
        return render_template('taken.html')
    info[username]=password
    user_name=username
    return render_template('NextPage.html',username=username)

@app.route('/login')
def main3():
    return render_template('login.html')

@app.route('/profile',methods=['POST'])
def main4():
    username=request.form['username']
    password=request.form['password']
    username=username.replace(' ','')
    if username in info.keys() and password==info.get(username):
        return render_template('profile.html', username=username,password=password)
    else:
        return render_template('Wrong.html')         
@app.route('/profile/receivedata',methods=['POST'])
def main5():
    text=request.form['text']
    title=request.form['title']
    username=request.form['name']
    password=request.form['password']
    now=dt.today()
    try:
        os.mkdir(f'Info/{username}',511)
    except:
        pass
    now=str(now)
    res=re.findall(r'[.]\d*',now)
    now=now.replace(res[0],'')
    with open(f'Info/{username}/{title}.txt','a') as file:
        file.write(f'Time : {now}\n')
        file.write(text)
    return render_template('receivedata.html',name=username,password=password)
@app.route('/profile/datamanager',methods=['POST'])
def main6():
    username=request.form['username']
    password=request.form['password']
    filelist=os.listdir(f"Info/{username}")
    return render_template("datamanager.html",filelist=filelist,username=username,password=password)
@app.route('/profile/datamanager/readdata',methods=['POST'])
def main7():
    username=request.form['username']
    password=request.form['password']
    filename=request.form['filename']
    filename=filename.replace('.txt','')
    try:
        with open(f'Info/{username}/{filename}.txt','r') as file:
            text=file.read()
    except FileNotFoundError:
        return render_template('filenotfound.html',username=username,password=password)
    return f'<h3>Your Data :</h3><p>{text}</p>'+render_template('readdata.html',username=username,password=password)
app.run()
