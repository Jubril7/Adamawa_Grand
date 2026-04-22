"""
Generate styled placeholder images for rooms and hero slides.
Run with: python3 generate_images.py
"""
import os, math
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from PIL import Image, ImageDraw, ImageFont
from rooms.models import Room
from pages.models import HeroSlide

NAVY   = (28, 43, 58)
NAVY2  = (13, 27, 42)
GOLD   = (184, 134, 11)
GOLD_L = (212, 160, 23)
WHITE  = (255, 255, 255)
CREAM  = (245, 237, 213)


def lerp_color(c1, c2, t):
    return tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3))


def draw_gradient(draw, w, h, top_color, bottom_color):
    for y in range(h):
        t = y / h
        color = lerp_color(top_color, bottom_color, t)
        draw.line([(0, y), (w, y)], fill=color)


def draw_pattern(img, color, count=8):
    """Draw subtle diagonal lines as a texture."""
    draw = ImageDraw.Draw(img)
    w, h = img.size
    spacing = w // count
    for i in range(-h, w + h, spacing):
        draw.line([(i, 0), (i + h, h)], fill=(*color, 18), width=2)


def add_gold_bar(draw, w, h):
    bar_h = 6
    for x in range(w):
        t = x / w
        c = lerp_color(GOLD, GOLD_L, t)
        draw.line([(x, h - bar_h), (x, h)], fill=c)


def make_room_image(filename, room_number, room_type, floor):
    W, H = 800, 560

    # Different gradient per room type
    gradients = {
        'Standard':          (NAVY2, (30, 55, 75)),
        'Deluxe':            ((20, 40, 60), (45, 70, 90)),
        'Suite':             ((15, 30, 50), (40, 60, 80)),
        'Presidential Suite':((10, 20, 35), (35, 55, 75)),
    }
    top, bot = gradients.get(room_type, (NAVY2, NAVY))

    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img, 'RGBA')

    draw_gradient(draw, W, H, top, bot)

    # Diagonal texture
    draw_pattern(img, (255, 255, 255), count=12)

    # Re-draw after texture
    draw = ImageDraw.Draw(img)

    # Decorative circle (blurred glow)
    cx, cy = int(W * 0.72), int(H * 0.38)
    for r in range(180, 0, -4):
        alpha = int(12 * (1 - r / 180))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*GOLD, alpha))

    # Gold accent bar bottom
    add_gold_bar(draw, W, H)

    # Gold horizontal rule
    rule_y = H // 2 - 20
    draw.rectangle([60, rule_y, 160, rule_y + 2], fill=GOLD_L)

    # Room type label (small caps)
    try:
        font_sm  = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 18)
        font_med = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
        font_lg  = ImageFont.truetype('/System/Library/Fonts/Georgia.ttf',   62)
    except:
        font_sm  = ImageFont.load_default()
        font_med = ImageFont.load_default()
        font_lg  = ImageFont.load_default()

    draw.text((60, rule_y - 44), room_type.upper(), font=font_sm, fill=GOLD_L)
    draw.text((60, rule_y + 14), f'ROOM {room_number}', font=font_lg, fill=WHITE)
    draw.text((60, rule_y + 90), f'Floor {floor}  ·  Adamawa Grand Hotel & Suites', font=font_sm, fill=(*CREAM, 180))

    # Small decorative squares
    sq = 8
    for i, offset in enumerate([0, 14, 28]):
        c = GOLD if i == 0 else (*GOLD, 120)
        draw.rectangle([60 + offset, H - 42, 60 + offset + sq, H - 42 + sq], fill=c)

    path = f'/Users/jubrilafc/Documents/HotelRoomBooking/media/rooms/{filename}'
    img.save(path, 'JPEG', quality=92)
    print(f'  Created: {filename}')
    return f'rooms/{filename}'


def make_slide_image(filename, title, subtitle, variant=0):
    W, H = 1400, 800

    palettes = [
        ((10, 20, 35), (28, 43, 58)),
        ((15, 30, 50), (8, 20, 38)),
        ((20, 15, 35), (30, 43, 60)),
    ]
    top, bot = palettes[variant % len(palettes)]

    img = Image.new('RGB', (W, H))
    draw = ImageDraw.Draw(img, 'RGBA')

    draw_gradient(draw, W, H, top, bot)
    draw_pattern(img, (255, 255, 255), count=16)

    draw = ImageDraw.Draw(img)

    # Large glow orb
    cx, cy = int(W * 0.75), int(H * 0.4)
    for r in range(320, 0, -6):
        alpha = int(10 * (1 - r / 320))
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(*GOLD, alpha))

    # Gold bottom bar
    add_gold_bar(draw, W, H)

    # Gold rule line
    rule_y = H // 2 - 60
    draw.rectangle([80, rule_y, 220, rule_y + 3], fill=GOLD)

    try:
        font_eyebrow = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 22)
        font_title   = ImageFont.truetype('/System/Library/Fonts/Georgia.ttf',   88)
        font_sub     = ImageFont.truetype('/System/Library/Fonts/Helvetica.ttc', 28)
    except:
        font_eyebrow = ImageFont.load_default()
        font_title   = ImageFont.load_default()
        font_sub     = ImageFont.load_default()

    draw.text((80, rule_y - 52), 'ADAMAWA GRAND HOTEL & SUITES', font=font_eyebrow, fill=GOLD_L)
    draw.text((80, rule_y + 16), title, font=font_title, fill=WHITE)
    if subtitle:
        draw.text((80, rule_y + 118), subtitle, font=font_sub, fill=(*CREAM, 200))

    # Bottom decorative row
    for i in range(5):
        x = 80 + i * 18
        draw.rectangle([x, H - 48, x + 10, H - 48 + 10], fill=(*GOLD, 180 if i == 0 else 80))

    path = f'/Users/jubrilafc/Documents/HotelRoomBooking/media/slides/{filename}'
    img.save(path, 'JPEG', quality=93)
    print(f'  Created: {filename}')
    return f'slides/{filename}'


# ── Generate Room Images ──────────────────────────────────────
print('\nGenerating room images...')
rooms = Room.objects.all().order_by('room_number')
for room in rooms:
    fname = f'room_{room.room_number}.jpg'
    rel_path = make_room_image(fname, room.room_number, str(room.room_type), room.floor)
    room.image = rel_path
    room.save(update_fields=['image'])

# ── Generate Hero Slide Images ────────────────────────────────
print('\nGenerating hero slide images...')
slides_data = [
    ('slide_1.jpg', 'Welcome to Adamawa Grand', 'Luxury & Comfort in the Heart of Yola, Nigeria', 0),
    ('slide_2.jpg', 'Experience True Luxury',   'Elegantly Designed Rooms & World-Class Service',  1),
    ('slide_3.jpg', 'Discover Adamawa State',   'Kiri Dam · Sukur UNESCO Site · Mandara Mountains', 2),
]

HeroSlide.objects.all().delete()
for i, (fname, title, sub, variant) in enumerate(slides_data):
    rel_path = make_slide_image(fname, title, sub, variant)
    HeroSlide.objects.create(
        title=title,
        subtitle=sub,
        image=rel_path,
        is_active=True,
        order=i,
    )

print(f'\nDone. {Room.objects.exclude(image="").count()} rooms with images, {HeroSlide.objects.count()} hero slides.')
