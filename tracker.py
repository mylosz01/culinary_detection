import numpy as np
import cv2
import math
import config

FRAME_WIDTH = config.FRAME_WIDTH
FRAME_HEIGHT = config.FRAME_HEIGHT

#single detect object class
class Object:

    def __init__(self,item) -> None:
        self.center_pt = (int(item.xywh[0][0]), int(item.xywh[0][1]))
        self.pt1 = (int(item.xyxy[0][0]), int(item.xyxy[0][1]))
        self.pt2 = (int(item.xyxy[0][2]), int(item.xyxy[0][3]))
        self.conf = item.conf[0]
        self.class_id = int(item.cls[0])

    def __str__(self):
        return f'Class_ID: {self.class_id}\nConf: {self.conf}\nCenter pt: {self.center_pt}\nPt1: {self.pt1}\nPt2: {self.pt2}\n'

#class used to tracking objects from frames
class Tracker:

    def __init__(self) -> None:
        self.items_counter = [0,0,0]
        self.cls_name = ['fork','knife','spoon']
        self.current_objects = {}
        self.color_rect = ((255,0,0),(0,255,0),(0,0,255))
        self.thickness_rect = 2
        self.color_text = ((255,0,0),(0,255,0),(0,0,255))
        self.scale_text = 3
        self.font_text = cv2.FONT_HERSHEY_PLAIN
        self.thickness_text = 2
        self.id_count = 0
        self.zone_width = 50

    #update position of detected items
    def update(self,predict_results):
        if len(predict_results) == 0:
            return None
        
        objects_list = {}
        #check if objects are in zone
        list_objects_in_zone = [item for item in predict_results[0].boxes if (FRAME_WIDTH//2) - self.zone_width < item.xywh[0][0] < (FRAME_WIDTH//2) + self.zone_width]

        #print(f'OBJECTS IN ZONE {len(list_objects_in_zone)}')
        for item in list_objects_in_zone:
            #print(f'TRACKER FIND {self.cls_name[int(item.cls[0])]}')
            #print(f'TRACKER POS xyxy: {item.xyxy[0]}')
            #print(f'TRACKER POS xywh: {item.xywh[0]}')

            #create item class
            new_object = Object(item)
            #print(f'NEW OBJECT : {new_object}')

            same_object_detected = False
            
            #check the items in detected objects
            for idx, obj in self.current_objects.items():
                
                #calculate distance beetween objects in dict and new object
                dist = math.hypot(obj.center_pt[0] - new_object.center_pt[0], obj.center_pt[1] - new_object.center_pt[1])
                #print(f'Distance: {dist}')

                #distance between same objects
                if dist < 200:
                    if new_object.class_id != obj.class_id:
                        same_object_detected = True
                        break
                    
                    #uptade new cord to exist object
                    self.current_objects[idx] = new_object
                    objects_list[idx] = new_object
                    same_object_detected = True
                    break
                
            #add new object to detected objects
            if same_object_detected is False:
                self.current_objects[self.id_count] = new_object
                objects_list[self.id_count] = new_object
                self.items_counter[new_object.class_id] += 1
                self.id_count += 1

        #update detected objects
        for idx, obj in self.current_objects.items():
            is_object_used = False

            for item in list_objects_in_zone:
                current_item = Object(item)

                if obj.center_pt == current_item.center_pt:
                    is_object_used = True
                    break
            
            #deleting not used object
            if is_object_used == False:  
                objects_list.pop(idx,None)

        self.current_objects = objects_list.copy()

    #reset stats
    def reset_stats(self):
        self.items_counter = [0,0,0]

    #annotate detected objects
    def annotate_objects(self,img):

        for item in self.current_objects.values():
            #create rectangle around object
            cv2.rectangle(img,
                        item.pt1,
                        item.pt2,
                        self.color_rect[item.class_id],
                        self.thickness_rect)
            
            #create text above object
            self.draw_text(img,
                            f"{self.cls_name[item.class_id]} {f'{float(item.conf):.2f}'}",
                            self.font_text,
                            (item.pt1[0] - 10, item.pt1[1] - 40),
                            self.scale_text,
                            self.thickness_text,
                            self.color_text[item.class_id],
                            )
        return img

    #draw stats in frame
    def show_stats(self,frame):
        self.draw_text(frame,f' fork : {self.items_counter[0]}',cv2.FONT_HERSHEY_PLAIN,(10,20),2,2,self.color_rect[0],(0,0,0))
        self.draw_text(frame,f' knife: {self.items_counter[1]}',cv2.FONT_HERSHEY_PLAIN,(10,70),2,2,self.color_rect[1],(0,0,0))
        self.draw_text(frame,f'spoon: {self.items_counter[2]}',cv2.FONT_HERSHEY_PLAIN,(10,120),2,2,self.color_rect[2],(0,0,0))

    #print text in frame
    def draw_text(self,img, text, font=cv2.FONT_HERSHEY_PLAIN, pos=(0, 0), font_scale=3, font_thickness=2, text_color=(0, 255, 0), text_color_bg=(0, 0, 0)):
        x, y = pos
        text_size, _ = cv2.getTextSize(text, font, font_scale, font_thickness)
        text_w, text_h = text_size
        cv2.rectangle(img, pos, (x + text_w, y + text_h), text_color_bg, - 1)
        cv2.putText(img, text, (x, y + text_h + font_scale - 1), font, font_scale, text_color, font_thickness)
