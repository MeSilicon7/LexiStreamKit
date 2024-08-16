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
load_dotenv()  # Load environment variables from .env file
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")


app = Flask(__name__)
CORS(app)

# This is a temporary solution to store the chat history of a thread
# Use a database or a file to store the chat history in a real-world application
# This is how save_thread will look like:
# save_thread = [
#     {
#         "thread_id": "thread_Bk3LznxbN17uqJxHiWq1ulJ6",
#         "chat_history": [
#             {"role": "user", "content": "Hello"},
#             {"role": "assistant", "content": "Hello! How can I assist you today?"},
#         ]
#     },
# ]

save_thread = []


# Global variable to store current response messages from
response_messages = []

# Global variable to store thread_id
current_thread_id = None

# Function to process the response messages, save them to the chat history, and clear the list
def post_stream_processing():
    global response_messages
    global current_thread_id

    # convert to string and save to the chat history
    response_messages_str = "".join(response_messages)
    response_messages_str = response_messages_str.replace("/n/n", "").strip()
    # print("Full message:", response_messages_str)

    # Save the response_messages_str to the chat history
    for thread in save_thread:
        if thread["thread_id"] == current_thread_id:
            thread["chat_history"].append(
                {"role": "assistant", "content": response_messages_str}
            )
            break

    # Clear the list to reuse it for the next stream
    response_messages.clear()


@app.route("/", methods=["GET"])
def index():
    return render_template("index.html", threads=save_thread)


@app.route("/chat/<thread_id>", methods=["GET"])
def chat_with_thread(thread_id):
    for thread in save_thread:
        if thread["thread_id"] == thread_id:
            # print(thread_id)
            return render_template(
                "index.html",
                threads=save_thread,
                chat_history=thread["chat_history"],
                threadId=thread_id,
            )
    return jsonify({"message": "Thread not found", "threadId": thread_id})


# Routes For Assistants API Functionality
# -------------------------------------------------------------------------------------
@app.route("/new-thread-id", methods=["GET"])
def new_thread_id():
    thread = client.beta.threads.create()
    print(f"Created new thread: {thread.id}")
    return jsonify({"threadId": thread.id})


@app.route("/add-message", methods=["POST"])
def add_message():
    data = request.get_json()
    thread_id = data.get("threadId")
    message = data.get("message")

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
        save_thread.append(
            {
                "thread_id": thread_id,
                "chat_history": [{"role": "user", "content": message}],
            }
        )
    return jsonify({"success": True})


@app.route("/stream", methods=["GET"])
def stream():
    global current_thread_id
    thread_id = request.args.get("threadId")
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)

    # Set the global thread_id
    current_thread_id = thread_id

    # Reference the Assistants API Docs here for more info on how streaming works:
    # https://platform.openai.com/docs/api-reference/runs/createRun

    def event_generator():
        global response_messages
        finished = False
        with client.beta.threads.runs.create(
            thread_id=thread_id, assistant_id=ASSISTANT_ID, stream=True
        ) as stream:
            for event in stream:
                if event.event == "thread.message.delta":
                    for content in event.data.delta.content:
                        if content.type == "text":
                            data = content.text.value.replace("\n", " <br> ")
                            yield f"data: {data}\n\n"
                            response_messages.append(data)

                elif event.event == "done":
                    finished = True
                    break
        yield f"data: finish_reason: stop\n\n"

        if finished:
            return

    response = Response(
        stream_with_context(event_generator()), mimetype="text/event-stream"
    )
    response.call_on_close(post_stream_processing)
    return response


# when the user stops the stream, we need to call post_stream_processing
@app.route("/stop-stream", methods=["POST"])
def stop_stream():
    data = request.get_json()
    thread_id = data.get("threadId")
    # Explicitly call post_stream_processing here
    if thread_id == current_thread_id:
        post_stream_processing()
    return jsonify({"success": True})


if __name__ == "__main__":
    app.run(port=5000)
