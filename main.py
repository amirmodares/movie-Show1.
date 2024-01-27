from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import requests

API_KEY = "4696c85a8e3baedc5cabe604b9198b7e"
URL = "https://api.themoviedb.org/3/search/movie"


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///movie-collections.db'
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
db = SQLAlchemy(app)
app.app_context().push()
Bootstrap(app)


class LoginForm(FlaskForm):
    movie_rating = StringField("Your Rating", validators=[DataRequired()])
    movie_review = StringField("Your Review", validators=[DataRequired()])
    submit = SubmitField(label="Done")


class AddForm(FlaskForm):
    movie_title = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField(label="Add")


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(300), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    ranking = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(300), nullable=False)
    img_url = db.Column(db.String(300), nullable=False)

    def __repr__(self):
        return f'<Movie{self.title}>'


# db.create_all()

new_movie = Movie(
    title="Phone Booth",
    year=2002,
    description="Publicist Stuart Shepard finds himself trapped in a phone booth, pinned down by an extortionist's"
                " sniper rifle. Unable to leave or receive outside help, Stuart's negotiation with the caller leads"
                " to a jaw-dropping climax.",
    rating=7.3,
    ranking=10,
    review="My favourite character was the caller.",
    img_url="https://image.tmdb.org/t/p/w500/tjrX2oWRCM3Tvarz38zlZM7Uc10.jpg"
)


@app.route("/")
def home():
    all_movies = db.session.query(Movie).all()
    return render_template("index.html", all_movies=all_movies)


@app.route('/add', methods=['GET', 'POST'])
def add():
    add_form = AddForm()
    if add_form.validate_on_submit():
        return redirect(url_for("home"))
    return render_template("add.html", form=add_form)


@app.route('/edit', methods=['GET', 'POST'])
def editing():
    movie_id = request.args.get("movie_id")
    movie_title = request.args.get("movie_title")
    login_form = LoginForm()
    if login_form.validate_on_submit():
        movie_id = request.args.get("movie_id")
        movie_to_update = Movie.query.get(movie_id)
        movie_to_update.rating = login_form.movie_rating.data
        movie_to_update.review = login_form.movie_review.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("edit.html", movie_title=movie_title, movie_id=movie_id, form=login_form)


@app.route('/delete')
def delete():
    movie_id = request.args.get("movie_id")
    movie_to_delete = Movie.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


if __name__ == '__main__':
    app.run(debug=True)
