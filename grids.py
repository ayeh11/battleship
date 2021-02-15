import random

class ShipsGrid():
    def __init__(self, colors):
        self.colors = colors
        self.grid, self.blocks = self.make_grid(10, 10)
        self.lengths = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
        self.around_zones = []
        self.all_ships, self.ship_blocks = self.make_ships(self.lengths, self.around_zones)
        self.shots = []

    class ShipBlocks:
        def __init__(self, row, col, colors, status):
            self.row = row
            self.col = col
            self.pos = (col, row)
            self.status = status
            self.color_list = colors
            self.circle = False
            self.color = colors[0]

        def change_color(self, color):
            self.color = color

        def status_check(self):
            if self.status == "bad_pos":
                self.change_color(self.color_list[2])
                self.circle = False
            elif self.status == "ship":
                self.change_color(self.color_list[1])
                self.circle = False
            elif self.status == "az":
                self.change_color(self.color_list[0])
                self.circle = self.color_list[4]
            elif self.status == "miss_shot":
                self.change_color(self.color_list[0])
                self.circle = self.color_list[1]
            elif self.status == "hit_ship":
                self.change_color(self.color_list[1])
                self.circle = self.color_list[2]
            elif self.status == "u_sunk_ship":
                self.change_color(self.color_list[5])
                self.circle = False
            else:
                self.change_color(self.color_list[0])
                self.circle = False
# MAKING
    def make_grid(self, rows, cols):
        grid = []
        blocks = []
        for i in range(rows):
            grid.append([])
            for j in range(cols):
                block = self.ShipBlocks(i, j, self.colors, "")
                blocks.append(block)
                grid[i].append(block)

        return grid, blocks

    def make_ships(self, lengths, around_zones):
        all_ships = []
        ship_blocks = []
        oris = []
        ship_parts = []

        for ship_id in range(len(lengths)):
            checked = False
            for j in range(lengths[ship_id]):
                while not checked:
                    random_ori = random.randrange(0, 2)  # 0 is horizontal and 1 is vertical
                    if random_ori == 0:
                        random_col = random.randrange(0, 11 - lengths[ship_id])
                        random_row = random.randrange(0, 10)
                    else:
                        random_col = random.randrange(0, 10)
                        random_row = random.randrange(0, 11 - lengths[ship_id])

                    checked = self.checking(ship_id, lengths, random_col, random_row, random_ori, ship_blocks, around_zones)
                else:
                    if random_ori == 0:
                        ship_part = (random_row, random_col + j)
                    else:
                        ship_part = (random_row + j, random_col)
                    ship_parts.append(ship_part)
                    ship_blocks.append(ship_part)

            oris.append(random_ori)

        for ship_id in range(len(lengths)):
            pos = ship_parts[:lengths[ship_id]]
            ship = (ship_id, lengths[ship_id], oris[ship_id], pos)
            all_ships.append(ship)
            del ship_parts[:lengths[ship_id]]

        return all_ships, ship_blocks

    def checking(self, id, lengths, rand_col, rand_row, rand_ori, ship_blocks, all_azs):
        shipself = self.get_whole_ship(rand_row, rand_col, lengths[id], rand_ori)
        around_zone = self.get_around_zone(shipself, lengths[id], rand_ori)

        for s in shipself:
            if s in ship_blocks:
                return False
            for a in all_azs:
                if s in a:
                    return False
        else:
            all_azs.append((around_zone))
            return True
