from src.api.v1.endpoints import new_task, get_all_tasks, get_task, change_task, check_memory
from src.settings import app


app.add_url_rule("/api/v1/create-task", view_func=new_task, methods=["POST"])
app.add_url_rule("/api/v1/get-all-tasks", view_func=get_all_tasks, methods=["GET"])
app.add_url_rule("/api/v1/get-task/<int:task_id>", view_func=get_task, methods=["GET"])
app.add_url_rule("/api/v1/change-task/<int:task_id>", view_func=change_task, methods=["PUT"])
app.add_url_rule("/api/v1/memory-alarm", view_func=check_memory, methods=["POST"])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)

