from typing import Annotated
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, status, Path
from models import Todos
from database import SessionLocal
from .auth import get_current_user


router = APIRouter()

router = APIRouter(
  prefix='/todos',
  tags=['todos']
)

def get_db():
  db = SessionLocal()
  try:
    yield db
  finally:
    db.close()

db_dependencies = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
  title: str = Field(min_length=3)
  description: str = Field(min_length=3, max_length=100)
  priority: int = Field(gt=0, lt=6)
  complete: bool

# ToDo: Fetch All - GET
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all(user: user_dependency, db: db_dependencies):
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed!')
  
  return db.query(Todos).filter(Todos.owner_id == user.get('id')).all()


# ToDo: Fetch Single - GET
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user: user_dependency, db: db_dependencies, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed!')
  
  todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

  if todo_model is not None:
    return todo_model
  raise HTTPException(status_code=404, detail='Item Not Found')


# ToDo: Creat a todo - POST
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependencies, todo_request: TodoRequest):

  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed!')
  
  todo_model = Todos(**todo_request.model_dump(), owner_id=user.get('id'))

  db.add(todo_model)
  db.commit()


# ToDo: Update Todo - PUT
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user: user_dependency, db: db_dependencies, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed!')
  
  todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

  if todo_model is None:
    raise HTTPException(status_code=404, detail='Item Not Found')
  todo_model.title = todo_request.title
  todo_model.description = todo_request.description
  todo_model.priority = todo_request.priority
  todo_model.complete = todo_request.complete

  db.add(todo_model)
  db.commit()

#ToDo: Delete todo - DELETE
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user: user_dependency, db: db_dependencies, todo_id: int = Path(gt=0)):
  if user is None:
    raise HTTPException(status_code=401, detail='Authentication Failed!')
  
  todo_model = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()

  if todo_model is None:
    raise HTTPException(status_code=404, detail='Item Not Found')
  db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()

  db.commit()