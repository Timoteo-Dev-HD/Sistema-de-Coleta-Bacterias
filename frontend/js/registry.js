async function loadRegistries() {
  try {
    const response = await api.get("/registry");
    renderTable(response.data);
    

  } catch (err) {
    console.error(err);
    alert("Erro ao carregar registros");
  }
}

window.loadRegistries = loadRegistries;