# USEFUL FUNCS
    def get_whole_ship(self, row, col, length, ori):
        itself = []

        for i in range(length):
            if ori == 0:
                part = (row, col+i)
            else:
                part = (row + i, col)
            itself.append(part)

        return itself

    def get_around_zone(self, shipself_num, length, ori):
        around_zone = []

        top_side = False
        left_side = False
        bottom_side = False
        right_side = False

        n1 = shipself_num[0]

        if n1[0] == 0:
            top_side = True
        if n1[1] == 0:
            left_side = True

        if ori == 0:
            if n1[0] == 9:
                bottom_side = True
            if n1[1] == 10 - length:
                right_side = True
        else:
            if n1[0] == 10 - length:
                bottom_side = True
            if n1[1] == 9:
                right_side = True

        if ori == 0:
            if not left_side:
                others = (n1[0], n1[1] -1)
                around_zone.append(others)
            if not right_side:
                others = (n1[0], n1[1] +length)
                around_zone.append(others)
            if not top_side:
                for s in shipself_num:
                    others = (n1[0]-1, s[1])
                    around_zone.append(others)
            if not bottom_side:
                for s in shipself_num:
                    others = (n1[0]+1, s[1])
                    around_zone.append(others)
        else:
            if not left_side:
                for s in shipself_num:
                    others = (s[0], n1[1] -1)
                    around_zone.append(others)
            if not right_side:
                for s in shipself_num:
                    others = (s[0], n1[1] +1)
                    around_zone.append(others)
            if not top_side:
                others = (n1[0]-1, n1[1])
                around_zone.append(others)
            if not bottom_side:
                others = (n1[0]+length, n1[1])
                around_zone.append(others)

        return around_zone

    def get_pos_in_shipblocks(self, id):
        pos_in_shipblocks = 0

        for i in range(id):
            pos_in_shipblocks += self.lengths[i]

        return pos_in_shipblocks

    def checking_for_dupes(self, pos):
        if self.ship_blocks.count(pos) > 1:
            return True

        return False

    def edit_all_ships(self):
        edit = []
        for s in self.all_ships:
            id, length, ori, pos = s
            edit.append(pos)

        return edit

    def update_allships(self, id, length, ori, new_pos, pos_in_shipblocks):
        self.all_ships[id] = (id, length, ori, new_pos)
        for l in range(length):
            self.ship_blocks[pos_in_shipblocks + l] = new_pos[l]

    def update_blocks(self):
        allzs = []
        for zone in self.around_zones:
            for z in zone:
                allzs.append(z)

        for b in self.blocks:
            if (b.pos in self.ship_blocks and b.pos in allzs) or (self.checking_for_dupes(b.pos)):
                b.status = "bad_pos"
            elif b.pos in self.ship_blocks:
                b.status = "ship"
                if b.pos in self.shots:
                    b.status = "hit_ship"
            elif b.pos in self.shots:
                b.status = "miss_shot"
            elif b.pos in allzs:
                b.status = "az"
            else:
                b.status = ""

        edited_ships = self.edit_all_ships()
        for s in range(len(edited_ships)):
            if all(elem in self.shots for elem in edited_ships[s]):  # if shots contain all pos of a specific ship
                for b in self.blocks:
                    for u in edited_ships[s]:
                        if b.pos == u:
                            b.status = "u_sunk_ship"
                    for z in self.around_zones[s]:
                        if b.pos == z:
                            b.status = "miss_shot"

    def within_border(self, moving_ship, col, row):
        id, length, ori, pos = moving_ship
        if ori == 0:
            if col < 0:
                col = 0
            elif col > 10-length:
                col = 10-length

            if row < 0:
                row = 0
            elif row > 9:
                row = 9

            return col, row

        else:
            if col < 0:
                col = 0
            elif col > 9:
                col = 9

            if row < 0:
                row = 0
            elif row > 10-length:
                row = 10-length

            return col, row

    def reset(self):
        self.grid, self.blocks = self.make_grid(10, 10)
        self.around_zones = []
        self.all_ships, self.ship_blocks = self.make_ships(self.lengths, self.around_zones)
        self.shots = []

