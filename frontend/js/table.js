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


function filterRecords() {
  const nameQuery = document.getElementById("searchInput").value
    .trim()
    .toLowerCase();

  const monthValue = document.getElementById("monthFilter").value;

  const filtered = allRecords.filter(r => {
    // 🔎 FILTRO POR NOME
    const matchName = r.nome_paciente
      ?.toLowerCase()
      .includes(nameQuery);

    // 📅 FILTRO POR MÊS
    let matchMonth = true;

    if (monthValue !== "") {
      const date = r.data_da_coleta || r.data_admissao;
      if (!date) return false;

      const recordMonth = new Date(date).getMonth();
      matchMonth = recordMonth === Number(monthValue);
    }

    return matchName && matchMonth;
  });

  renderRecords(filtered);
}

document.addEventListener("DOMContentLoaded", () => {
  const searchInput = document.getElementById("searchInput");
  const monthFilter = document.getElementById("monthFilter");

  searchInput.addEventListener("input", filterRecords);
  monthFilter.addEventListener("change", filterRecords);
});

