# BetterCurses - colorizer.py
# github.com/leftbones/colorizer

import curses, re

class Colorizer:
    def __init__(self, terminal):
        self.terminal = terminal

        self.color_cache = []
        self.pair_cache = []

        self.color_idx = 0
        self.pair_idx = 0

        self.default_fg = '#ffffff'
        self.default_bg = '#000000'
        self.highlight_bg = '#cccccc'

        self.transparent_bg = True

    def hex_to_rgb(self, color_hex):
        """
        Convert a hex code (string) to RGB (tuple)
        """
        if color_hex.startswith('#'): color_hex = color_hex[1:]
        rgb = tuple(int(color_hex[i:i+2], 16) for i in (0, 2, 4))

    def parse_text(self, text):
        """
        Search text for color tags and strings between tags and return an ordered list of tokens
        All text inside [square brackets] is considered a tag, during printing if a tag is found to be invalid, it is
        instead printed as text to avoid considering every pair of square brackets as a non-printable tag
        """
        pos = 0
        tokens = []

        while pos < len(text):
            if text[pos] == '[':
                token = ''
                while text[pos] != ']':
                    token += text[pos]
                    pos += 1
                token += ']'
                tokens.append(token)
                pos += 1
            else:
                token = ''
                while text[pos] != '[':
                    token += text[pos]
                    pos += 1
                    if pos == len(text): break
                tokens.append(token)

            return tokens

    def get_pair(self, fg_hex=None, bg_hex=None):
        """
        Retrieve an existing color pair based on the passed foreground and background hex codes
        If the pair does not exist, create and add a new pair to the cache
        If a color does not exist, create and add a new color to the cache
        """
        # Foreground
        if not fg_hex: fg_rgb = self.hex_to_rgb(self.default_fg)
        else: fg_rgb = self.hex_to_rgb(fg_hex)

        if not self.color_exists(fg_rgb):
            curses.init_color(self.color_idx, int(fg_rgb[0]/0.255), int(fg_rgb[1]/0.255), int(fg_rgb[2]/0.255))
            fg_color = self.color_idx
            self.color_cache.append(fg_rgb)
            self.color_idx += 1
        else:
            fg_color = self.color_cache.index(fg_rgb)

        # Background
        if not bg_hex: bg_rgb = self.hex_to_rgb(self.default_bg)
        else: bg_rgb = self.hex_to_rgb(bg_hex)

        if not self.color_exists(bg_rgb):
            curses.init_color(self.color_idx, int(bg_rgb[0]/0.255), int(bg_rgb[1]/0.255), int(bg_rgb[2]/0.255))
            bg_color = self.color_idx
            self.color_cache.append(bg_rgb)
            self.color_idx += 1
        else:
            bg_color = self.color_cache.index(bg_rgb)

        if self.transparent_bg and not bg_hex: bg_color = -1

        # Pair
        pair_exists = False
        for pair in self.pair_cache:
            if pair[1] == fg_color and pair[2] == bg_color:
                pair_exists = True
                pair = pair[0]
                break

        if not pair_exists:
            curses.init_pair(self.pair_idx, fg_color, bg_color)
            pair = self.pair_idx
            self.pair_cache.append([self.pair_idx, fg_color, bg_color])
            self.pair_idx += 1

        return pair

    def print(self, window, row, col, text):
        """
        Print tagged string to the screen, applying colors based on the tags
        Example: "This is not red, [color #FF0000]but this is![/color]"
        """
        tokens = self.parse_text(text)
        pair = curses.color_pair(0)

        i = 0
        for token in tokens:
            if token.startswith('[color #'):
                try:
                    color = re.findall('\ (.*?)\>', token)[0]
                    pair = curses.color_pair(self.get_pair(color))
                except Exception as e:
                    log.write(e)
                    pair = curses.color_pair(0)
                    pass
            elif token == '[/color]':
                pair == curses.color_pair(0)
            elif token == '\n':
                pass
            else:
                for char in token:
                    window.screen.insch(row, col + i, char, pair)
                    i += 1
