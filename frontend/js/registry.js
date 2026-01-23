async function loadRegistries() {
  try {
    const response = await api.get("/registry");
    
    allRecords = response.data;
    renderRecords(allRecords);

  } catch (err) {
    console.error(err);
    alert("Erro ao carregar registros");
  }
}

window.loadRegistries = loadRegistries;
