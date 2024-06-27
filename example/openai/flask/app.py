from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    jsonify,
)
import openai
from flask_cors import CORS

client = openai.OpenAI()

app = Flask(__name__)
CORS(app)

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", chat_history=chat_history)


@app.route("/chat", methods=["POST"])
def chat():
    content = request.json.get("message")
    chat_history.append({"role": "user", "content": content})
    return jsonify(success=True)



@app.route("/stream", methods=["GET"])
def stream():
    def generate():
        assistant_response_content = ""
        finished = False
        with client.chat.completions.create(
            model="gpt-4-turbo",
            messages=chat_history,
            stream=True,
        ) as stream:
            for chunk in stream:
                if chunk.choices[0].delta and chunk.choices[0].delta.content:
                    content = chunk.choices[0].delta.content
                    assistant_response_content += content
                    data = chunk.choices[0].delta.content.replace('\n', ' <br> ')
                    yield f"data: {data}\n\n"


                if chunk.choices[0].finish_reason == "stop":
                    finished = True
                    break  
        
        yield f"data: finish_reason: stop\n\n"
        chat_history.append({"role": "assistant", "content": assistant_response_content})
        if finished:
            return

    return Response(stream_with_context(generate()), mimetype="text/event-stream")


@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=5000)