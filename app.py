from flask import Flask, render_template,request,make_response
import plotly
import plotly.graph_objs as go
import mysql.connector
from mysql.connector import Error
import sys

import pandas as pd
import numpy as np
import json  #json request
from werkzeug.utils import secure_filename
import os
import csv #reading csv
import geocoder
from random import randint
import math


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('login.html')

@app.route('/dataloader')
def indexnew1():    
    return render_template('forecast.html')

@app.route('/index')
def indexnew():    
    return render_template('index.html')

@app.route('/register')
def register():    
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')



""" REGISTER CODE  """
rcount = 0
@app.route('/regdata', methods =  ['GET','POST'])
def regdata():
    connection = mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    cursor = connection.cursor()
    email = request.args['email']
    sq_query="select count(*) from userdata where Email='"+email+"'"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    rcount = int(data[0][0])
    if(rcount==0):
        uname = request.args['uname']
        name = request.args['name']
        pswd = request.args['pswd']
        phone = request.args['phone']
        addr = request.args['addr']
        value = randint(123, 99999)
        uid="User"+str(value)
        print(addr)
            
        #cursor = connection.cursor()
        sql_Query = "insert into userdata values('"+uid+"','"+uname+"','"+name+"','"+pswd+"','"+email+"','"+phone+"','"+addr+"')"
            
        cursor.execute(sql_Query)
        connection.commit() 
        connection.close()
        cursor.close()
        msg="Data stored successfully"
        #msg = json.dumps(msg)
        resp = make_response(json.dumps(msg))
        
        print(msg, flush=True)
        #return render_template('register.html',data=msg)
        #return render_template('login.html')
        return resp
    else:
        msg="User Already Exists"
        resp = make_response(json.dumps(msg))
        
        print(msg, flush=True)
        #return render_template('register.html',data=msg)
        return resp
       




"""LOGIN CODE """

@app.route('/logdata', methods =  ['GET','POST'])
def logdata():
    connection=mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    lgemail=request.args['email']
    lgpssword=request.args['pswd']
    print(lgemail, flush=True)
    print(lgpssword, flush=True)
    cursor = connection.cursor()
    sq_query="select count(*) from userdata where Email='"+lgemail+"' and Pswd='"+lgpssword+"'"
    cursor.execute(sq_query)
    data = cursor.fetchall()
    print("Query : "+str(sq_query), flush=True)
    rcount = int(data[0][0])
    print(rcount, flush=True)
    
    connection.commit() 
    connection.close()
    cursor.close()
    
    if rcount>0:
        msg="Success"
        resp = make_response(json.dumps(msg))
        return resp
    else:
        msg="Failure"
        resp = make_response(json.dumps(msg))
        return resp
        
   
@app.route('/dashboard')
def dashboard():
    try:        
        g = geocoder.ip('me')
        print(g.latlng[0])
        print(g.latlng[1])
    except:
        print("Done")
    try:        
        connection=mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
        cursor = connection.cursor()
        sq_query="select count(*) from userdata"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        rcount = int(data[0][0])
        print(rcount, flush=True)

        sq_query="select count(distinct Area) from cropdataset"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        regcount = int(data[0][0])
        print(regcount, flush=True)

        sq_query="select count(distinct Crop) from cropdataset"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        ccount = int(data[0][0])
        print(ccount, flush=True)

        sq_query="select count(*) from cropdataset"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        dscount = int(data[0][0])
        print(dscount, flush=True)


        sq_query="select Sum(Profit)as aa from cropdataset group by Crop"
        cursor.execute(sq_query)
        data = cursor.fetchall()
        print("Query : "+str(sq_query), flush=True)
        print(data)
        gdata=[]
        if len(data)>0:
            gdata.append(round(data[0][0],2))
            gdata.append(round(data[1][0],2))
            gdata.append(round(data[2][0],2))
            gdata.append(round(data[3][0],2))
        print(gdata)
            
        #gdata = data
        print(gdata, flush=True)
        
        connection.commit() 
        connection.close()
        cursor.close()
        return render_template('dashboard.html',pplcount=rcount,regcount=regcount,ccount=ccount,dscount=dscount,gdata=gdata)
    except:
        print("No Data to be Displayed")
        return render_template('dashboard.html')

