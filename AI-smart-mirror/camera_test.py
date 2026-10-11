
import cv2
import time

backends = [
    ("Default", cv2.CAP_ANY),
    ("DirectShow", cv2.CAP_DSHOW),
    ("Media Foundation", cv2.CAP_MSMF),
]

for name, backend in backends:
    print(f"\n--- {name} ---")

    cap = cv2.VideoCapture(0, backend)
    print("Opened:", cap.isOpened())

    if cap.isOpened():
        time.sleep(2)

        for attempt in range(5):
            ret, frame = cap.read()

            if ret and frame is not None:
                print("SUCCESS:", frame.shape)
                cv2.imshow(name, frame)
                cv2.waitKey(1000)
                break

            print(f"Frame {attempt + 1} failed")
            time.sleep(0.5)

    cap.release()

cv2.destroyAllWindows()
print("\nCamera test finished.")
