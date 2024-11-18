from aiogram import Router, F, types
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
import logging

from logger import configure_logging
from keyboards import create_markup, home_menu_markup, profile_menu_markup
from json_actions import get_json_data, set_json_data
from interface import *

router = Router()

logger = logging.getLogger(__name__)
configure_logging(logging.DEBUG)


class AddChat(StatesGroup):
    name = State()


class AddGroupName(StatesGroup):
    name = State()


class RemoveGroupName(StatesGroup):
    name = State()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    logger.debug("cmd_start - start")

    chat_id = message.chat.id
    data = await get_json_data()

    await message.answer(text=start_text)

    if f"{chat_id}" in data.keys():
        await home_menu(message)
    else:
        await create_session(message, state)


async def create_session(message: Message, state: FSMContext):
    logger.debug("create_session - start")

    await state.set_state(AddChat.name)
    await message.answer("enter session name")


@router.message(AddChat.name)
async def set_session_name(message: Message, state: FSMContext):
    logger.debug("set_session_name - start")

    await state.update_data(name=message.text)
    name = await state.get_data()
    await state.clear()

    data = await get_json_data()
    data[f"{message.chat.id}"] = {"name":f"{name["name"]}"}
    await set_json_data(data)
    await home_menu(message)


@router.message(Command("info"))
async def info_cmd(message: Message):
    await message.answer(text="info panel")


@router.message(Command("home"))
async def home_menu(message: Message):
    logger.debug("home_menu - start")

    chat_id = message.chat.id
    data = await get_json_data()

    await message.answer(text=f"{data[f"{chat_id}"]["name"]}", reply_markup=home_menu_markup)


@router.message(F.text == children_list_btn)
@router.message(Command("group"))
async def groups_menu(message: Message):
    logger.debug("groups_menu - start")

    data = await get_json_data()
    buttons = {f"call_group_{i}": key for i, key in enumerate(data[f"{message.chat.id}"]["pool"].keys())}
    logger.info("buttons comprehension: %s", buttons)
    buttons.update({"add_group":"add"})

    if buttons != {"add_group":"add"}:
        buttons.update({"remove_group":"remove"})

    markup = await create_markup(buttons)
    await message.answer(text="Groups:", reply_markup=markup)


@router.callback_query(F.data == "add_group")
async def add_group(call: CallbackQuery, state: FSMContext):
    logger.debug("callback add_group - start")
    await call.answer()
    await state.set_state(AddGroupName.name)
    await call.message.answer("enter group name")


@router.callback_query(F.data == "remove_group")
async def remove_group(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state(RemoveGroupName.name)
    await call.message.answer("enter group name to delete")


@router.message(RemoveGroupName.name)
async def remove_group_name(message: Message, state: FSMContext):
    data = await get_json_data()
    chat_id = message.chat.id

    if message.text in data[f"{chat_id}"]["pool"].keys():
        await state.update_data(name=message.text)
        name = await state.get_data()
        data[f"{chat_id}"]["pool"].pop(name["name"])
        await set_json_data(data)
        await message.answer("succesfully deleted")

    elif message.text == "stop":
        pass

    else:
        await message.answer(text="Don't have such a group")
        return

    await groups_menu(message)
    await state.clear()


@router.message(AddGroupName.name)
async def add_group_name(message: Message, state:FSMContext):
    logger.debug("add_group_name - start")

    data = await get_json_data()
    chat_id = message.chat.id

    if message.text in data[f"{chat_id}"]["pool"].keys():
        logger.info("group name already ocupid, resatrt")
        await message.answer(text="Group name already exists. try again")
        return

    elif message.text == "stop":
        pass

    else:
        await message.answer(text="Successfully added group")
        await state.update_data(name=message.text)
        name = await state.get_data()

        data[f"{chat_id}"]["pool"].update({f"{name["name"]}":[]})
        await set_json_data(data)

    await groups_menu(message)
    await state.clear()


async def button_callback_handler(callback_query: types.CallbackQuery):
    if callback_query.data.startswith("call_group_"):
        logger.info("callback groups: %s", callback_query.data)
        await callback_query.message.answer(f"{callback_query.data}")

