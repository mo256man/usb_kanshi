import subprocess as sp
from flask import Flask, render_template

app = Flask(__name__)

class Product:
    def __init__(self, vid, pid, pname):
        self.vender_id = vid
        self.product_id = pid
        self.product_name = pname

def get_usb_devices():
    products = []
    command = ["lsusb"]
    ret = sp.run(command, capture_output=True, text=True)
    for line in ret.stdout.splitlines():	# 標準出力の各行について
        fields = line.split()				# スペースで区切る
        vid = fields[5][:4]				# 5番目のフィールド（例 "1d6b:0003"）の、最初の4文字
        pid = fields[5][-4:]			# 5番目のフィールド（例 "1d6b:0003"）の、最後の4文字
        pname = " ".join(fields[6:])	# 6番目以降のフィールド（例 "Linux"と"Foundation"）を半角スペースで結合する

        if vid != "1d6b" and vid != "2109":	# inux Foundation と VIA は除外する
            product = Product(vid, pid, pname)
            products.append(product)

    return products


@app.route("/")
def index():
    products = get_usb_devices()
    for p in products:
        print(p.vender_id, p.product_id, p.product_name)

    return f"USB接続機器数＝{len(products)}"

if __name__ == "__main__":
    app.run(debug=True)
