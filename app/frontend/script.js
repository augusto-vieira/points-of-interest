/* ============================================================================
 * MÓDULO: Mapa e Marcadores
 * ============================================================================
 */

// Inicializa o mapa globalmente
let map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Array para guardar os marcadores ativos
let poiMarkers = [];

/**
 * Exibe POIs no mapa.
 * Remove marcadores antigos e centraliza no grupo de novos POIs.
 * @param {Array} pois - lista de objetos {name, x, y}
 */
function showPOIsOnMap(pois) {
    poiMarkers.forEach(marker => map.removeLayer(marker));
    poiMarkers = [];

    if (!pois || pois.length === 0) return;

    pois.forEach(poi => {
        let marker = L.marker([poi.x, poi.y]).addTo(map)
            .bindPopup(`<b>${poi.name}</b><br>(${poi.x}, ${poi.y})`);
        poiMarkers.push(marker);
    });

    let group = new L.featureGroup(poiMarkers);
    map.fitBounds(group.getBounds().pad(0.5));
}

/* ============================================================================
 * MÓDULO: API Helpers
 * Centraliza chamadas ao backend
 * ============================================================================
 */

const API_BASE = "http://localhost:8000/api";

/**
 * Executa uma requisição genérica.
 * @param {string} url - endpoint completo
 * @param {string} method - método HTTP
 * @param {Object} [body] - payload (opcional)
 */
async function apiRequest(url, method = "GET", body = null) {
    const options = { method, headers: { "Content-Type": "application/json" } };
    if (body) options.body = JSON.stringify(body);

    try {
        const response = await fetch(url, options);
        const data = await response.json();
        return { ok: response.ok, data };
    } catch (err) {
        return { ok: false, data: { error: "Falha de conexão com API." } };
    }
}

/* ============================================================================
 * MÓDULO: UI Helpers
 * ============================================================================
 */

/**
 * Atualiza o painel direito com HTML dinâmico.
 * @param {string} html - conteúdo do formulário
 */
function setForm(html) {
    document.getElementById("form-container").innerHTML = html;
}

/**
 * Exibe mensagens de feedback.
 * @param {string} containerId - ID do elemento onde a mensagem aparecerá
 * @param {string} type - success, danger, warning, info
 * @param {string} message - texto da mensagem
 */
function showAlert(containerId, type, message) {
    document.getElementById(containerId).innerHTML =
        `<div class="alert alert-${type}">${message}</div>`;
}

/* ============================================================================
 * MÓDULO: Form Actions
 * ============================================================================
 */