@app.route('/dataloader')
def dataloader():
    lat=0
    lon=0
    try:        
        g = geocoder.ip('me')
        lat=g.latlng[0]
        lon=g.latlng[1]
        print(g.latlng[0])
        print(g.latlng[1])
    except:
        print("Done")

    return render_template('dataloader.html',lat=lat,lon=lon)

@app.route('/dataloader1')
def dataloader1():
    return render_template('dataloader1.html')

@app.route('/banks')
def bank():
    '''return render_template('bank.html')'''
    loc = request.args['lon']
    long = loc[:5]
    uplon2=float(long)+0.02
    uplon1=float(long)+0.01
    dolon2=float(long)-0.02
    dolon1=float(long)-0.01
    print(loc)
    connection = mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    #sql_select_Query = "select * from bankdet where lon='"+long+"'"
    #sql_select_Query = "select * from bankdet where Lon LIKE '%"+long+"%' or Lon LIKE '%"+str(uplon2)+"%' or Lon LIKE '%"+str(uplon1)+"%' or Lon LIKE '%"+str(dolon1)+"%' or Lon LIKE '%"+str(dolon2)+"%'"
    sql_select_Query = "select * from bankdet where Branch LIKE '%Metagalli%'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()  
    
    return render_template('bank.html', data=data)

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/fd')
def fd():
    return render_template('interest.html')



@app.route('/cleardataset', methods = ['POST'])
def cleardataset():
    connection = mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    cursor = connection.cursor()
    query="delete from cropdataset"
    cursor.execute(query)
    connection.commit()      
    connection.close()
    cursor.close()
    return render_template('dataloader.html')

@app.route('/uploadajax', methods = ['GET','POST'])
def upldfile():
    resp='';
    print("request :"+str(request), flush=True)
    if request.method == 'GET':
        import nltk
        f = open("intent.json", "r")
        intentval=f.read()
        print('*****************************INTENTS LOADED*****************************')
        print(intentval)
        print('------------------------------------------------------------------------')
        
        #nltk.download()
        content=request.args['message']
        print("Entered Message :"+str(content))
        # Tokenizing sentences
        sentences = nltk.sent_tokenize(content)
        print("Sentences are : ")
        print(sentences)

        # Tokenizing words
        words = nltk.word_tokenize(content)
        print("Words are : ")
        print(words)

        msg=""
        resp = make_response(json.dumps(msg))
        
    return resp



@app.route('/planning')
def planning():
    connection = mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    sql_select_Query = "select * from cropdataset"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


   
    
    return render_template('planning.html', data=data)




@app.route('/forecast')
def forecast():
    g = geocoder.ip('me')
    print(g.latlng[0])
    print(g.latlng[1])
    print(g)
    
    abc=str(g[0])
    xyz=abc.split(', ')
    print(xyz[0][1:])
    print(xyz[1])
    loc=xyz[0][1:]+", "+xyz[1]
    connection = mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    sql_select_Query = "select * from cropdataset where Area='Nanjangud' and (DYear='2018' or DYear='2019')"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()  
    
    return render_template('forecast.html', data=data,glat=g.latlng[0],glon=g.latlng[1],curloc=loc)



@app.route('/locdata')
def locdata():
    cloc = request.args['loc']
    from  geopy.geocoders import Nominatim
    geolocator = Nominatim()
    city =cloc
    country ="India"
    loc = geolocator.geocode(city+','+ country)
    print("latitude is :-" ,loc.latitude,"\nlongtitude is:-" ,loc.longitude)
    lat=str(loc.latitude)
    lon=str(loc.longitude)
    #g = geocoder.ip('me')
    #print(g.latlng[0])
    #print(g.latlng[1])
    #print(g)
    
    #abc=str(g[0])
    #xyz=abc.split(', ')
    #print(xyz[0][1:])
    #print(xyz[1])
    loc=cloc+", "+country
    import datetime
    mydate = datetime.datetime.now()
    month=mydate.strftime("%B")
    connection = mysql.connector.connect(host='localhost',database='croppredflask',user='root',password='')
    #sql_select_Query = "select * from cropdataset where Area='"+cloc+"' and Month='"+month+"' and (DYear='2018' or DYear='2019')"
    sql_select_Query = "select * from cropdataset where Area='"+cloc+"' and (DYear='2018' or DYear='2019')"
    print(sql_select_Query)
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()  
    
    return render_template('forecast.html', data=data,glat=lat,glon=lon,curloc=loc)
    

