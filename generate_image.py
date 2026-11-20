#!/usr/bin/env python3
"""Build entry.png: a one-image front page summing up Friday 20 November 2026.

Every headline below was reported on 20 November 2026 (see SOURCES.md).
The picture is drawn with Pillow from system fonts only, so the text is
sharp and correctly spelled. Run at build time only:

    python3 generate_image.py

It writes entry.png (1024 x 1024) next to this file. The graded program
(main.ts) simply copies that file to the output directory.
"""

from PIL import Image, ImageDraw, ImageFont

W = H = 1024
PAPER = (248, 244, 233)
INK = (17, 17, 17)
MUTED = (84, 84, 84)
RED = (185, 28, 28)
NAVY = (20, 33, 61)
BLUE = (29, 78, 216)
ORANGE = (194, 65, 12)
TEAL = (15, 118, 110)
WHITE = (255, 255, 255)

SERIF_BLACK = "/usr/share/fonts/truetype/noto/NotoSerifDisplay-Black.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(draw, text, path, max_size, max_width, min_size=20):
    size = max_size
    while size > min_size:
        f = font(path, size)
        if draw.textlength(text, font=f) <= max_width:
            return f
        size -= 2
    return font(path, min_size)


def wrap(draw, text, f, max_width):
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=f) <= max_width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_lines(draw, lines, f, x, y, fill, line_height):
    for line in lines:
        draw.text((x, y), line, font=f, fill=fill)
        y += line_height
    return y


def story(draw, x, y, width, kicker, kicker_color, headline, body):
    """One news block: coloured kicker, serif headline, short factual body."""
    draw.rectangle([x, y + 2, x + 9, y + 23], fill=kicker_color)
    draw.text((x + 17, y), kicker, font=font(SANS_BOLD, 21), fill=kicker_color)
    y += 25
    head_font = font(SERIF_BOLD, 33)
    y = draw_lines(draw, wrap(draw, headline, head_font, width),
                   head_font, x, y, INK, 36)
    y += 3
    body_font = font(SANS, 22)
    y = draw_lines(draw, wrap(draw, body, body_font, width),
                   body_font, x, y, (38, 38, 38), 25)
    return y


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    margin = 36
    right = W - margin

    # Masthead
    draw.line([margin, 26, right, 26], fill=INK, width=3)
    title = "THE WORLD TODAY"
    tf = fit_font(draw, title, SERIF_BLACK, 96, right - margin)
    tw = draw.textlength(title, font=tf)
    draw.text(((W - tw) / 2, 34), title, font=tf, fill=INK)
    draw.line([margin, 132, right, 132], fill=INK, width=3)

    # Date bar: the day this image sums up, impossible to miss.
    draw.rectangle([margin, 142, right, 188], fill=INK)
    date_text = "FRIDAY  •  20 NOVEMBER 2026  •  THE WORLD IN ONE IMAGE"
    df = fit_font(draw, date_text, SANS_BOLD, 30, right - margin - 24)
    dw = draw.textlength(date_text, font=df)
    draw.text(((W - dw) / 2, 151), date_text, font=df, fill=WHITE)

    # Lead story: the Shenzhen trilateral summit.
    y = 200
    draw.rectangle([margin, y, right, y + 7], fill=RED)
    y += 16
    draw.text((margin, y), "SHENZHEN, CHINA  —  DIPLOMACY",
              font=font(SANS_BOLD, 23), fill=RED)
    y += 30
    lead_head = "TRUMP, XI & PUTIN HOLD FIRST-EVER SUMMIT"
    hf = font(SERIF_BOLD, 52)
    y = draw_lines(draw, wrap(draw, lead_head, hf, right - margin),
                   hf, margin, y, INK, 57)
    y += 2
    lead_body = ("The three leaders sign a \u201cDeclaration toward Peace\u201d \u2014 a nuclear war "
                 "\u201cmust never be fought\u201d \u2014 and agree talks on cutting nuclear risks. "
                 "No breakthrough on Ukraine, Iran or Taiwan.")
    bf = font(SANS, 26)
    y = draw_lines(draw, wrap(draw, lead_body, bf, right - margin),
                   bf, margin, y, (38, 38, 38), 30)
    y += 10
    draw.line([margin, y, right, y], fill=INK, width=2)
    y += 12

    # Four stories in two columns.
    col_w = 464
    left_x, right_x = margin, W // 2 + 12
    top = y
    y_left = story(
        draw, left_x, top, col_w,
        "THE HAGUE  —  WORLD COURT", BLUE,
        "ICJ: MYANMAR COMMITTED GENOCIDE",
        "A 9\u20136 verdict on the Rohingya: the first time a state is held "
        "responsible for genocide. Reparations ordered.")
    y_right = story(
        draw, right_x, top, col_w,
        "RIYADH  —  CONFLICT", RED,
        "MISSILE HITS RIYADH'S TALLEST TOWER",
        "A Houthi projectile struck the PIF Tower, blowing out windows "
        "across eight floors. No injuries were reported.")
    row2 = max(y_left, y_right) + 10
    draw.line([W // 2 - 4, top, W // 2 - 4, row2 + 140], fill=(190, 182, 160), width=2)
    y_left2 = story(
        draw, left_x, row2, col_w,
        "ODISHA, INDIA  —  WEATHER", ORANGE,
        "CYCLONE AKVAN MAKES LANDFALL",
        "Landfall near Gopalpur on Friday morning, gusting to 90 km/h. "
        "300,000 evacuated; no major damage reported.")
    y_right2 = story(
        draw, right_x, row2, col_w,
        "ANTALYA  —  COP31, FINAL DAY", TEAL,
        "\u201cFOSSIL FUELS\u201d VANISH FROM DRAFT DEAL",
        "A new draft dropped every mention of fossil fuels, sparking "
        "outcry among nearly 200 nations.")
    y = max(y_left2, y_right2) + 12

    # Markets band.
    draw.rectangle([margin, y, right, y + 96], fill=NAVY)
    draw.text((margin + 22, y + 11), "MARKETS  —  THE BIGGEST IPO EVER, AND A SELLOFF",
              font=font(SANS_BOLD, 24), fill=(147, 197, 253))
    market_body = ("Anthropic raised a record $81 billion, closing up 17% at $97.17 \u2014 "
                   "yet the Dow fell 1,101 points (2.2%) in an AI sell-off.")
    mf = font(SANS, 24)
    draw_lines(draw, wrap(draw, market_body, mf, right - margin - 44),
               mf, margin + 22, y + 40, WHITE, 28)
    y += 96 + 8

    # Also-today ticker: three more stories reported the same day.
    ticker = ("ALSO TODAY:  US Senate rejects an Iran war-powers measure 51\u201348  •  "
              "Trump pardons baseball great Pete Rose posthumously  •  "
              "UK pledges 1,000+ drones for Ukraine (\u00a3260m)")
    tf2 = font(SANS_BOLD, 19)
    draw_lines(draw, wrap(draw, ticker, tf2, right - margin),
               tf2, margin, y, MUTED, 25)

    img.save("entry.png", optimize=True)
    print("wrote entry.png", img.size)


if __name__ == "__main__":
    main()
