import pickle
from flask import Flask, render_template, request

app = Flask(__name__)

# Load model
with open("models/sqft_bed_bath_model.pkl", "rb") as f:
    model = pickle.load(f)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/predict", methods=["POST"])
def predict():
    try:
        sqft = float(request.form.get("sqft"))
        bed = int(request.form.get("bedrooms"))
        bath = int(request.form.get("bathrooms"))

        # Predict
        prediction = model.predict([[sqft, bed, bath]])[0]

        # Prevent negative predictions
        prediction = max(prediction, 0)

        # Round & format
        formatted_price = f"{round(prediction, 2):,}"

        return render_template("index.html", result=formatted_price)

    except Exception:
        return render_template("index.html", result="Invalid Input")


if __name__ == "__main__":
    app.run()
