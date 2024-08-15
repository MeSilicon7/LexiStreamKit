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
    data = request.get_json()
    thread_id = data.get('threadId')
    message = data.get('message')

    client.beta.threads.messages.create(
        thread_id=thread_id,
        role="user",
        content=message,
    )
    for thread in save_thread:
        if thread["thread_id"] == thread_id:
            thread["chat_history"].append({"role": "user", "content": message})
            break
    else:
        save_thread.append({"thread_id": thread_id, "chat_history": [{"role": "user", "content": message}]})
    return jsonify({'success': True})


response_messages = []
# Global variable to store thread_id
current_thread_id = None

@app.route("/stream", methods=["GET"])
def stream():
    global current_thread_id  # Declare the global variable
    thread_id = request.args.get('threadId')
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)

    # Set the global thread_id
    current_thread_id = thread_id

    def event_generator():
        global response_messages
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
                            response_messages.append(data)
                
                elif event.event == "done":
                    finished = True
                    break  
        yield f"data: finish_reason: stop\n\n"

        if finished:
            return

    response = Response(stream_with_context(event_generator()), mimetype="text/event-stream")
    response.call_on_close(post_stream_processing)
    return response

def post_stream_processing():
    global response_messages
    global current_thread_id  # Access the global thread_id

    # convert to string and save to the chat history
    response_messages_str = ''.join(response_messages)
    response_messages_str = response_messages_str.replace("/n/n", "").strip()
    print("Full message:", response_messages_str)

    # Save the response_messages_str to the chat history
    for thread in save_thread:
        if thread["thread_id"] == current_thread_id:
            thread["chat_history"].append({"role": "assistant", "content": response_messages_str})
            break

    # Clear the list if you plan to reuse it for the next stream
    response_messages.clear()

if __name__ == "__main__":
    app.run(port=5000)