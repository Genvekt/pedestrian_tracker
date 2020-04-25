# Object Tracker

This project contains the application that may be used for simple objects tracking on video stream.

## How to run
Requirements:
- Linux or macOS with Python 3.6+
- gcc & g++ (5+)

Environment preparation:

```commandline
$ python3 -m venv trackerVenv
$ source trackerVenv/bin/activate
$ pip install -r requirements.txt
```
Install detectron2, full guide is available 
[here](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md).
```commandline
python -m pip install 'git+https://github.com/facebookresearch/detectron2.git'
```
Clone project
```commandline
$ git clone https://github.com/Genvekt/pedestrian_tracker
$ cd pedestrian_tracker
```
Get model an sample files
```commandline
$ cd model
$ wget https://dl.fbaipublicfiles.com/detectron2/COCO-Detection/faster_rcnn_R_101_FPN_3x/137851257/model_final_f6e8b1.pkl
$ cd ..
$ cd resources
$ wget https://www.robots.ox.ac.uk/ActiveVision/Research/Projects/2009bbenfold_headpose/Datasets/TownCentreXVID.avi
$ cd ..
```
Demo run example
```commandline
$ python demo.py -v="resources/TownCentreXVID.avi" -c=0.85 -l=0 -s=4
```
Demo may be stopped with `Esc` key.
## Project Parameters

Next parameters are used in demo:
```python
"-v", "--video"      : Path to input video, 'webcam' for webcam stream
"-y", "--yaml"       : Path to model .yaml config
"-w", "--weights"    : Path to model .pkl weights
"-c", "--confidence" : Minimum probability to filter weak detections
"-s", "--skip"       : N for predicting boxes each N frames
"-H", "--height"     : Max frame height, default 720
"-W", "--weight"     : Max frame width, default 1280
"-l", "--label"      : Label to track, full list at 'utils/coco_labels.py'
"-t", "--ttl"        : Number of detection trials to keep undetected tracks
      "--save"       : Path to save result
```

## Project Elements
### Predictor
The Predictor class defined at `predictor.py` is responsible for objects detection.
It is based on [detectron2](https://github.com/facebookresearch/detectron2) library which uses PyTorch models.

As a default, it will use pretrained **R101-FPN** Faster R-CNN model, available at 
[this](https://github.com/facebookresearch/detectron2/blob/master/MODEL_ZOO.md) page.
It is also possible to use any Faster R-CNN model defined there by means of downloading its configs, weights and specify them as
`--yaml` and `--weights` parameters accordingly.

Basically, it may be substituted by any class which will detect boxes in similar format.

### Tracker
Tracker class defined at `tracker.py`  takes care of assigning unique id to each new box and then tracking it over video frames.

### Comparison function
The demo uses **Intersection over union** in order to find the best box from new ones for track to be assigned to. 
To use other function, it may be specified at `utils/compare_functions.py` and then passed to `Tracker` on its creation.
