const container = document.getElementById("products");

/* Cargar productos desde Python */
fetch("/products")
.then(res => res.json())
.then(data => {
    data.forEach(p => {
        container.innerHTML += `
        <div class="card">
            <img src="${p.img}">
            <h4>${p.name}</h4>
            <p>$${p.price}</p>
            <button onclick="addToCart('${p.id}')">Agregar</button>
        </div>`;
    });
});

function addToCart(id){
    alert("Producto agregado: " + id);
}

/* ESCANER */
let codeReader;

function openScanner(){
    document.getElementById("scannerModal").style.display="flex";

    codeReader = new ZXing.BrowserBarcodeReader();

    codeReader.decodeFromVideoDevice(null, 'video', (result, err) => {
        if(result){
            alert("Código: " + result.text);
            searchProduct(result.text);
            closeScanner();
        }
    });
}

function closeScanner(){
    document.getElementById("scannerModal").style.display="none";
    if(codeReader) codeReader.reset();
}

/* Buscar producto en backend */
function searchProduct(code){
    fetch("/product/" + code)
    .then(res => res.json())
    .then(data => {
        if(data.error){
            alert("No encontrado");
        } else {
            alert("Producto: " + data.name);
        }
    });
}
