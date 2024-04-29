import fitz
import io
import base64
from PIL import Image
from .open_ai_service import handle_image
from fastapi import HTTPException


async def handle_pdf(file):
    pdf_bytes = await file.read()
    page_count = 0
    images_base64 = []
    result = ''

    try:
        pdf = fitz.open(stream=pdf_bytes, filetype="pdf")
        page_count = len(pdf)

        for page_num in range(page_count):
            page = pdf[page_num]
            pix = page.get_pixmap(dpi=300)
            img = Image.open(io.BytesIO(pix.tobytes()))
            # img.save(f'output_{page_num + 1}.png', 'PNG', quality=100) #SAVE images for test
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG", quality=100)
            img_base64 = base64.b64encode(
                buffered.getvalue()).decode('utf-8')
            images_base64.append(img_base64)

        result = await handle_image(images_base64)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if pdf and not pdf.is_closed:
            pdf.close()

    return result
