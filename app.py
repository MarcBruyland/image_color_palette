import os
import numpy as np
from PIL import Image
from flask import Flask, render_template, request


def get_colors_in_image(filepath):
    def rgb_to_hex(r, g, b):
        ans = ('{:02X}{:02X}{:02X}').format(r, g, b)
        #print(r, g, b, "#" + ans)
        return "#" + ans

    def hex_to_rgb(h):
        rgb = []
        for i in (0, 2, 4):
            decimal = int(h[i:i + 2], 16)
            rgb.append(decimal)

        return tuple(rgb)

    def get_top_10(hex_list):
        hex_frequency = {}

        for item in hex_list:
            if item in hex_frequency:
                hex_frequency[item] += 1
            else:
                hex_frequency[item] = 1

        #check if result is correct
        mx_v = 0
        mx_k = ""
        for k, v in hex_frequency.items():
            if v > mx_v:
                mx_v = v
                mx_k = k
                print(mx_k, mx_v)

        sorted_hex = dict(sorted(hex_frequency.items(), key=lambda item: item[1]))
        result1 = list(sorted_hex.keys())[-10:][::-1]
        result2 = [hex_frequency[item] for item in result1]
        return result1, result2

    image_file = Image.open(filepath)
    image_array = np.array(image_file)

    shape = image_array.shape
    print(shape)

    x = shape[0]    # number of rows
    y = shape[1]    # number of cols

    hex_list = []
    for x in range(x):
        for y in range(y):
            rgb = image_array[x, y, :]

            r = rgb[0]
            g = rgb[1]
            b = rgb[2]

            hex_list.append(rgb_to_hex(r, g, b))

    top_10_hex, top_10_freq = get_top_10(hex_list)
    top_10_rgb = [hex_to_rgb(i[-6:]) for i in top_10_hex]

    return top_10_hex, top_10_rgb, top_10_freq


app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/img/'
app.config['MAX_CONTENT_PATH'] = 10


@app.route('/')
def home():
    return render_template("index.html")


@app.route("/submit", methods=["GET", "POST"])
def submit():
    if request.method == "POST":
        f = request.files['file']
        filename = f.filename
        href = "./static/img/" + filename

    if len(filename) > 1:
        fullpath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        f.save(fullpath)
        palette_hex, palette_rgb, palette_freq = get_colors_in_image(fullpath)
        return render_template("index.html", hex_success=True, palette_hex=palette_hex, palette_rgb=palette_rgb, palette_freq=palette_freq, img_href=href)

    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
