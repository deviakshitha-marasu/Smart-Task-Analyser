from django.http import JsonResponse
import json

def analyze_task(request):
    if request.method == "POST":
        data = json.loads(request.body)
        task = data.get("task", "")

        # SIMPLE ANALYSIS EXAMPLE
        result = {
            "task_length": len(task),
            "uppercase_version": task.upper(),
            "word_count": len(task.split())
        }

        return JsonResponse(result)

    return JsonResponse({"error": "Invalid request"}, status=400)
