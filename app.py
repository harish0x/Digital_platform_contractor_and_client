from flask import Flask, render_template, request, session, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import json

import os
from werkzeug.utils import secure_filename
app = Flask(__name__)

type_user = 'client'
type_user1= 'builder'
UPLOAD_FOLDER = '/home/harishankar/test2/uploader'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


app = Flask(__name__)
app.secret_key = 'your_secret_key'

# MongoDB connection
client = 
db = client['construction_site']


# Module 1: Welcome page - Login or Registration
@app.route('/')
def index():
    return render_template('index.html')
@app.route('/register')
def register():
    return render_template('register.html')


# Module 2: Registration page
@app.route('/client-registration', methods=['GET', 'POST'])
def client_registration():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        password = request.form['password']
        phone_no = request.form['phone_no']
        telephone_no = request.form['telephone_no']
        
        client_data = {
            'name': name,
            'username': username,
            'password': password,
            'phone_no': phone_no,
            'telephone_no': telephone_no,
            'user_type' : type_user
        }
        
        db.client_registration.insert_one(client_data)
        return redirect('/login')
    
    return render_template('client_registration.html')


# Builder Registration Page
@app.route('/builder-registration', methods=['GET', 'POST'])
def builder_registration():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        services_provided = request.form['services_provided']
        gstin = request.form['gstin']
        address = request.form['address']
        
        builder_data = {
            'username': name,
            'password': password,
            'services_provided': services_provided,
            'gstin': gstin,
            'address': address,
            'user_type' : type_user1
        }
        
        db.builder_registration.insert_one(builder_data)
        return redirect('/login')
    
    return render_template('builder_registration.html')
# Module 3: Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


@app.route('/client-login', methods=['GET', 'POST'])
def client_login():

    if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            # Check if the user exists in the client registration collection
            client_user = db.client_registration.find_one({'username': username, 'password': password})
            if client_user:
                session['username'] = username
                session['user_type'] = 'client'
                return redirect('/client-dashboard')
    return render_template('client_login.html')

@app.route('/client-home')
def client_home():
    return render_template('client_home.html')


@app.route('/builder-home')
def builderhome():
    return render_template("builder_home.html")



@app.route('/builder-login', methods=['GET', 'POST'])
def builder_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        builder_user = db.builder_registration.find_one({'username': username, 'password': password})
        if builder_user:
            session['username'] = username
            session['user_type'] = 'builder'
            return redirect('/builder-dashboard')

        return "Invalid username or password"
    return render_template('builder_login.html')

@app.route('/client-dashboard', methods=['GET', 'POST'])
def client_dashboard():
    if 'username' in session and session['user_type'] == 'client':
        if request.method == 'POST':
            building_id = request.form['building_id']
            name = request.form['building_name']
            building_type = request.form['building_type']
            dimension = request.form['dimension']
            num_floors = request.form['num_floors']
            building_area = request.form['building_area']
            description = request.form['description']
            address = request.form['address']

            building_data = {
                'building_id': building_id,
                'name': name,
                'building_type': building_type,
                'dimension': dimension,
                'num_floors': num_floors,
                'building_area': building_area,
                'description': description,
                'address': address
            }

            db.building_data.insert_one(building_data)
            
        return render_template('client_dashboard.html')
    else:
        return redirect('/login')





'''@app.route('/builder-dashboard' ,methods=['GET', 'POST'])
def builder_dashboard():
        building_data = db.building_data.find()
        return render_template('builder.html', building_data=building_data)'''

@app.route('/builder-dashboard', methods=['GET', 'POST'])
def builder_dashboard():
    if request.method == 'POST':
        id = request.form['id']
        building_data = db.building_data.find_one({'building_id': id})
        if building_data:
            return render_template('builder.html', building_data=building_data)
        else:
            return render_template('builder.html', error="Building not found.")
    else:
        return render_template('builder.html')

def allowed_file(filename):
    allowed_extensions = {'jpg', 'jpeg', 'png', 'gif'}
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions



@app.route('/status', methods=['GET', 'POST'])
def status():
        if request.method == 'POST':
            status_text = request.form['status_text']
            status_image = request.files['status_image']
            building_id = request.form['building_id']

            # Update building status in the database
            '''
            db.building_data.update_one(
                {'_id':ObjectId(building_id)},
                {'$set': {'status_text': status_text, 'status_image': filename}}
            )'''
            print(building_id)
            db.building_status.insert_one({'building_id': building_id, 'status_text': status_text, 'status_image': status_image.filename})


            return redirect('/builder-dashboard')

        building_data = db.building_data.find()
        return render_template('status.html', building_data=building_data)
        return redirect('/login')

@app.route('/show-status/', methods=['GET'])
def show_status():
    status_data = list(db.building_status.find())
    status_data = list(db.building_status.find())
    for data in status_data:
        image_id = data.get('status_image')
        if image_id:
            image_data = db.images.find_one({'_id': image_id})
            if image_data:
                image = image_data.get('image', None)
                data['status_image'] = image
    print(status_data)
    return render_template('show_status.html', building_data=status_data)

'''@app.route('/build-status/', methods=['GET'])
def show_status():
    status_data = list(db.building_status.find())
    status_data = list(db.building_status.find())
    for data in status_data:
        image_id = data.get('status_image')
        if image_id:
            image_data = db.images.find_one({'_id': image_id})
            if image_data:
                image = image_data.get('image', None)
                data['status_image'] = image
    print(status_data)
    return render_template('build-status.html', building_data=status_data)
'''
@app.route('/your-projects', methods=['GET', 'POST'])
def your_projects():
    if 'username' in session and session['user_type'] == 'client':
        #building_id = request.form['building_id']

        print(session['username'])
        building_data = db.building_data.find()
        return render_template('your_projects.html',projects=building_data)
    else:
        return redirect('/login')

@app.route('/shows', methods=['GET', 'POST'])
def show():
    with open("file_name.json", "r") as f:
        data = json.load(f)
        items = []

        for item in data:
            position = item['position']
            title = item['title']
            place_id = item['place_id']
            data_id = item['data_id']
            data_cid = item['data_cid']
            reviews_link = item['reviews_link']
            photos_link = item['photos_link']
            gps_coordinates = item['gps_coordinates']
            place_id_search = item['place_id_search']
            rating = item['rating']
            reviews = item['reviews']
            item_type = item['type']
            address = item['address']
            open_state = item['open_state']
            hours = item['hours']
            operating_hours = item['operating_hours']
            #phone = item['phone']
            #service_options = item['service_options']
            thumbnail = item['thumbnail']

            item_dict = {
                'position': position,
                'title': title,
                'place_id': place_id,
                'data_id': data_id,
                'data_cid': data_cid,
                'reviews_link': reviews_link,
                'photos_link': photos_link,
                'gps_coordinates': gps_coordinates,
                'place_id_search': place_id_search,
                'rating': rating,
                'reviews': reviews,
                'item_type': item_type,
                'address': address,
                'open_state': open_state,
                'hours': hours,
                'operating_hours': operating_hours,
                #'phone': phone,
                #'service_options': service_options,
                'thumbnail': thumbnail
            }

            items.append(item_dict)
            #print(items)


        return render_template('show.html', items=items)


    
    
# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')





























































if __name__ == '__main__':
    app.run(debug=True)
