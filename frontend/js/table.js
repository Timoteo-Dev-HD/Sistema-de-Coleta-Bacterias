function renderTable(data) {
  const tbody = document.querySelector("#dataTable tbody");
  const emptyState = document.getElementById("emptyState");

  tbody.innerHTML = "";

  if (!data.length) {
    emptyState.style.display = "block";
    return;
  }

  emptyState.style.display = "none";

  data.forEach(item => {
    const row = document.createElement("tr");

    row.innerHTML = `
      <td>${item.tipo}</td>
      <td>${item.descricao}</td>
      <td>${item.valor}</td>
      <td>${item.data}</td>
      <td>
        <div class="actions">
          <button class="btn btn-icon" title="Editar" onclick="editRow(${item.id})">
            ${iconEdit()}
          </button>
          <button class="btn btn-icon btn-danger" title="Deletar" onclick="deleteRow(${item.id})">
            ${iconDelete()}
          </button>
        </div>
      </td>
    `;

    tbody.appendChild(row);
  });
}
