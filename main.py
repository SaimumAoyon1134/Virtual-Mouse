#
# import cv2
# import mediapipe as mp
# import pyautogui
#
# cap = cv2.VideoCapture(0)
#
# mp_hands = mp.solutions.hands
# hand_detector = mp_hands.Hands()
# drawing_utils = mp.solutions.drawing_utils
# screen_width, screen_height = pyautogui.size()
# index_y=0
#
# while True:
#     success, frame = cap.read()
#     if not success:
#         continue
#
#     frame = cv2.flip(frame, 1)
#     rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
#
#     output = hand_detector.process(rgb_frame)
#     hands = output.multi_hand_landmarks
#
#     if hands:
#         for hand in hands:
#             drawing_utils.draw_landmarks(
#                 frame,
#                 hand,
#                 mp_hands.HAND_CONNECTIONS
#             )
#
#             for id, landmark in enumerate(hand.landmark):
#                 h, w, c = frame.shape
#                 x = int(landmark.x * w)
#                 y = int(landmark.y * h)
#                 if id ==8 :
#                     cv2.circle(frame, (x, y), 10, (0, 0, 255))
#                     index_x = screen_width / w * x
#                     index_y = screen_height / h * y
#                     pyautogui.moveTo(index_x, index_y)
#                 if id ==4:
#                     cv2.circle(frame, (x, y), 10, (0, 0, 255))
#                     thumb_x = screen_width / w * x
#                     thumb_y = screen_height / h * y
#                     print(abs(thumb_y - index_y))
#                     if  abs(thumb_y - index_y) < 20:
#                         pyautogui.click()
#                         pyautogui.sleep(1)
#
#
#
#     cv2.imshow('Virtual Mouse', frame)
#
#     if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
#         break
#
# cap.release()
# cv2.destroyAllWindows()
import cv2
import mediapipe as mp
import pyautogui
import math


cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
draw = mp.solutions.drawing_utils

screen_w, screen_h = pyautogui.size()

pyautogui.FAILSAFE = False


def distance(x1, y1, x2, y2):

    return math.hypot(x2 - x1, y2 - y1)


while True:
    success, frame = cap.read()
    if not success:
        continue

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    h, w, c = frame.shape

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:

            draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)


            index = hand_landmarks.landmark[8]
            thumb = hand_landmarks.landmark[4]

            ix, iy = int(index.x * w), int(index.y * h)
            tx, ty = int(thumb.x * w), int(thumb.y * h)

            # Cursor position on screen
            screen_x = screen_w / w * ix
            screen_y = screen_h / h * iy

            # Move cursor
            pyautogui.moveTo(screen_x, screen_y, duration=0.01)

            # Draw pointers
            cv2.circle(frame, (ix, iy), 10, (0, 0, 255), -1)
            cv2.circle(frame, (tx, ty), 10, (255, 0, 0), -1)

            # Distance between thumb & index
            finger_dist = distance(ix, iy, tx, ty)

            # If they come close → click
            if finger_dist < 35:
                cv2.putText(frame, "CLICK!", (30, 80), cv2.FONT_HERSHEY_SIMPLEX,
                            1, (0, 0,255), 3)
                pyautogui.click()
                pyautogui.sleep(0.3)

    # Instructions
    cv2.putText(frame, "Move Index Finger = Move Mouse", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.putText(frame, "Pinch (Thumb + Index) = Click", (10, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Virtual Mouse", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()