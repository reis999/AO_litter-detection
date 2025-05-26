import argparse
import cv2
import time
import numpy as np
from ultralytics import YOLO
from reciclagem_utils import category_to_bin, bin_colors, recycling_info, get_bin_color, get_advice
from PIL import ImageFont, ImageDraw, Image

# Argumentos
parser = argparse.ArgumentParser(description="YOLOv8 inference com webcam e sugestão de reciclagem")
parser.add_argument(
    "--model",
    type=str,
    default="runs/detect/train/yolov8s_100epochs/weights/best.pt",
    help="path para o modelo YOLO treinado"
)
parser.add_argument(
    "--threshold",
    type=float,
    default=0.5,
    help="Limiar de confiança para detecções"
)
args = parser.parse_args()

# Carregar o modelo
model = YOLO(args.model)

# Abrir webcam
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Erro ao aceder à webcam")
    exit()

# Configurações de exibição
window_name = "YOLOv8 - Detecção de Lixo e Reciclagem"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
cv2.resizeWindow(window_name, 1280, 720)

# Variáveis para FPS
prev_time = time.time()
fps = 0
fps_update_interval = 0.5
fps_timer = time.time()

show_info_panel = True
selected_item = None
last_detection_time = {}

while True:
    ret, frame = cap.read()
    if not ret:
        break

    current_time = time.time()
    if current_time - fps_timer >= fps_update_interval:
        fps = 1.0 / (current_time - prev_time)
        fps_timer = current_time
    prev_time = current_time

    overlay = frame.copy()

    results = model.predict(source=frame, conf=args.threshold, verbose=False)
    current_detections = []

    for r in results:
        if r.boxes is not None:
            for box in r.boxes:
                cls_id = int(box.cls[0])
                class_name = model.names[cls_id]
                conf = float(box.conf[0])

                last_detection_time[class_name] = time.time()
                current_detections.append(class_name)

                x1, y1, x2, y2 = map(int, box.xyxy[0])

                bin_type = category_to_bin.get(class_name, "Desconhecido")
                label = f"{class_name}: {conf:.2f}"
                box_color = get_bin_color(bin_type)

                cv2.rectangle(overlay, (x1, y1), (x2, y2), box_color, 2)
                cv2.rectangle(overlay, (x1, y1-30), (x1 + len(label)*11, y1), box_color, -1)
                cv2.putText(overlay, label, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                cv2.putText(overlay, bin_type, (x1, y2+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, box_color, 2)

                if selected_item is None:
                    selected_item = class_name

    current_time = time.time()
    to_remove = []
    for item, last_time in last_detection_time.items():
        if current_time - last_time > 3 and item not in current_detections:
            to_remove.append(item)

    for item in to_remove:
        del last_detection_time[item]

    if not current_detections:
        selected_item = None

    alpha = 0.7
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

    cv2.putText(frame, f"FPS: {fps:.1f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    if show_info_panel and selected_item is not None:
        bin_type = category_to_bin.get(selected_item, "Desconhecido")
        main_bin = bin_type.split(" - ")[0]

        info_panel = f"Item: {selected_item}"
        info_panel += f"\nOnde reciclar: {bin_type}"
        if main_bin in recycling_info:
            info_panel += f"\nInfo: {recycling_info[main_bin]}"

        advice = get_advice(selected_item)
        if advice:
            info_panel += f"\nDica: {advice}"

        panel_color = get_bin_color(bin_type)

        # Pillow para suporte UTF-8
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_img = Image.fromarray(frame_rgb)
        draw = ImageDraw.Draw(pil_img)

        try:
            font = ImageFont.truetype("arial.ttf", 22)  # Usa uma fonte TrueType com suporte a acentos
        except IOError:
            font = ImageFont.load_default()
            print("Fonte TTF não encontrada. Fonte padrão será usada.")

        draw.rectangle(
            [(10, frame.shape[0] - 120), (frame.shape[1] - 10, frame.shape[0] - 10)],
            fill=(0, 0, 0)
        )

        y_offset = frame.shape[0] - 100
        for line in info_panel.split('\n'):
            draw.text((20, y_offset), line, font=font, fill=panel_color)
            y_offset += 25

        frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    cv2.imshow(window_name, frame)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        break
    elif key == ord('i'):
        show_info_panel = not show_info_panel

cap.release()
cv2.destroyAllWindows()
