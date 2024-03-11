import cv2
from tkinter import *
import tkinter as tk

contour_threshold = 6000
camera = True
video = False


def main_function():
    if camera:
        cap = cv2.VideoCapture(0)  # Connect to the default camera
    else:
        cap = cv2.VideoCapture('assets/videos/walking-people.mp4')  # Connect to a file

    mog = cv2.createBackgroundSubtractorMOG2()  # Create the MOG2 background subtractor object

    while True:

        ret, frame = cap.read()  # Read a frame from a video stream

        if not ret:
            print('The video has ended')
            break

        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)  # Convert the frame to grayscale
        gray_frame = cv2.GaussianBlur(gray_frame, (15, 15), 0)

        fg_mask = mog.apply(gray_frame)  # Apply background subtraction

        # Apply morphological operations to reduce noise and fill gaps
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (4, 4))
        fg_mask = cv2.erode(fg_mask, kernel, iterations=3)
        fg_mask = cv2.dilate(fg_mask, kernel, iterations=5)

        contours, _ = cv2.findContours(fg_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:

            if cv2.contourArea(contour) < contour_threshold:  # Ignore small contours
                continue

            x, y, w, h = cv2.boundingRect(contour)  # Draw bounding box around contour
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)

        pressed_key = cv2.waitKey(1)

        if pressed_key == ord('q'):
            break
        elif pressed_key == ord('a'):
            take_picture(frame, fg_mask, x, y, w, h)
        elif pressed_key == ord('f'):
            cv2.imshow('Video Stream', fg_mask)
        elif pressed_key == ord('g'):
            cv2.imshow('Video Stream', gray_frame)
        else:
            cv2.imshow('Video Stream', frame)

    cap.release()
    cv2.destroyAllWindows()


def take_picture(frame, fg_mask, x, y, w, h):
    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
    cv2.imshow('Test', frame)
    cv2.imshow('Test foreground', fg_mask)


def big_threshold():
    global contour_threshold
    contour_threshold = 6000


def small_threshold():
    global contour_threshold
    contour_threshold = 600


def uploaded_video():
    global video
    global camera
    video = True
    camera = False


def web_cam():
    global camera
    global video
    camera = True
    video = False


def start():
    menu.destroy()
    main_function()


menu = tk.Tk()
menu.geometry("500x100")

Label(text="Choose the size of the objects", width=25).grid(row=0, column=0)
Label(text="Choose the type of video", width=25).grid(row=1, column=0)

button1 = Button(menu, text="Big", command=big_threshold)
button2 = Button(menu, text="Small", command=small_threshold)
button3 = Button(menu, text="Web camera", command=web_cam)
button4 = Button(menu, text="Uploaded video", command=uploaded_video)
button5 = Button(menu, text="Start", command=start)

button1.place(x=270, y=5)
button2.place(x=300, y=5)
button3.place(x=270, y=30)
button4.place(x=300, y=30)
button5.place(x=200, y=60)

menu.mainloop()
