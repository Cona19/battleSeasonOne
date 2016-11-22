# -*-coding:utf-8-*-
from baseClass.PixelsParser import PixelsParser
import random
import copy

dx = [0,1,0,-1]
dy = [1,0,-1,0]
think_depth = 9 # Very Important

class TooDeepParser(PixelsParser):
    def sweep(self, w, h, ca, ra, ruler, col, start_x, start_y):
        q = []
        q.insert(0,(start_y,start_x))
        ra[start_y][start_x] = ruler
        cnt = 0
        while len(q) > 0:
            cnt += 1
            y,x = q.pop()
            for i in range(4):
                if 0 <= y +dy[i] < h and 0 <= x + dx[i] < w:
                    ty = y+dy[i]
                    tx = x+dx[i]
                    if ca[ty][tx] == col and ra[ty][tx] == 0:
                        ra[ty][tx] = ruler
                        q.insert(0, (ty,tx))
        self.change_color(w,h,ca,ra,ruler,col)
        return cnt

    def change_color(self, w, h, ca, ra, ruler, col):
        for y in range(h):
            for x in range(w):
                if ra[y][x] == ruler:
                    ca[y][x] = col

    def simulate(self, w, h, ca, ra, ruler, col):
        cnt = 0
        for y in range(h):
            for x in range(w):
                if ra[y][x] == 0 and ca[y][x] == col and (
                    (x > 0 and ra[y][x - 1] == ruler)  # Check left side
                    or (x < (w - 1) and ra[y][x + 1] == ruler)  # Check right side
                    or (y > 0 and ra[y - 1][x] == ruler)  # Check up side
                    or (y < (h - 1) and ra[y + 1][x] == ruler)  # Check down side
                ):  # Count the number of area that we can rule, with dividing according to colors.
                    cnt += self.sweep(w,h,ca,ra,ruler,col,x,y)
        return cnt,ca,ra

    def get_best_select(self, w, h, ca, ra, ruler, num_of_color):
        best_res = None
        start_point_y = self.game_data['start_point_y']
        start_point_x = self.game_data['start_point_x']
        ban_col1 = ca[start_point_y[0]][start_point_x[0]]
        ban_col2 = ca[start_point_y[1]][start_point_x[1]]
        for col in range(1,num_of_color+1):
            if col == ban_col1 or col == ban_col2:
                continue
            enemy_res = self.simulate(w, h, copy.deepcopy(ca), copy.deepcopy(ra), ruler, col)
            if best_res == None or best_res[0] < enemy_res[0]:
                best_res = enemy_res

        return best_res

    def loop_phase(self):
        width = self.width
        height = self.height
        color_array = self.color_array
        ruler_array = self.ruler_array
        start_point_y = self.game_data['start_point_y']
        start_point_x = self.game_data['start_point_x']
        ruler_self = self.game_data['ruler_self']
        ruler_enemy = self.game_data['ruler_enemy']
        enemy_chosen_color = self.game_data['enemy_chosen_color']

        num_of_color = 6

        if ruler_self == 1:
            my_color = color_array[start_point_y[0]][start_point_x[0]]
        elif ruler_self == 2:
            my_color = color_array[start_point_y[1]][start_point_x[1]]

        max_first_val = -999999999 
        maxval = -999999999
        maxi = 0
        for col in range(1,num_of_color+1):
            if col == my_color or col == enemy_chosen_color:
                continue
            res = self.simulate(width, height, copy.deepcopy(color_array), copy.deepcopy(ruler_array), ruler_self, col)
            first_val = res[0]
            val = res[0]
            for t in range(think_depth): 
                if t%2 == 0:
                    res = self.get_best_select(width, height, res[1], res[2], ruler_enemy, num_of_color)
                    val -= res[0]
                if t%2 == 1:
                    res = self.get_best_select(width, height, res[1], res[2], ruler_self, num_of_color)
                    val += res[0]

            if maxval < val or (maxval == val and max_first_val < first_val):
                max_first_val = first_val
                maxval = val
                maxi = col

        if maxi == 0:
            for col in range(1,num_of_color+1):
                if col == my_color or col == enemy_chosen_color:
                    continue
                res = self.simulate(width, height, copy.deepcopy(color_array), copy.deepcopy(ruler_array), ruler_self, col)
                if maxval < res[0]:
                    maxval = res[0]
                    maxi = col

        print "-------------------------"
        print "maxval : " + str(maxval)
        print "maxi : " + str(maxi)
        print "-------------------------"
        output_data = {'chosen_color': maxi}
        return output_data
