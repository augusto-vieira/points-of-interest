// Inicialize o mapa globalmente
let map = L.map('map').setView([0, 0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
}).addTo(map);

// Array para guardar os marcadores
let poiMarkers = [];

// Função para mostrar POIs no mapa cartesiano
function showPOIsOnMap(pois) {
    // Remove marcadores antigos
    poiMarkers.forEach(marker => map.removeLayer(marker));
    poiMarkers = [];
    if (!pois || pois.length === 0) return;
    pois.forEach(poi => {
        // Adiciona marcador
        let marker = L.marker([poi.x, poi.y]).addTo(map)
            .bindPopup(`<b>${poi.name}</b><br>(${poi.x}, ${poi.y})`);
        poiMarkers.push(marker);
    });
    // Centraliza o mapa nos POIs
    let group = new L.featureGroup(poiMarkers);
    map.fitBounds(group.getBounds().pad(0.5));
}

// Função para trocar formulário dinamicamente
function showForm(action) {
    let container = document.getElementById("form-container");

    if (action === "add") {
        container.innerHTML = `
            <h5>Add POI</h5>
            <form id="add-poi-form">
                <div class="mb-3">
                    <label class="form-label">Name</label>
                    <input type="text" class="form-control" id="add-poi-name" placeholder="POI Name">
                </div>
                <div class="mb-3">
                    <label class="form-label">Coordinates (X, Y)</label>
                    <input type="text" class="form-control" id="add-poi-coords" placeholder="e.g. 40.7, -73.9">
                </div>
                <button type="submit" class="btn btn-primary w-100">Add</button>
            </form>
            <div id="add-poi-result" class="mt-3"></div>
        `;

        // Adiciona o event listener ao formulário de adicionar
        setTimeout(() => {
            const form = document.getElementById("add-poi-form");
            if (form) {
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const name = document.getElementById("add-poi-name").value.trim();
                    const coords = document.getElementById("add-poi-coords").value.trim();
                    const resultEl = document.getElementById("add-poi-result");

                    // Validação simples
                    if (!name || !coords) {
                        resultEl.innerHTML = "<div class='alert alert-warning'>Preencha todos os campos.</div>";
                        return;
                    }

                    const [x, y] = coords.split(',').map(s => s.trim());
                    if (isNaN(x) || isNaN(y)) {
                        resultEl.innerHTML = "<div class='alert alert-warning'>Coordenadas inválidas.</div>";
                        return;
                    }

                    resultEl.innerHTML = "<div class='alert alert-info'>Adicionando...</div>";
                    try {
                        const response = await fetch("http://localhost:8000/api/pois", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ name, x: parseFloat(x), y: parseFloat(y) })
                        });
                        const data = await response.json();
                        if (response.ok) {
                            resultEl.innerHTML = "<div class='alert alert-success'>POI adicionado com sucesso!</div>";
                        } else {
                            resultEl.innerHTML = `<div class='alert alert-danger'>Erro: ${data.error || "Não foi possível adicionar o POI."}</div>`;
                        }
                    } catch (err) {
                        resultEl.innerHTML = "<div class='alert alert-danger'>Erro ao adicionar POI.</div>";
                    }
                });
            }
        }, 10);
        
    } else if (action === "delete") {
        container.innerHTML = `
            <h5>Delete POI</h5>
            <form id="delete-poi-form">
                <div class="mb-3">
                    <label class="form-label">POI ID</label>
                    <input type="number" class="form-control" id="delete-poi-id" placeholder="ID do POI">
                </div>
                <button type="submit" class="btn btn-danger w-100">Delete</button>
            </form>
            <div id="delete-poi-result" class="mt-3"></div>
        `;

        // Adiciona o event listener ao formulário de deletar
        setTimeout(() => {
            const form = document.getElementById("delete-poi-form");
            if (form) {
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const id = document.getElementById("delete-poi-id").value.trim();
                    const resultEl = document.getElementById("delete-poi-result");

                    if (!id) {
                        resultEl.innerHTML = "<div class='alert alert-warning'>Informe o ID do POI.</div>";
                        return;
                    }

                    resultEl.innerHTML = "<div class='alert alert-info'>Deletando...</div>";
                    try {
                        const response = await fetch(`http://localhost:8000/api/pois/${id}`, {
                            method: "DELETE"
                        });
                        const data = await response.json();
                        if (response.ok) {
                            resultEl.innerHTML = "<div class='alert alert-success'>POI deletado com sucesso!</div>";
                        } else {
                            resultEl.innerHTML = `<div class='alert alert-danger'>Erro: ${data.error || "Não foi possível deletar o POI."}</div>`;
                        }
                    } catch (err) {
                        resultEl.innerHTML = "<div class='alert alert-danger'>Erro ao deletar POI.</div>";
                    }
                });
            }
        }, 10);

    } else if (action === "find") {
        container.innerHTML = `
            <h5>Find POI</h5>
            <form id="find-poi-form">
                <div class="mb-3">
                    <label class="form-label">Nome</label>
                    <input type="text" class="form-control" id="find-poi-name" placeholder="Digite o nome do POI">
                </div>
                <button type="submit" class="btn btn-info w-100">Find</button>
            </form>
            <ul id="find-poi-result" class="mt-3 list-group"></ul>
        `;
        
        // Adiciona o event listener ao formulário de busca
        setTimeout(() => {
            const form = document.getElementById("find-poi-form");
            if (form) {
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const name = document.getElementById("find-poi-name").value.trim();
                    const resultEl = document.getElementById("find-poi-result");
                    resultEl.innerHTML = "<li class='list-group-item'>Buscando...</li>";
                    try {
                        const response = await fetch(`http://localhost:8000/api/pois/by-name?name=${encodeURIComponent(name)}`);
                        const data = await response.json();
                        resultEl.innerHTML = "";
                        if (data.results && data.results.length > 0) {
                            data.results.forEach(poi => {
                                const li = document.createElement("li");
                                li.className = "list-group-item";
                                li.textContent = `${poi.name} (${poi.x}, ${poi.y})`;
                                resultEl.appendChild(li);
                            });
                        } else {
                            resultEl.innerHTML = "<li class='list-group-item'>Nenhum POI encontrado.</li>";
                        }
                    } catch (err) {
                        resultEl.innerHTML = "<li class='list-group-item text-danger'>Erro ao buscar POIs.</li>";
                    }
                });
            }
        }, 10);

    } else if (action === "list") {
        container.innerHTML = `
            <h5>Listar POIs</h5>
            <button id="load-pois-btn" class="btn btn-success w-100">Carregar POIs</button>
            <ul id="poi-list" class="mt-3 list-group"></ul>
        `;

        // Adiciona o event listener após renderizar o botão
        setTimeout(() => {
            const btn = document.getElementById("load-pois-btn");
            if (btn) {
                btn.addEventListener("click", async () => {
                    const listEl = document.getElementById("poi-list");
                    listEl.innerHTML = "<li class='list-group-item'>Carregando...</li>";
                    try {
                        const response = await fetch("http://localhost:8000/api/list");
                        const data = await response.json();
                        listEl.innerHTML = "";
                        if (data.results && data.results.length > 0) {
                            data.results.forEach(poi => {
                                const li = document.createElement("li");
                                li.className = "list-group-item";
                                li.textContent = `${poi.name} (${poi.x}, ${poi.y})`;
                                listEl.appendChild(li);
                                showPOIsOnMap(data.results);
                            });
                        } else {
                            listEl.innerHTML = "<li class='list-group-item'>Nenhum POI encontrado.</li>";
                        }
                    } catch (err) {
                        listEl.innerHTML = "<li class='list-group-item text-danger'>Erro ao carregar POIs.</li>";
                    }
                });
            }
        }, 10);
    
    } else if (action === "update") { 
            container.innerHTML = `
            <h5>Update POI</h5>
            <form id="update-poi-form">
                <div class="mb-3">
                    <label class="form-label">POI ID</label>
                    <input type="number" class="form-control" id="update-poi-id" placeholder="ID do POI">
                </div>
                <div class="mb-3">
                    <label class="form-label">Novo Nome</label>
                    <input type="text" class="form-control" id="update-poi-name" placeholder="Novo nome do POI">
                </div>
                <div class="mb-3">
                    <label class="form-label">Novas Coordenadas (X, Y)</label>
                    <input type="text" class="form-control" id="update-poi-coords" placeholder="e.g. 40.7, -73.9">
                </div>
                <button type="submit" class="btn btn-warning w-100">Update</button>
            </form>
            <div id="update-poi-result" class="mt-3"></div>
        `;

        setTimeout(() => {
            const form = document.getElementById("update-poi-form");
            if (form) {
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const id = document.getElementById("update-poi-id").value.trim();
                    const name = document.getElementById("update-poi-name").value.trim();
                    const coords = document.getElementById("update-poi-coords").value.trim();
                    const resultEl = document.getElementById("update-poi-result");

                    if (!id || !name || !coords) {
                        resultEl.innerHTML = "<div class='alert alert-warning'>Preencha todos os campos.</div>";
                        return;
                    }

                    const [x, y] = coords.split(',').map(s => s.trim());
                    if (isNaN(x) || isNaN(y)) {
                        resultEl.innerHTML = "<div class='alert alert-warning'>Coordenadas inválidas.</div>";
                        return;
                    }

                    resultEl.innerHTML = "<div class='alert alert-info'>Atualizando...</div>";
                    try {
                        const response = await fetch(`http://localhost:8000/api/pois/${id}`, {
                            method: "PUT",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ name, x: parseFloat(x), y: parseFloat(y) })
                        });
                        const data = await response.json();
                        if (response.ok) {
                            resultEl.innerHTML = "<div class='alert alert-success'>POI atualizado com sucesso!</div>";
                        } else {
                            resultEl.innerHTML = `<div class='alert alert-danger'>Erro: ${data.error || "Não foi possível atualizar o POI."}</div>`;
                        }
                    } catch (err) {
                        resultEl.innerHTML = "<div class='alert alert-danger'>Erro ao atualizar POI.</div>";
                    }
                });
            }
        }, 10);
    } 
     else if (action === "nearby") {
        container.innerHTML = `
            <h5>Buscar POIs Próximos</h5>
            <form id="nearby-poi-form">
                <div class="mb-3">
                    <label class="form-label">Coordenadas (X, Y)</label>
                    <input type="text" class="form-control" id="nearby-poi-coords" placeholder="e.g. 40.7, -73.9">
                </div>
                <div class="mb-3">
                    <label class="form-label">Distância Máxima</label>
                    <input type="number" class="form-control" id="nearby-poi-dmax" placeholder="Distância em km">
                </div>
                <button type="submit" class="btn btn-secondary w-100">Buscar</button>
            </form>
            <ul id="nearby-poi-result" class="mt-3 list-group"></ul>
        `;

        setTimeout(() => {
            const form = document.getElementById("nearby-poi-form");
            if (form) {
                form.addEventListener("submit", async (e) => {
                    e.preventDefault();
                    const coords = document.getElementById("nearby-poi-coords").value.trim();
                    const dmax = document.getElementById("nearby-poi-dmax").value.trim();
                    const resultEl = document.getElementById("nearby-poi-result");

                    if (!coords || !dmax) {
                        resultEl.innerHTML = "<li class='list-group-item'>Preencha todos os campos.</li>";
                        return;
                    }

                    const [x, y] = coords.split(',').map(s => s.trim());
                    if (isNaN(x) || isNaN(y) || isNaN(dmax)) {
                        resultEl.innerHTML = "<li class='list-group-item'>Valores inválidos.</li>";
                        return;
                    }

                    resultEl.innerHTML = "<li class='list-group-item'>Buscando...</li>";
                    try {
                        const response = await fetch("http://localhost:8000/api/search", {
                            method: "POST",
                            headers: { "Content-Type": "application/json" },
                            body: JSON.stringify({ x: parseFloat(x), y: parseFloat(y), max_distance: parseFloat(dmax) })
                        });
                        const data = await response.json();
                        resultEl.innerHTML = "";
                        if (data.results && data.results.length > 0) {
                            showPOIsOnMap(data.results);
                            data.results.forEach(poi => {
                                const li = document.createElement("li");
                                li.className = "list-group-item";
                                li.textContent = `${poi.name} (${poi.x}, ${poi.y})`;
                                resultEl.appendChild(li);
                            });
                        } else {
                            resultEl.innerHTML = "<li class='list-group-item'>Nenhum POI encontrado.</li>";
                        }
                    } catch (err) {
                        resultEl.innerHTML = "<li class='list-group-item text-danger'>Erro ao buscar POIs próximos.</li>";
                    }
                });
            }
        }, 10);
    }

    else {
        container.innerHTML = `
            <h5>Selecione uma ação</h5>
            <p>Use o menu ao lado para gerenciar POIs.</p>
        `;
    }
}