import argparse
import os
from collections import defaultdict
import cv2
from PIL import ImageFont, ImageDraw, Image
import numpy as np
from tqdm import tqdm
from ultralytics import YOLO

from reciclagem_utils import category_to_bin, get_advice, get_bin_color
from gerar_relatorio_pdf import gerar_relatorio_pdf  # ← Certifica-te que este ficheiro existe

# Funções auxiliares
def draw_text_utf8(img_cv2, text, position, font_path="arial.ttf", font_size=20, color=(255, 255, 255)):
    img_pil = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)
    try:
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print(f"[AVISO] Fonte '{font_path}' não encontrada. A usar fonte padrão sem acentos.")
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)

def gerar_resumo_txt(contador, caminho_saida):
    linhas = ["Foram detetados os seguintes resíduos:\n"]
    for classe, n in contador.items():
        bin_label = category_to_bin.get(classe, "Comum (Verificar)")
        advice = get_advice(classe)
        linhas.append(f"- {classe} (x{n}):")
        linhas.append(f"  → Ecoponto: {bin_label}")
        if advice:
            linhas.append(f"  → Como reciclar: {advice}")
        linhas.append("")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas))

# Argumentos
parser = argparse.ArgumentParser(description="YOLOv8 Litter Detection com Dicas de Reciclagem")
parser.add_argument("--model", type=str, default="runs/detect/train/yolov8s_100epochs/weights/best.pt")
parser.add_argument("--source", type=str, default="assets/litter.mp4")
parser.add_argument("--save", action="store_true", help="Guardar previsões com sobreposição de info")
args = parser.parse_args()

# Setup
os.makedirs("resultados", exist_ok=True)
output_video_path = os.path.join("resultados", f"output_{os.path.basename(args.source)}")
output_txt_path = os.path.splitext(output_video_path)[0] + ".txt"
output_pdf_path = os.path.splitext(output_video_path)[0] + ".pdf"
FONT_PATH = "arial.ttf"

# Modelo YOLO
model = YOLO(args.model)
is_video = args.source.lower().endswith((".mp4", ".avi", ".mov"))
results = model.predict(source=args.source, save=False, stream=True)
writer = None
contador_classes = defaultdict(int)

# Barra de progresso para vídeo
if is_video:
    cap = cv2.VideoCapture(args.source)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    cap.release()
    results = tqdm(results, total=total_frames, desc="A processar vídeo")

for result in results:
    frame = result.orig_img.copy()
    deteccoes_info = {}

    for box in result.boxes.data:
        x1, y1, x2, y2, conf, cls = box.tolist()
        class_id = int(cls)
        class_name = model.names[class_id]

        if not is_video:
            contador_classes[class_name] += 1

        bin_label = category_to_bin.get(class_name, "Comum (Verificar)")
        color = get_bin_color(bin_label)
        advice = get_advice(class_name)

        # Contagem detalhada para PDF
        if class_name not in deteccoes_info:
            deteccoes_info[class_name] = {
                "quantidade": 0,
                "ecoponto": bin_label,
                "dica": advice
            }
        deteccoes_info[class_name]["quantidade"] += 1

        cv2.rectangle(frame, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)
        text = f"{class_name} → {bin_label}"
        frame = draw_text_utf8(frame, text, (int(x1), int(y1) - 20), font_path=FONT_PATH, font_size=18, color=color)
        if advice:
            frame = draw_text_utf8(frame, f"Nota: {advice}", (int(x1), int(y2) + 5), font_path=FONT_PATH, font_size=16)

    # Gravação vídeo ou imagem
    if is_video:
        if writer is None:
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            h, w = frame.shape[:2]
            writer = cv2.VideoWriter(output_video_path, fourcc, 20, (w, h))
        writer.write(frame)
        cv2.imshow("Detecção com Dicas", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        cv2.imshow("Detecção com Dicas", frame)
        if args.save:
            cv2.imwrite(output_video_path, frame)

            # Guardar relatório TXT
            gerar_resumo_txt(contador_classes, output_txt_path)

            # Guardar relatório PDF
            gerar_relatorio_pdf(output_video_path, deteccoes_info, output_pdf_path)
            print(f"[INFO] Relatório PDF guardado em: {output_pdf_path}")

        cv2.waitKey(0)
        break

# Finalizar
if writer:
    writer.release()
cv2.destroyAllWindows()
