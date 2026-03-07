import os
import aiofiles
from uuid import uuid4
from config import settings

class StorageProvider:
    async def save(self, file, filename: str) -> tuple[str, int]:
        raise NotImplementedError
    
class LocalStorage(StorageProvider):

    async def save(self, content, filename: str):
        os.makedirs(settings.LOCAL_UPLOAD_PATH, exist_ok=True)

        unique_name = f"{uuid4()}_{filename}"
        file_path = os.path.join(settings.LOCAL_UPLOAD_PATH, unique_name)

        async with aiofiles.open(file_path, "wb") as out_file:
            await out_file.write(content)

        return file_path, len(content)