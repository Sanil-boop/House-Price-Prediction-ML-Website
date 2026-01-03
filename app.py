import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load model safely
with open("models/sqft_bed_bath_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        sqft = float(request.form["sqft"])
        bed = int(request.form["bedrooms"])
        bath = int(request.form["bathrooms"])

        # Predict price
        prediction = model.predict([[sqft, bed, bath]])[0]

        # Avoid negative predictions
        prediction = max(prediction, 0)

        # Round & format for display
        formatted_price = format(round(prediction, 2), ",")
        
        return render_template("index.html", result=formatted_price)

    except Exception as e:
        return render_template("index.html", result="Input Error")


if __name__ == "__main__":
    app.run()
