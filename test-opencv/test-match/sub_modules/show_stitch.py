import cv2
import numpy as np
import math
from .print_log import print_log
from sympy import Point, Line, Polygon
from collections import deque


def get_trans_matrix(scale, rotate, trans_x, trans_y):
    return np.matrix(
        [[scale * math.cos(rotate), -scale * math.sin(rotate), trans_x], [scale * math.sin(rotate), scale * math.cos(rotate), trans_y], [0, 0, 1]])


def cout_corners(corners):
    for corner in corners:
        print(corner[0], corner[1])


def find_valid_corners(mat_size, corners):
    popped = False
    top_edge_line = Line(Point(0, 0), Point(100, 0))
    while corners and corners[0][1] < 0:
        pt = corners.popleft()
        left_line = Line(pt, corners[0])
        temp_pt = left_line.intersection(top_edge_line)
        popped = True
    if popped:
        first_pt = corners[0]
        if first_pt[1] != temp_pt[0].y:
            new_point = (int(temp_pt[0].x), int(temp_pt[0].y))
            if new_point[0] != corners[0][0] and new_point[1] != corners[0[1]]:
                corners.appendleft(new_point)

    popped = False
    bottom_edge_line = Line(Point(0, mat_size[1] - 1), Point(100, mat_size[1] - 1))
    while corners[-1][1] >= mat_size[1] and len(corners) > 0:
        pt = corners.pop()
        left_line = Line(pt, corners[-1])
        temp_pt = left_line.intersection(bottom_edge_line)
        popped = True
    if popped:
        first_pt = corners[0]
        if first_pt[1] != temp_pt[0].y:
            new_point = (int(temp_pt[0].x), int(temp_pt[0].y))
            if new_point[0] != corners[-1][0] and new_point[1] != corners[-1][1]:
                corners.append(new_point)
    return corners


def find_left_and_right_points_on_lines_from_corners(corners, mat_size):
    corners_tmp = deque(list(map(lambda x: list(map(lambda y: int(y), x)), corners)))
    assert (len(corners_tmp) == 4)
    left_top_c_id = 0
    for c_id, c in enumerate(corners_tmp):
        if c[1] < corners_tmp[left_top_c_id][1]:
            left_top_c_id = c_id
        elif c[1] == corners_tmp[left_top_c_id][1] and c[0] < corners[left_top_c_id][0]:
            left_top_c_id = c_id
    corners = deque([])
    for i in list(range(left_top_c_id, len(corners_tmp))) + list(range(0, left_top_c_id)):
        corners.append(corners_tmp[i])
    left_corners, right_corners = deque([]), deque([])
    if corners[0][1] == corners[1][1]:
        left_corners.append(corners[0])
        right_corners.append(corners[1])
    elif corners[0][1] < corners[1][1]:
        left_corners.append(corners[0])
        right_corners.append(corners[0])
        right_corners.append(corners[1])
    else:
        left_corners.append(corners[1])
        left_corners.append(corners[0])
        right_corners.append(corners[1])
    if corners[2][1] == corners[3][1]:
        right_corners.append(corners[2])
        left_corners.append(corners[3])
    elif corners[2][1] < corners[3][1]:
        left_corners.append(corners[3])
        right_corners.append(corners[2])
        right_corners.append(corners[3])
    else:
        left_corners.append(corners[3])
        left_corners.append(corners[2])
        right_corners.append(corners[2])

    left_corners = find_valid_corners(mat_size, left_corners)
    right_corners = find_valid_corners(mat_size, right_corners)

    if not (left_corners and right_corners):
        return []
    assert (left_corners[0][1] == right_corners[0][1])

    left1 = left_corners.popleft()
    left2 = left_corners.popleft()
    left_line = Line(left1, left2)

    right1 = right_corners.popleft()
    right2 = right_corners.popleft()
    right_line = Line(right1, right2)

    pts_on_lines = []  # y, left_x, right_x
    curr_y = left1[1]
    while True:
        if curr_y > left2[1]:
            if not left_corners:
                break
            else:
                left1 = left2
                left2 = left_corners.popleft()
                left_line = Line(left1, left2)
        if curr_y > right2[1]:
            if not right_corners:
                break
            else:
                right1 = right2
                right2 = right_corners.popleft()
                right_line = Line(right1, right2)
        hor_line_with_curr_y = Line(Point(0, curr_y), Point(100, curr_y))
        temp_pt = left_line.intersection(hor_line_with_curr_y)
        left_cross = temp_pt[0]
        left_x = 0 if left_cross.x < 0 else (left_cross.x if left_cross.x < mat_size[0] else (mat_size[0] - 1))
        temp_pt = right_line.intersection(hor_line_with_curr_y)
        right_cross = temp_pt[0]
        right_x = 0 if right_cross.x < 0 else (right_cross.x if right_cross.x < mat_size[0] else (mat_size[0] - 1))
        pts_on_lines.append((curr_y, int(left_x), int(right_x)))
        curr_y += 1
    return pts_on_lines


