from sqlalchemy import Column, Integer, String, Text, Enum, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .connection import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    email = Column(String(150), unique=True, index=True, nullable=False)
    password_hash = Column(String(200), nullable=False)
    role = Column(Enum("user","admin", name= "user_roles"), default = "user", nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # relationship - one user has many todos
    todos = relationship("Todo", back_populates="owner")


class Todo(Base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum("pending", "completed", name="todo_status"), default="pending")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # foreign Key
    user_id = Column(Integer, ForeignKey("users.id"))

    # Relationship → each todo belongs to one user
    owner = relationship("User", back_populates="todos")
