def bb_IOU(boxA, boxB):
    """
    Function that compares boxes by Intersection Over Union value
    :param boxA: dict with keys 'leftup' and 'rightdown', each having 'x' and 'y' coordinates
    :param boxB: dict with keys 'leftup' and 'rightdown', each having 'x' and 'y' coordinates
    :return: Intersection Over Union value
    """

    # Determine coordinates of the intersection region
    xA = max(boxA['leftup']['x'], boxB['leftup']['x'])
    yA = max(boxA['leftup']['y'], boxB['leftup']['y'])
    xB = min(boxA['rightdown']['x'], boxB['rightdown']['x'])
    yB = min(boxA['rightdown']['y'], boxB['rightdown']['y'])

    # Compute the area of intersection region
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)

    # Compute the area of both boxes
    boxAArea = (boxA['rightdown']['x'] - boxA['leftup']['x'] + 1) * (boxA['rightdown']['y'] - boxA['leftup']['y'] + 1)
    boxBArea = (boxB['rightdown']['x'] - boxB['leftup']['x'] + 1) * (boxB['rightdown']['y'] - boxB['leftup']['y'] + 1)

    # Compute the intersection over union
    iou = interArea / float(boxAArea + boxBArea - interArea)

    # Return the intersection over union value
    return iou