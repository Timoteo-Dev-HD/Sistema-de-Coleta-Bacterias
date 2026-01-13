async function deleteRow(id) {
  if (!confirm("Deseja excluir este registro?")) return;

  try {
    await api.delete(`/registry/${id}`);
    await loadRegistries(); // 🔄 recarrega tabela
  } catch (err) {
    console.error(err);
    alert("Erro ao deletar registro");
  }
}

async function editRow(id) {
  const row = tableData.find(r => r.id === id);

  if (!row) return;

  const diagnostico = prompt("Diagnóstico:", row.diagnostico);
  const desfecho = prompt("Desfecho:", row.desfecho);

  if (!diagnostico) return;

  try {
    await api.put(`/registry/${id}`, {
      diagnostico,
      desfecho
    });

    await loadRegistries(); // 🔄 atualiza tabela
  } catch (err) {
    console.error(err);
    alert("Erro ao editar registro");
  }
}
