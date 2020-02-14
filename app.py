import os, random, flask_sijax
from flask import Flask, request, render_template, g, redirect, url_for, send_from_directory
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from itsdangerous import URLSafeTimedSerializer
from randomPicture import RandomPicture

from forms import SignupForm, LoginForm
from database import db, dbPictures
from models import User, Picture

from flask_mail import Mail, Message
from aws_upload import upload_file_to_s3, S3_LOCATION, S3_SECRET, S3_KEY, S3_BUCKET

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

path = os.path.join('.', os.path.dirname(__file__), 'static/js/sijax/')
SECRET_KEY = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

app = Flask(__name__)
app.config['SIJAX_STATIC_PATH'] = path
app.config['SIJAX_JSON_URI'] = '/static/js/sijax/json2.js'
flask_sijax.Sijax(app)  

app.secret_key = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://xzjjjptliolldc:f952f5ebe57b62a95d137b0811203a843b5e2b1d38619736cc2dfffa65424ca8@ec2-107-20-224-137.compute-1.amazonaws.com:5432/de6jpcsf9jd7hm'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

ts = URLSafeTimedSerializer(app.secret_key) #instance of URLSafeTimedSerializer class

# initialize database
def init_db():
    db.init_app(app)
    dbPictures.init_app(app)
    db.app = app
    dbPictures.app = app
    # db.create_all()
    # dbPictures.create_all()

    # dbPictures.session.add(newpic)
    # dbPictures.session.commit()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# initialize mail
mail = Mail(app)  # instantiation of mail

app.config.update(
    DEBUG=True,
    #email settings
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=465,
    MAIL_USE_SSL=True,
    MAIL_USERNAME='greenboxMIT@gmail.com',
    MAIL_PASSWORD='greenbox2017'
    )

mail = Mail(app)  #confirm updates


def send_email(to, subject, contents):
    msg = Message(
        sender='greenboxMIT@gmail.com',
        subject=subject,
        recipients=[to],
        html=contents,
    )

    msg.body = "This is the email body"
    mail.send(msg)


# tests emailing works
@app.route("/email")
def basic_email():
    msg = Message(
        'Hello',
        sender='greenboxMIT@gmail.com',
        recipients=['jedrbox@gmail.com'])
    msg.body = "This is the email body"
    mail.send(msg)
    return "Sent"


# welcome page
@app.route("/")
def main():
    return render_template('welcome.html')


# main site
@flask_sijax.route(app, '/main')
def site():

    currentPic = RandomPicture()

    def share(obj_response):
        obj_response.alert(currentPic.url)

    def new_photo(obj_response):
        # validImages = [x for x in os.listdir('static/MAIN/') if x[0] != "."]
        # randomImage = random.choice(validImages)

        currentPic.randomize()

        obj_response.html('#randomLikes', currentPic.likes)
        obj_response.html('#randomImg', '<img id = "randomImg" src = {}>'.format(currentPic.url))
        obj_response.html('#randomTxt', currentPic.txt)

    def upvote(obj_response):
        user = current_user
        picUrl = currentPic.getUrl()
        picture = Picture.query.filter_by(url=currentPic.url).first()

        if picUrl not in user.picsLiked:

            if picUrl in user.picsUnliked:
                newLike = int(picture.likes) + 2

            else:
                newLike = int(picture.likes) + 1

            picture.likes = newLike

            user.appendLikedPics(picUrl)

        elif picUrl in user.picsLiked:

            newLike = int(picture.likes) - 1
            picture.likes = newLike
            user.removeFromLikedPics(picUrl)

        obj_response.html('#randomLikes', picture.likes)
        db.session.commit()
        dbPictures.session.commit()

    def downvote(obj_response):
        user = current_user
        picUrl = currentPic.getUrl()
        picture = Picture.query.filter_by(url=currentPic.url).first()

        if picUrl not in user.picsUnliked:

            if picUrl in user.picsLiked:
                newLike = int(picture.likes) - 2

            else:
                newLike = int(picture.likes) - 1

            picture.likes = newLike

            user.appendUnlikedPics(picUrl)

        elif picUrl in user.picsUnliked:

            newLike = int(picture.likes) + 1
            picture.likes = newLike
            user.removeFromUnlikedPics(picUrl)

        obj_response.html('#randomLikes', picture.likes)
        db.session.commit()
        dbPictures.session.commit()

    if g.sijax.is_sijax_request:
        # Sijax request detected - let Sijax handle it
        g.sijax.register_callback('new_photo', new_photo)
        g.sijax.register_callback('like_photo', upvote)
        g.sijax.register_callback('unlike_photo', downvote)
        g.sijax.register_callback('share_photo', share)
        return g.sijax.process_request()

    return render_template('main.html',
                           randomPictureUrl=currentPic.getUrl(),
                           randomPictureText=currentPic.getTxt(),
                           randomPictureLikes=currentPic.getLikes())


