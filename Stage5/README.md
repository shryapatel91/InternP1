
# Stage 5

## Task:
Create and Train a Image Segmentation (Min 2 Segmentation if available)  application with fully functional Backend Queue System for Multiple Parallel Tasks. Implement the Backend Queue System using  Flask


## Description
- This program takes input .jpg image, performs image segementation on it and shows the processed image. 
- The model used here for segmentation is 'deeplabv3_resnet50' which performs semantic segmentation and it is fairly accurate.
- To implement backend queue system, 'Celery' is used to manage tasks queue and to execute the tasks.
- 'Redis' is used as a message broker, a communicator between the flask application and the Celery workers. 
- Flask is used as web framework which creates the tasks. 
## Installation
```bash
pip install flask
```
```bash
pip install celery
```
```bash
pip install torch
```
```bash
pip install torchvision
```
```bash
pip install Pillow
```
```bash
pip install numpy
```

## Run the application
- First go to https://github.com/MicrosoftArchive/redis/releases, download Redis-x64-3.0.504.zip, and extract it
- Open command prompt, open the directory Redis-x64-3.0.504
- Write the following command:
```bash
redis-server.exe redis.windows.conf
```
- This will start the redis server
- Now to start Celery, go to terminal and install:
```bash
pip install gevent
```
OR 
```bash
pip install eventlet
```
Then
```bash
celery -A app.celery worker --loglevel=info -P gevent
```
- This will start celery. When the line 
```bash
[2024-05-22 16:03:00,404: INFO/MainProcess] celery@LAPTOP-2AHLVDQN ready.
``` 
comes then have new terminal and give command:
```bash
python app.py
```
- Click on the URL
- Upload a .jpg image
- The input image(.jpg) and the processed image(.png) will be stored static/uploads folder.


    