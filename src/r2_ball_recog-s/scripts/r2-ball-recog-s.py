#!/usr/bin/env python3

# サイロ用

from ultralytics import YOLO
import cv2
import rospy
from std_msgs.msg import Int16MultiArray
import numpy as np

sairo = np.zeros((3, 5))

def array_detection(x_value, y_value, judge, conf, a1, b1, c1, d1, e1, a4, b4, c4, d4, e4):
    global sairo
    pub = rospy.Publisher('ball-s', Int16MultiArray, queue_size=10)
    rospy.init_node('r2_ball_recog_s', anonymous=True)
    r = rospy.Rate(10) 
    if not rospy.is_shutdown():
        sairo = sairo.astype(int)
        if conf >= 0.5:         
            if x_value in range(a1[0], a4[0]) and y_value in range(a1[1], int(a1[1]+(a4[1]-a1[1])/3)) :
                sairo[0][0] = judge
            elif x_value in range(b1[0], b4[0]) and y_value in range(a1[1], int(a1[1]+(a4[1]-a1[1])/3)) :
                sairo[0][1] = judge
            elif x_value in range(c1[0], c4[0]) and y_value in range(a1[1], int(a1[1]+(a4[1]-a1[1])/3)) :
                sairo[0][2] = judge
            elif x_value in range(d1[0], d4[0]) and y_value in range(a1[1], int(a1[1]+(a4[1]-a1[1])/3)) :
                sairo[0][3] = judge
            elif x_value in range(e1[0], e4[0]) and y_value in range(a1[1], int(a1[1]+(a4[1]-a1[1])/3)) :
                sairo[0][4] = judge

            elif x_value in range(a1[0], a4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])/3), int(a1[1]+(a4[1]-a1[1])*2/3)) :
                sairo[1][0] = judge
            elif x_value in range(b1[0], b4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])/3), int(a1[1]+(a4[1]-a1[1])*2/3)) :
                sairo[1][1] = judge
            elif x_value in range(c1[0], c4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])/3), int(a1[1]+(a4[1]-a1[1])*2/3)) :
                sairo[1][2] = judge
            elif x_value in range(d1[0], d4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])/3), int(a1[1]+(a4[1]-a1[1])*2/3)) :
                sairo[1][3] = judge
            elif x_value in range(e1[0], e4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])/3), int(a1[1]+(a4[1]-a1[1])*2/3)) :
                sairo[1][4] = judge

            elif x_value in range(a1[0], a4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])*2/3), a4[1]) :
                sairo[2][0] = judge
            elif x_value in range(b1[0], b4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])*2/3), a4[1]) :
                sairo[2][1] = judge
            elif x_value in range(c1[0], c4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])*2/3), a4[1]) :
                sairo[2][2] = judge
            elif x_value in range(d1[0], d4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])*2/3), a4[1]) :
                sairo[2][3] = judge
            elif x_value in range(e1[0], e4[0]) and y_value in range(int(a1[1]+(a4[1]-a1[1])*2/3), a4[1]) :
                sairo[2][4] = judge

            # rospy.loginfo(sairo)
            # print(sairo)

            # Int16MultiArray メッセージの初期化
            msg = Int16MultiArray()
            msg.layout.dim = []
            msg.data = sairo.flatten().tolist()  # 2次元配列を1次元に平坦化し、リストに変換
            pub.publish(msg)

