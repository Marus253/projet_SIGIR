import qrcode
from io import BytesIO
from django.core.files.base import ContentFile

def generate_qr_code(data):
    qr = qrcode.make(data)
    stream = BytesIO()
    qr.save(stream, "PNG")
    return ContentFile(stream.getvalue())
