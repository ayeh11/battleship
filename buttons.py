class Button:
    def __init__(self, x, y, colors, text):
        self.x = x
        self.y = y
        self.width = 150
        self.height = 80
        self.colors = colors
        self.color = self.colors[3]
        self.text = text

    def draw(self, grid):
        self.ready = self.check_ready(grid)
        if self.text == "Rematch?":
            self.color = self.colors[3]
        elif self.text == "waiting":
            self.color = self.colors[1]
        elif self.text == "Fire!":
            if self.ready:
                self.color = self.colors[2]
            else:
                self.color = self.colors[1]
        else:
            if self.ready:
                self.color = self.colors[3]
                self.text = "Ready!"
            else:
                self.color = self.colors[2]
                self.text = "no"

    def check_ready(self, grid):
        if self.text == "Fire!":
            for b in grid.blocks:
                if b.status == "select":
                    return True
        else:
            for b in grid.blocks:
                if b.status == "bad_pos":
                    return False
                else:
                    return True

    def click(self, pos):
        x1 = pos[0]
        y1 = pos[1]

        if self.ready:
            if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
                return True
            else:
                return False

    def change_text(self, text):
        self.text = text