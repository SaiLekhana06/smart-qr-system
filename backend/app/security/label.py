from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

from reportlab.pdfgen import canvas
from reportlab.lib.units import mm


LABEL_DIR = Path(__file__).resolve().parents[3] / "generated_labels"
LABEL_DIR.mkdir(exist_ok=True)


def generate_label(
    qr_image_path: str,
    product_name: str,
    sku: str,
    qr_id: int
) -> str:

    qr_img = Image.open(qr_image_path)

    qr_size = 300

    # Keep QR edges sharp
    qr_img = qr_img.resize(
        (qr_size, qr_size),
        Image.Resampling.NEAREST
    )

    label_width = 400
    label_height = qr_size + 100

    label = Image.new(
        "RGB",
        (label_width, label_height),
        "white"
    )

    qr_x = (label_width - qr_size) // 2

    label.paste(qr_img, (qr_x, 20))

    draw = ImageDraw.Draw(label)
    font = ImageFont.load_default()

    text_y = qr_size + 30

    draw.text(
        (20, text_y),
        f"Product: {product_name}",
        fill="black",
        font=font
    )

    draw.text(
        (20, text_y + 20),
        f"SKU: {sku}",
        fill="black",
        font=font
    )

    draw.text(
        (20, text_y + 40),
        "Scan to verify authenticity",
        fill="black",
        font=font
    )

    filename = f"label_{qr_id}.png"
    filepath = LABEL_DIR / filename

    label.save(filepath)

    return str(filepath)


def generate_label_pdf(
    label_image_path: str,
    qr_id: int
) -> str:

    filename = f"label_{qr_id}.pdf"
    filepath = LABEL_DIR / filename

    label_img = Image.open(label_image_path)

    width_px, height_px = label_img.size

    # Convert pixels → mm
    width_mm = width_px * 0.264583
    height_mm = height_px * 0.264583

    c = canvas.Canvas(
        str(filepath),
        pagesize=(
            width_mm * mm,
            height_mm * mm
        )
    )

    c.drawImage(
        label_image_path,
        0,
        0,
        width=width_mm * mm,
        height=height_mm * mm
    )

    c.save()

    return str(filepath)