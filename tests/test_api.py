import json
import unittest
from datetime import date

from app import create_app, db
from models.task import Task
from schema.task import TaskSchema


class TasksTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.task_schema = TaskSchema()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        self.task1 = Task(title="Task 1", description="Description 1", status="in_progress", priority="low",
                          due_date=date(2023, 5, 15))
        self.task2 = Task(title="Task 2", description="Description 2", status="completed", priority="low",
                          due_date=date(2023, 5, 16))
        db.session.add(self.task1)
        db.session.add(self.task2)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_all_tasks(self):
        response = self.client.get('/tasks')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)

    def test_get_filtered_tasks(self):
        response = self.client.get('/tasks?status=in_progress')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['status'], 'in_progress')

        response = self.client.get('/tasks?priority=low')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['priority'], 'low')

        response = self.client.get('/tasks?status=in_progress&priority=low')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(len(data), 1)

    def test_create_task(self):
        new_task = {
            "title": "New Task",
            "description": "New Description",
            "status": "to_do",
            "priority": "high",
            "due_date": "2023-05-17"
        }
        response = self.client.post('/tasks', json=new_task)
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIsNotNone(data['id'])

        task = Task.query.filter_by(title="New Task").first()
        self.assertIsNotNone(task)
        self.assertEqual(task.description, "New Description")
        self.assertEqual(task.status, "to_do")
        self.assertEqual(task.priority, "high")
        self.assertEqual(task.due_date, date(2023, 5, 17))

    def test_create_task_with_invalid_data(self):
        invalid_task = {
            "title": "New Task",
            "description": "New Description",
            "status": "invalid status",
            "priority": "invalid priority",
            "due_date": "invalid date"
        }
        response = self.client.post('/tasks', json=invalid_task)
        self.assertEqual(response.status_code, 422)

    def test_update_task_successfully(self):
        data = {'title': 'Updated Test Task', 'description': 'This is an updated test task', 'status': 'completed',
                'priority': 'high', 'due_date': str(date.today())}

        response = self.client.put(f'/tasks/{self.task1.id}', data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 200)

        updated_task = Task.query.get(self.task1.id)
        self.assertEqual(updated_task.title, "Updated Test Task")
        self.assertEqual(updated_task.description, "This is an updated test task")
        self.assertEqual(updated_task.status, "completed")
        self.assertEqual(updated_task.priority, "high")
        self.assertEqual(updated_task.due_date, date.today())

        result = self.task_schema.dump(updated_task)
        self.assertEqual(result, json.loads(response.data))

    def test_update_task_not_found(self):
        data = {'title': 'Updated Test Task', 'description': 'This is an updated test task', 'status': 'completed',
                'priority': 'high', 'due_date': str(date.today())}

        response = self.client.put('/tasks/999', data=json.dumps(data), content_type='application/json')

        self.assertEqual(response.status_code, 404)

    def test_update_task_with_invalid_data(self):
        data = {'title': '', 'status': 'invalid_status', 'priority': 'high', 'due_date': 'invalid_date'}

        response = self.client.put(f'/tasks/{self.task1.id}', data=json.dumps(data),
                                   content_type='application/json')

        self.assertEqual(response.status_code, 400)

        updated_task = Task.query.get(self.task1.id)
        self.assertEqual(updated_task.title, "Task 1")
        self.assertEqual(updated_task.status, "in_progress")
        self.assertEqual(updated_task.priority, "low")

    def test_delete_task(self):
        response = self.client.delete(f'/tasks/{self.task2.id}')

        self.assertEqual(response.status_code, 200)

        deleted_task = Task.query.get(self.task2.id)
        self.assertEqual(deleted_task, None)

        expected_message = {'message': 'Task successfully deleted'}
        self.assertEqual(response.get_json(), expected_message)

    def test_get_task(self):
        response = self.client.get(f'/tasks/{self.task1.id}')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['title'], 'Task 1')
        self.assertEqual(response.json['description'], 'Description 1')
        self.assertEqual(response.json['status'], 'in_progress')
        self.assertEqual(response.json['priority'], "low")
        self.assertEqual(response.json['due_date'], '2023-05-15')

    def test_get_non_existent_task(self):
        response = self.client.get('/tasks/999')
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json['error'], 'Task not found')
