from flask import Flask, render_template, request
import ipaddress

app = Flask(__name__)

def binario_color(ip, mask):
    ip_bin = ''.join([f'{int(octeto):08b}' for octeto in ip.split('.')])
    mask_bin = ''.join([f'{int(octeto):08b}' for octeto in mask.split('.')])
    bits_red = mask_bin.count('1')
    bits_host = 32 - bits_red
    return f"<span style='color:red'>{ip_bin[:bits_red]}</span><span style='color:green'>{ip_bin[bits_red:]}</span>"

@app.route("/", methods=["GET", "POST"])
def index():
    data = {}
    if request.method == "POST":
        try:
            ip = request.form["ip"]
            mask = request.form["mask"]
            red = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)

            data["ip_red"] = str(red.network_address)
            data["broadcast"] = str(red.broadcast_address)
            data["hosts"] = red.num_addresses - 2
            data["rango"] = f"{list(red.hosts())[0]} - {list(red.hosts())[-1]}"

            primer_octeto = int(ip.split('.')[0])
            if primer_octeto <= 126:
                data["clase"] = "A"
            elif primer_octeto <= 191:
                data["clase"] = "B"
            elif primer_octeto <= 223:
                data["clase"] = "C"
            elif primer_octeto <= 239:
                data["clase"] = "D"
            else:
                data["clase"] = "E"

            if (primer_octeto == 10) or (primer_octeto == 172 and 16 <= int(ip.split('.')[1]) <= 31) or (primer_octeto == 192 and int(ip.split('.')[1]) == 168):
                data["tipo"] = "Privada"
            else:
                data["tipo"] = "Pública"

            data["binario"] = binario_color(ip, mask)

        except Exception as e:
            data["error"] = f"Error: {e}"

    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)