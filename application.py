from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
from functools import wraps

app = Flask(__name__)

app.config['SECRET_KEY'] = "abcdefgh"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))


@app.route("/")
def login_home():
    return render_template("login.html")


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message' : 'Token is missing !!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query \
                .filter_by(public_id=data['public_id']) \
                .first()
        except:
            return jsonify({'message' : 'Token is invalid !!'}), 401
        return f(current_user, *args, **kwargs)

    return decorated


@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):
    users = User.query.all()
    output = []
    for user in users:
        output.append({
            'public_id': user.public_id,
            'name': user.name,
            'email': user.email
        })
    return jsonify({'users': output})

map = {}

@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    print(auth)
    if not auth or not auth.get('email') or not auth.get('password'):
        msg = f"User {auth.get('email')} does not exist !!!"
        return render_template("login.html", msg=msg)
        # return make_response(
        #     'Could not verify1',
        #     401,
        #     {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        # )

    user = User.query \
            .filter_by(email=auth.get('email')) \
            .first()

    if not user:
        msg = f"User {auth.get('email')} does not exist !!!"
        return render_template("login.html", msg=msg)
        # return f"<h3>User {auth.get('email')} does not exits, Please enter valid user details</h3>"
            # returns 401 if user does not exist
            # return make_response(
            #     'Could not verify2',
            #     401,
            #     {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
            # )

    if check_password_hash(user.password, auth.get('password')):
            # generates the JWT Token
            token = jwt.encode({
                'public_id': user.public_id,
                'exp': datetime.utcnow() + timedelta(minutes=30)
            }, app.config['SECRET_KEY'])

            data = make_response(jsonify({'token': token.decode('UTF-8')}), 201)
            map[user.email] = data.json["token"]

            print(data.json["token"])
            return data
        # returns 403 if password is wrong
    msg = f"User {auth.get('email')} does not exist !!!"
    return render_template("login.html", msg=msg)
    # return make_response(
    #         'Could not verify3',
    #         403,
    #         {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    #     )


@app.route('/register', methods=['GET'])
def register():
    return render_template("register.html")


@app.route('/signup', methods=['POST'])
def signup():
    # creates a dictionary of the form data
    data = request.form
    print(data)
    # gets name, email and password
    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    # checking for existing user
    user = User.query \
        .filter_by(email=email) \
        .first()
    if not user:
        # database ORM object
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        # insert user
        db.session.add(user)
        db.session.commit()
        return render_template("login.html")
        # return make_response('Successfully registered.', 201)
    else:
        # returns 202 if user already exists
        return make_response('User already exists. Please Log in.', 202)


if __name__ == "__main__":
    # setting debug to True enables hot reload
    # and also provides a debugger shell
    # if you hit an error while running the server
    app.run(debug=True)