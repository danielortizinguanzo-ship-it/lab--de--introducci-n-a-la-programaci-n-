from flask import Flask, render_template, jsonify

app = Flask(__name__)

# Simulación de base de datos
products = [
    {"id": "123", "name": "Audífonos", "price": 200, "img": "https://via.placeholder.com/150"},
    {"id": "456", "name": "Cafetera", "price": 800, "img": "https://via.placeholder.com/150"}
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/products")
def get_products():
    return jsonify(products)

@app.route("/product/<code>")
def get_product(code):
    for p in products:
        if p["id"] == code:
            return jsonify(p)
    return jsonify({"error": "Producto no encontrado"}), 404

if __name__ == "__main__":
    app.run(debug=True)