# MOVEMENT
    def moving_ships(self, moving_ship, m_col, m_row):
        id, length, ori, pos = moving_ship

        pos_in_shipblocks = self.get_pos_in_shipblocks(id)

        self.around_zones[id] = (0, 0)

        if length == 1:
            self.all_ships[id] = (id, length, ori, [(m_row, m_col)])
            self.ship_blocks[pos_in_shipblocks] = (m_row, m_col)
        else:
            new_pos = self.get_whole_ship(m_row, m_col, length, ori)
            self.update_allships(id, length, ori, new_pos, pos_in_shipblocks)

    def placed_ship(self, moving_ship, col, row):
        id, length, ori, pos = moving_ship
        entire_ship = self.get_whole_ship(row, col, length, ori)
        new_az = self.get_around_zone(entire_ship, length, ori)
        self.around_zones[id] = new_az

    def rotate_ship(self, grid, moving_ship):
        id, length, ori, pos = moving_ship
        pos_in_shipblocks = self.get_pos_in_shipblocks(id)
        row, col = pos[0]

        if ori == 0:
            if row + length < 11:
                new_pos = self.get_whole_ship(row, col, length, 1)
            else:
                return moving_ship
        else:
            if col + length < 11:
                new_pos = self.get_whole_ship(row, col, length, 0)
            else:
                return moving_ship

        if ori == 0:
            rori = 1
        else:
            rori = 0
        self.update_allships(id, length, rori, new_pos, pos_in_shipblocks)

        rot_ship = grid.all_ships[id]
        return rot_ship


class FireGrid():
    def __init__(self, colors):
        self.colors = colors
        self.grid, self.blocks = self.make_grid(10, 10)
        self.other_ships = []
        self.other_az = []
        self.shots = []
        self.selected = ()

    class FireBlocks:
        def __init__(self, row, col, colors, status):
            self.row = row
            self.col = col
            self.pos = (col, row)
            self.status = status
            self.color_list = colors
            self.circle = False
            self.color = colors[0]

        def change_color(self, color):
            self.color = color

        def status_check(self):
            if self.status == "az" or self.status == "miss_shot":
                self.change_color(self.color_list[0])
                self.circle = self.color_list[1]
            elif self.status == "hit_ship":
                self.change_color(self.color_list[0])
                self.circle = self.color_list[2]
            elif self.status == "u_sunk_ship":
                self.change_color(self.color_list[5])
                self.circle = False
            elif self.status == "select":
                self.change_color(self.color_list[3])
                self.circle = False
            else:
                self.change_color(self.color_list[0])
                self.circle = False

    def make_grid(self, rows, cols):
        grid = []
        blocks = []
        for i in range(rows):
            grid.append([])
            for j in range(cols):
                block = self.FireBlocks(i, j, self.colors, "")
                blocks.append(block)
                grid[i].append(block)

        return grid, blocks

    def edit_other_ships(self):
        edit = []
        for s in self.other_ships:
            id, length, ori, pos = s
            edit.append(pos)

        ship_blocks = []
        for e in edit:
            for i in e:
                ship_blocks.append(i)

        return edit, ship_blocks

    def update_blocks(self):
        edited_ships, ship_blocks = self.edit_other_ships()

        for b in self.blocks:
            if b.pos in self.shots:
                b.status = "miss_shot"
                if b.pos in ship_blocks:
                    b.status = "hit_ship"
            elif b.pos == self.selected:
                b.status = "select"
            else:
                b.status = ""

        for s in range(len(edited_ships)):
            if all(elem in self.shots for elem in edited_ships[s]): # if shots contain all pos of a specific ship
                for b in self.blocks:
                    for u in edited_ships[s]:
                        if b.pos == u:
                            b.status = "u_sunk_ship"
                    for z in self.other_az[s]:
                        if b.pos == z:
                            b.status = "az"

    def win(self):
        _, ship_blocks = self.edit_other_ships()
        if all(elem in self.shots for elem in ship_blocks):
            return True
        else:
            return False

    def reset(self):
        self.grid, self.blocks = self.make_grid(10, 10)
        self.other_ships = []
        self.other_az = []
        self.shots = []
        self.selected = ()


