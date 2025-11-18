import qrcode
import io
import base64
import uuid

def generate_qr_code(data: str) -> str:
    """Генерирует QR код и возвращает base64 строку"""
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Конвертируем в base64
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return f"data:image/png;base64,{img_str}"

def generate_ticket_qr(ticket_id: int, user_id: int) -> str:
    """Генерирует уникальный QR код для билета"""
    unique_code = str(uuid.uuid4())
    data = f"TICKET:{ticket_id}:USER:{user_id}:CODE:{unique_code}"
    return generate_qr_code(data)