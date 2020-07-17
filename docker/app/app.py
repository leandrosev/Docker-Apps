from typing import List, Dict
from flask import Flask, redirect, url_for, render_template,request, Response
import json
from pymongo import MongoClient
from bson import BSON
from bson import json_util
import matplotlib
import io
import sys
import random
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd

app = Flask(__name__ )

client = MongoClient('mongodb://mongodb:27017/')
mongodb = client.mydb

data =  [  {"student_id":"me1901","grade" : "5"},
           {"student_id":"me1902","grade" : "6"},
           {"student_id":"me1903","grade" : "7"},
           {"student_id":"me1904","grade" : "7"},
           {"student_id":"me1905","grade" : "8"},
           {"student_id":"me1906","grade" : "9"}, 
           {"student_id":"me1907","grade" : "5"},
           {"student_id":"me1908","grade" : "6"},
           {"student_id":"me1909","grade" : "7"},
           {"student_id":"me1910","grade" : "7"},
           {"student_id":"me1911","grade" : "8"},
           {"student_id":"me1912","grade" : "9"} 
        ] 


@app.before_first_request
def insert_data_to_mongodb():

    mongodb.mydb.insert(data)



@app.route('/')

def index():
    
    return render_template('index.html')


@app.route('/mongodb')

def mongo():
          
    data = mongodb.mydb.find()

    return render_template('main.html',data = data, db= "mongo")
    


@app.route('/mongodb_chart.png')

def plot_mongodb_data():
    fig = make_mongodb_chart()
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    
    return Response(output.getvalue(), mimetype='image/png')   

def make_mongodb_chart():
    data = mongodb.mydb.find()
 
    labels=[]
    grades=[]

    for row in data:

        labels.append(row['student_id'])
        grades.append(int(row['grade']))

    fig = Figure(figsize=(16,5))

    axis = fig.add_subplot(1, 3, 1)
    axis.barh(width=grades,y = labels)
    axis.set_title('Student grades barplot from MongoDB database')
    axis.set_xlabel('Grade')

    axis = fig.add_subplot(1, 3, 2)
    axis.hist(grades)
    axis.set_title('Student grades Histogram from MongoDB database')
    axis.set_xlabel('Grade')

    axis = fig.add_subplot(1, 3, 3)
    data_df = pd.DataFrame({'student_id':labels,'grade':grades})
    stats = data_df[['grade']].describe()
    stats_labels = ['Count','Mean','Std','Min','25%','50%','75%','Max']
    axis.axis('tight')
    axis.axis('off')
    axis.table(cellText=stats.values , colLabels=['Student Grades'],rowLabels=stats_labels, cellLoc='center',rowLoc='center',loc='center' )
    axis.set_title('Statistics from MongoDB data')
    
    return fig

@app.route("/analytics")
def show_charts():

    return render_template('analytics.html') 

@app.route("/insert_mongodb", methods=['POST'])    
def insert_to_mongodb ():    
    #Adding new grade to mongodb  
    student_id=request.values.get("student_id")    
    grade=request.values.get("grade")    

    mongodb.mydb.insert({ "student_id":student_id, "grade":grade})  

    return redirect("/mongodb")    

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
    
    
    
    
