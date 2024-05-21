import asyncio
import fitz
import io
import base64
from PIL import Image
from .open_ai_service import handle_image
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)


async def handle_pdf(file):
    pdf_bytes = await file.read()
    images_base64 = []

    try:
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")

        for page_num in range(len(pdf)):
            page = pdf[page_num]
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes()))
            # img.save(f'output_{page_num + 1}.png', 'PNG', quality=100) #SAVE images for test
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=100)
            img_base64 = base64.b64encode(buffered.getvalue()).decode('utf-8')
            images_base64.append(img_base64)

        result = await handle_image(images_base64)

        return result
    except Exception as e:
        logger.error(f"Error processing PDF: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if pdf and not pdf.is_closed:
            pdf.close()
