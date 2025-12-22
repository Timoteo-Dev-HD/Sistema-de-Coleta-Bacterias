document.getElementById("uploadBtn").addEventListener("click", async () => {
  const input = document.getElementById("pdfInput");

  if (!input.files.length) {
    alert("Selecione um arquivo PDF");
    return;
  }

  const formData = new FormData();
  formData.append("file", input.files[0]);

  try {
    const response = await api.post("/pdf/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    renderTable(response.data);
  } catch (err) {
    alert("Erro ao enviar PDF");
    console.error(err);
  }
});
