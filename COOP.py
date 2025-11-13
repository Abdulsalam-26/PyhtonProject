from flask import Flask, render_template, request, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# إعداد قاعدة البيانات
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # منع إشعارات التغييرات
db = SQLAlchemy(app)

# نموذج Trainer لقاعدة البيانات
class Trainer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    university = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f'<Trainer {self.name}>'

# إنشاء قاعدة البيانات (يجب أن يتم تشغيل هذا مرة واحدة فقط)
with app.app_context():
    db.create_all()

@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        name = request.form['name']
        university = request.form['university']
        rating = request.form['rating']

        # تحقق من المدخلات
        if not (1 <= int(rating) <= 10):
            flash("Rating must be between 1 and 10!", "danger")
            return redirect("/")

        new_trainer = Trainer(name=name, university=university, rating=rating)

        try:
            db.session.add(new_trainer)
            db.session.commit()
            flash("Trainer added successfully!", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"Error: {str(e)}", "danger")

        return redirect("/")

    trainers = Trainer.query.all()
    return render_template("index.html", trainers=trainers)

if __name__ == "__main__":
    app.run(debug=True)
