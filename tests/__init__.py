#
#
#
#
#
#
#
#
# import json
# import unittest
# from datetime import date
# from datetime import datetime
#
# from app import create_app, db
# from models.task import Task
# from schema.task import TaskSchema
#
#
# class TestTaskAPI(unittest.TestCase):
#
#     def setUp(self):
#         self.app = create_app()
#         self.client = self.app.test_client()
#         self.db = db
#         self.task_schema = TaskSchema()
#
#         # Create the database tables
#         with self.app.app_context():
#             self.db.create_all()
#
#     def tearDown(self):
#         # Clean up the database tables
#         with self.app.app_context():
#             self.db.drop_all()
#
#     def test_get_tasks(self):
#         # Create a task
#         task = Task(
#             title='Task 1',
#             description='Description 1',
#             status='in_progress',
#             priority='high',
#             due_date=date(2022, 1, 1)
#         )
#         self.db.session.add(task)
#         self.db.session.commit()
#
#         # Test getting all tasks
#         response = self.app.get('/api/tasks')
#         self.assertEqual(response.status_code, 200)
#         expected_result = [
#             {
#                 'id': task.id,
#                 'title': 'Task 1',
#                 'description': 'Description 1',
#                 'status': 'in_progress',
#                 'priority': 'high',
#                 'due_date': '2022-01-01'
#             }
#         ]
#         self.assertEqual(json.loads(response.data), expected_result)
#
#         # Test getting tasks by status
#         response = self.app.get('/api/tasks?status=in_progress')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(json.loads(response.data), expected_result)
#
#         # Test getting tasks by priority
#         response = self.app.get('/api/tasks?priority=high')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(json.loads(response.data), expected_result)
#
#         # Test getting tasks by status and priority
#         response = self.app.get('/api/tasks?status=in_progress&priority=high')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(json.loads(response.data), expected_result)
#
#     def test_create_task(self):
#         # Define the test data
#         data = {
#             'title': 'Test task',
#             'description': 'Test description',
#             'status': 'in_progress',
#             'priority': 'high',
#             'due_date': str(datetime.now().date()),
#         }
#
#         # Make POST request to '/tasks' endpoint with test data
#         response = self.client.post('/api/tasks', data=json.dumps(data), content_type='application/json')
#
#         # Assert the response status code is 201
#         self.assertEqual(response.status_code, 201)
#
#         # Assert the response data matches the expected data
#         expected_data = {
#             'id': 1,
#             'title': data['title'],
#             'description': data['description'],
#             'status': data['status'],
#             'priority': data['priority'],
#             'due_date': data['due_date'],
#         }
#         self.assertEqual(json.loads(response.data), expected_data)
#
#     def test_update_task_successfully(self):
#         # Create a task to update
#         task = Task(title='Test Task', description='This is a test task', status='in_progress', priority='high',
#                     due_date=date.today())
#         self.db.session.add(task)
#         self.db.session.commit()
#
#         # Set up the request data
#         data = {'title': 'Updated Test Task', 'description': 'This is an updated test task', 'status': 'completed',
#                 'priority': 'high', 'due_date': str(date.today())}
#
#         # Send the request to update the task
#         response = self.client.put(f'/api/tasks/{task.id}', data=json.dumps(data), content_type='application/json')
#
#         # Check that the response status code is 200
#         assert response.status_code == 200
#
#         # Check that the task was updated correctly
#         updated_task = Task.query.get(task.id)
#         assert updated_task.title == 'Updated Test Task'
#         assert updated_task.description == 'This is an updated test task'
#         assert updated_task.status == 'completed'
#         assert updated_task.priority == 'high'
#         assert updated_task.due_date == date.today()
#
#         # Check that the response data matches the updated task
#         result = self.task_schema.dump(updated_task)
#         assert result == json.loads(response.data)
#
#     def test_update_task_not_found(self):
#         # Set up the request data
#         data = {'title': 'Updated Test Task', 'description': 'This is an updated test task', 'status': 'completed',
#                 'priority': 'high', 'due_date': str(date.today())}
#
#         # Send the request to update a task that doesn't exist
#         response = self.client.put('/api/tasks/999', data=json.dumps(data), content_type='application/json')
#
#         # Check that the response status code is 404
#         assert response.status_code == 404
#
#     def test_update_task_with_invalid_data(self):
#         # Create a task to update
#         task = Task(title='Test Task', description='This is a test task', status='in_progress', priority='high',
#                     due_date=date.today())
#         self.db.session.add(task)
#         self.db.session.commit()
#
#         # Set up the request data with invalid values
#         data = {'title': '', 'status': 'invalid_status', 'priority': 'high', 'due_date': 'invalid_date'}
#
#         # Send the request to update the task with invalid data
#         response = self.client.put(f'/api/tasks/{task.id}', data=json.dumps(data), content_type='application/json')
#
#         # Check that the response status code is 400
#         assert response.status_code == 400
#
#         # Check that the task was not updated
#         updated_task = Task.query.get(task.id)
#         assert updated_task.title == 'Test Task'
#         assert updated_task.status == 'in_progress'
#         assert updated_task.priority == 'high'
#         assert updated_task.due_date == date.today()
#
#     def test_delete_task(self):
#         # Create a new task to delete
#         task = Task(title='Test Task', description='This is a test task', status='to_do', priority='high',
#                     due_date=date.today())
#         self.db.session.add(task)
#         self.db.session.commit()
#
#         # Make the DELETE request to delete the task
#         response = self.client.delete(f'/api/tasks/{task.id}')
#
#         # Check if the response has a success status code
#         assert response.status_code == 200
#
#         # Check if the task was deleted from the database
#         deleted_task = Task.query.get(task.id)
#         assert deleted_task is None
#
#         # Check if the response message is correct
#         expected_message = {'message': 'Task successfully deleted'}
#         assert response.get_json() == expected_message
#
#     def test_get_task(self):
#         # Create a task
#         task = Task(
#             title='Task 1',
#             description='Description 1',
#             status='to_do',
#             priority='high',
#             due_date=date(2022, 12, 31)
#         )
#         self.db.session.add(task)
#         self.db.session.commit()
#
#         response = self.client.get(f'/api/v1/tasks/{task.id}')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['title'], 'Task 1')
#         self.assertEqual(response.json['description'], 'Description 1')
#         self.assertEqual(response.json['status'], 'to_do')
#         self.assertEqual(response.json['priority'], "high")
#         self.assertEqual(response.json['due_date'], '2022-12-31')
#
#     def test_get_non_existent_task(self):
#         response = self.client.get('/api/v1/tasks/999')
#         self.assertEqual(response.status_code, 404)
#         self.assertEqual(response.json['error'], 'Task not found')
