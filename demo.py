import argparse
import cv2
from predictor import Predictor
from tracker import Tracker
from utils.compare_functions import bb_IOU
from define import *

# Construct the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", default=DEFAULT_VIDEO, help="Path to input video, 'webcam' for webcam stream")
ap.add_argument("-y", "--yaml", default=MODEL_YAML, help="Path to model .yaml config")
ap.add_argument("-w", "--weights", default=MODEL_WEIGHTS, help="Path to model .pkl weights")
ap.add_argument("-c", "--confidence", type=float, default=MIN_CONFIDENCE,
                help="Minimum probability to filter weak detections")
ap.add_argument("-s", "--skip", type=int, default=SKIP_FRAME_RATIO, help="N for predicting boxes each N frames")
ap.add_argument("-H", "--height", type=int, default=MAX_FRAME_H, help="Max frame height")
ap.add_argument("-W", "--width", type=int, default=MAX_FRAME_W, help="Max frame width")
ap.add_argument("-l", "--label", type=int, default=TRACK_CLASS,
                help="Label to track, full list at 'utils/coco_labels.py'")
ap.add_argument("-t", "--ttl", type=int, default=TRACK_TTL,
                help="Number of detection trials to keep undetected tracks")
ap.add_argument("--save", default='',
                help="Path to save result")

if __name__ == '__main__':
    args = vars(ap.parse_args())

    # Define the model for predicting bounding boxes
    print("[INFO] Loading predictor from disk...")
    predictor = Predictor(args['yaml'], args['weights'], threshold=args['confidence'])

    # Define tracker for tracking bounding boxes
    print("[INFO] Initialising tracker...")
    tracker = Tracker(bb_IOU, args['ttl'])

    # Define the video stream
    print("[INFO] Starting video stream...")
    if args['video'] == 'webcam':
        capturer = cv2.VideoCapture(0)
    else:
        capturer = cv2.VideoCapture(args['video'])
    # Save result
    if args['save'] != '':
        print("[INFO] Saving to " + args['save'] + " ...")
        fps = capturer.get(cv2.CAP_PROP_FPS)
        out = cv2.VideoWriter('results/output2.mp4', cv2.VideoWriter.fourcc('X', 'V', 'I', 'D'), fps, (args['width'], args['height']))
    # Start stream
    frame_count = 0
    print("[INFO] Stream may be stopped with 'Esc'.")
    while True:
        ok, frame = capturer.read()
        if not ok:
            break

        # Resize frame
        fx = min(1, args['height'] / frame.shape[0])
        fy = min(1, args['width'] / frame.shape[1])
        frame = cv2.resize(frame, (-1, -1), fx=fx, fy=fy)

        # Detect boxes every N frames and update tracks
        if frame_count % args['skip'] == 0:
            boxes = predictor.predict(frame, args['label'])
            tracker.update_tracks(boxes)

        # Draw all boxes
        for track_id, track_box in tracker.tracks.items():

            upper_point = (track_box['leftup']['x'], track_box['leftup']['y'])
            lower_point = (track_box['rightdown']['x'], track_box['rightdown']['y'])

            # Define the color of box
            if track_box["ttl"] < args['ttl']:
                color = (100, 100, 100)         # Gray if track was not detected on this frame
            else:
                color = (0, 0, 255)             # Red if track was detected on this frame

            # Draw box
            frame = cv2.rectangle(frame, upper_point, lower_point, color, 1)

            # Draw track id
            frame = cv2.putText(frame, str(track_id), (upper_point[0], upper_point[1]+10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        # Show result
        cv2.imshow("Video", frame)
        if args['save'] != '':
            out.write(frame)
        frame_count += 1

        # End program with 'Esc' key
        key = cv2.waitKey(1)
        if key == 27:
            break

    # Clear resources
    print("[INFO] Stopping stream...")
    capturer.release()
    if args['save'] != '':
        print("[INFO] Saving recording...")
        out.release()
    print("[INFO] Program finished.")
    cv2.destroyAllWindows()