@app.route('/ABCdata',methods=['GET'])
def procABC():
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    selVal = request.args['selected']
    
    print("Selected Val :"+str(selVal), flush=True)
    sql_select_Query=""

    if(selVal=='All'):
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset"
    else:
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset where Inv_Class='"+selVal+"'"

    
    print("Query :"+str(sql_select_Query), flush=True)

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


    A,B,C=getTilesdata1()
    A1,B1,C1=getTilesdata2()
    AC,BC,CC=getTilesdata3()
    X,Y,Z=getTilesdata4()
    xyzTot=X+Y+Z
    xper=X/xyzTot

    
    AX,AY,AZ,BX,BY,BZ,CX,CY,CZ=getHybridData()
    
    
    xper=xper*100;
    xper=round(xper)
    
    yper=Y/xyzTot
    yper=yper*100;
    yper=round(yper)
    
    zper=Z/xyzTot
    zper=zper*100;
    zper=round(zper)
    
    return render_template('planning.html', data=data,aval=A,bval=B,cval=C,aper=A1,bper=B1,cper=C1,X=X,Y=Y,Z=Z,xper=xper,yper=yper,zper=zper,AX=AX,AY=AY,AZ=AZ,BX=BX,BY=BY,BZ=BZ,CX=CX,CY=CY,CZ=CZ)



@app.route('/XYZdata',methods=['GET'])
def procXYZ():
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    selVal = request.args['selected1']
    
    print("Selected Val :"+str(selVal), flush=True)
    sql_select_Query=""

    if(selVal=='All'):
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset"
    else:
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset where XYZ_Class='"+selVal+"'"

    
    print("Query :"+str(sql_select_Query), flush=True)

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


    A,B,C=getTilesdata1()
    A1,B1,C1=getTilesdata2()
    AC,BC,CC=getTilesdata3()
    X,Y,Z=getTilesdata4()
    xyzTot=X+Y+Z
    xper=X/xyzTot


    
    AX,AY,AZ,BX,BY,BZ,CX,CY,CZ=getHybridData()
    
    xper=xper*100;
    xper=round(xper)
    
    yper=Y/xyzTot
    yper=yper*100;
    yper=round(yper)
    
    zper=Z/xyzTot
    zper=zper*100;
    zper=round(zper)
    
    return render_template('planning.html', data=data,aval=A,bval=B,cval=C,aper=A1,bper=B1,cper=C1,X=X,Y=Y,Z=Z,xper=xper,yper=yper,zper=zper,AX=AX,AY=AY,AZ=AZ,BX=BX,BY=BY,BZ=BZ,CX=CX,CY=CY,CZ=CZ)


@app.route('/HybridData',methods=['GET'])
def procHybrid():
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    selVal = request.args['selected2']
    
    print("Selected Val :"+str(selVal), flush=True)
    sql_select_Query=""

    if(selVal=='All'):
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset"
    else:
        sql_select_Query = "Select Item_desc,SUBSTRING(Part_desc,1,20),Inv_Class,XYZ_Class ,CONCAT(Inv_Class,XYZ_Class),Ceil(CAST(Q2 as Decimal(30))),Ceil(CAST(Q3 as Decimal(30))),Ceil(CAST(Q4 as Decimal(30))),Ceil(CAST(Q5 as Decimal(30))),Ceil(CAST(Q6 as Decimal(30))),Ceil(CAST(Q7 as Decimal(30))),Ceil(CAST(Q8 as Decimal(30))),Ceil(CAST(Q9 as Decimal(30))),round(CAST(Grand_Tot as Decimal(30))) from dataset where CONCAT(Inv_Class,XYZ_Class)='"+selVal+"'"

    
    print("Query :"+str(sql_select_Query), flush=True)

    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    data = cursor.fetchall()
    connection.close()
    cursor.close()


    A,B,C=getTilesdata1()
    A1,B1,C1=getTilesdata2()
    AC,BC,CC=getTilesdata3()
    X,Y,Z=getTilesdata4()

    
    AX,AY,AZ,BX,BY,BZ,CX,CY,CZ=getHybridData()
    
    xyzTot=X+Y+Z
    xper=X/xyzTot
    
    xper=xper*100;
    xper=round(xper)
    
    yper=Y/xyzTot
    yper=yper*100;
    yper=round(yper)
    
    zper=Z/xyzTot
    zper=zper*100;
    zper=round(zper)
    
    return render_template('planning.html', data=data,aval=A,bval=B,cval=C,aper=A1,bper=B1,cper=C1,X=X,Y=Y,Z=Z,xper=xper,yper=yper,zper=zper,AX=AX,AY=AY,AZ=AZ,BX=BX,BY=BY,BZ=BZ,CX=CX,CY=CY,CZ=CZ)


