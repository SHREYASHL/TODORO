from fastapi import APIRouter, Depends,HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List,Optional
from app.api.deps import get_db, get_current_user, require_admin
from app.database import models
from app.schemas.todo_schema import TodoCreate, TodoUpdate, TodoOut

router = APIRouter(prefix="/todos", tags=["Todos"])

#createe
@router.post("/", response_model=TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(
    todo: TodoCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    new_todo = models.Todo(
        title=todo.title,
        description=todo.description,
        user_id=current_user.id,
    )
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo)
    return new_todo

#readall
@router.get("/", response_model=List[TodoOut])
def read_todos(
    status: Optional[str] = Query(None, regex="^(pending|completed)$"),
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    query = db.query(models.Todo).filter(models.Todo.user_id == current_user.id)

    if status:
        query = query.filter(models.Todo.status == status)

    todos = query.offset(offset).limit(limit).all()
    return todos

#read one with id
@router.get("/{todo_id}", response_model=TodoOut)
def read_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    todo = (
        db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

#update
@router.put("/{todo_id}", response_model=TodoOut)
def update_todo(
    todo_id: int,
    todo_update: TodoUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    todo = (
        db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id == current_user.id).first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    if todo_update.title is not None:
        todo.title = todo_update.title
    if todo_update.description is not None:
        todo.description = todo_update.description
    if todo_update.status is not None:
        if todo_update.status not in ("pending", "completed"):
            raise HTTPException(
                status_code=400, detail="Status must be 'pending' or 'completed'"
            )
        todo.status = todo_update.status

    db.commit()
    db.refresh(todo)
    return todo

#delete
@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    todo_id: int,
    db: Session = Depends(get_db),
    admin_user: models.User = Depends(require_admin),
):
    todo = (
        db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.user_id).first()
    )
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")

    db.delete(todo)
    db.commit()
    return None
