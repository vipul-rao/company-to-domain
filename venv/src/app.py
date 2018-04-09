import os
import csv
import pandas as pd
from flask import Flask, render_template, request, send_file
import clearbit
import json
clearbit.key = 'sk_f104a33b0acba1831224e8e02b00c6b6'
app = Flask(__name__)

APP__ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload.html")

@app.route("/return-file/")
def return_file():

    return send_file('/home/vipul/PycharmProjects/csvbrain/venv/src/new.csv', as_attachment=True)


@app.route("/upload", methods=['POST'])
def upload():
    target = os.path.join(APP__ROOT)
    print(target)

    if not os.path.isdir(target):
        os.mkdir(target)

    for file in request.files.getlist("file"):
        filename = file.filename
        print(filename)
        destination = "/".join([target, filename])
        print(destination)
        file.save(destination)
        new_path = os.path.abspath(filename)
        print(new_path)
    df = pd.read_csv(new_path, sep=',', encoding="ISO-8859-1")
    saved_column = df['Company'].dropna()
    i = 0
    res = []
    for data in saved_column:
        n = saved_column.get(i)
        ns = len(n.split())
        if ns > 4:
            n = 'never get a website'
        else:
            print("a")
        i = i + 1
        print(n)
        data = clearbit.NameToDomain.find(name=n)
        print("\n")
        print(data)
        if data != None:
            res.append(data['domain'])
        else:
            res.append('none.com')
    print(res)
    df['Domain'] = res
    print(df['Domain'])
    df.to_csv("/home/vipul/PycharmProjects/csvbrain/venv/src/new.csv",index = False)
    downloadpath = "/home/vipul/PycharmProjects/csvbrain/venv/src/new.csv"
    return render_template("complete.html", name=downloadpath)



if __name__ == "__main__":
    app.run(port=4559, debug=True)