def create_plot(feature):
    if feature == 'Bar':
        N = 40
        x = np.linspace(0, 1, N)
        y = np.random.randn(N)
        df = pd.DataFrame({'x': x, 'y': y}) # creating a sample dataframe
        data = [
            go.Bar(
                x=df['x'], # assign x as the dataframe column 'x'
                y=df['y']
            )
        ]
    else:
        N = 1000
        random_x = np.random.randn(N)
        random_y = np.random.randn(N)

        # Create a trace
        data = [go.Scatter(
            x = random_x,
            y = random_y,
            mode = 'markers'
        )]


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
	



def create_forecastplot(feature):
    
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')   
    #connection = mysql.connector.connect(host='182.50.133.84',database='ascdb',user='ascroot',password='ascroot@123')  
    #sql_select_Query ="Select Prod_Val from category  where Description='Cold & Flu Tablets' order by Month asc"
    #"Select Q2,Q3,Q4,Q5,Q6,Q7,Q8,Q9,Forecasting from dataset where Part_desc='BIOCOOL 100-P 205 Ltrs Barrel' "

    ordered=[]
    consumed=[]
    sql_select_Query ="Select sum(Ordered_qty),sum(Cons_qty) from dataset1 where Mon='M03' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    ordered.append(records[0][0])
    consumed.append(records[0][1])

    
    sql_select_Query ="Select sum(Ordered_qty),sum(Cons_qty) from dataset1 where Mon='M02' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    ordered.append(records[0][0])
    consumed.append(records[0][1])

    
    sql_select_Query ="Select sum(Ordered_qty),sum(Cons_qty) from dataset1 where Mon='M01' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    ordered.append(records[0][0])
    consumed.append(records[0][1])

    
        
    x=["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
    ordy=[21422,20437,19737,19327,21422,20437,19737,19327,20111,ordered[2],ordered[1],ordered[0]]
    consy=[20422,21437,20737,19827,20422,21437,18737,20327,20221,consumed[2],consumed[1],consumed[0]]
    #x=["Q2","Q3","Q4","Q5","Q6","Q7","Q8","Q9","Forecasting"]
    ##y=[]
    #y=[22,33,44,88,55,66,22,33,44,88,55,66]
	
    #print("Y Axis :"+str(y), flush=True)

    
    ##for r in records:
        #row = cursor.fetchone()
        ##print(r, flush=True)
        ##y.append(int(r[0])*1000)
        
    ##print("Y Axis :"+str(y), flush=True)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=ordy, mode='lines+markers',   name='lines+markers'))
    fig.add_trace(go.Scatter(x=x, y=consy, mode='lines+markers',   name='lines+markers'))
    #fig.update_layout(title='Order v/s Consumption',width=1000,xaxis_title='Month',yaxis_title='Count')
    #fig.update_layout(plot_bgcolor='rgba(192,192,192,1)',width=1000,xaxis=dict(title='Count'),yaxis=dict(title='Month'),)


    #data=[go.Scatter(x=x, y=y)],layout = go.Layout(xaxis=dict(title='Count'),yaxis=dict(title='Month'))
    ##fig = go.Figure(data=[go.Scatter(x=x, y=y)],layout=go.Layout(plot_bgcolor='rgba(192,192,192,1)',width=1000,xaxis=dict(title='Count'),yaxis=dict(title='Month'),))
    fig.update_xaxes(zeroline=True, zerolinewidth=2, zerolinecolor='white',showgrid=True, gridwidth=1, gridcolor='white')
    fig.update_yaxes(zeroline=True, zerolinewidth=4, zerolinecolor='white',showgrid=True, gridwidth=1, gridcolor='white')
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON,ordy,consy


#from dataset where CONCAT(Inv_Class,XYZ_Class)='"+selVal+"'	


def getTilesdata1():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')         
    sql_select_Query = "Select count(*) from cpsoilinfo Group By SoilName"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][0]
    
    print("A Val :"+str(aval), flush=True)

    
    sql_select_Query = "Select count(*) from cpsoilinfo Group By CropInfo"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    bval=records[0][0]
    print("B Val :"+str(bval), flush=True)
    
    
    sql_select_Query = "Select count(*) from cpsoilinfo Group By Location"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    cval=records[0][0]
    print("C Val :"+str(cval), flush=True)



    
    connection.close()
    cursor.close()   

    return aval,bval,cval



