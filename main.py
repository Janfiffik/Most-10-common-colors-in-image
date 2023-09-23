from tkinter import filedialog, Image
import numpy
from PIL import Image
from flask import Flask, render_template
from numpy import asarray


# --------------FUNCTIONS--------------------
def rgb_to_hex(rgb):
    return "#{0:02x}{1:02x}{2:02x}".format(rgb[0], rgb[1], rgb[2])


app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def home():
    return render_template("index.html")


@app.route('/open_file', methods=["POST", "GET"])
def open_file():
    image = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *jpeg")])
    img = Image.open(image)
    img.save("Static/images/img.png")
    open_image = "Static/images/img.png"
    saved_image = Image.open(open_image)
    saved_image = saved_image.resize((400, 400))  # resize for optimization

    # noinspection PyTypeChecker
    nump_array = asarray(saved_image)
    data = nump_array.reshape((-1, 3))
    colors, counts = numpy.unique(data, axis=0, return_counts=True)
    sorted_indices = numpy.argsort(-counts)
    most_common_colors = colors[sorted_indices[:10]]
    hex_colors = [rgb_to_hex(rgb) for rgb in most_common_colors]

    return render_template("index.html", image=open_image, hex_list=hex_colors)

if __name__ == "__main__":
    app.run(debug=True)
