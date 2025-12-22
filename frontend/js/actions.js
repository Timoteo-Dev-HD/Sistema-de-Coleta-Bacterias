function editRow(id) {
  alert("Editar registro " + id);
}

async function deleteRow(id) {
  if (!confirm("Deseja realmente excluir?")) return;
  await api.delete(`/records/${id}`);
  alert("Registro deletado");
}
