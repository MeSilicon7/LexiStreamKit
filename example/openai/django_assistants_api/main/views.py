from django.shortcuts import render

# Create your views here.

import json
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
from openai import OpenAI
import os

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
ASSISTANT_ID = os.environ.get("OPENAI_ASSISTANT_ID")

# Global variables
save_thread = []
response_messages = []
current_thread_id = None

def post_stream_processing():
    global response_messages, current_thread_id
    response_messages_str = "".join(response_messages)
    response_messages_str = response_messages_str.replace("/n/n", "").strip()
    
    for thread in save_thread:
        if thread["thread_id"] == current_thread_id:
            thread["chat_history"].append(
                {"role": "assistant", "content": response_messages_str}
            )
            break
    response_messages.clear()

def index(request):
    return render(request, "index.html", {"threads": save_thread})

def chat_with_thread(request, thread_id):
    for thread in save_thread:
        if thread["thread_id"] == thread_id:
            return render(request, "index.html", {
                "threads": save_thread,
                "chat_history": thread["chat_history"],
                "threadId": thread_id,
            })
    return JsonResponse({"message": "Thread not found", "threadId": thread_id})

@csrf_exempt
def new_thread_id(request):
    thread = client.beta.threads.create()
    return JsonResponse({"threadId": thread.id})

@csrf_exempt
def add_message(request):
    if request.method == "POST":
        data = json.loads(request.body)
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
            save_thread.append({
                "thread_id": thread_id,
                "chat_history": [{"role": "user", "content": message}],
            })
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

@csrf_exempt
def stream(request):
    global current_thread_id
    thread_id = request.GET.get("threadId")
    
    if not thread_id:
        thread = client.beta.threads.create()
        thread_id = thread.id
    else:
        thread = client.beta.threads.retrieve(thread_id)

    current_thread_id = thread_id

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
            post_stream_processing()
            return

    return StreamingHttpResponse(event_generator(), content_type="text/event-stream")

@csrf_exempt
def stop_stream(request):
    if request.method == "POST":
        data = json.loads(request.body)
        thread_id = data.get("threadId")
        if thread_id == current_thread_id:
            post_stream_processing()
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})