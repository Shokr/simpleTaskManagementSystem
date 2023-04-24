from datetime import datetime

from flask import jsonify, request

from app import db
from models.task import Task
from schema.task import TaskSchema
from . import api_bp

task_schema = TaskSchema()


@api_bp.route('/tasks', methods=['GET'])
def get_tasks():
    try:
        # Get query parameters
        status = request.args.get('status')
        priority = request.args.get('priority')

        # Get all tasks or filtered tasks
        if status is None and priority is None:
            tasks = Task.query.all()
        elif status is not None and priority is None:
            tasks = Task.query.filter_by(status=status).all()
        elif status is None and priority is not None:
            tasks = Task.query.filter_by(priority=priority).all()
        else:
            tasks = Task.query.filter_by(status=status, priority=priority).all()

        if not tasks:
            return jsonify({'error': 'Tasks not found'}), 404

        # Serialize the tasks and return response
        serialized_tasks = list(map(lambda task: task_schema.dump(task), tasks))
        return jsonify(serialized_tasks), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    try:
        task = Task.query.get(task_id)
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        result = task_schema.dump(task)
        return jsonify(result), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tasks', methods=['POST'])
def create_task():
    try:
        # Parse request body
        data = request.get_json()

        # Validate request body
        errors = task_schema.validate(data)
        if errors:
            return jsonify(errors), 422

        # Create new task
        title = data['title']
        description = data['description']
        status = data['status']
        priority = data['priority']
        due_date_str = data['due_date']
        due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

        new_task = Task(title=title, description=description, status=status, priority=priority, due_date=due_date)

        db.session.add(new_task)
        db.session.commit()

        # Return response
        result = task_schema.dump(new_task)
        return jsonify(result), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    try:
        # get the task to update
        task = Task.query.get(task_id)

        # check if the task exists
        if not task:
            return jsonify({'error': 'Task not found'}), 404

        # get the request data
        data = request.get_json()

        # validate the request data
        errors = task_schema.validate(data, partial=True)
        if errors:
            return jsonify({'error': errors}), 400

        # update the task with the request data
        if 'title' in data:
            task.title = data['title']
        if 'description' in data:
            task.description = data['description']
        if 'status' in data:
            task.status = data['status']
        if 'priority' in data:
            task.priority = data['priority']
        if 'due_date' in data:
            due_date_str = data['due_date']
            due_date = datetime.strptime(due_date_str, '%Y-%m-%d').date()

            task.due_date = due_date

        print(task)

        # commit the changes to the database
        db.session.commit()

        result = task_schema.dump(task)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@api_bp.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    try:
        task = Task.query.get(task_id)

        if not task:
            return jsonify({'error': 'Task not found'}), 404

        db.session.delete(task)
        db.session.commit()

        return jsonify({'message': 'Task successfully deleted'}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
