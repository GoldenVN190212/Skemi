from transformers import pipeline, set_seed
import json

generator = pipeline("text-generation", model="distilgpt2")
set_seed(42)

topics = [
    "Photosynthesis", "Magnetism", "Respiration in Humans", "Electricity",
    "Geometry", "Vietnamese Literature", "Chemistry", "Astronomy",
    "Vietnamese History", "Geography"
]

dataset = []

for topic in topics:
    print(f"🔄 Đang sinh dữ liệu cho: {topic}")
    for i in range(300):  # 👉 300 mẫu mỗi chủ đề × 10 chủ đề = 3000 dòng
        prompt = f"{topic} là quá trình"
        result = generator(prompt, max_length=50, num_return_sequences=1)[0]["generated_text"]
        dataset.append({ "text": result.strip(), "label": topic })

# 💾 Lưu ra file
with open("Train/dataset.json", "w", encoding="utf-8") as f:
    json.dump(dataset, f, ensure_ascii=False, indent=2)

print("✅ Đã sinh xong 3000 dòng dữ liệu và lưu vào Train/dataset.json")