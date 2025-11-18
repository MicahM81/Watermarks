from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


def apply_watermark(input_path: str, watermark_text: str) -> str:
    """
    Takes a path to an image, adds a simple text watermark,
    and saves a new image next to the original.
    Returns the output file path.
    """
    input_path = Path(input_path)
    image = Image.open(input_path).convert("RGBA")

    # Create watermark overlay
    watermark_text = watermark_text
    width, height = image.size
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    # Use a basic font; you can customize later
    font_size = max(20, width // 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0,0),text=watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Bottom-right corner with small padding
    padding = 10
    x = width - text_width - padding
    y = height - text_height - padding

    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    # Combine original image with watermark overlay
    watermarked = Image.alpha_composite(image, watermark_layer)

    # Save result next to original
    output_path = input_path.with_name(f"{input_path.stem}_watermarked{input_path.suffix}")
    watermarked.convert("RGB").save(output_path)

    return str(output_path)

def apply_watermark_preview(input_path: str, watermark_text: str):
    from PIL import Image, ImageDraw, ImageFont

    image = Image.open(input_path).convert("RGBA")

    width, height = image.size
    watermark_layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(watermark_layer)

    font_size = max(20, width // 20)
    try:
        font = ImageFont.truetype("arial.ttf", font_size)
    except OSError:
        font = ImageFont.load_default()

    bbox = draw.textbbox((0, 0), watermark_text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    padding = 10
    x = width - text_width - padding
    y = height - text_height - padding

    draw.text((x, y), watermark_text, font=font, fill=(255, 255, 255, 128))

    watermarked = Image.alpha_composite(image, watermark_layer)

    return watermarked.convert("RGB")