def getHybridData():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    
    #from dataset where CONCAT(Inv_Class,XYZ_Class)='"+selVal+"'
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='AX'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    AX=records[0][0]
    

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='AY'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    AY=records[0][0]
    
    
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='AZ'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    AZ=records[0][0]

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='BX'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    BX=records[0][0]
    

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='BY'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    BY=records[0][0]
    
    
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='BZ'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    BZ=records[0][0]


    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='CX'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    CX=records[0][0]
    

    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='CY'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    CY=records[0][0]
    
    
    sql_select_Query = "Select count(*) from dataset where CONCAT(Inv_Class,XYZ_Class)='CZ'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    CZ=records[0][0]
    
   


    
    connection.close()
    cursor.close()   

    return AX,AY,AZ,BX,BY,BZ,CX,CY,CZ



	
def getTilesdata2():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')

    sql_select_Query = "Select count(*) from dataset"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    tval=records[0][0]

    
    sql_select_Query = "Select count(Inv_Class) from dataset where Inv_Class='A'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][0]
    aval=aval/tval
    aval=aval*100;
    aval=round(aval)
    
    print("A % :"+str(aval), flush=True)

    
    sql_select_Query = "Select count(Inv_Class) from dataset where Inv_Class='B'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    bval=records[0][0]
    bval=bval/tval
    bval=bval*100;
    bval=round(bval)
    
    print("B % :"+str(bval), flush=True)
    
    
    sql_select_Query = "Select count(Inv_Class) from dataset where Inv_Class='C'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    cval=records[0][0]
    cval=cval/tval
    cval=cval*100;
    cval=round(cval)
    
    print("C % :"+str(cval), flush=True)



    
    connection.close()
    cursor.close()   

    return aval,bval,cval	
	




	
def getTilesdata3():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    
    sql_select_Query = "Select sum(Grand_Tot) from dataset where Inv_Class='A'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][0]
    aval=round(aval,2)
    
    
    sql_select_Query = "Select sum(Grand_Tot) from dataset where Inv_Class='B'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    bval=records[0][0]
    bval=round(bval,2)
    
    
    
    sql_select_Query = "Select sum(Grand_Tot) from dataset where Inv_Class='C'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    cval=records[0][0]
    cval=round(cval,2)
    
    
    connection.close()
    cursor.close()   

    return aval,bval,cval	
	


def getTilesdata4():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')         
    sql_select_Query = "Select count(XYZ_Class) from dataset where XYZ_Class='X'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    xval=records[0][0]
    

    
    sql_select_Query = "Select count(XYZ_Class) from dataset where XYZ_Class='Y'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    yval=records[0][0]
    
    
    sql_select_Query = "Select count(XYZ_Class) from dataset where XYZ_Class='Z'"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    zval=records[0][0]
    
    connection.close()
    cursor.close()   

    return xval,yval,zval



