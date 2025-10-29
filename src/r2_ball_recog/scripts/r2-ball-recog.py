#!/usr/bin/env python3

# 機体内用

from ultralytics import YOLO
import cv2
import rospy
from std_msgs.msg import Bool 
from std_msgs.msg import Int8
import time
import numpy as np



# def talker(judge, is_detect, detect_time):
    
#     pubpur = rospy.Publisher('ball_purple', R2Modules, queue_size=10)
#     R2_msg = R2Modules()
#     pub2balls = rospy.Publisher('ball_2_balls', Int8, queue_size=10)
#     Inty8 = Int8()
    
#     rospy.init_node('r2-ball-recog', anonymous=True)
#     r = rospy.Rate(10) 
#     if not rospy.is_shutdown():
#         if is_detect:
#             if rospy.get_time()-detect_time < 3:
#                 return is_detect, detect_time
#             else:
#                 is_detect = False
#                 pubpur.publish(R2_msg)


#         if judge == 1: # 赤
#            R2_msg.data = False
#            pubpur.publish(R2_msg)

#            has_ball = 1
#            pub2balls.publish(has_ball)


#         if judge == 2: # 青
#            R2_msg.data = False
#            pubpur.publish(R2_msg)

#            has_ball = 2
#            pub2balls.publish(has_ball)


#         if judge == 3 and not is_detect: # 紫
#            R2_msg.data = True
#            detect_time = rospy.get_time()
#            is_detect = True


#            has_ball = 3
#            pub2balls.publish(has_ball)


#         if judge == 0: # 何も持ってない
#            R2_msg.data = False
#            pubpur.publish(R2_msg)

#            has_ball = 0
#            pub2balls.publish(has_ball)

#         return is_detect, detect_time


#######################################################################
# 青ダミー用
#######################################################################
#######################################################################
#######################################################################

def talker(judge, conf, is_detect, detect_time):
    
    pubpur = rospy.Publisher('toggle_emit', Bool, queue_size=10)
    R2_msg = Bool()
    pub2balls = rospy.Publisher('ball_2_balls', Int8, queue_size=10)
    Inty8 = Int8()
    
    rospy.init_node('r2_ball_recog', anonymous=True)
    r = rospy.Rate(10) 
    if not rospy.is_shutdown():
        if conf >= 0.5:
            if is_detect:
                if rospy.get_time()-detect_time < 3: # 空籾を認識してから3秒後に排出
                    return is_detect, detect_time
                elif rospy.get_time() - detect_time < 6: # 排出状態を最低3秒は維持
                    R2_msg.data= True
                    pubpur.publish(R2_msg)
                else: 
                    is_detect = False
                
            else: 
                if judge == 1: # 赤
                    R2_msg.data = False
                    pubpur.publish(R2_msg)
                
                    has_ball = 1
                    pub2balls.publish(has_ball)
            
            
                if judge == 2: # 青
                    # R2_msg.data = True
                    # pubpur.publish(R2_msg)
                    detect_time = rospy.get_time()
                    is_detect = True
                    
                    has_ball = 2
                    pub2balls.publish(has_ball)
                    
                if judge == 3: # 紫
                    # R2_msg.data = True
                    # pubpur.publish(R2_msg)
                    detect_time = rospy.get_time()
                    is_detect = True
                    
                    has_ball = 3
                    pub2balls.publish(has_ball)
                    
                
                if judge == 0: # 何も持ってない
                    R2_msg.data = False
                    pubpur.publish(R2_msg)
                
                    has_ball = 0
                    pub2balls.publish(has_ball)



        return is_detect, detect_time
#######################################################################
#######################################################################

def object_detection(model):

    is_detect = False
    detect_time = 0

    cap = cv2.VideoCapture('/dev/video14')
    # カメラがどこにあるかわからないときはcmdで　$ls -l /dev/video*　と打って違いが出たところ
    cap.set(cv2.CAP_PROP_FPS, 60)
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print('fps is ', fps)

    w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))              
    # カメラの横幅を取得
    print("カメラの横幅は ", w)
    h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))             
    # カメラの縦幅を取得
    print("カメラの縦幅は ", h)

    x_value = 0  # x_value を初期化
    y_value = 0  # y_value を初期化
    conf = 0  # conf を初期化



    a = (int(w/4), int(0))
    # b = (int(2*w/3), int(h/8))
    # c = (int(w/3), int(7*h/8))
    d = (int(3*w/4), int(3*h/4))

    # w = b[0]-a[0]
    # h = c[1]-a[1]

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        mask = np.zeros(frame.shape, dtype = np.uint8)
        cv2.rectangle(mask, a, d, (255, 255, 255), -1)
        maskresult = cv2.bitwise_and(frame, mask)


        
        # フレームで物体検出
        results = model(maskresult)

        judge = 0
        # print("out loop")      
        for result in results:
            # print("result loop")
        
        # resultsから検出された物体情報を１つずつ取り出す
            boxes = result.boxes
            # 検出された物体に含まれる各ボックス情報を取得            
            for box in boxes:
                # print("box loop")
            # 各ボックスに対する操作
                box = box.numpy()
                # ボックス情報をNumPy配列に変換
                item_number = int(box.cls.item())
                # 物体のクラスIDを取得
                # print(item_number, end=" ")

                conf = box.conf.item()
                # 物体の信頼度を取得
                # print("信頼度は ", conf, "!!!!!")

                xywh = box.xywh
                # ボックスの座標情報を取得
                # print(xywh)
                
                # print(model.names[item_number])
                # modelオブジェクトのnames属性からitem_numberに対応する物体のクラス名を出力

                judge = 0


                # print(judge)
                x_value = int(xywh[0][0])
                y_value = int(xywh[0][1])
                cv2.circle(maskresult, (x_value, y_value), 2, (255 ,255, 255), 3)
                


                if item_number == 2: # 赤用
                    judge = 1
                    # print("赤あるよ(笑)")
                    # talker(judge)
                elif item_number == 0: # 青用
                    judge = 2
                    # print("青あるよ(笑)")
                    # talker(judge)
                elif item_number == 1: # 紫用
                    judge = 3
                    # print("紫あるよ(笑)")
                    # talker(judge)
                
                break
            # print("End of box loop")
            # print(judge)
            is_detect, detect_time = talker(judge, conf, is_detect, detect_time)   

        # アノテートされたフレームを表示
        annotated_frame = results[0].plot()

        cv2.imshow("mask", mask)
        cv2.imshow("YOLOv8!!!", annotated_frame)

        # 'q'が押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # YOLOモデルを読み込む
    model = YOLO('r2_ball_recog/yolov8_weights_folderv2/2/best.pt')
    # Webカメラのフレームで物体検出を実行
    object_detection(model)
    
