import math
import colorsys
from PIL import Image, ImageDraw, ImageFilter

WIDTH, HEIGHT = 800, 280
FPS = 18
DURATION_SECONDS = 12
FRAME_COUNT = FPS * DURATION_SECONDS

BAR_COUNT = 42
BAR_WIDTH = 12
GAP = 6
BASELINE = 235
MAX_HEIGHT = 205

SEGMENT_HEIGHT = 8
SEGMENT_GAP = 3


def neon_color(position, time):
    """Dégradé néon rose, violet, bleu et cyan."""
    hue = (0.91 - position * 0.47 + 0.035 * math.sin(time * 0.7)) % 1.0
    rgb = colorsys.hsv_to_rgb(hue, 0.88, 1.0)
    return tuple(int(channel * 255) for channel in rgb)


def make_frame(frame_index):
    time = frame_index / FPS
    image = Image.new("RGBA", (WIDTH, HEIGHT), (3, 4, 13, 255))

    bar_area_width = BAR_COUNT * (BAR_WIDTH + GAP) - GAP
    start_x = (WIDTH - bar_area_width) // 2
    heights = []

    # Grandes vagues combinées et pics mobiles pour une forte amplitude.
    for i in range(BAR_COUNT):
        position = i / (BAR_COUNT - 1)
        beat = time * 2 * math.pi

        wave = (
            0.48
            + 0.29 * math.sin(beat * 0.65 - i * 0.24)
            + 0.22 * math.sin(beat * 1.15 + i * 0.37)
            + 0.15 * math.sin(beat * 1.8 - i * 0.62)
        )

        peak = max(0, math.sin(beat * 0.5 - i * 0.27)) ** 3
        wave += 0.55 * peak

        center_shape = 0.72 + 0.28 * (
            1 - abs(position - 0.5) * 1.7
        )

        height = int(MAX_HEIGHT * max(0.05, wave) * center_shape)
        heights.append(max(8, min(height, MAX_HEIGHT)))

    # Halo néon doux derrière les barres. Aucun flash.
    glow = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow)

    for i, height in enumerate(heights):
        x = start_x + i * (BAR_WIDTH + GAP)
        color = neon_color(i / (BAR_COUNT - 1), time)

        glow_draw.rounded_rectangle(
            (
                x - 6,
                BASELINE - height - 6,
                x + BAR_WIDTH + 6,
                BASELINE + 3,
            ),
            radius=8,
            fill=(*color, 65),
        )

    glow = glow.filter(ImageFilter.GaussianBlur(17))
    image = Image.alpha_composite(image, glow)
    draw = ImageDraw.Draw(image)

    draw.line(
        (
            start_x - 18,
            BASELINE + 8,
            start_x + bar_area_width + 18,
            BASELINE + 8,
        ),
        fill=(75, 95, 160, 130),
        width=2,
    )

    step = SEGMENT_HEIGHT + SEGMENT_GAP

    for i, height in enumerate(heights):
        x = start_x + i * (BAR_WIDTH + GAP)
        color = neon_color(i / (BAR_COUNT - 1), time)
        segment_count = max(1, height // step)

        for segment in range(segment_count):
            y_bottom = BASELINE - segment * step
            y_top = y_bottom - SEGMENT_HEIGHT

            brightness = 1.0 if segment == segment_count - 1 else 0.82
            segment_color = tuple(int(channel * brightness) for channel in color)

            draw.rounded_rectangle(
                (x, y_top, x + BAR_WIDTH, y_bottom),
                radius=2,
                fill=(*segment_color, 255),
            )

            if segment == segment_count - 1:
                draw.line(
                    (x + 2, y_top + 1, x + BAR_WIDTH - 2, y_top + 1),
                    fill=(255, 255, 255, 210),
                    width=1,
                )

    return image.convert("RGB")


frames = [make_frame(i) for i in range(FRAME_COUNT)]

frames[0].save(
    "ibiza_dj.gif",
    save_all=True,
    append_images=frames[1:],
    duration=1000 // FPS,
    loop=0,
    optimize=True,
)

print(f"GIF créé : equalizer.gif ({DURATION_SECONDS} secondes)")