@login_required
@app.route('/change', methods=['GET', 'POST'])
def change():

    user = current_user
    print(user.username)

    if request.method == 'GET':
        return render_template('upload.html')

    elif request.method == 'POST':
        if "user_file" not in request.files:
            return "No user_file key in request.files"

        file = request.files["user_file"]

        if file.filename == "":
            return "Please select a file"

        if file and allowed_file(file.filename):
            file.filename = user.username + '.' + file.filename.rsplit('.', 1)[1].lower()

            output = upload_file_to_s3(file, S3_BUCKET)
            user.profilePicUrl = str(output)
            db.session.commit()
            return redirect("/account/{}".format(user.username))

        else:
            return redirect("/change")


@flask_sijax.route(app, '/about')
def about():
    return render_template('about.html')


@flask_sijax.route(app, '/contact')
def contact():
    return render_template('contact.html')


@app.route("/account/<username>")
def account(username):

    user = User.query.filter_by(username=username).first_or_404()

    return render_template('profile.html',
                           name=user.name,
                           lastname=user.lastname,
                           username=user.username,
                           picsLiked=user.getPicsLikes(),
                           picsUnliked=user.getPicsUnlikes(),
                           profilePicUrl=user.profilePicUrl)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)

    elif request.method == 'POST':

        if form.validate():
            if User.query.filter_by(email=form.email.data).first():
                return "Email address already exists"
            if User.query.filter_by(username=form.username.data).first():
                return "username already exists"
            else:
                newuser = User(email=form.email.data,
                               password=form.password.data,
                               username=form.username.data,
                               name=form.name.data,
                               lastname=form.lastname.data
                               )
                db.session.add(newuser)
                db.session.commit()
                login_user(newuser)

                subject = "Confirm your email"

                token = ts.dumps(form.email.data, salt='email-confirm-key')

                confirm_url = url_for(
                    'confirm_email',
                    token=token,
                    _external=True)

                html = render_template(
                    'activate.html',
                    confirm_url=confirm_url)

                send_email(newuser.email, subject=subject, contents=html)
                return "User created!!! check {}".format(newuser.email)
        else:
            return "Form didn't validate"


@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        #load confirm key with age of 86400 seconds or 24 hours
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)

    except:
        return "Error. Token expired."

    user = User.query.filter_by(email=email).first_or_404()
    user.email_confirmed = True

    db.session.add(user)
    db.session.commit()

    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if request.method == 'GET':
        return render_template('login.html', form=form)
    elif request.method == 'POST':
        print(form.data)
        if form.validate_on_submit():
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                if user.password == form.password.data:
                    login_user(user)
                    return redirect(url_for('site'))

                else:
                    return "Wrong password"
            else:
                return "user doesn't exist"
    else:
        return "form not validated"


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('site'))


@app.route("/in")
def extension():
    return render_template('child.html')


@app.route('/protected')
@login_required
def protected():
    return "protected area"


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).first()

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.ico', mimetype='image/png')


init_db()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
