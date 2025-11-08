from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import joblib
from Train_model import train_model
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

app = Flask(__name__)
CORS(app)  # ✅ Cho phép mọi origin, xử lý cả preflight

# ======================= TẢI MÔ HÌNH VÀ VECTORIZER =======================
MODEL_PATH = "Train/skemi_model.pkl"
VECTORIZER_PATH = "Train/skemi_vectorizer.pkl"

def load_model():
    if not os.path.exists(MODEL_PATH) or not os.path.exists(VECTORIZER_PATH):
        print("⚠️ Chưa có mô hình, hãy huấn luyện trước.")
        return None, None
    model = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
    print("✅ Đã tải mô hình và vectorizer.")
    return model, vectorizer

model, vectorizer = load_model()

# ======================= DỰ ĐOÁN CHỦ ĐỀ =======================
@app.route("/predict", methods=["POST"])
def predict():
    global model, vectorizer
    data = request.get_json()
    text = data.get("text", "")

    if not model or not vectorizer:
        model, vectorizer = load_model()
        if not model:
            return jsonify({"status": "error", "message": "❌ Chưa có mô hình được huấn luyện."})

    X = vectorizer.transform([text])
    prediction = model.predict(X)[0]
    return jsonify({"status": "success", "topic": prediction})

# ======================= TRÍCH Ý CHÍNH CHO MINDMAP =======================
@app.route("/extract_subtopics", methods=["POST", "OPTIONS"])
def extract_subtopics():
    if request.method == "OPTIONS":
        return '', 200  # ✅ Trả về OK cho preflight request

    data = request.get_json()
    text = data.get("text", "")
    mode = data.get("mode", "summary")

    sentences = text.split(".")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]

    if mode == "summary":
        return jsonify({"subtopics": sentences[:3]})

    if mode == "detail":
        vectorizer = TfidfVectorizer()
        X = vectorizer.fit_transform(sentences)
        kmeans = KMeans(n_clusters=5, random_state=42)
        kmeans.fit(X)
        clusters = [[] for _ in range(5)]
        for i, label in enumerate(kmeans.labels_):
            clusters[label].append(sentences[i])
        subtopics = ["; ".join(cluster[:2]) for cluster in clusters]
        return jsonify({"subtopics": subtopics})

    return jsonify({"subtopics": ["Không thể phân tích nội dung"]})

# ======================= THÊM MẪU VÀ HUẤN LUYỆN LẠI =======================
@app.route("/add_sample", methods=["POST"])
def add_sample():
    data = request.get_json()
    text = data.get("text")
    label = data.get("label")

    if not text or not label:
        return jsonify({"status": "error", "message": "Thiếu dữ liệu văn bản hoặc nhãn."})

    dataset_path = "Train/dataset.json"

    if not os.path.exists(dataset_path):
        with open(dataset_path, "w", encoding="utf-8") as f:
            json.dump([], f, ensure_ascii=False, indent=2)

    with open(dataset_path, "r", encoding="utf-8") as f:
        dataset = json.load(f)

    dataset.append({"text": text, "label": label})

    with open(dataset_path, "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, indent=2)

    try:
        print("🧠 Đang huấn luyện lại mô hình với dữ liệu mới...")
        train_model()
        print("✅ Huấn luyện xong, nạp lại mô hình...")
        global model, vectorizer
        model, vectorizer = load_model()
        return jsonify({"status": "success", "message": "✅ Đã huấn luyện lại mô hình AI"})
    except Exception as e:
        return jsonify({"status": "error", "message": f"❌ Lỗi khi huấn luyện lại: {str(e)}"})

# ======================= KIỂM TRA SERVER =======================
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "🚀 Server Flask đang chạy và sẵn sàng!"})

# ======================= CHẠY SERVER =======================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)