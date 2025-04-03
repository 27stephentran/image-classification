from flask import Flask, render_template, request
from keras.preprocessing.image import load_img, img_to_array
from keras.applications.mobilenet_v2 import MobileNetV2, decode_predictions, preprocess_input
import os

app = Flask(__name__)

# Tạo model MobileNetV2 (nhẹ hơn ResNet50)
model = MobileNetV2(weights='imagenet')

# Route cho trang chủ
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

# Route xử lý tải ảnh và dự đoán
@app.route('/', methods=['POST'])
def predict():
    imagefile = request.files['imagefile']
    image_path = "static/images/" + imagefile.filename
    
    # Tạo thư mục 'static/images/' nếu chưa tồn tại
    if not os.path.exists(os.path.dirname(image_path)):
        os.makedirs(os.path.dirname(image_path))
    
    imagefile.save(image_path)

    # Tiền xử lý ảnh
    image = load_img(image_path, target_size=(224, 224))
    image = img_to_array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)

    # Dự đoán
    yhat = model.predict(image)
    label = decode_predictions(yhat)
    label = label[0][0]

    classification = '%s (%.2f%%)' % (label[1], label[2] * 100)

    return render_template('index.html', prediction=classification)

# Thiết lập cổng cho Render
port = int(os.environ.get("PORT", 5000))  # Render sẽ đặt biến PORT, mặc định 5000

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=port, debug=True)
