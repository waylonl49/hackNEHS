from flask import Flask, redirect, url_for, render_template, request
import pickle

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))


@app.route("/")
def homepage():
    return render_template("index.html")

@app.route("/height")
def height():
    return render_template("height.html")

@app.route('/predictheight', methods=["POST", "GET"])
def heightpredictions():
    momheight = request.form['mother']
    dadheight = request.form['father']
    gender = ""
    if request.form.get('Malegender'):
        gender = 'Male'
    
    elif request.form.get('Femalegender'):
        gender = 'Female'

    momheight = int(momheight)
    dadheight = int(dadheight)

    predheight = 0

    predheight += momheight+dadheight
    if gender == 'Male':
        predheight += 5
    elif gender == 'Female':
        predheight -=5
    
    predheight /= 2

    return render_template('predictheight.html', predheight=f'Your predicted height is {predheight} inches', mheight=momheight, fheight=dadheight)


@app.route("/lungcancer")
def age():
    return render_template("lungcancer.html")

@app.route("/lungcancerprediction", methods=["POST", "GET"])
def lungcancerprediction():
    age = request.form["Age"]
    age = int(age)
    newsmoke = ''
    newalcohol = ''
    newfamily = ''
    newdiet = ''

    total = 0

    if request.form.get("Yess"):
        total += 1
        newsmoke = 'Yes'
    else:
        newsmoke = 'No'
    
    if request.form.get("Yesalc"):
        total += 1
        newalcohol = "Yes"
    else:
        newalcohol = 'No'
        
    if request.form.get("Yeslc"):
        total += 1
        newfamily = "Yes Family History"
    else:
        newfamily = 'No Family History'

    if request.form.get("Yesd"):
        
        newdiet = 'Healthy Diet'
    else:
        total +=1
        newdiet = "Unhealthy Diet"
    
    print(total)
    print(age)

    if total >= 3 and age >= 55:
        return render_template("truelungcancer.html", 
        age=age,
        newsmoke=newsmoke,
        newalcohol=newalcohol,
        newfamily=newfamily,
        newdiet=newdiet)

    else:
        return render_template("falselungcancer.html", 
        age=age,
        newsmoke=newsmoke,
        newalcohol=newalcohol,
        newfamily=newfamily,
        newdiet=newdiet)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/cardio")
def cardio():
    return render_template("cardio.html")

@app.route("/covid19")
def covid():
    return render_template("covid19.html")

@app.route("/predictcardio", methods=["POST", "GET"])
def predictcar():
    if request.method == 'POST':
        age = request.form['Age']
        height = request.form['Height']
        weight = request.form['Weight']
        gender = request.form['Gender']
        cholesterol = request.form['Cholesterol']
        glucose = request.form['Glucose']
        smoke = 0
        alcohol = 0
        active = 0
        
        if request.form.get('Yess'):
            smoke = 1
        else:
            smoke = 0
        
        if request.form.get('Yesalc'):
            alcohol = 1
        else:
            alcohol = 0

        if request.form.get('Yesa'):
            active = 1
        else:
            active = 0
        
        age = int(age) *365
        height = int(round(int(height) * 2.54))
        weight = float(int(weight) / 2.205)
        gender = int(gender)
        cholesterol = int(cholesterol)
        glucose = int(glucose)
        newg = ""
        newc = ""
        newglu = ""
        newsm = ""
        newalc = ""
        newact = ""

        if gender == 2:
            newg = "Male"
        else:
            newg = "Female"

        if cholesterol == 1:
            newc = "Normal"
        elif cholesterol == 2:
            newc = "Above Average"
        else:
            newc = "Abnormal"

        if glucose == 1:
            newglu = "Normal"
        elif glucose == 2:
            newglu = "Above Average"
        else:
            newglu = "Abnormal"

        
        if smoke == 0:
            newsm = "No"
        elif smoke == 1:
            newsm = "Yes"

        if alcohol == 0:
            newalc = "No"
        elif alcohol == 1:
            newalc = "Yes"

        if active == 0:
            newact = "No"
        elif active == 1:
            newact = "Yes"

        arr = [age, gender, height, weight, cholesterol, glucose, smoke, alcohol, active]
        print(arr)
        prediction = model.predict([arr])

        output = int(prediction[0])

        if output == 1:
            return render_template('falsecardio.html',
            age = f"{int(age/356)}",
            height = f"{int(height/2.54)} inches",
            weight= f"{round(weight*2.205)} pounds",
            gender = newg,
            cholesterol = newc,
            glucose=newglu,
            smoke = newsm,
            alcohol = newalc,
            active=newact)
        elif output == 0:
            return render_template('truecardio.html',
            age = f"{int(age/356)}",
            height = f"{int(height/2.54)} inches",
            weight= f"{round(weight*2.205)} pounds",
            gender = newg,
            cholesterol = newc,
            glucose=newglu,
            smoke = newsm,
            alcohol = newalc,
            active=newact)
           
@app.route('/predictcovid', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        total = 0
        if request.form.get('Tfever'):
            total +=1       

        if request.form.get('Ttired'):
            total +=1
       
        if request.form.get('Tcough'):
            total +=1

        if request.form.get('Tbreathing'):
            total +=1

        if request.form.get('Tsore'):
            total +=1

        if request.form.get('Tpain'):
            total +=1
        
        if request.form.get('Tnasal'):
            total +=1    
        
        if request.form.get('Trunny'):
            total +=1

        print(total)

        if total >= 6:
            return render_template('predictcovid.html', covidp='You likely have coronavirus. Stay at home and do not expose yourself to other people to prevent the spread of the virus.', source='https://npr.brightspotcdn.com/dims4/default/4c7b997/2147483647/strip/true/crop/1500x1000+0+0/resize/880x587!/quality/90/?url=http%3A%2F%2Fnpr-brightspot.s3.amazonaws.com%2Flegacy%2Fsites%2Fkwmu%2Ffiles%2F202003%2F032920_DK_CovidStayHome.png')
        elif total <6:
            return render_template('predictcovid.html', covidn='You have a very low chance of having coronavirus. However, still be safe and make sure to wear a mask when going outdoors.', source='https://www.redcross.org/content/dam/redcross/about-us/news/2020/coronavirus-safety-tw.jpg')

if __name__ == "__main__":
    app.run(debug=True)