def getdbTilesdata4():        
    connection = mysql.connector.connect(host='localhost',database='croppreddb',user='root',password='')
    mdata=[]


    
    sql_select_Query = "Select sum(Total_cost) from dataset1 where Mon='M03' and Qtr='Q9'"    
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    mdata.append(records[0][0])
    

    
    sql_select_Query = "Select sum(Total_cost) from dataset1 where Mon='M02' and Qtr='Q9'"   
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    mdata.append(records[0][0])
    
    sql_select_Query = "Select sum(Total_cost) from dataset1 where Mon='M01' and Qtr='Q9'"   
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    mdata.append(records[0][0])
    
    connection.close()
    cursor.close()   
    print("Month Data :"+str(mdata), flush=True)

    return mdata
	

def create_category():        
    #connection = mysql.connector.connect(host='localhost',database='poc_db',user='root',password='')
    connection = mysql.connector.connect(host='182.50.133.84',database='croppreddb',user='ascroot',password='ascroot@123')        
    sql_select_Query = "Select distinct xyz,count(xyz) from datavalues group by xyz order by xyz asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    xval=records[0][1]
    yval=records[1][1]
    zval=records[2][1]
    connection.close()
    cursor.close()
    if feature == 'All':
        labels = ['X','Y','Z']
        values = [xval, yval, zval]
        data=[go.Pie(labels=labels, values=values)]        
    elif feature == 'X':
        labels = ['X']
        values = [xval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'Y':
        labels = ['Y']
        values = [yval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'Z':
        labels = ['Z']
        values = [zval]
        data=[go.Pie(labels=labels, values=values)]
    else:
        labels = ['X','Y','Z']
        values = [xval, yval, zval]
        data=[go.Pie(labels=labels, values=values)] 


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

def create_geography():
    connection = mysql.connector.connect(host='182.50.133.84',database='croppreddb',user='ascroot',password='ascroot@123')   
    sql_select_Query = "Select distinct abc,count(abc) from datavalues group by abc order by abc asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    aval=records[0][1]
    bval=records[1][1]
    cval=records[2][1]
    connection.close()
    cursor.close()
    if feature == 'All':
        labels = ['A','B','C']
        values = [aval, bval, cval]
        data=[go.Pie(labels=labels, values=values)]        
    elif feature == 'A':
        labels = ['A']
        values = [aval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'B':
        labels = ['B']
        values = [bval]
        data=[go.Pie(labels=labels, values=values)]
    elif feature == 'C':
        labels = ['C']
        values = [cval]
        data=[go.Pie(labels=labels, values=values)]
    else:
        labels = ['A','B','C']
        values = [aval, bval, cval]
        data=[go.Pie(labels=labels, values=values)] 


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON
	

def create_moving(feature):
    connection = mysql.connector.connect(host='182.50.133.84',database='croppreddb',user='ascroot',password='ascroot@123')   
    sql_select_Query = "Select distinct fsn,count(fsn) from datavalues group by fsn order by fsn asc"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()
    fval=records[0][1]
    nval=records[1][1]
    sval=records[2][1]
    connection.close()
    cursor.close()
    if feature == 'All':
        labels = ['F','N','S']
        values = [fval, nval, sval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]        
    elif feature == 'F':
        labels = ['F']
        values = [fval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]
    elif feature == 'S':
        labels = ['S']
        values = [sval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]
    elif feature == 'N':
        labels = ['N']
        values = [nval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]
    else:
        labels = ['F','N','S']
        values = [fval, nval, sval]
        data=[go.Pie(labels=labels, values=values, hole=.3)]   


    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON

@app.route('/bar', methods=['GET', 'POST'])
def change_features():

    feature = request.args['selected']
    graphJSON= create_plot(feature)




    return graphJSON
	
@app.route('/xyz', methods=['GET', 'POST'])
def change_features1():

    feature = request.args['selected']
    graphJSON= create_xyzplot(feature)




    return graphJSON


@app.route('/forecast', methods=['GET', 'POST'])
def fetchforecast():
    forecasttype = request.args['selected']
    graphJSON,oy,cy= create_forecastplot(forecasttype)
    return graphJSON
	

if __name__ == '__main__':
    UPLOAD_FOLDER = 'D:/Upload'
    app.secret_key = "secret key"
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run()