def object_detection(model):
    global sairo
    
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

    # 左から各列の一番上のボール場所の左上座標
    a1 = (int(w/10-3*w/40), int(h/3))
    b1 = (int(30*w/100-3*w/40), int(h/3))
    c1 = (int(w/2-3*w/40), int(h/3))
    d1 = (int(70*w/100-3*w/40), int(h/3))
    e1 = (int(9*w/10-3*w/40), int(h/3))

    # 左から各列の一番下のボール場所の右下座標
    a4 = (int(w/10+3*w/40), int(9*h/10))
    b4 = (int(30*w/100+3*w/40), int(9*h/10))
    c4 = (int(w/2+3*w/40), int(9*h/10))
    d4 = (int(70*w/100+3*w/40), int(9*h/10))
    e4 = (int(9*w/10+3*w/40), int(9*h/10))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # frame2 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mask = np.zeros(frame.shape, dtype = np.uint8)
        # cv2.rectangle(mask, a, d, (255, 255, 255), -1)
        
        white = (255, 255, 255)
        # blue = (255, 0, 0)
        # green = (0, 255, 0)
        # red = (0, 0, 255)
        # purple = (255, 0, 255)
        
        cv2.rectangle(mask, a1, a4, white, -1)
        cv2.rectangle(mask, b1, b4, white, -1)
        cv2.rectangle(mask, c1, c4, white, -1)
        cv2.rectangle(mask, d1, d4, white, -1)
        cv2.rectangle(mask, e1, e4, white, -1)
        
        maskresult = cv2.bitwise_and(frame, mask)
        

        sairo = np.zeros((3, 5))

        # フレームで物体検出
        results = model(maskresult)

        judge = 0
        
        for result in results:
        # resultsから検出された物体情報を１つずつ取り出す
            boxes = result.boxes
            # 検出された物体に含まれる各ボックス情報を取得            
            for box in boxes:
            # 各ボックスに対する操作
                box = box.numpy()
                # ボックス情報をNumPy配列に変換
                item_number = int(box.cls.item())
                # 物体のクラスIDを取得
                # print(item_number, end=" ")
                # print("\n")

                conf = box.conf.item()
                # 物体の信頼度を取得
                # print("信頼度は ", conf, "!!!!!")

                xywh = box.xywh
                # ボックスの座標情報を取得
                # print("このボールの正規化されたxy座標と横幅と縦幅は", xywhn, "だよ")
                
                # xn_value = float(xywhn[0][0])
                # yn_value = float(xywhn[0][1])
                # x_value = int(xn_value * int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  )
                # y_value = int(yn_value * int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  )

                x_value = int(xywh[0][0])
                y_value = int(xywh[0][1])

                # print("x座標は ", x_value, " y座標は ", y_value)

                cv2.circle(maskresult, (x_value, y_value), 2, (255 ,255, 255), 3)

                # print(model.names[item_number])
                # modelオブジェクトのnames属性からitem_numberに対応する物体のクラス名を出力
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

                
            array_detection(x_value, y_value, judge, conf, a1, b1, c1, d1, e1, a4, b4, c4, d4, e4) 
        # print(sairo)

        # アノテートされたフレームを表示
        annotated_frame = results[0].plot()
        
        cv2.line(annotated_frame, (int(a1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (int(a1[0]+a4[0]-a1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(a1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (int(a1[0]+a4[0]-a1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(b1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (int(b1[0]+b4[0]-b1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(b1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (int(b1[0]+b4[0]-b1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(c1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (int(c1[0]+c4[0]-c1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(c1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (int(c1[0]+c4[0]-c1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(d1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (int(d1[0]+d4[0]-d1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(d1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (int(d1[0]+d4[0]-d1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(e1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (int(e1[0]+e4[0]-e1[0]), int(a1[1]+(a4[1]-a1[1])/3)), (0, 255, 0), 1)
        cv2.line(annotated_frame, (int(e1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (int(e1[0]+e4[0]-e1[0]), int(a1[1]+(a4[1]-a1[1])*2/3)), (0, 255, 0), 1)
  
        cv2.imshow("mask", mask)
        cv2.imshow("YOLOv8!!!", annotated_frame)
        

        # 'q'が押されたらループを終了
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # YOLOモデルを読み込む
    model = YOLO('r2_ball_recog-s/yolov8_weights_folderv2/2/best.pt')
    # Webカメラのフレームで物体検出を実行
    object_detection(model)
    
