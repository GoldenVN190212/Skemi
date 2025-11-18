from flask import Flask, request, jsonify
from Ai_router import route_message, analyze_user_file, create_mindmap_description

app = Flask(__name__)

@app.route("/chat", methods=["POST"])
def chat_route():
    q = request.json["message"]
    answer = route_message(q)
    return jsonify({"answer": answer})


@app.route("/analyze-file", methods=["POST"])
def analyze_file_route():
    file_path = request.json["file_path"]
    data = analyze_user_file(file_path)

    description = create_mindmap_description(
        topic=data["topic"],
        details=data["detail"]
    )

    return jsonify({
        "topic": data["topic"],
        "detail": data["detail"],
        "summary": data["summary"],
        "mindmap_description": description
    })


app.run(host="0.0.0.0", port=8000)
