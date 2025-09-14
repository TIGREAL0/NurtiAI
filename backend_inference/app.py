
from flask import Flask, request, jsonify
import base64, io, random, math
from PIL import Image
app = Flask(__name__)

def heuristic_nutrition_from_image(pil_img):
    # Heuristic: use image size to decide number of items and approximate grams.
    w,h = pil_img.size
    area = w*h
    # larger images -> assume larger portion
    base_grams = max(80, min(400, int(area / (100*100) * 200)))
    # pick 1-3 items
    n = random.choice([1,1,2,2,3])
    items = []
    sample = [
        ('Rice', 1.3), ('Grilled Chicken', 2.0), ('Salad', 0.4), ('Paneer', 2.2),
        ('Bread', 2.5), ('Curd', 0.6), ('Dal', 1.1), ('Potato (fried)', 2.5)
    ]
    for i in range(n):
        name, kcal_per_100g = random.choice(sample)
        grams = int(base_grams * (0.6 + random.random()*0.8))
        calories = int(grams * kcal_per_100g / 100.0)
        items.append({'name': name, 'estimated_grams': grams, 'calories': calories})
    total = sum(it['calories'] for it in items)
    return items, total

@app.route('/api/infer', methods=['POST'])
def infer():
    data = request.json or {}
    img_b64 = data.get('image_base64')
    if not img_b64:
        return jsonify({'error':'no image provided'}), 400
    try:
        img_bytes = base64.b64decode(img_b64)
        pil_img = Image.open(io.BytesIO(img_bytes)).convert('RGB')
    except Exception as e:
        return jsonify({'error': 'invalid image', 'details': str(e)}), 400

    items, total = heuristic_nutrition_from_image(pil_img)
    resp = {'items': items, 'total_calories': total, 'confidence': 0.6}
    return jsonify(resp)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
