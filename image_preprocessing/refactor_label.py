#copy labels
import os

BASE_PATH = '../data/labels'
LABELS = '../labels'

class_names = os.listdir(f'{BASE_PATH}')
print(class_names)

if not os.path.exists(f'{LABELS}'):
    print(f"CREATING {LABELS}")
    os.mkdir(f"{LABELS}")

index_class = 0

for name in class_names:
    annotations = os.listdir(f'{BASE_PATH}/{name}')
    #print(annotations)
    for annot in annotations:
        if annot == 'classes.txt':
            continue
        
        with open(f'{BASE_PATH}/{name}/{annot}','r') as file:
            res = file.read()
            #print(res)

            with open(f'{LABELS}/{annot}','w') as f:
                res = res.replace(res[0],str(index_class),1)
                f.write(res)

    index_class += 1
