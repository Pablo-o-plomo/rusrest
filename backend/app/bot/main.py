import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
from pathlib import Path
from app.core.config import settings
from app.db.session import SessionLocal
from app.services.imports import process_uploaded_file, UPLOAD_DIR

bot=Bot(token=settings.admin_telegram_bot_token)
dp=Dispatcher()

@dp.message(Command('start'))
async def start(m:Message): await m.answer('Отправьте файл с подписью: SOCHI R02 2026-05-01')

@dp.message(F.document)
async def upload_doc(m:Message):
    if not m.caption:
        return await m.answer('Добавьте caption: REST_CODE REPORT_CODE YYYY-MM-DD')
    parts=m.caption.split(); rest,report=parts[0].upper(),parts[1].upper()
    file=await bot.get_file(m.document.file_id)
    dst=UPLOAD_DIR/f"tg_{m.document.file_name}"
    await bot.download_file(file.file_path, destination=dst)
    db=SessionLocal()
    try:
        imp=process_uploaded_file(db, restaurant_code=rest, report_code=report, filename=m.document.file_name, source_path=Path(dst), source='telegram')
        await m.answer(f'Импорт создан: {imp.id}, статус: {imp.status.value}')
    except Exception as e:
        await m.answer(f'Ошибка: {e}')
    finally:
        db.close()

if __name__=='__main__':
    asyncio.run(dp.start_polling(bot))
