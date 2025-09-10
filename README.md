# Object Detection Microservice

This project implements a microservice for object detection using the ultralytics/yolov5 implementation. It consists of a UI backend service for handling user uploads and an AI backend service for performing object detection.

## Prerequisites

- Docker
- Docker Compose
- Git

## Setup

1. Clone this repository:
```bash
git clone https://github.com/iyappan04/object_detect.git
cd object_detect
```

2. Build and run the Docker containers:
```bash
sudo docker compose up --build
```

## Usage

1. Open a web browser and navigate to `http://localhost:8080`
2. Upload an image using the provided form
3. The system will process the image using YOLOv5 and return the detected objects
4. Results can be found in:
   - `outputs/`: Processed images with detection boxes and JSON files containing detection results.



## Project Structure

```
object_detect/
├── ui_backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
│   └── templates/
│       └── upload.html
├── ai_backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app.py
├── outputs/
└── docker-compose.yml
```

## Detection Results

The system returns results in the following format:
```json
{
    "detections": [
        {
            "box": {
                "x1": 82,
                "x2": 135,
                "y1": 31,
                "y2": 201
            },
            "confidence": 0.73,
            "label": "vase"
        },
        {
            "box": {
                "x1": 82,
                "x2": 135,
                "y1": 31,
                "y2": 201
            },
            "confidence": 0.59,
            "label": "bottle"
        },
        {
            "box": {
                "x1": 0,
                "x2": 222,
                "y1": 125,
                "y2": 224
            },
            "confidence": 0.51,
            "label": "dining table"
        }
    ],
    "image_path": "outputs/ca7d05b3.jpg",
    "json_path": "outputs/ca7d05b3.json",
    "message": "Detection completed"
}
```

## Check Output
```
http://ai_backend:5000/${image_path}
http://ai_backend:5000/${json_path}
```

### Example:
```
http://ai_backend:5000/outputs/ca7d05b3.json
http://ai_backend:5000/outputs/ca7d05b3.jpg
```