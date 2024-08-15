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

# This is a temporary solution to store the chat history of a thread
# This will be replaced with a database in the future

save_thread = [
    {
        "thread_id": "thread_Bk3LznxbN17uqJxHiWq1ulJ6",
        "chat_history": [
            {"role": "user", "content": "Hello"},
            {"role": "assistant", "content": "Hello! How can I assist you today?"},
        ]
    },
]

@app.route("/", methods=["GET"])
def index():
    # send existing all thread to render template as a list
    return render_template("index.html", threads=save_thread)

#Todo: new route for chat with old thread which should take thread id as input and return the chat history of that thread
@app.route("/chat/<thread_id>", methods=["GET"])
def chat_with_thread(thread_id):
    # it will render index.html with chat history of the thread 
    for thread in save_thread:
        if thread["thread_id"] == thread_id:
            print(thread_id)
            # Pass the thread_id to the template along with other data
            return render_template("index.html", threads=save_thread, chat_history=thread["chat_history"], threadId=thread_id)
    # Return JSON response with thread_id when not found
    return jsonify({"message": "Thread not found", "threadId": thread_id})



# Routes For Assistants API Functionality
# -------------------------------------------------------------------------------------
@app.route("/new-thread-id", methods=["GET"])
def new_thread_id():
    thread = client.beta.threads.create()
    print(f"Created new thread: {thread.id}")
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
    # debug
    print(f"Added message to thread {thread_id}: {message}")

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


if __name__ == "__main__":
    app.run(port=5000)