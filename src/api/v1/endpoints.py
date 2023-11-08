from typing import List, Dict

from apiflask import HTTPError
from apiflask.app import Response

from src.database.repositories import TaskRepository
from src.settings import app
from src.validation.models import TaskModel, MemoryModel


@app.route("/api/v1/create-task", methods=['POST'])
@app.input(TaskModel)
def new_task(json_data) -> Response:
    """
    Create new task in db
    :param json_data: input data from user
    :return: new task id or raise Integrity error
    """
    return app.response_class(
        response=TaskRepository().insert(params=json_data),
        status=201,
        mimetype="application/json"
    )


@app.route("/api/v1/get-all-tasks", methods=['GET'])
def get_all_tasks() -> List[Dict]:
    """
    Get all tasks from database
    :return: list of tasks from db
    """
    return TaskRepository().get_all()


@app.route("/api/v1/get-task/<int:task_id>", methods=["GET"])
def get_task(task_id: int) -> Dict:
    """
    Get task by id
    :param task_id: id of task
    :return: task data from db or raise Not found error
    """
    task = TaskRepository().get(id_=task_id)
    if not task:
        raise HTTPError(status_code=404, message="Not found", detail="Task was not found")
    return task


@app.route("/api/v1/change-task/<int:task_id>", methods=["PUT"])
@app.input(TaskModel)
def change_task(task_id: int, json_data) -> Response:
    """
    Change the task parameters
    :param task_id: id of the task need to change
    :param json_data: user's input data
    :return: id of the task was changed or raise Not found error
    """
    return Response(
        response=TaskRepository().put(task_id=task_id, params=json_data),
        status=200,
        mimetype="application/json"
    )


@app.route("/api/v1/memory-alarm", methods=["POST"])
@app.input(MemoryModel)
def check_memory(json_data):
    """
    Alarm if memory size is high
    :param json_data: memory data
    :return: response with status 200 OK
    """
    print(f"ALARM ! Used memory is: {json_data.get('used_memory')}. Alarm memory level is "
          f"{json_data.get('alarm_memory_value')}")
    return Response(
        status=200
    )



