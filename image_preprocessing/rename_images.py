import os
import shutil

IMAGES_PATH = '../data_image'
DATA_BASE_PATH = '../data'

class_names = os.listdir(f'{IMAGES_PATH}')
print(class_names)

#creating main file
if not os.path.exists(DATA_BASE_PATH):
    print(f"Creating {DATA_BASE_PATH}")
    os.mkdir(DATA_BASE_PATH)

for names in class_names:
    idx_img = 0
    if not os.path.exists(f'{DATA_BASE_PATH}/{names}'):
        print(f"CREATING {DATA_BASE_PATH}/{names}")
        os.mkdir(f'{DATA_BASE_PATH}/{names}')

    images = os.listdir(f'{IMAGES_PATH}/{names}')
    for img in images:
        ext = os.path.splitext(img)[-1].lower()
        idx_img += 1
        shutil.copy(f'{IMAGES_PATH}/{names}/{img}',f'{DATA_BASE_PATH}/{names}/{names}_{idx_img}_{ext}')
        print(f'COPY: {IMAGES_PATH}/{names}/{img}  -> {DATA_BASE_PATH}/{names}/{names}_{idx_img}_{ext}')