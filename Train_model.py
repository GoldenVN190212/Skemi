def train_model():
    import json
    import joblib
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.linear_model import LogisticRegression

    with open("Train/dataset.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    texts = [item["text"] for item in data]
    labels = [item["label"] for item in data]

    if len(set(labels)) < 2:
        raise ValueError("❌ Cần ít nhất 2 chủ đề khác nhau để huấn luyện.")

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(texts)

    model = LogisticRegression(max_iter=200)
    model.fit(X, labels)

    joblib.dump(model, "Train/skemi_model.pkl")
    joblib.dump(vectorizer, "Train/skemi_vectorizer.pkl")

    print("✅ Huấn luyện xong mô hình AI (tự động cập nhật)")
