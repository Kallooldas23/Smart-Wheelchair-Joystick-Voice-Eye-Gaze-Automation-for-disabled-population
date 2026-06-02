import cv2
from picamera2 import Picamera2
import mediapipe as mp
import numpy as np

# ---------------------------
# Landmarks
# ---------------------------
LEFT_EYE = [362,382,381,380,374,373,390,249,263,466,388,387,386,385,384,398]
RIGHT_EYE = [33,7,163,144,145,153,155,133,173,157,158,159,160,161,246]
LEFT_IRIS = [474,475,476,477]
RIGHT_IRIS = [469,470,471,472]

# Specific eyelid points
LEFT_TOP = 386
LEFT_BOTTOM = 374
RIGHT_TOP = 159
RIGHT_BOTTOM = 145

# ---------------------------
# Mediapipe
# ---------------------------
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True)

# ---------------------------
# Camera
# ---------------------------
picam2 = Picamera2()
picam2.preview_configuration.main.size = (640, 480)
picam2.preview_configuration.main.format = "RGB888"
picam2.preview_configuration.align()
picam2.configure("preview")
picam2.start()

closed_frames = 0

while True:
    frame = picam2.capture_array()
    frame = cv2.flip(frame, -1)
    frame = cv2.resize(frame, (1020, 500))

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    command = "NO FACE"

    if results.multi_face_landmarks:
        meshpoints = np.array([
            np.multiply([p.x, p.y], [w, h]).astype(int)
            for p in results.multi_face_landmarks[0].landmark
        ])

        # ---------------------------
        # LEFT / RIGHT (your working logic)
        # ---------------------------
        left_eye = meshpoints[LEFT_EYE]
        lx_min, lx_max = np.min(left_eye[:,0]), np.max(left_eye[:,0])

        (lix, liy), _ = cv2.minEnclosingCircle(meshpoints[LEFT_IRIS])
        lix = int(lix)

        l_ratio = (lix - lx_min) / (lx_max - lx_min)

        right_eye = meshpoints[RIGHT_EYE]
        rx_min, rx_max = np.min(right_eye[:,0]), np.max(right_eye[:,0])

        (rix, riy), _ = cv2.minEnclosingCircle(meshpoints[RIGHT_IRIS])
        rix = int(rix)

        r_ratio = (rix - rx_min) / (rx_max - rx_min)

        x_ratio = (l_ratio + r_ratio) / 2

        # ---------------------------
        # EYE CLOSE (ONLY TOP/BOTTOM POINTS)
        # ---------------------------
        left_top_y = meshpoints[LEFT_TOP][1]
        left_bottom_y = meshpoints[LEFT_BOTTOM][1]

        right_top_y = meshpoints[RIGHT_TOP][1]
        right_bottom_y = meshpoints[RIGHT_BOTTOM][1]

        left_eye_height = abs(left_top_y - left_bottom_y)
        right_eye_height = abs(right_top_y - right_bottom_y)

        eye_height = (left_eye_height + right_eye_height) / 2

        # Debug
        cv2.putText(frame, f"EyeH: {eye_height:.1f}", (30, 130),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,0), 2)

        # ---------------------------
        # CLOSE DETECTION
        # ---------------------------
        if eye_height < 5:   # 🔥 key threshold
            closed_frames += 1
        else:
            closed_frames = 0

        # ---------------------------
        # COMMAND LOGIC
        # ---------------------------
        if closed_frames > 3:
            command = "STOP"
        elif x_ratio < 0.45:
            command = "RIGHT"
        elif x_ratio > 0.55:
            command = "LEFT"
        else:
            command = "FORWARD"

        # ---------------------------
        # DRAW IRIS
        # ---------------------------
        cv2.circle(frame, (lix, int(liy)), 3, (0,0,255), -1)
        cv2.circle(frame, (rix, int(riy)), 3, (255,0,0), -1)

    cv2.putText(frame, f"Command: {command}", (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0,255,255), 3)

    cv2.imshow("Eye Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

picam2.stop()
cv2.destroyAllWindows()
