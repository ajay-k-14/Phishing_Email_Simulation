
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

campaigns = [
    {"id": 1, "name": "Account Verification", "type": "Credential Safety", "sent": 42, "clicked": 10, "reported": 18},
    {"id": 2, "name": "Invoice Review", "type": "Urgency", "sent": 38, "clicked": 8, "reported": 21},
    {"id": 3, "name": "Company Update", "type": "Social Engineering", "sent": 44, "clicked": 9, "reported": 25},
]

@app.route("/")
def home():
    return render_template("index.html", campaigns=campaigns)

@app.get("/simulation")
def simulation():
    return render_template(
        "simulation.html",
        template=request.args.get("template", "Account Verification"),
        recipient=request.args.get("recipient", "user@email.com"),
    )
 
@app.post("/api/simulate")
def simulate():
    data = request.get_json(silent=True) or {}
    template = data.get("template", "Account Verification")
    # Safe simulation only: no credentials are collected.
    return jsonify({
        "success": True,
        "message": f"Safe simulation created using the '{template}' scenario.",
        "safety": "No real passwords, payment details, or credentials are collected."
    })

@app.get("/api/stats")
def stats():
    sent = sum(c["sent"] for c in campaigns)
    clicked = sum(c["clicked"] for c in campaigns)
    reported = sum(c["reported"] for c in campaigns)
    return jsonify({
        "campaigns": len(campaigns),
        "sent": sent,
        "clicked": clicked,
        "reported": reported,
        "click_rate": round(clicked / sent * 100, 1) if sent else 0
    })

if __name__ == "__main__":
    app.run(debug=True)
