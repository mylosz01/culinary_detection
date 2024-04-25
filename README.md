# _Culinary detection_

Culinary detection is a system that allows for real-time identification of cutlery in an image captured from a camera.

## Table of contents
* [Description](#description)
* [Features](#features)
* [Technologies](#technologies)
* [Installation](#installation)
* [License](#license)

## Description
The project included collecting appropriate data - images of cutlery, in order to then train a ready-made YOLOv8 model using the Ultralytics library. The tracker implemented in the system tracks the location of the identified cutlery and then counts it when it crosses the identification area.

![GIFMaker_me](https://github.com/mylosz01/culinary_detection/assets/97054791/e47613fe-4f0e-4ed4-85cd-eca7d567e314)

## Features
* identification of cutlery in the image
* counting cutlery

## Technologies
Project is created with:
* Python 3.10+
* Ultralytics
* OpenCV

## Installation
1. Clone the repository:

   ```sh
   git clone https://github.com/mylosz01/culinary_detection
3. Navigate to the repository folder:
3. In app.py if you are using your camera through net, config IP address of your camera or write 0 if you are using your manual camera:
```python
#IP CAMERA
URL_CAMERA = 'https://x.x.x.x:8080/video'
#OR
#URL_CAMERA = 0
```
4. Run the script:
   ```sh
   python app.py
5. System is ready to use :)
## License

[MIT](https://choosealicense.com/licenses/mit/)
