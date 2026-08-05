"""Render Q train arrivals across the folded 192x64 LED matrix panels.

Requires the rpi-rgb-led-matrix Python bindings (https://github.com/hzeller/rpi-rgb-led-matrix),
built and installed separately on the Raspberry Pi -- this only runs there,
not on a dev machine.
"""

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

import config

# U-mapper folds the 6-panel chain into 2 physical rows of 3, so the logical
# canvas is 3 panels wide by 2 panels tall, not 6 panels wide by 1 tall.
DISPLAY_WIDTH = config.PANEL_COLS * (config.CHAIN_LENGTH // 2)  # 192
DISPLAY_HEIGHT = config.PANEL_ROWS * 2  # 64
ROW_HEIGHT = DISPLAY_HEIGHT // 2  # 32px per arrival row -- one physical panel row each

YELLOW = graphics.Color(255, 199, 0)
WHITE = graphics.Color(255, 255, 255)
BLACK = graphics.Color(0, 0, 0)


class Display:
    def __init__(self):
        # Font must load before the matrix is built: RGBMatrix() drops root
        # privileges after setting up GPIO, and the lower-privilege user it
        # drops to can't necessarily read files under the home directory.
        self.label_font = graphics.Font()
        self.label_font.LoadFont(config.LABEL_FONT_FILE)

        self.matrix = self._build_matrix()
        self.canvas = self.matrix.CreateFrameCanvas()

    @staticmethod
    def _build_matrix():
        options = RGBMatrixOptions()
        options.rows = config.PANEL_ROWS
        options.cols = config.PANEL_COLS
        options.chain_length = config.CHAIN_LENGTH
        options.parallel = config.PARALLEL_CHAINS
        options.pixel_mapper_config = config.PIXEL_MAPPER
        options.hardware_mapping = config.HARDWARE_MAPPING
        options.led_rgb_sequence = config.LED_RGB_SEQUENCE
        options.gpio_slowdown = config.GPIO_SLOWDOWN
        options.brightness = config.BRIGHTNESS
        return RGBMatrix(options=options)

    def render(self, arrival_minutes):
        """Draw up to two arrival rows. arrival_minutes is a list of ints/floats,
        soonest first; missing rows are padded with None (shown as "---")."""
        rows = list(arrival_minutes[:2])
        while len(rows) < 2:
            rows.append(None)

        self.canvas.Clear()
        for row_index, minutes in enumerate(rows):
            self._draw_row(row_index, minutes)
        self.canvas = self.matrix.SwapOnVSync(self.canvas)

    def _draw_row(self, row_index, minutes):
        y_top = row_index * ROW_HEIGHT
        center_y = y_top + ROW_HEIGHT // 2
        # Baseline offset to visually center the label font on center_y;
        # approximate without exact BDF metrics, fine-tune during the smoke test.
        text_baseline = center_y + 4

        self._draw_bullet(config.BULLET_CENTER_X, center_y)

        self._draw_tracked_text(
            self.label_font, config.LABEL_X, text_baseline, WHITE,
            config.DESTINATION_LABEL,
        )

        label = self._format_minutes(minutes)
        label_width = self._tracked_text_width(self.label_font, label)
        label_x = DISPLAY_WIDTH - config.RIGHT_MARGIN - label_width
        self._draw_tracked_text(
            self.label_font, label_x, text_baseline, WHITE, label
        )

    def _space_width(self, font):
        # The BDF space glyph is wider than looks right at this scale --
        # e.g. it left visible gaps around "&" in DESTINATION_LABEL and
        # between the number and "MIN" in the arrival label, enough to
        # crowd the display's fixed width. Scale it down instead of using
        # the font's native advance, then nudge by a flat pixel amount for
        # finer tuning. Adjust SPACE_WIDTH_SCALE / SPACE_WIDTH_ADJUST_PX in
        # config.py after checking it live on the physical display.
        scaled = font.CharacterWidth(ord(" ")) * config.SPACE_WIDTH_SCALE
        return round(scaled) + config.SPACE_WIDTH_ADJUST_PX

    def _kerning_adjust(self, this_char, next_char):
        # Flat pixel nudge (negative = tighter) between two specific adjacent
        # characters that still look too loose even at their normal BDF
        # widths -- e.g. "LY" in "BROOKLYN". See config.KERNING_ADJUSTMENTS_PX.
        return config.KERNING_ADJUSTMENTS_PX.get((this_char, next_char), 0)

    def _tracked_text_width(self, font, text):
        """Like summing CharacterWidth, but with a narrowed space (see
        _space_width) and any per-pair kerning nudges (see _kerning_adjust)."""
        space_width = self._space_width(font)
        total = 0
        for i, ch in enumerate(text):
            total += space_width if ch == " " else font.CharacterWidth(ord(ch))
            if i + 1 < len(text):
                total += self._kerning_adjust(ch, text[i + 1])
        return total

    def _draw_tracked_text(self, font, x, y, color, text):
        """DrawText, but with a narrowed space (see _space_width) instead of
        the font's native (too-wide, at this scale) space advance, plus any
        per-pair kerning nudges (see _kerning_adjust)."""
        space_width = self._space_width(font)
        cursor_x = x
        for i, ch in enumerate(text):
            if ch == " ":
                cursor_x += space_width
            else:
                cursor_x += graphics.DrawText(self.canvas, font, cursor_x, y, color, ch)
            if i + 1 < len(text):
                cursor_x += self._kerning_adjust(ch, text[i + 1])
        return cursor_x

    def _draw_bullet(self, center_x, center_y):
        radius = config.BULLET_DIAMETER / 2
        r_squared = radius * radius

        top = int(center_y - radius)
        bottom = int(center_y + radius)
        left = int(center_x - radius)
        right = int(center_x + radius)

        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                dx = x - center_x
                dy = y - center_y
                if dx * dx + dy * dy <= r_squared:
                    self.canvas.SetPixel(x, y, YELLOW.red, YELLOW.green, YELLOW.blue)

        # Same font/size as the stop and time text, in black against the
        # yellow bullet, per the real MTA bullet styling.
        q_width = self.label_font.CharacterWidth(ord("Q"))
        q_x = center_x - q_width // 2
        q_y = center_y + 4  # same baseline offset as text_baseline in _draw_row
        graphics.DrawText(self.canvas, self.label_font, q_x, q_y, BLACK, "Q")

    @staticmethod
    def _format_minutes(minutes):
        if minutes is None:
            return "---"
        if minutes <= 0:
            return "NOW"
        return f"{minutes} MIN"


if __name__ == "__main__":
    import time

    display = Display()
    display.render([2, 12])
    print("Rendered test arrivals (2 min, 12 min). Ctrl+C to exit.")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
