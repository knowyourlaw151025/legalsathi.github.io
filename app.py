
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/get_law", methods=["POST"])
def get_law():
    user_question = request.json.get("question", "")
    query = user_question.lower().replace(" ", "-")
    api_url = f"https://apisetu.gov.in/public/marketplace/api/indiacode/india-code/v1/acts/{query}"
    
    try:
        res = requests.get(api_url)
        res.raise_for_status()
        data = res.json()
        title = data.get("title", user_question)
        summary = data.get("summary", "No summary available")
        source = data.get("sourceUrl", "https://indiacode.nic.in/")
        return jsonify({"title": title, "summary": summary, "source": source})
    except:
        return jsonify({"title": "Law not found",
                        "summary": "Could not find this law.",
                        "source": ""})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