def affine_two_images(src, dst, h, result_size):
    trans_matrix = np.matrix(h)
    height, width = src.shape[0], src.shape[1]
    transed_corners = trans_matrix * np.matrix(
        [[0, width - 1, width - 1, 0], [0, 0, height - 1, height - 1], [1, 1, 1, 1]])
    corners = []
    for pt in transed_corners.transpose():
        corners.append((pt.item((0, 0)), pt.item((0, 1))))
    pts_on_lines_to_copy = find_left_and_right_points_on_lines_from_corners(corners, result_size)
    h_affine = h[0:2]
    result = cv2.warpAffine(src, h_affine, result_size)
    jump = 0
    for (y, x1, x2) in pts_on_lines_to_copy:
        if jump < 10:
            jump += 1
            continue
        for x in range(x1 + 2, x2 - 1):
            dst[y][x] = result[y][x]
    return dst


def show_stitched_imgs(imgs_with_stitch_info, wait_key=-1):
    if len(imgs_with_stitch_info) < 2:
        return
    else:
        affine_info_list = []
        min_x, min_y, max_x, max_y = (0, 0, 0, 0)
        last_h = np.matrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
        for image_data in imgs_with_stitch_info:
            (image, (scale, trans_x, trans_y, angle)) = image_data
            h = get_trans_matrix(scale, -angle, trans_x, trans_y)
            h = cv2.getRotationMatrix2D(tuple(map(lambda x: int(x/2), image.shape)), -angle*180.0/3.1415927, scale)
            h[0, 2] += trans_x
            h[1, 2] += trans_y
            h = np.vstack((h, [0, 0, 1]))
            last_h = last_h * h
            print(h)
            affine_info_list.append(last_h)
            trans_matrix = np.matrix(last_h)
            height, width = image.shape[0], image.shape[1]
            transed_corners = trans_matrix * np.matrix(
                [[0, width - 1, width - 1, 0], [0, 0, height - 1, height - 1], [1, 1, 1, 1]])
            for pt in transed_corners.transpose():
                min_x = min_x if pt.item((0, 0)) >= min_x else pt.item((0, 0))
                min_y = min_y if pt.item((0, 1)) >= min_y else pt.item((0, 1))
                max_x = max_x if pt.item((0, 0)) <= max_x else pt.item((0, 0))
                max_y = max_y if pt.item((0, 1)) <= max_y else pt.item((0, 1))
                # print min_x, min_y, max_x, max_y

        result_height, result_width = int(max_y - min_y + 10), int(max_x - min_x + 10)
        print_log(result_height, result_width)
        result = np.zeros((result_height, result_width), dtype=np.uint8)
        for i, (image, match_info) in enumerate(imgs_with_stitch_info):
            # print affine_info_list[i], affine_info_list[i][0, 2], affine_info_list[i][1, 2]
            print(affine_info_list[i])
            affine_info_list[i][0, 2] -= min_x
            affine_info_list[i][1, 2] -= min_y
            # font = cv2.FONT_HERSHEY_SIMPLEX
            image2 = image.copy()
            # cv2.putText(image2, str(match_info[3]), (50, 50), font, 1, (255, 255, 255), 1, 1)
            # cv2.putText(image2, str(match_info[3]), (52, 52), font, 1, (0, 0, 0), 1, 1)
            cv2.imshow("img2", image2)
            result = affine_two_images(image2, result, affine_info_list[i].A.astype(float), (result_width, result_height))
            cv2.imshow("stitched_img", result)
            cv2.waitKey(wait_key)
        print_log("Finish Drawing")
        cv2.imshow("stitched_img", result)
        cv2.waitKey(-1)
        return result


def show_stitch(img1, img2, match_info, wait_key=-1):
    cv2.imshow("img1", img1)
    cv2.imshow("img2", img2)
    return show_stitched_imgs([(img1, (1, 0, 0, 0)), (img2, match_info)], wait_key)
