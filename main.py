from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import FileResponse
from src.file_service import handle_pdf
import aiohttp

app = FastAPI()

@app.get('/')
async def index():
    return "Hello :)"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    if file.filename.endswith('.pdf'):
        return await handle_pdf(file)

    raise HTTPException(status_code=400, detail="Unsupported file format")


@app.post("/url/")
async def download_file_from_link(url: str):
    if url.endswith('.pdf'):
        print(url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status == 200:
                    return await handle_pdf(response)
                else:
                    raise HTTPException(
                        status_code=400, detail="Error downloading the file")

    raise HTTPException(status_code=400, detail="Unsupported file format")

# @app.get("/share/short.pdf")
# def share_file():
#     return FileResponse("share/short.pdf")