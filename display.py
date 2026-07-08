"""Render Q train arrivals across the chained 256x32 LED matrix panels.

Requires the rpi-rgb-led-matrix Python bindings (https://github.com/hzeller/rpi-rgb-led-matrix),
built and installed separately on the Raspberry Pi -- this only runs there,
not on a dev machine.
"""

from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics

import config

DISPLAY_WIDTH = config.PANEL_COLS * config.CHAIN_LENGTH  # 256
DISPLAY_HEIGHT = config.PANEL_ROWS  # 32
ROW_HEIGHT = DISPLAY_HEIGHT // 2  # 16px per arrival row, two rows stacked

YELLOW = graphics.Color(255, 199, 0)
BLACK = graphics.Color(0, 0, 0)
WHITE = graphics.Color(255, 255, 255)


class Display:
    def __init__(self):
        self.matrix = self._build_matrix()
        self.canvas = self.matrix.CreateFrameCanvas()

        self.label_font = graphics.Font()
        self.label_font.LoadFont(config.LABEL_FONT_FILE)

        self.bullet_font = graphics.Font()
        self.bullet_font.LoadFont(config.BULLET_FONT_FILE)

    @staticmethod
    def _build_matrix():
        options = RGBMatrixOptions()
        options.rows = config.PANEL_ROWS
        options.cols = config.PANEL_COLS
        options.chain_length = config.CHAIN_LENGTH
        options.parallel = config.PARALLEL_CHAINS
        options.hardware_mapping = config.HARDWARE_MAPPING
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
        text_baseline = y_top + ROW_HEIGHT - 3

        self._draw_bullet(config.BULLET_CENTER_X, center_y)

        graphics.DrawText(
            self.canvas, self.label_font, config.LABEL_X, text_baseline, WHITE,
            config.DESTINATION_LABEL,
        )

        label = self._format_minutes(minutes)
        label_width = self._text_width(self.label_font, label)
        label_x = DISPLAY_WIDTH - config.RIGHT_MARGIN - label_width
        graphics.DrawText(
            self.canvas, self.label_font, label_x, text_baseline, WHITE, label
        )

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

        q_width = self.bullet_font.CharacterWidth(ord("Q"))
        q_x = center_x - q_width // 2
        q_y = center_y + 2  # nudge down to account for BDF baseline offset
        graphics.DrawText(self.canvas, self.bullet_font, q_x, q_y, BLACK, "Q")

    @staticmethod
    def _text_width(font, text):
        return sum(font.CharacterWidth(ord(ch)) for ch in text)

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
