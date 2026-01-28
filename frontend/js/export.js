document.getElementById("exportBtn").addEventListener("click", () => {
  const monthSelect = document.getElementById("monthFilter");
  const month = monthSelect.value;

  if (month === "") {
    alert("Selecione um mês para exportar o relatório");
    return;
  }

  // Backend espera mês 1–12
  const monthApi = Number(month) + 1;
  const year = new Date().getFullYear() - 1;

  // ⚠️ AQUI É O PONTO-CHAVE
  const url = `http://127.0.0.1:5000/registry/export?month=${monthApi}&year=${year}`;


  // 👉 usa a MESMA origem do backend
  // const url = `/registry/export?month=${monthApi}&year=${year}`;
  // print(url)

  window.location.href = url;
});
