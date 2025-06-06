from ninja import Schema
from pydantic import BaseModel
from typing import  List
from datetime import datetime

class NinjaResponseSchema(BaseModel):
    status_code: int
    stdout: str
    stderr: str
    log: str

    model_config = {
        "arbitrary_types_allowed": True,
    }

class AuthSchema(Schema):
    username: str
    password: str

class ExecuteInput(BaseModel):
    binary: str
    command: str
    args: List[str] = []

    model_config = {
        "arbitrary_types_allowed": True,
    }

class ExecuteOutput(Schema):
    status_code: int
    stdout: str
    stderr: str
    log: str

class LogOutput(BaseModel):
    id: int
    timestamp: datetime
    binary: str
    command: str
    args: List[str]
    stdout: str
    stderr: str
    status_code: int

    model_config = {
        "arbitrary_types_allowed": True,
    }