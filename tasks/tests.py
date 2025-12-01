# from django.test import TestCase
# from .scoring import calculate_task_score
# from datetime import date, timedelta

# class ScoringTests(TestCase):

#     def test_basic_scoring_overdue(self):
#         today = date.today()
#         t = {
#             "id": 1,
#             "title": "Overdue task",
#             "due_date": (today - timedelta(days=2)).isoformat(),
#             "importance": 8,
#             "estimated_hours": 1,
#             "dependencies": []
#         }
#         all_map = {1: t}
#         res = calculate_task_score(t, all_map)
#         self.assertTrue(res["score"] >= 100)
#         self.assertEqual(res["priority"], "high")

#     def test_dependency_penalty(self):
#         today = date.today()
#         t1 = {"id":1, "title":"A","due_date":(today+timedelta(days=10)).isoformat(), "importance":5, "estimated_hours":2, "dependencies":[2]}
#         t2 = {"id":2, "title":"B","due_date":(today+timedelta(days=3)).isoformat(), "importance":5, "estimated_hours":1, "dependencies":[], "done":True}
#         all_map = {1:t1, 2:t2}
#         res = calculate_task_score(t1, all_map)
#         # dependency resolved (done=True), so penalty shouldn't apply
#         self.assertNotIn(2, res["unresolved_dependencies"])
