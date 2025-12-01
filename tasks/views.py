# from django.http import JsonResponse
# from django.views.decorators.csrf import csrf_exempt
# import json
# from .scoring import calculate_task_score

# @csrf_exempt
# def analyze_tasks(request):
#     if request.method == "POST":
#         try:
#             data = json.loads(request.body)

#             # Accept JSON as: { "tasks": [ ... ] }
#             tasks = data.get("tasks", [])

#             scored_tasks = []
#             for task in tasks:
#                 score = calculate_task_score(task)
#                 task["score"] = score
#                 scored_tasks.append(task)

#             scored_tasks.sort(key=lambda x: x["score"], reverse=True)

#             return JsonResponse(scored_tasks, safe=False)

#         except Exception as e:
#             return JsonResponse({"error": str(e)}, status=400)

#     return JsonResponse({"message": "Use POST request"}, status=405)



# @csrf_exempt
# def suggest_tasks(request):
#     if request.method == "GET":
#         sample_tasks = [
#             {"title": "Example Task 1", "due_date": "2025-02-01", "importance": 8, "estimated_hours": 2, "dependencies": []},
#             {"title": "Example Task 2", "due_date": "2025-01-28", "importance": 5, "estimated_hours": 1, "dependencies": []},
#         ]

#         # Apply scoring
#         for task in sample_tasks:
#             task["score"] = calculate_task_score(task)

#         # Return top 3 suggestions
#         sample_tasks.sort(key=lambda x: x["score"], reverse=True)
#         top_tasks = sample_tasks[:3]

#         return JsonResponse(top_tasks, safe=False)

#     return JsonResponse({"message": "Use GET request"}, status=405)

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .scoring import calculate_task_score


@csrf_exempt
def analyze_tasks(request):
    if request.method != "POST":
        return JsonResponse({"error": "Use POST method"}, status=400)

    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        return JsonResponse({"error": "Invalid JSON format"}, status=400)

    # if not isinstance(data, list):
    #     return JsonResponse({"error": "Expected a list of tasks"}, status=400)

    analyzed = []

    for task in data:
        score = calculate_task_score(task)
        task["score"] = score
        analyzed.append(task)

    # Sort tasks by score descending
    analyzed.sort(key=lambda x: x["score"], reverse=True)

    return JsonResponse({"tasks": analyzed}, safe=False)
