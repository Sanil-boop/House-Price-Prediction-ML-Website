import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# load model from models folder
model = pickle.load(open("models/sqft_bed_bath_model.pkl", "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():

    sqft = float(request.form["sqft"])
    bed = int(request.form["bedrooms"])
    bath = int(request.form["bathrooms"])

    prediction = model.predict([[sqft, bed, bath]])[0]
    prediction = round(prediction, 2)

    return render_template("index.html", result=prediction)

if __name__ == "__main__":
    app.run(debug=True)
