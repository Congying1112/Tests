import cv2
import numpy as np
import random
import math
from sub_modules.print_log import print_log


class MaxGetter:
    def __init__(self, offset, interval, vals=[]):
        self.dict = {}
        self.offset = offset
        self.interval = interval
        for (idx, val) in vals:
            self.add(idx, val)

    def add(self, idx, val):
        index = int((val + self.offset) / self.interval)
        if index not in self.dict:
            self.dict[index] = []
        self.dict[index].append((idx, val))

    def get_max(self):
        max_vals = []
        for key, value in self.dict.items():
            if len(value) > len(max_vals):
                max_vals = value
        return max_vals


class Matcher:
    def __init__(self):
        self.matcher = cv2.BFMatcher()

    @staticmethod
    def stat_scale(pts1, pts2, first_pt_ids, second_pt_ids, ids_of_pt_id):
        max_scale_getter = MaxGetter(1, 0.05)
        for id_of_pt_id in ids_of_pt_id:
            first_pt_id = first_pt_ids[id_of_pt_id]
            second_pt_id = second_pt_ids[id_of_pt_id]
            # cv2.line(show_img1, tuple(pts1[first_pt_id][0]), tuple(pts1[second_pt_id][0]), (0, 0, 255))
            # cv2.line(show_img2, tuple(pts2[first_pt_id][0]), tuple(pts2[second_pt_id][0]), (0, 0, 255))
            # cv2.imshow("img1", show_img1)
            # cv2.imshow("img2", show_img2)
            scale = Matcher.calculate_scale(pts1[first_pt_id], pts1[second_pt_id], pts2[first_pt_id], pts2[second_pt_id])
            max_scale_getter.add(id_of_pt_id, scale)
        return max_scale_getter.get_max()


    @staticmethod
    def stat_angle_and_trans(pts1, pts2, first_pt_ids, second_pt_ids, ids_of_pt_id):
        max_angle_getter = MaxGetter(math.pi, 0.05)
        max_trans_x_getter = MaxGetter(0, 1)
        max_trans_y_getter = MaxGetter(0, 1)
        for id_of_pt_id in ids_of_pt_id:
            first_pt_id = first_pt_ids[id_of_pt_id]
            second_pt_id = second_pt_ids[id_of_pt_id]
            trans = Matcher.get_trans((pts1[first_pt_id], pts1[second_pt_id]), (pts2[first_pt_id], pts2[second_pt_id]))
            (delta_angle, (trans_x, trans_y)) = trans
            max_angle_getter.add(id_of_pt_id, delta_angle)
            max_trans_x_getter.add(id_of_pt_id, trans_x)
            max_trans_y_getter.add(id_of_pt_id, trans_y)
        return max_angle_getter.get_max(), max_trans_x_getter.get_max(), max_trans_y_getter.get_max()


    @staticmethod
    def calculate_scale(pt11, pt12, pt21, pt22):
        delta_l1, delta_l2 = pt11 - pt12, pt21 - pt22
        delta_l1 = delta_l1[0]
        delta_l2 = delta_l2[0]
        length1 = delta_l1[0] * delta_l1[0] + delta_l1[1] * delta_l1[1]
        length2 = delta_l2[0] * delta_l2[0] + delta_l2[1] * delta_l2[1]
        if length2 < 0.0000001:
            length2 = 0.0000001
        return math.sqrt(length1 / length2)

    @staticmethod
    def get_trans(line1, line2):
        # print "delta length", delta_length
        line1 = (line1[0][0], line1[1][0])
        line2 = (line2[0][0], line2[1][0])
        l1_dir = math.atan2(line1[1][1] - line1[0][1], line1[1][0] - line1[0][0])
        l2_dir = math.atan2(line2[1][1] - line2[0][1], line2[1][0] - line2[0][0])
        # print "dirs", math.degrees(l1_dir), math.degrees(l2_dir)
        delta_angle = l1_dir - l2_dir
        # print "delta angle", math.degrees(delta_angle)
        cos_delta_angle = math.cos(delta_angle)
        sin_delta_angle = math.sin(delta_angle)
        trans_x = -line2[0][0] * cos_delta_angle + line2[0][1] * sin_delta_angle + line1[0][0]
        trans_y = -line2[0][0] * sin_delta_angle - line2[0][1] * cos_delta_angle + line1[0][1]
        # m1 = np.matrix([[1, 0, line1[0].x], [0, 1, line1[0].y], [0, 0, 1]])
        # m2 = np.matrix(
        #     [[math.cos(delta_angle), -math.sin(delta_angle), 0], [math.sin(delta_angle), math.cos(delta_angle), 0],
        #      [0, 0, 1]])
        # m3 = np.matrix([[1, 0, -line2[0].x], [0, 1, -line2[0].y], [0, 0, 1]])
        # print m1, m2, m3
        # print m1 * m2 * m3
        return delta_angle, (trans_x, trans_y)

    @staticmethod
    def get_trans_matrix(rotate, trans_x, trans_y):
        return np.matrix(
            [[math.cos(rotate), -math.sin(rotate), trans_x], [math.sin(rotate), math.cos(rotate), trans_y], [0, 0, 1]])


    @staticmethod
    def cc_find_transformation(matches, kps1, kps2):
        if matches:
            # construct the two sets of points
            pts1 = np.float32([ kps1[m.queryIdx].pt for m in matches ]).reshape(-1,1,2)
            pts2 = np.float32([ kps2[m.trainIdx].pt for m in matches ]).reshape(-1,1,2)

            valid_match_count_thre = 100
            pt_count = len(pts1)
            first_pt_ids = []
            second_pt_ids = []
            for id1_of_pt_id in range(0, pt_count - 1):
                for id2_of_pt_id in range(id1_of_pt_id + 1, pt_count):
                    first_pt_ids.append(id1_of_pt_id)
                    second_pt_ids.append(id2_of_pt_id)
            if valid_match_count_thre < len(first_pt_ids):
                ids_of_pt_id = random.sample(range(len(first_pt_ids)), valid_match_count_thre)
            else:
                ids_of_pt_id = range(len(first_pt_ids))

            max_scale_list = Matcher.stat_scale(pts1, pts2, first_pt_ids, second_pt_ids, ids_of_pt_id)
            valid_ids_of_pt_id = list(map(lambda x: x[0], max_scale_list))
            scale = np.mean(list(map(lambda x: x[1], max_scale_list)))

            max_angles, max_xs, max_ys = Matcher.stat_angle_and_trans(pts1, pts2, first_pt_ids, second_pt_ids, valid_ids_of_pt_id)

            if max_angles and max_xs and max_ys:
                max_angle = np.mean(list(map(lambda x: x[1], max_angles)))
                max_trans_x = np.mean(list(map(lambda x: x[1], max_xs)))
                max_trans_y = np.mean(list(map(lambda x: x[1], max_ys)))
                match_detail = {
                    "max_angle_count": len(max_angles),
                    "max_x_count": len(max_xs),
                    "max_y_count": len(max_ys),
                    "match_count": len(valid_ids_of_pt_id),
                    "raw_matched_count": len(matches)
                    # "features1": len(features1),
                    # "features2": len(features2)
                }
                return {"trans": [scale, max_trans_x, max_trans_y, max_angle], "detail": match_detail}
            else:
                print_log("Not match")
                return None
        else:
            print_log("No raw match")
        return None

    def match(self, description1, description2, ratio=1.0):
        (kps1, features1) = description1
        (kps2, features2) = description2
        valid_match_count_thre = 100
        if features1 is None or features2 is None:
            # print_log("No feature features found")
            return None
        raw_matches = self.matcher.match(features1, features2)
        raw_matches = sorted(raw_matches, key = lambda x:x.distance)
        good_matches = raw_matches[:10]

        match_info = Matcher.cc_find_transformation(good_matches, kps1, kps2)
        return match_info["trans"]