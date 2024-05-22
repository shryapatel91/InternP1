from flask import Flask, request, jsonify, render_template
from celery import Celery
import os
import torch
from torchvision.models.segmentation import deeplabv3_resnet50, DeepLabV3_ResNet50_Weights
from PIL import Image
import numpy as np
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='redis://localhost:6379/0',
    CELERY_RESULT_BACKEND='redis://localhost:6379/0',
    CELERY_IMPORTS=('app',),  # Ensure the correct module name is used
    BROKER_CONNECTION_RETRY_ON_STARTUP=True
)

celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)

# Load pre-trained DeepLabV3 model with weights
weights = DeepLabV3_ResNet50_Weights.COCO_WITH_VOC_LABELS_V1
model = deeplabv3_resnet50(weights=weights)
model.eval()

transform = weights.transforms()

# Define a color map for visualization
def random_color_map(n):
    np.random.seed(42)  # For reproducibility
    colors = np.random.randint(0, 255, size=(n, 3), dtype=np.uint8)
    return colors

def decode_segmap(output_predictions, num_classes=21):
    height, width = output_predictions.shape
    colors = random_color_map(num_classes)
    
    rgb_image = np.zeros((height, width, 3), dtype=np.uint8)
    for class_idx in range(num_classes):
        mask = output_predictions == class_idx
        if class_idx == 0:  # Background class (blue)
            rgb_image[mask] = [0, 0, 0]  # Black color
        else:
            rgb_image[mask] = colors[class_idx]
    
    return rgb_image

@celery.task(bind=True, name='app.process_image')  # Ensure the task name is correct
def process_image(self, image_path):
    logger.info("Entered the process_image function")
    try:
        logger.info(f"Processing image at path: {image_path}")
        image = Image.open(image_path).convert("RGB")
        input_tensor = transform(image).unsqueeze(0)
        with torch.no_grad():
            output = model(input_tensor)['out'][0]
        output_predictions = output.argmax(0).byte().cpu().numpy()
        
        output_image_np = decode_segmap(output_predictions)
        output_image = Image.fromarray(output_image_np)
        output_image_path = image_path.replace('.jpg', '_segmented.png')
        output_image.save(output_image_path)
        return output_image_path
    except Exception as e:
        logger.error(f"Error processing image: {e}")
        self.retry(exc=e)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400
    save_path = os.path.join('static/uploads/', file.filename)
    file.save(save_path)
    logger.info(f"File saved at path: {save_path}")
    task = process_image.apply_async(args=[save_path])
    logger.info(f"Task created with ID: {task.id}")
    return jsonify({"task_id": task.id}), 202

@app.route('/status/<task_id>', methods=['GET'])
def task_status(task_id):
    task = process_image.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {'state': task.state, 'status': 'Pending...'}
    elif task.state != 'FAILURE':
        response = {'state': task.state, 'result': task.result}
    else:
        response = {'state': task.state, 'status': str(task.info)}
    return jsonify(response)

if __name__ == '__main__':
    os.makedirs('static/uploads', exist_ok=True)
    app.run(debug=True)


'''------------------------------------------------------------------------------------------------------'''

