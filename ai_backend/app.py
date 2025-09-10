from flask import Flask, request, jsonify
from ultralytics import YOLO
import cv2
import numpy as np
import os
import uuid
import json
from flask import send_from_directory

app = Flask(__name__)


model = YOLO('yolov5s.pt')  

OUTPUT_DIR = "outputs"
os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route('/outputs/<filename>')
def serve_output_file(filename):
    return send_from_directory(OUTPUT_DIR, filename)

@app.route("/detect", methods=["POST"])
def detect():
    if 'image' not in request.files:
        return jsonify({"error": "No image uploaded"}), 400

    image_file = request.files["image"]
    image = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)

    
    results = model(image)[0]  
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])  
        cls_id = int(box.cls[0])              
        conf = float(box.conf[0])           
        label = model.names[cls_id]        
        
        cv2.rectangle(image, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(image, f"{label} {conf:.2f}", (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        detections.append({
            "label": label,
            "confidence": round(conf, 2),
            "box": {
                "x1": x1,
                "y1": y1,
                "x2": x2,
                "y2": y2
            }
        })

    image_id = str(uuid.uuid4())[:8]
    output_image_path = os.path.join(OUTPUT_DIR, f"{image_id}.jpg")
    output_json_path = os.path.join(OUTPUT_DIR, f"{image_id}.json")

    
    cv2.imwrite(output_image_path, image)
    with open(output_json_path, "w") as f:
        json.dump(detections, f, indent=2)


    return jsonify({
        "message": "Detection completed",
        "image_path": output_image_path,
        "json_path": output_json_path,
        "detections": detections
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
