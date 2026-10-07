import os

import boto3
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


AWS_REGION = os.getenv("AWS_REGION", "us-east-2")
DYNAMODB_TABLE = os.getenv("DYNAMODB_TABLE", "todo-app-todos")


dynamodb = boto3.resource(
    "dynamodb",
    region_name=AWS_REGION
)

table = dynamodb.Table(DYNAMODB_TABLE)


app = FastAPI(
    title="Todo API",
    version="1.0.0"
)


class TodoCreate(BaseModel):
    title: str


class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/todos")
def get_todos():
    response = table.scan()

    items = response.get("Items", [])

    return items


@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):

    response = table.scan(
        ProjectionExpression="id"
    )

    items = response.get("Items", [])

    if items:
        next_id = max(int(item["id"]) for item in items) + 1
    else:
        next_id = 1

    new_todo = {
        "id": next_id,
        "title": todo.title,
        "completed": False
    }

    table.put_item(Item=new_todo)

    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, todo: TodoCreate):

    response = table.get_item(
        Key={"id": todo_id}
    )

    if "Item" not in response:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    updated_todo = {
        "id": todo_id,
        "title": todo.title,
        "completed": response["Item"].get(
            "completed",
            False
        )
    }

    table.put_item(Item=updated_todo)

    return updated_todo


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):

    response = table.get_item(
        Key={"id": todo_id}
    )

    if "Item" not in response:
        raise HTTPException(
            status_code=404,
            detail="Todo not found"
        )

    table.delete_item(
        Key={"id": todo_id}
    )

    return {"message": "Todo deleted"}
