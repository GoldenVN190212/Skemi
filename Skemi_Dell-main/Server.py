# Server.py
import os
import asyncio
from datetime import datetime, timedelta
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from ollama import chat   # Ollama Python SDK

app = FastAPI()

# ----- CORS -----
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----- Static folders -----
if os.path.exists("Css"):
    app.mount("/Css", StaticFiles(directory="Css"), name="Css")
if os.path.exists("Js"):
    app.mount("/Js", StaticFiles(directory="Js"), name="Js")

@app.get("/")
async def index():
    html_path = os.path.join(os.getcwd(), "Chatbot.html")
    if os.path.exists(html_path):
        return FileResponse(html_path)
    return JSONResponse({"message": "Chatbot.html không tồn tại"}, status_code=404)

# ------------------ SESSION & QUEUE ------------------
queue = asyncio.Queue()
sessions = {}  # {session_id: {"messages": [], "last_active": timestamp}}
SESSION_TIMEOUT = timedelta(minutes=120)

class Question(BaseModel):
    session_id: str
    question: str

# ------------------ MODEL ROUTER ------------------
def choose_model(text: str):
    short = len(text.strip())

    # Câu quá ngắn → phi3:mini (rất nhanh)
    if short < 25:
        return "phi3:mini"

    # Câu trung bình nhưng không quá phức tạp
    if short < 200:
        return "llama3.2:11b"  # bản không vision → nhanh hơn vision

    # Câu dài → vẫn là llama 11b
    return "llama3.2:11b"


# ------------------ BACKGROUND WORKER ------------------
async def worker():
    while True:
        session_id, message, fut = await queue.get()
        try:
            # Lấy session cũ hoặc tạo session mới
            session = sessions.get(session_id, {"messages": [], "last_active": datetime.utcnow()})
            messages = session["messages"]

            # Lưu câu hỏi vào session
            messages.append({"role": "user", "content": message})

            # Router chọn model
            model_name = choose_model(message)
            print(f"🚀 Model được chọn: {model_name}")

            # Gọi model
            response = chat(
                model=model_name,
                messages=[
                    {"role": "system", "content": "Bạn là chatbot thân thiện, trả lời rõ ràng và tự nhiên."}
                ] + messages,
            )

            # Lấy nội dung trả lời
            answer = ""
            if isinstance(response, dict):
                if "message" in response:
                    answer = response["message"]["content"]
                elif "messages" in response and isinstance(response["messages"], list):
                    answer = response["messages"][-1].get("content", "")
            else:
                answer = getattr(response.message, "content", "")

            if not answer:
                answer = "Skemi không trả lời được."

            # Lưu câu trả lời vào session
            messages.append({"role": "assistant", "content": answer})

            sessions[session_id] = {
                "messages": messages,
                "last_active": datetime.utcnow()
            }

            fut.set_result(answer)

        except Exception as e:
            fut.set_result(f"Lỗi xử lý model: {e}")

        finally:
            queue.task_done()


# ------------------ CLEAN SESSION ------------------
async def session_cleaner():
    while True:
        now = datetime.utcnow()
        to_delete = []

        for session_id, data in sessions.items():
            if now - data["last_active"] > SESSION_TIMEOUT:
                to_delete.append(session_id)

        for s in to_delete:
            print(f"🗑 Xóa session hết hạn: {s}")
            del sessions[s]

        await asyncio.sleep(60)


# ------------------ SERVER STARTUP ------------------
@app.on_event("startup")
async def startup_event():
    asyncio.create_task(worker())
    asyncio.create_task(session_cleaner())


# ------------------ API CHAT ------------------
@app.post("/ask")
async def ask_ai(data: Question):
    loop = asyncio.get_event_loop()
    fut = loop.create_future()
    await queue.put((data.session_id, data.question, fut))
    answer = await fut
    return {"answer": answer}


# ------------------ END SESSION ------------------
@app.post("/end_session")
async def end_session(data: dict):
    sid = data.get("session_id")
    if sid in sessions:
        del sessions[sid]
        print(f"🗑 Session {sid} bị xóa bởi user")
    return {"message": "Session deleted"}
