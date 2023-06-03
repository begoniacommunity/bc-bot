from aiogram import Bot, Dispatcher, executor, types
import asyncio

async def exec_command(command):
    command = " ".join(command)
    process = await asyncio.create_subprocess_shell(command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
        shell=True)
    stdout, stderr = await process.communicate()
    return stdout.decode(), stderr.decode(), process.returncode

async def exec(message: types.Message):
    arg = message.get_args()
    if not arg:
        await message.reply("Пожалуйста, укажите команду для выполнения.")
        return
    command = arg.split()
    stdout, stderr, returncode = await exec_command(command)

    chat_type = message.chat.type
    if chat_type == "private":
        chat_id = message.from_user.id
    else:
        chat_id = message.chat.id

    first_message = None

    if stdout:
        if not first_message:
            first_message = f"{stdout}"
        else:
            await message.answer(chat_id, f"{stdout}")

    if stderr:
        if not first_message:
            first_message = f"{stderr}"
        else:
            await message.answer(chat_id, f"{stderr}")

    if returncode != 0:
        if not first_message:
            first_message = f"Код возврата: {returncode}"
        else:
            await message.answer(chat_id, f"Код возврата: {returncode}")

    if first_message:
        await message.reply(first_message)
