# script to prepare data to train model
import os
from PIL import Image

DATA_PATH = 'data_image'
MAIN_FILE_PATH_SAVE = 'good_data'

#read class names
class_name = os.listdir(f'./{DATA_PATH}')
print(f'Class names: {class_name}')

#create main directory
if not os.path.exists(f'./{MAIN_FILE_PATH_SAVE}'):
    print('Create main directory')
    os.mkdir(f'./{MAIN_FILE_PATH_SAVE}')

#create directory for each class
for name in class_name:
    if not os.path.exists(f'./{MAIN_FILE_PATH_SAVE}/{name}'):
        print(f'Create {name} directory')
        os.mkdir(f'./{MAIN_FILE_PATH_SAVE}/{name}')

#load image for each class and rotate them
for names in class_name:
    print(f'Preproccess {names}')
    images_name = os.listdir(f'./{DATA_PATH}/{names}')

    for image in images_name:
        # rotate image
        for degree in range(0,360,20):

            try:
                img = Image.open(f'./{DATA_PATH}/{names}/{image}')
                rotated_img = img.rotate(degree)
                rotated_img.save(f'./{MAIN_FILE_PATH_SAVE}/{names}/{degree}_{image}')
            except:
                print(f'Some error with file {names} -> {image}')
                break

print("Preprocessing finished...")
