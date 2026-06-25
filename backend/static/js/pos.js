// Lógica del punto de venta (POS) - carrito de compras
const Carrito = (function () {
  let items = [];

  function agregar(producto) {
    const existente = items.find((i) => i.producto_id === producto.id);
    if (existente) {
      if (existente.cantidad + 1 > producto.stock) {
        mostrarAlerta(`No hay suficiente stock de "${producto.nombre}".`);
        return;
      }
      existente.cantidad = Math.round((existente.cantidad + 1) * 10) / 10;
    } else {
      if (producto.stock <= 0) {
        mostrarAlerta(`"${producto.nombre}" está agotado.`);
        return;
      }
      items.push({
        producto_id: producto.id,
        nombre: producto.nombre,
        precio: producto.precio,
        cantidad: 1,
        stock_max: producto.stock,
      });
    }
    render();
  }

  function cambiarCantidad(producto_id, delta) {
    const item = items.find((i) => i.producto_id === producto_id);
    if (!item) return;
    const nueva = Math.round((item.cantidad + delta) * 10) / 10;
    if (nueva <= 0) {
      eliminar(producto_id);
      return;
    }
    if (nueva > item.stock_max) {
      mostrarAlerta(`Stock máximo disponible: ${item.stock_max}`);
      return;
    }
    item.cantidad = nueva;
    render();
  }

  function setCantidad(producto_id, valor) {
    const item = items.find((i) => i.producto_id === producto_id);
    if (!item) return;
    const nueva = Math.round(parseFloat(valor) * 10) / 10;
    if (isNaN(nueva) || nueva <= 0) {
      eliminar(producto_id);
      return;
    }
    if (nueva > item.stock_max) {
      mostrarAlerta(`Stock máximo disponible: ${item.stock_max}`);
      return;
    }
    item.cantidad = nueva;
    actualizarTotales();
  }

  function eliminar(producto_id) {
    items = items.filter((i) => i.producto_id !== producto_id);
    render();
  }

  function vaciar() {
    items = [];
    render();
  }

  function subtotal() {
    return items.reduce((acc, i) => acc + i.precio * i.cantidad, 0);
  }

  function mostrarAlerta(msg) {
    const el = document.getElementById("pos-alerta");
    if (!el) return;
    el.textContent = msg;
    el.classList.remove("d-none");
    setTimeout(() => el.classList.add("d-none"), 3000);
  }

  function render() {
    const tbody = document.getElementById("carrito-tbody");
    const vacio = document.getElementById("carrito-vacio");
    if (!tbody) return;

    tbody.innerHTML = "";
    if (items.length === 0) {
      vacio.classList.remove("d-none");
    } else {
      vacio.classList.add("d-none");
    }

    items.forEach((item) => {
      const tr = document.createElement("tr");
      tr.innerHTML = `
        <td>${item.nombre}</td>
        <td class="text-center" style="min-width:130px;">
          <div class="d-flex align-items-center justify-content-center gap-1">
            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="Carrito.cambiarCantidad(${item.producto_id}, -0.1)">-0.1</button>
            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="Carrito.cambiarCantidad(${item.producto_id}, -1)">-1</button>
            <input type="number" min="0.1" step="0.1" value="${item.cantidad}"
              class="form-control form-control-sm text-center px-1"
              style="width:60px;"
              onchange="Carrito.setCantidad(${item.producto_id}, this.value)"
              oninput="Carrito.setCantidad(${item.producto_id}, this.value)">
            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="Carrito.cambiarCantidad(${item.producto_id}, 1)">+1</button>
            <button type="button" class="btn btn-sm btn-outline-secondary" onclick="Carrito.cambiarCantidad(${item.producto_id}, 0.1)">+0.1</button>
          </div>
        </td>
        <td class="text-end">$${item.precio.toLocaleString("es-CO", {minimumFractionDigits: 2})}</td>
        <td class="text-end">$${(item.precio * item.cantidad).toLocaleString("es-CO", {minimumFractionDigits: 2})}</td>
        <td class="text-center">
          <button type="button" class="btn btn-sm btn-link text-danger" onclick="Carrito.eliminar(${item.producto_id})">
            <i class="fa-solid fa-trash"></i>
          </button>
        </td>`;
      tbody.appendChild(tr);
    });

    actualizarTotales();
  }

  function actualizarTotales() {
    const sub = subtotal();
    const valor = parseFloat(document.getElementById("input-descuento-valor")?.value || 0);
    const tipo = document.getElementById("tipo-descuento")?.value || "pesos";
    const descuento = tipo === "porcentaje" ? (sub * valor) / 100 : valor;
    let total = sub - descuento;
    if (total < 0) total = 0;

    document.getElementById("input-descuento").value = descuento.toFixed(2);
    document.getElementById("pos-subtotal").textContent =
      "$" + sub.toLocaleString("es-CO", { minimumFractionDigits: 2 });
    document.getElementById("pos-total").textContent =
      "$" + total.toLocaleString("es-CO", { minimumFractionDigits: 2 });

    document.getElementById("input-items-json").value = JSON.stringify(
      items.map((i) => ({ producto_id: i.producto_id, cantidad: i.cantidad, precio: i.precio }))
    );
  }

  function init() {
    document.getElementById("input-descuento-valor")?.addEventListener("input", actualizarTotales);
    document.getElementById("tipo-descuento")?.addEventListener("change", actualizarTotales);
    const form = document.getElementById("form-venta");
    if (form) {
      form.addEventListener("submit", (e) => {
        if (items.length === 0) {
          e.preventDefault();
          mostrarAlerta("Agrega al menos un producto al carrito antes de confirmar.");
        }
      });
    }
  }

  return { agregar, cambiarCantidad, setCantidad, eliminar, vaciar, init };
})();

document.addEventListener("DOMContentLoaded", Carrito.init);

function filtrarProductosPOS() {
  const texto = document.getElementById("buscar-producto-pos").value.toLowerCase();
  document.querySelectorAll(".pos-product-card").forEach((card) => {
    const nombre = card.dataset.nombre.toLowerCase();
    card.parentElement.style.display = nombre.includes(texto) ? "" : "none";
  });
}
