import cv2
import mediapipe as mp
import pyautogui
import time
import sys
import csv
import os
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

def run_navigation(shared_data):
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.6,
    )
    pyautogui.FAILSAFE = False

    close_var = 0
    x_rat = 1920 / 650
    y_rat = 1200 / 480
    drag_var = 0
    calc_dist = 0
    percent_calc = 0
    PALMSIZE = 0

    speakers = AudioUtilities.GetSpeakers()
    volume = speakers.EndpointVolume

    cap = cv2.VideoCapture(0)
    smooth_factor = 0.6

    while True:
        if shared_data.get('shutdown') == True:
            break

        ret, frame = cap.read()
        if not ret:
            break
        try:
            bi = shared_data.get('mode', 0)
        except Exception:
            bi = 0
        if bi == 1:
            if not ret:
                break
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:
                    Hand = []
                    for id, lm in enumerate(hand.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        Hand.append((cx, cy))
                    PALMSIZE = int((((Hand[5][0] - Hand[0][0]) ** 2) + ((Hand[5][1] - Hand[0][1]) ** 2)) ** 0.5)
                    calc_dist = int((((Hand[8][0] - Hand[4][0]) ** 2) + ((Hand[8][1] - Hand[4][1]) ** 2)) ** 0.5)
                    percent_calc = float((calc_dist * 0.73 / PALMSIZE) * 100) - 13
                    percent_calc = max(0, min(percent_calc, 100))
                    screen_x = int(Hand[8][0] * x_rat)
                    screen_y = int(Hand[8][1] * y_rat)
                    calc_dist = int((((Hand[8][0] - Hand[4][0]) ** 2) + ((Hand[8][1] - Hand[4][1]) ** 2)) ** 0.5)
                    screen_x = int(Hand[8][0] * x_rat)
                    screen_y = int(Hand[8][1] * y_rat)

                    prev_x, prev_y = pyautogui.position()
                    screen_x = int(prev_x + (screen_x - prev_x) * smooth_factor)
                    screen_y = int(prev_y + (screen_y - prev_y) * smooth_factor)
                    if -2 < screen_x - prev_x < 2:
                        screen_x = prev_x
                    if -2 < screen_y - prev_y < 2:
                        screen_y = prev_y
                    prev_x, prev_y = screen_x, screen_y

                    pyautogui.moveTo(screen_x, screen_y, 0.0000001)

                    if percent_calc < 3:
                        pyautogui.click()
                    elif Hand[12][1] < Hand[8][1]:
                        if Hand[12][1] > Hand[11][1]:
                            pyautogui.scroll(150)
                        else:
                            pyautogui.scroll(-150)

        if bi == 3:
            frame = cv2.flip(frame, 1)
            rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = hands.process(rgb)
            if result.multi_hand_landmarks:
                for hand in result.multi_hand_landmarks:
                    Hand = []
                    for id, lm in enumerate(hand.landmark):
                        h, w, c = frame.shape
                        cx, cy = int(lm.x * w), int(lm.y * h)
                        Hand.append((cx, cy))
                    PALMSIZE = int((((Hand[5][0] - Hand[0][0]) ** 2) + ((Hand[5][1] - Hand[0][1]) ** 2)) ** 0.5)
                    calc_dist = int((((Hand[8][0] - Hand[4][0]) ** 2) + ((Hand[8][1] - Hand[4][1]) ** 2)) ** 0.5)
                    percent_calc = float((calc_dist * 0.73 / PALMSIZE) * 100) - 13
                    percent_calc = max(0, min(percent_calc, 100))
                    screen_x = int(Hand[8][0] * x_rat)
                    screen_y = int(Hand[8][1] * y_rat)

                    prev_x, prev_y = pyautogui.position()
                    screen_x = int(prev_x + (screen_x - prev_x) * smooth_factor)
                    screen_y = int(prev_y + (screen_y - prev_y) * smooth_factor)
                    if -2 < screen_x - prev_x < 2:
                        screen_x = prev_x
                    if -2 < screen_y - prev_y < 2:
                        screen_y = prev_y
                    prev_x, prev_y = screen_x, screen_y

                    pyautogui.moveTo(screen_x, screen_y)

                    if Hand[8][1] > Hand[6][1] and Hand[12][1] < Hand[10][1] and Hand[16][1] < Hand[14][1] and Hand[20][1] < Hand[18][1] and Hand[20][1] < Hand[8][1]:
                        close_var += 1
                        time.sleep(0.5)
                        if close_var >= 3:
                            shared_data['shutdown'] = True
                            break
                    elif percent_calc < 3:
                        if drag_var >= 3:
                            pyautogui.click()
                        else:
                            drag_var += 1
                            pyautogui.click()
                            time.sleep(0.3)
                    elif Hand[8][1] < Hand[6][1] and Hand[12][1] < Hand[10][1] and Hand[16][1] < Hand[14][1] and Hand[20][1] < Hand[18][1]:
                        pyautogui.hotkey('win', 'tab')
                        time.sleep(1)
                    elif Hand[20][1] < Hand[8][1]:
                        volume.SetMasterVolumeLevelScalar(percent_calc / 100, None)
                    elif Hand[12][1] < Hand[8][1]:
                        if Hand[12][1] > Hand[11][1]:
                            pyautogui.scroll(150)
                        else:
                            pyautogui.scroll(-150)

                    if percent_calc != 0:
                        pyautogui.mouseUp()
                        drag_var = 0

                    if not (Hand[8][1] > Hand[6][1] and Hand[12][1] < Hand[10][1] and Hand[16][1] < Hand[14][1] and Hand[20][1] < Hand[18][1] and Hand[20][1] < Hand[8][1]):
                        close_var = 0

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()