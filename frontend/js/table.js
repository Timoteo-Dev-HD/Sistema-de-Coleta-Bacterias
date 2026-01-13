let tableData = [];

function renderTable(data) {
  tableData = data;

  const tbody = document.getElementById("tableBody");
  tbody.innerHTML = "";

  data.forEach((row, index) => {
    const tr = document.createElement("tr");

    tr.innerHTML = `
      <td>${row.paciente}</td>
      <td>${row.data_admissao}</td>
      <td>${row.data_da_coleta}</td>
      <td>${row.data_ence ?? "Vazio/Null"}</td>
      <td>${row.tempo_colet ?? "Vazio/Null"}</td>
      <td>${row.diagnostico}</td>
      <td>${row.desfecho ?? ""}</td>
      <td class="actions">
        <button class="btn-icon edit" onclick="editRow(${row.id})">
          ${iconEdit()}
        </button>
        <button class="btn-icon delete" onclick="deleteRow(${row.id})">
          ${iconDelete()}
        </button>
      </td>
    `;

    tbody.appendChild(tr);
  });
}
