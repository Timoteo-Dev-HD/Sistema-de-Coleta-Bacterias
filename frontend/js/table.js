let recordsData = [];

function renderRecords(data) {
  recordsData = data;

  const container = document.getElementById("recordsContainer");
  const emptyState = document.getElementById("emptyState");

  container.innerHTML = "";

  if (!data || data.length === 0) {
    emptyState.style.display = "block";
    return;
  }

  emptyState.style.display = "none";

  data.forEach((row) => {
    const card = document.createElement("div");
    card.className = "record-card";

    card.innerHTML = `
      <div class="record-header">
        <strong>${row.nome_paciente}</strong>
        <div class="actions">
          <button class="btn-icon" onclick="viewRow(${row.id})">
            ${iconView()}
          </button>
          <button class="btn-icon edit" onclick="editRow(${row.id})">
            ${iconEdit()}
          </button>
          <button class="btn-icon delete" onclick="deleteRow(${row.id})">
            ${iconDelete()}
          </button>
        </div>

      </div>

      <div class="record-body">
        <div><span>Data Admissão:</span> ${formatDate(row.data_admissao)}</div>
        <div><span>Data da Coleta:</span> ${formatDate(row.data_da_coleta)}</div>
        <div><span>Data Encerramento:</span> ${formatDate(row.data_encerramento)}</div>
        <div><span>Tempo Coleta:</span> ${row.tempo_coletar}</div>
        <div><span>Diagnóstico:</span> ${row.diagnostico}</div>
        <div><span>Desfecho:</span> ${row.desfecho ?? "—"}</div>
        <div><span>Data de Inserção do dado:</span> ${formatDate(row.data_criacao)}</div>
        <div><span>Data da Ultima Atualização do Registro:</span> ${formatDate(row.data_atulizacao)}</div>
      </div>
    `;

    container.appendChild(card);
  });
}


function filterRecords(query) {
  const q = query.trim().toLowerCase();

  // 🔹 Se o campo estiver vazio, mostra tudo
  if (!q) {
    renderRecords(allRecords);
    return ;
  }

  const filtered = allRecords.filter(r =>
    r.nome_paciente.toLowerCase().includes(q)
  );

  renderRecords(filtered);
}

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");

  if (!searchInput) return;

  searchInput.addEventListener("input", (e) => {
    filterRecords(e.target.value);
  });
});
