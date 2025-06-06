import os
import json
import shutil
import random
from tqdm import tqdm

# === Caminhos ===
ANNOTATIONS_PATH = './data/annotations.json'
OUTPUT_DIR = './taco_yolo'
IMG_DIR = os.path.join(OUTPUT_DIR, 'images')
LBL_DIR = os.path.join(OUTPUT_DIR, 'labels')
YAML_PATH = os.path.join(OUTPUT_DIR, 'taco.yaml')

# === Divisões ===
SPLITS = {'train': 0.8, 'val': 0.1, 'test': 0.1}

# === Cria estrutura de diretórios ===
for split in SPLITS:
    os.makedirs(os.path.join(IMG_DIR, split), exist_ok=True)
    os.makedirs(os.path.join(LBL_DIR, split), exist_ok=True)

# === Carrega o JSON ===
with open(ANNOTATIONS_PATH, 'r') as f:
    data = json.load(f)

images = {img['id']: img for img in data['images']}
annotations = data['annotations']
categories = {cat['id']: cat['name'] for cat in data['categories']}
category_name_to_id = {name: idx for idx, name in enumerate(sorted(set(categories.values())))}

# === Organiza anotações por imagem ===
img_to_anns = {}
for ann in annotations:
    img_id = ann['image_id']
    if img_id not in img_to_anns:
        img_to_anns[img_id] = []
    img_to_anns[img_id].append(ann)

# === Divide em train/val/test ===
img_ids = list(images.keys())
random.shuffle(img_ids)
n = len(img_ids)
split_idxs = {
    'train': img_ids[:int(n * SPLITS['train'])],
    'val': img_ids[int(n * SPLITS['train']):int(n * (SPLITS['train'] + SPLITS['val']))],
    'test': img_ids[int(n * (SPLITS['train'] + SPLITS['val'])):]
}

# === Função para converter bbox para YOLO ===
def convert_bbox(bbox, img_w, img_h):
    x, y, w, h = bbox
    x_center = (x + w / 2) / img_w
    y_center = (y + h / 2) / img_h
    w /= img_w
    h /= img_h
    return [x_center, y_center, w, h]

# === Processa cada imagem ===
for split, img_ids_split in split_idxs.items():
    for img_id in tqdm(img_ids_split, desc=f'Processando {split}'):
        img_info = images[img_id]
        anns = img_to_anns.get(img_id, [])

        # Caminhos de destino
        src_img_path = os.path.join('./data', img_info['file_name'])  # onde está a imagem original
        dst_img_path = os.path.join(IMG_DIR, split, os.path.basename(img_info['file_name']))
        lbl_path = os.path.join(LBL_DIR, split, os.path.splitext(os.path.basename(img_info['file_name']))[0] + '.txt')

        # Copia imagem
        if not os.path.isfile(dst_img_path):
            shutil.copyfile(src_img_path, dst_img_path)

        # Escreve anotação
        with open(lbl_path, 'w') as f:
            for ann in anns:
                cat_name = categories[ann['category_id']]
                class_id = category_name_to_id[cat_name]
                yolo_bbox = convert_bbox(ann['bbox'], img_info['width'], img_info['height'])
                f.write(f"{class_id} {' '.join(f'{x:.6f}' for x in yolo_bbox)}\n")

# === Cria taco.yaml ===
with open(YAML_PATH, 'w') as f:
    f.write(f"path: {OUTPUT_DIR}\n")
    f.write(f"train: images/train\n")
    f.write(f"val: images/val\n")
    f.write(f"test: images/test\n\n")
    f.write(f"names: {json.dumps([name for name, _ in sorted(category_name_to_id.items(), key=lambda x: x[1])])}\n")

print(f"\nConversão concluída com sucesso! Dados prontos em: {OUTPUT_DIR}")
