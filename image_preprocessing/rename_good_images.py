import os

IMAGES_PATH = '../extra_fork/train/images'

LABELS_PATH = '../extra_fork/train/labels'

CLASS_NAME = 'spoon'
SP_CHAR = '1'

images_files = os.listdir(f'{IMAGES_PATH}')
print(images_files)

labels_files = os.listdir(f'{LABELS_PATH}')
print(labels_files)

idx_img = 0

for img_names in images_files:

    ext = os.path.splitext(img_names)[-1].lower()
    idx_img += 1
    os.rename(f'{IMAGES_PATH}/{img_names}', f'{IMAGES_PATH}/{CLASS_NAME}_{idx_img}_{SP_CHAR}_{ext}')
    print(f'RENAME IMAGE: {IMAGES_PATH}/{img_names} -> {IMAGES_PATH}/{CLASS_NAME}_{idx_img}_{SP_CHAR}_{ext}')

idx_lab = 0

for lbl_names in labels_files:

    ext = os.path.splitext(lbl_names)[-1].lower()
    idx_lab += 1
    os.rename(f'{LABELS_PATH}/{lbl_names}', f'{LABELS_PATH}/{CLASS_NAME}_{idx_lab}_{SP_CHAR}_{ext}')
    print(f'RENAME LABEL: {LABELS_PATH}/{lbl_names} -> {LABELS_PATH}/{CLASS_NAME}_{idx_lab}_{SP_CHAR}_{ext}')