from flask import (
    Flask,
    render_template,
    request,
    Response,
    stream_with_context,
    jsonify,
)
from openai import OpenAI
from flask_cors import CORS
import os
from dotenv import load_dotenv

# client = openai.OpenAI()
load_dotenv()   # Load environment variables from .env file
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")


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


# Routes For Assistants API Functionality
# -------------------------------------------------------------------------------------
@app.route("/new-thread-id", methods=["GET"])
def new_thread_id():
    thread = client.beta.threads.create()
    return jsonify({'threadId': thread.id})


@app.route('/add-message', methods=['POST'])
def add_message():
    # adds a message to a provided thread_id
    # will be used just before /stream is called
    data = request.get_json()
    thread_id = data.get('threadId')
    message = data.get('message')

    # Add user message to thread
    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )
    
    # Logic to add the message to the specified thread
    return jsonify({'success': True})


# Stream Assitants API Response
@app.route("/stream", methods=["GET"])
def stream():

    thread_id = request.args.get('threadId')

    # This is added redundancy
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)

    # Reference the Assistants API Docs here for more info on how streaming works:
    # https://platform.openai.com/docs/api-reference/runs/createRun
    def event_generator():
        finished = False
        with client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=ASSISTANT_ID,
            stream=True
        ) as stream:
            for event in stream:
                if event.event == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == 'text':
                            data = content.text.value.replace('\n', ' <br> ')
                            yield f"data: {data}\n\n"
                
                elif event.event == "done":
                    finished = True
                    break  
        yield f"data: finish_reason: stop\n\n"

        if finished:
            return

    return Response(stream_with_context(event_generator()), mimetype="text/event-stream")



@app.route("/reset", methods=["POST"])
def reset_chat():
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return jsonify(success=True)

if __name__ == "__main__":
    app.run(port=5000)