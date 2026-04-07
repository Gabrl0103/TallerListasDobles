const API = "/api/history";

let isReversed = false;

async function fetchHistory() {
    const res = await fetch(`${API}?reversed=${isReversed}`);
    const data = await res.json();
    renderHistory(data.entries, data.total);
    updateStats(data.total, data.entries);
}

function renderHistory(entries, total) {
    const container = document.getElementById("history-list");
    document.getElementById("total-badge").textContent = `${total} entradas`;

    if (entries.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">[ ]</div>
                <p>No hay entradas en el historial.</p>
            </div>`;
        return;
    }

    container.innerHTML = entries.map((entry, index) => {
        const realIndex = isReversed ? total - 1 - index : index;
        return `
        <div class="history-item" id="item-${realIndex}">
            <div class="item-index">
                <span class="index-number">${realIndex}</span>
                <span>idx</span>
            </div>
            <div class="item-content">
                <div class="item-title">${escapeHtml(entry.title)}</div>
                <div class="item-url">${escapeHtml(entry.url)}</div>
                <div class="item-time">${entry.visited_at}</div>
            </div>
            <div class="item-actions">
                <button class="btn btn-danger btn-sm" onclick="removeEntry(${realIndex})">Remove</button>
            </div>
        </div>`;
    }).join("");
}

function renderStructureView(entries) {
    const container = document.getElementById("structure-view");
    if (entries.length === 0) {
        container.innerHTML = `<span style="color:var(--text-dim)">NULL &lt;--&gt; NULL (lista vacía)</span>`;
        return;
    }

    const nodes = entries.map((entry, i) => {
        let cls = "";
        if (i === 0) cls = "head-node";
        if (i === entries.length - 1) cls = "tail-node";
        const label = entry.title.length > 14 ? entry.title.substring(0, 14) + "..." : entry.title;
        return `<span class="node-box ${cls}">${label}</span>`;
    });

    const connected = ["NULL"].concat(
        nodes.flatMap((n, i) => {
            if (i < nodes.length - 1) return [n, `<span class="arrow">&lt;--&gt;</span>`];
            return [n];
        })
    ).concat(["NULL"]);

    container.innerHTML = `<div class="node-block">${connected.join(" ")}</div>`;
}

function updateStats(total, entries) {
    document.getElementById("stat-total").textContent = total;
    document.getElementById("stat-head").textContent = entries.length > 0 ? "0" : "-";
    document.getElementById("stat-tail").textContent = entries.length > 0 ? `${total - 1}` : "-";
}

async function addEntry() {
    const url = document.getElementById("input-url").value.trim();
    const title = document.getElementById("input-title").value.trim();
    const position = document.getElementById("input-position").value;
    const index = document.getElementById("input-index").value;

    if (!url || !title) {
        showToast("URL y título son requeridos.", "error");
        return;
    }

    const body = { url, title, position };
    if (position === "index") {
        body.index = parseInt(index) || 0;
    }

    const res = await fetch(API, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(body),
    });

    const data = await res.json();

    if (!res.ok) {
        showToast(data.error, "error");
        return;
    }

    document.getElementById("input-url").value = "";
    document.getElementById("input-title").value = "";
    showToast(`Entrada agregada. Total: ${data.total}`, "success");
    fetchHistory();
}

async function removeEntry(index) {
    const res = await fetch(`${API}/${index}`, { method: "DELETE" });
    const data = await res.json();

    if (!res.ok) {
        showToast(data.error, "error");
        return;
    }

    showToast(`Eliminada: "${data.entry.title}"`, "success");
    fetchHistory();
}

async function searchEntries() {
    const keyword = document.getElementById("search-input").value.trim();
    if (!keyword) {
        fetchHistory();
        return;
    }

    const res = await fetch(`/api/history/search?q=${encodeURIComponent(keyword)}`);
    const data = await res.json();

    if (!res.ok) {
        showToast(data.error, "error");
        return;
    }

    const container = document.getElementById("history-list");
    document.getElementById("total-badge").textContent = `${data.count} results`;

    if (data.results.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">[ ? ]</div>
                <p>No se encontraron resultados para "${escapeHtml(keyword)}".</p>
            </div>`;
        return;
    }

    container.innerHTML = data.results.map(entry => `
        <div class="history-item">
            <div class="item-index">
                <span class="index-number">${entry.index}</span>
                <span>idx</span>
            </div>
            <div class="item-content">
                <div class="item-title">${escapeHtml(entry.title)}</div>
                <div class="item-url">${escapeHtml(entry.url)}</div>
                <div class="item-time">${entry.visited_at}</div>
            </div>
            <div class="item-actions">
                <button class="btn btn-danger btn-sm" onclick="removeEntry(${entry.index})">Eliminar</button>
            </div>
        </div>`).join("");
}

function toggleReverse() {
    isReversed = !isReversed;
    const btn = document.getElementById("btn-reverse");
    btn.textContent = isReversed ? "Orden Regular" : "Orden Inverso";
    fetchHistory();
}

function onPositionChange() {
    const position = document.getElementById("input-position").value;
    const wrapper = document.getElementById("index-input-wrapper");
    if (position === "index") {
        wrapper.classList.add("visible");
    } else {
        wrapper.classList.remove("visible");
    }
}

function showToast(message, type = "info") {
    const container = document.getElementById("toast-container");
    const toast = document.createElement("div");
    toast.className = `toast ${type}`;
    toast.textContent = message;
    container.appendChild(toast);
    setTimeout(() => {
        toast.style.opacity = "0";
        toast.style.transition = "opacity 0.3s";
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement("div");
    div.appendChild(document.createTextNode(text));
    return div.innerHTML;
}

document.getElementById("search-input").addEventListener("keydown", (e) => {
    if (e.key === "Enter") searchEntries();
});

fetchHistory();