function showForm(action) {
    switch (action) {
        /* -------------------- LISTAR -------------------- */
        case "list":
            setForm(`
                <h5>Listar POIs</h5>
                <button id="load-pois-btn" class="btn btn-success w-100">Listar POIs</button>
                <ul id="poi-list" class="mt-3 list-group"></ul>
            `);

            document.getElementById("load-pois-btn").addEventListener("click", async () => {
                const listEl = document.getElementById("poi-list");
                listEl.innerHTML = "<li class='list-group-item'>Carregando...</li>";

                const { ok, data } = await apiRequest(`${API_BASE}/list`);
                listEl.innerHTML = "";

                if (ok && data.results?.length > 0) {
                    showPOIsOnMap(data.results);
                    data.results.forEach(poi => {
                        listEl.innerHTML += `<li class="list-group-item">${poi.name} (${poi.x}, ${poi.y})</li>`;
                    });
                } else {
                    listEl.innerHTML = "<li class='list-group-item'>Nenhum POI encontrado.</li>";
                }
            });
            break;

        /* -------------------- ADICIONAR -------------------- */
        case "add":
            setForm(`
                <h5>Adicionar POI</h5>
                <form id="add-poi-form">
                    <div class="mb-3">
                        <label class="form-label">Nome</label>
                        <input type="text" class="form-control" id="add-poi-name">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Coordenadas (X, Y)</label>
                        <input type="text" class="form-control" id="add-poi-coords" placeholder="Ex: 23, 40">
                    </div>
                    <button type="submit" class="btn btn-primary w-100">Adicionar</button>
                </form>
                <div id="add-poi-result" class="mt-3"></div>
            `);

            document.getElementById("add-poi-form").addEventListener("submit", async (e) => {
                e.preventDefault();
                const name = document.getElementById("add-poi-name").value.trim();
                const coords = document.getElementById("add-poi-coords").value.trim();
                const resultEl = "add-poi-result";

                if (!name || !coords) return showAlert(resultEl, "warning", "Preencha todos os campos.");

                const [x, y] = coords.split(",").map(c => parseFloat(c.trim()));
                if (isNaN(x) || isNaN(y)) return showAlert(resultEl, "warning", "Coordenadas inválidas.");

                showAlert(resultEl, "info", "Adicionando...");
                const { ok, data } = await apiRequest(`${API_BASE}/pois/`, "POST", { name, x, y });
                ok ? showAlert(resultEl, "success", "POI adicionado com sucesso!") 
                   : showAlert(resultEl, "danger", data.error || "Erro ao adicionar POI.");
            });
            break;

        /* -------------------- EXCLUIR -------------------- */
        case "delete":
            setForm(`
                <h5>Excluir POI</h5>
                <form id="delete-poi-form">
                    <div class="mb-3">
                        <label class="form-label">ID do POI</label>
                        <input type="number" class="form-control" id="delete-poi-id">
                    </div>
                    <button type="submit" class="btn btn-danger w-100">Excluir</button>
                </form>
                <div id="delete-poi-result" class="mt-3"></div>
            `);

            document.getElementById("delete-poi-form").addEventListener("submit", async (e) => {
                e.preventDefault();
                const id = document.getElementById("delete-poi-id").value.trim();
                const resultEl = "delete-poi-result";

                if (!id) return showAlert(resultEl, "warning", "Informe o ID do POI.");

                showAlert(resultEl, "info", "Deletando...");
                const { ok, data } = await apiRequest(`${API_BASE}/pois/${id}`, "DELETE");
                ok ? showAlert(resultEl, "success", "POI excluído com sucesso!") 
                   : showAlert(resultEl, "danger", data.error || "Erro ao excluir POI.");
            });
            break;

        /* -------------------- ATUALIZAR -------------------- */
        case "update":
            setForm(`
                <h5>Atualizar POI</h5>
                <form id="update-poi-form">
                    <div class="mb-3">
                        <label class="form-label">ID do POI</label>
                        <input type="number" class="form-control" id="update-poi-id">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Novo Nome</label>
                        <input type="text" class="form-control" id="update-poi-name">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Novas Coordenadas (X, Y)</label>
                        <input type="text" class="form-control" id="update-poi-coords" placeholder="Ex: 20, 46">
                    </div>
                    <button type="submit" class="btn btn-warning w-100">Atualizar</button>
                </form>
                <div id="update-poi-result" class="mt-3"></div>
            `);

            document.getElementById("update-poi-form").addEventListener("submit", async (e) => {
                e.preventDefault();
                const id = document.getElementById("update-poi-id").value.trim();
                const name = document.getElementById("update-poi-name").value.trim();
                const coords = document.getElementById("update-poi-coords").value.trim();
                const resultEl = "update-poi-result";

                if (!id || !name || !coords) return showAlert(resultEl, "warning", "Preencha todos os campos.");

                const [x, y] = coords.split(",").map(c => parseFloat(c.trim()));
                if (isNaN(x) || isNaN(y)) return showAlert(resultEl, "warning", "Coordenadas inválidas.");

                showAlert(resultEl, "info", "Atualizando...");
                const { ok, data } = await apiRequest(`${API_BASE}/pois/${id}`, "PUT", { name, x, y });
                ok ? showAlert(resultEl, "success", "POI atualizado com sucesso!") 
                   : showAlert(resultEl, "danger", data.error || "Erro ao atualizar POI.");
            });
            break;

        /* -------------------- BUSCAR POR NOME -------------------- */
        case "find":
            setForm(`
                <h5>Buscar POI</h5>
                <form id="find-poi-form">
                    <div class="mb-3">
                        <label class="form-label">Nome</label>
                        <input type="text" class="form-control" id="find-poi-name">
                    </div>
                    <button type="submit" class="btn btn-info w-100">Buscar</button>
                </form>
                <ul id="find-poi-result" class="mt-3 list-group"></ul>
            `);

            document.getElementById("find-poi-form").addEventListener("submit", async (e) => {
                e.preventDefault();
                const name = document.getElementById("find-poi-name").value.trim();
                const resultEl = document.getElementById("find-poi-result");
                resultEl.innerHTML = "<li class='list-group-item'>Buscando...</li>";

                const { ok, data } = await apiRequest(`${API_BASE}/pois/by-name?name=${encodeURIComponent(name)}`);
                resultEl.innerHTML = "";

                if (ok && data.results?.length > 0) {
                    data.results.forEach(poi => {
                        resultEl.innerHTML += `<li class="list-group-item">${poi.name} (${poi.x}, ${poi.y})</li>`;
                    });
                    showPOIsOnMap(data.results);
                } else {
                    resultEl.innerHTML = "<li class='list-group-item'>Nenhum POI encontrado.</li>";
                }
            });
            break;

        /* -------------------- BUSCAR PRÓXIMOS -------------------- */
        case "nearby":
            setForm(`
                <h5>Buscar POIs Próximos</h5>
                <form id="nearby-poi-form">
                    <div class="mb-3">
                        <label class="form-label">Coordenadas (X, Y)</label>
                        <input type="text" class="form-control" id="nearby-poi-coords" placeholder="Ex: 42, 42">
                    </div>
                    <div class="mb-3">
                        <label class="form-label">Distância Máxima (km)</label>
                        <input type="number" class="form-control" id="nearby-poi-dmax">
                    </div>
                    <button type="submit" class="btn btn-secondary w-100">Buscar</button>
                </form>
                <ul id="nearby-poi-result" class="mt-3 list-group"></ul>
            `);

            document.getElementById("nearby-poi-form").addEventListener("submit", async (e) => {
                e.preventDefault();
                const coords = document.getElementById("nearby-poi-coords").value.trim();
                const dmax = document.getElementById("nearby-poi-dmax").value.trim();
                const resultEl = document.getElementById("nearby-poi-result");

                if (!coords || !dmax) return resultEl.innerHTML = "<li class='list-group-item'>Preencha todos os campos.</li>";

                const [x, y] = coords.split(",").map(c => parseFloat(c.trim()));
                if (isNaN(x) || isNaN(y) || isNaN(dmax)) return resultEl.innerHTML = "<li class='list-group-item'>Valores inválidos.</li>";

                resultEl.innerHTML = "<li class='list-group-item'>Buscando...</li>";

                const { ok, data } = await apiRequest(`${API_BASE}/search`, "POST", { x, y, max_distance: parseFloat(dmax) });
                resultEl.innerHTML = "";

                if (ok && data.results?.length > 0) {
                    showPOIsOnMap(data.results);
                    data.results.forEach(poi => {
                        resultEl.innerHTML += `<li class="list-group-item">${poi.name} (${poi.x}, ${poi.y})</li>`;
                    });
                } else {
                    resultEl.innerHTML = "<li class='list-group-item'>Nenhum POI encontrado.</li>";
                }
            });
            break;

        /* -------------------- DEFAULT -------------------- */
        default:
            setForm(`
                <h5>Selecione uma ação</h5>
                <p>Use o menu ao lado para gerenciar POIs.</p>
            `);
    }
}