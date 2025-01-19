import json
from django.shortcuts import render
from django.http import JsonResponse, StreamingHttpResponse
from django.views.decorators.csrf import csrf_exempt
import openai

client = openai.OpenAI()

chat_history = [
    {"role": "system", "content": "You are a helpful assistant."},
]

@csrf_exempt
def index(request):
    return render(request, "index.html", {"chat_history": chat_history})

@csrf_exempt
def chat(request):
    if request.method == "POST":
        data = json.loads(request.body)
        content = data.get("message")
        chat_history.append({"role": "user", "content": content})
        return JsonResponse({"success": True})
    return JsonResponse({"success": False})

@csrf_exempt
def stream(request):
    def generate():
        if not chat_history or len(chat_history) < 2:
            yield f"data: Error: No message to process\n\n"
            yield f"data: finish_reason: stop\n\n"
            return

        assistant_response_content = ""
        finished = False

        try:
            with client.chat.completions.create(
                model="gpt-4-turbo",
                messages=chat_history,
                stream=True,
            ) as stream:
                for chunk in stream:
                    if chunk.choices[0].delta and chunk.choices[0].delta.content:
                        content = chunk.choices[0].delta.content
                        assistant_response_content += content
                        data = content.replace("\n", " <br> ")
                        yield f"data: {data}\n\n"

                    if chunk.choices[0].finish_reason == "stop":
                        finished = True
                        break

            yield f"data: finish_reason: stop\n\n"
            chat_history.append({"role": "assistant", "content": assistant_response_content})

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"
            yield f"data: finish_reason: stop\n\n"

    return StreamingHttpResponse(generate(), content_type="text/event-stream")

@csrf_exempt
def reset_chat(request):
    global chat_history
    chat_history = [{"role": "system", "content": "You are a helpful assistant."}]
    return JsonResponse({"success": True})