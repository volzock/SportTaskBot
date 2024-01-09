from aiogram import Router, types
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
from sqlalchemy.orm import Session

from database import db, User
from docmaster import docmaster

service_router = Router()

@service_router.message(Command("service"))
async def service(message: Message, state: FSMContext) -> None:
    pass
