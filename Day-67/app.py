import sqlite3

from flask import Flask, render_template, redirect, url_for
from flask_bootstrap import Bootstrap
import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, URL
from flask_ckeditor import CKEditor, CKEditorField
from sqlite3 import *

tdy = datetime.datetime.now()
date = tdy.strftime("%m/%d/%Y")
print(date)

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
test = "CREATE TABLE blog_post (id INTEGER PRIMARY KEY, title varchar(250) NOT NULL, date VARCHAR(250) NOT NULL ,body varchar(250) NOT NULL ,author VARCHAR(250) NOT NULL ,img_url VARCHAR(250) NOT NULL ,subtitle VARCHAR(250))"
db = sqlite3.connect("posts.db", check_same_thread=False)
cursor = db.cursor()

# cursor.execute(test)
# db = sqlite3.connect("posts.db", check_same_thread=False)
##CONFIGURE TABLE

res = cursor.execute("SELECT * FROM blog_post")

lst_post = []
for all_post in res:
    lst_post.append(all_post)


##WTForm
class CreatePostForm(FlaskForm):
    title = StringField("Blog Post Title", validators=[DataRequired()])
    subtitle = StringField("Subtitle", validators=[DataRequired()])
    author = StringField("Your Name", validators=[DataRequired()])
    img_url = StringField("Blog Image URL", validators=[DataRequired(), URL()])
    body = CKEditorField('Body', validators=[DataRequired()])
    submit = SubmitField("Submit Post")


@app.route("/new-post", methods=["GET", "POST"])
def create_blog_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        blog_date = date
        body = form.body.data
        author = form.author.data
        img = form.img_url.data
        sql = '''INSERT INTO blog_post(title,date, body,author, img_url,subtitle) VALUES(?,?,?,?,?,?)'''
        new_posts = title, blog_date, body, author, img, subtitle
        cursor.execute(sql, new_posts)
        db.commit()
    return render_template("make-post.html", form=form)


@app.route('/')
def get_all_posts():
    return render_template("index.html", post=lst_post)


@app.route("/post/<int:index>")
def show_post(index):
    if index == lst_post[0]:
        print(lst_post)
    return render_template("post.html", post=lst_post[index - 1])


@app.route("/edit-post/<int:index>", methods=["GET", "POST"])
def edit_post(index):
    edit_posts = lst_post[index - 1]
    edit_form = CreatePostForm(title=edit_posts[1], body=edit_posts[3], author=edit_posts[4], img_url=edit_posts[5],
                               subtitle=edit_posts[6])
    if edit_form.validate_on_submit():
        titles = edit_form.title.data
        body = edit_form.body.data
        author = edit_form.author.data
        img_url = edit_form.img_url.data
        subtitle = edit_form.subtitle.data
        sql = '''UPDATE blog_post set title=?, body=?, author=?, img_url=?,subtitle=?'''
        edit_data = (titles, body, author, img_url, subtitle)
        cursor.execute(sql, edit_data)
        db.commit()
        return render_template("index.html")
    return render_template("make-post.html", form=edit_form)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


if __name__ == "__main__":
    app.run()
