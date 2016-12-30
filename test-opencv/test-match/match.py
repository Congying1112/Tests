import numpy as np
import cv2
import math
import random
from sub_modules import show_stitch
from sub_modules.matcher import MaxGetter


def stat_scale(pts1, pts2, first_pt_ids, second_pt_ids, ids_of_pt_id):
    max_scale_getter = MaxGetter(1, 0.05)
    for id_of_pt_id in ids_of_pt_id:
        first_pt_id = first_pt_ids[id_of_pt_id]
        second_pt_id = second_pt_ids[id_of_pt_id]
        # cv2.line(show_img1, tuple(pts1[first_pt_id][0]), tuple(pts1[second_pt_id][0]), (0, 0, 255))
        # cv2.line(show_img2, tuple(pts2[first_pt_id][0]), tuple(pts2[second_pt_id][0]), (0, 0, 255))
        # cv2.imshow("img1", show_img1)
        # cv2.imshow("img2", show_img2)
        scale = calculate_scale(pts1[first_pt_id], pts1[second_pt_id], pts2[first_pt_id], pts2[second_pt_id])
        max_scale_getter.add(id_of_pt_id, scale)
    return max_scale_getter.get_max()


def stat_angle_and_trans(pts1, pts2, first_pt_ids, second_pt_ids, ids_of_pt_id):
    max_angle_getter = MaxGetter(math.pi, 0.05)
    max_trans_x_getter = MaxGetter(0, 1)
    max_trans_y_getter = MaxGetter(0, 1)
    for id_of_pt_id in ids_of_pt_id:
        first_pt_id = first_pt_ids[id_of_pt_id]
        second_pt_id = second_pt_ids[id_of_pt_id]
        trans = get_trans((pts1[first_pt_id], pts1[second_pt_id]), (pts2[first_pt_id], pts2[second_pt_id]))
        (delta_angle, (trans_x, trans_y)) = trans
        max_angle_getter.add(id_of_pt_id, delta_angle)
        max_trans_x_getter.add(id_of_pt_id, trans_x)
        max_trans_y_getter.add(id_of_pt_id, trans_y)
    return max_angle_getter.get_max(), max_trans_x_getter.get_max(), max_trans_y_getter.get_max()


def calculate_scale(pt11, pt12, pt21, pt22):
    delta_l1, delta_l2 = pt11 - pt12, pt21 - pt22
    delta_l1 = delta_l1[0]
    delta_l2 = delta_l2[0]
    length1 = delta_l1[0] * delta_l1[0] + delta_l1[1] * delta_l1[1]
    length2 = delta_l2[0] * delta_l2[0] + delta_l2[1] * delta_l2[1]
    if length2 < 0.0000001:
        length2 = 0.0000001
    return math.sqrt(length1 / length2)


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


def cc_find_transformation(matches, img1, img2, kps1, kps2):
    if matches:
        # construct the two sets of points
        pts1 = np.float32([kps1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
        pts2 = np.float32([kps2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)

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

        max_scale_list = stat_scale(pts1, pts2, first_pt_ids, second_pt_ids, ids_of_pt_id)
        valid_ids_of_pt_id = list(map(lambda x: x[0], max_scale_list))
        print(valid_ids_of_pt_id)
        scale = np.mean(list(map(lambda x: x[1], max_scale_list)))

        (h, w) = img1.shape
        img2 = cv2.resize(img2, (int(w * scale), int(h * scale)))
        # cv2.imshow("img1", img1)
        # cv2.imshow("img2", img2)
        # cv2.waitKey(-1)
        pts2 = list(map(lambda x: x * scale, pts2))
        if True:
            show_img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2RGB)
            show_img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2RGB)
            for idx, pt1 in enumerate(pts1):
                print(idx, pt1[0])
                show_img1 = cv2.circle(show_img1, tuple(pt1[0]), 2, (0, 0, 255))
                show_img2 = cv2.circle(show_img2, tuple(pts2[idx][0]), 2, (0, 0, 255))
                cv2.imshow("img1", show_img1)
                cv2.imshow("img2", show_img2)
            cv2.waitKey(-1)

        max_angles, max_xs, max_ys = stat_angle_and_trans(pts1, pts2, first_pt_ids, second_pt_ids, valid_ids_of_pt_id)

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


def match_two(img1, img2):
    # SIFT
    # sift = cv2.xfeatures2d.SIFT_create()
    # kp1, des1 = sift.detectAndCompute(img1,None)
    # kp2, des2 = sift.detectAndCompute(img2,None)

    # ORB
    orb = cv2.ORB_create()
    kp1, des1 = orb.compute(img1, orb.detect(img1, None))
    kp2, des2 = orb.compute(img2, orb.detect(img2, None))

    # create BFMatcher object
    bf = cv2.BFMatcher()
    # Match descriptors.
    matches = bf.match(des1, des2)

    # Sort them in the order of their distance.
    matches = sorted(matches, key=lambda x: x.distance)
    good = matches[:10]

    match_info = cc_find_transformation(good, img1, img2, kp1, kp2)
    return match_info["trans"]


img1 = cv2.imread('/home/congying/Data/stitch-test/src/5/0.JPG', 0)
img2 = cv2.imread('/home/congying/Data/stitch-test/src/5/1.JPG', 0)
# img2 = cv2.imread('/home/congying/Data/stitch-test/4/2.JPG', 0)
# img3 = cv2.imread('/home/congying/Data/stitch-test/4/3.JPG', 0)
shape = (320, 240)
img1 = cv2.resize(img1, shape)
img2 = cv2.resize(img2, shape)
# img3 = cv2.resize(img3, shape)
# cv2.imshow("img1", img1)
# cv2.imshow("img2", img2)
match_info_12 = match_two(img1, img2)
# match_info_23 = match_two(img2, img3)

show_stitch.show_stitched_imgs([(img1, (1, 0, 0, 0)), (img2, match_info_12)], -1)
