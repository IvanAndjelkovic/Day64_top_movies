from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SubmitField
from wtforms.validators import DataRequired, NumberRange
import requests
import os
from dotenv import load_dotenv




'''
Red underlines? Install the required packages first: 
Open the Terminal in PyCharm (bottom left). 

On Windows type:
python -m pip install -r requirements.txt

On MacOS type:
pip3 install -r requirements.txt

This will install the packages from requirements.txt for this project.
'''

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)

#Movie API data data:

load_dotenv()
api_key = os.environ.get("API_KEY")
url = "https://api.themoviedb.org/3/search/movie"
headers = {"accept": "application/json"}

class MyForm(FlaskForm):
    
    rating = FloatField(label='Your new Rating from 0 to 10, eg. 7.5', validators=[DataRequired(), NumberRange(min=0, max=10)])
    movie_review = StringField(label='Your Review', validators=[DataRequired(message='movie review is required.')])
    submit = SubmitField(label='Done')


# CREATE DB
class Base(DeclarativeBase):
    pass
db = SQLAlchemy(model_class=Base)
# configure the SQLite database, relative to the app instance folder
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies-collection.db"
# initialize the app with the extension
db.init_app(app)

# CREATE TABLE


class Movies(db.Model):
    id: Mapped[int] = mapped_column (Integer, primary_key=True)
    title: Mapped[str] = mapped_column (String(250), unique = True, nullable = False)
    year: Mapped[int] = mapped_column (Integer, nullable = False)
    description: Mapped[str] = mapped_column (String(500))
    rating: Mapped[float] = mapped_column (Float, nullable = True)
    ranking: Mapped[int] = mapped_column (Integer, nullable = True)
    review: Mapped[str] = mapped_column (String(250), nullable = True)
    img_url: Mapped[str] = mapped_column (String(250), nullable = False)

    # Optional: this will allow each book object to be identified by its title when printed.
    def __repr__(self):
        return f'<Book {self.title}>'

with app.app_context():
    db.create_all()

# with app.app_context():
#     second_movie = Movies(
#         title="Avatar The Way of Water",
#         year=2022,
#         description="Set more than a decade after the events of the first film, learn the story of the Sully family (Jake, Neytiri, and their kids), the trouble that follows them, the lengths they go to keep each other safe, the battles they fight to stay alive, and the tragedies they endure.",
#         rating=7.3,
#         ranking=9,
#         review="I liked the water.",
#         img_url="https://image.tmdb.org/t/p/w500/t6HIqrRAclMCA60NsSmeqe9RmNV.jpg"
#     )
#     db.session.add(second_movie)
#     db.session.commit()




@app.route("/")
def home():

    all_movies = db.session.scalars(db.select(Movies).order_by(Movies.rating.desc())).all()
    print([movie.rating for movie in all_movies])
    return render_template("index.html", all_movies=all_movies)

@app.route("/edit/<int:movie_id>", methods=["GET","POST"])
def edit(movie_id):
    form=MyForm()
    movie=db.session.get(Movies, movie_id)
    if form.validate_on_submit() and request.method=="POST":
        movie.rating=float(request.form["rating"])
        movie.review=str(request.form["movie_review"])
        db.session.commit() 
        return redirect(url_for('home'))

    
    return render_template("edit.html", movie=movie, movie_id=movie_id, form=form)

@app.route("/delete/<int:movie_id>", methods=["GET","POST"])
def delete(movie_id):
    movie_to_delete=db.get_or_404(Movies, movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/add", methods=["GET","POST"])
def add():



    return render_template("add.html")

@app.route("/select", methods=["GET","POST"])
def select():
    
    if request.method=="POST":
        movie_title=request.form.get("movie_title")
        print(movie_title)
        params={
                "api_key": api_key, 
                "query":movie_title,
                "include_adult": False,
                "language": "en-US",
                "page":1
                }
        response = requests.get(url, headers=headers, params=params)
        
        data=response.json()
        movies_data=data["results"]
        return render_template("select.html", movies_data=movies_data)
    return render_template("select.html",movies_date=None)

@app.route("/movie_details/<movie_id>", methods=["GET"])
def movie_details(movie_id):

    url = f"https://api.themoviedb.org/3/movie/{movie_id}?language=en-US"
    api_token= os.environ.get("API_TOKEN")
    headers = {
                    "accept": "application/json",
                    "Authorization": f"Bearer {api_token}"
                }
    response = requests.get(url, headers=headers)

    data=response.json()
    db_title = data["title"]
    db_img_url = f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
    db_year=2025
    movie_id=int(data["id"]),
    db_description = data["overview"]
    print(db_title)
    with app.app_context():
        new_movie = Movies(
            id=data["id"],
            title=data["title"],
            year=data["release_date"][0:4],
            description=data["overview"],
            # rating=7.3,
            # ranking=9,
            # review="I liked the water.",
            img_url=f'https://image.tmdb.org/t/p/w500/{data["poster_path"]}'
        )
        db.session.add(new_movie)
        db.session.commit()
    return redirect(url_for('edit', movie_id=data["id"]))

    










if __name__ == '__main__':
    app.run(debug=True)
