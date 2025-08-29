import os
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from PIL import Image, ImageDraw, ImageFont
from dotenv import load_dotenv
from qrgenerator.models import QrImage
load_dotenv()

TEXT_COLOR = "#661DAF"

def draw_border(draw, text_position, text_width, text_height, padding=100, border_thickness=4, color=TEXT_COLOR):
    x, y = text_position
    # Calculate rectangle coordinates with padding
    rect_x0 = x - padding * 6
    rect_y0 = y - padding * 6
    rect_x1 = x + text_width + padding * 7
    rect_y1 = y + text_height + padding * 7

    # Draw single rectangle with stroke thickness
    draw.rectangle(
        [rect_x0, rect_y0, rect_x1, rect_y1],
        outline=color,
        width=border_thickness
    )


def create_text_image(text, font_size=32):
    font = ImageFont.load_default(font_size)
    bbox = font.getbbox(text)
    text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
    image = Image.new('RGB', (text_width + 100, text_height + 100), 'white')
    draw = ImageDraw.Draw(image)
    draw.text((50, 30), text, fill=TEXT_COLOR, font=font, stroke_width=4)
    draw_border(draw, (50, 50), text_width, text_height, 5, 8)
    # image.show()
    return image


def generate_qr_code(url, text, font_size=100):

    logo = create_text_image(text, font_size)
    basewidth = 40
    wpercent = (basewidth / float(logo.size[0]))
    hsize = int((float(logo.size[1]) * float(wpercent)))
    logo = logo.resize((basewidth, hsize), Image.Resampling.LANCZOS)
    
    QRcode = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    QRcode.add_data(url)
    QRcode.make()

    QRimg = QRcode.make_image(fill_color="black", back_color="white").convert('RGB')

    # set size of QR code
    pos = ((QRimg.size[0] - logo.size[0]) // 2, (QRimg.size[1] - logo.size[1]) // 2)
    QRimg.paste(logo, pos)
    return QRimg


def gen_images(tables, restaurant_id, base_url=''):
    if not base_url:
        base_url = os.environ.get('BASE_URL')
    for i in range(int(tables)):
        table_number = str(i + 1).zfill(2)
        file_name = f"qr_code_{restaurant_id}_{table_number}.PNG"
        full_url = f"{base_url}/{restaurant_id}/{table_number}"
        qr_image = generate_qr_code(full_url, text=table_number)
        image_model = QrImage.add(restaurant_id=restaurant_id, table_number=table_number)
        upload_to_media(qr_img=qr_image, image_model=image_model, filename=file_name)
    

def upload_to_media(qr_img, image_model, filename):
    buffer = BytesIO()
    qr_img.save(buffer, format='PNG')
    image_file = ContentFile(buffer.getvalue(), name=filename)

    # Assign directly to the field
    setattr(image_model, "image_field", image_file)
    image_model.save()


if __name__ == "__main__":
    
    restaurant_id = 1
    tables = 5
    gen_images(tables, restaurant_id)
    print(f"Generated {tables} QR codes for restaurant {restaurant_id}.")
