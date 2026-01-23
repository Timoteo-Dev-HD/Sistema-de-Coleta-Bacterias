document.getElementById("uploadBtn").addEventListener("click", async () => {
  const input = document.getElementById("pdfInput");
  const badge = document.getElementById("statusBadge");

  if (!input.files.length) {
    alert("Selecione um PDF");
    return;
  }

  const formData = new FormData();
  formData.append("file", input.files[0]);

  badge.innerText = "Processando...";
  badge.className = "badge loading";

  try {
    // 🔹 1️⃣ Faz o upload (backend salva no banco)
    await api.post("/pdf/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" }
    });

    // 🔹 2️⃣ Feedback visual
    badge.innerText = "Concluído";
    badge.className = "badge success";

    // 🔹 3️⃣ Limpa o input (boa prática)
    input.value = "";

    // 🔹 4️⃣ Recarrega dados do banco (ATUALIZA A TABELA)
    await loadRegistries();
    // return window.location.reload()

    // // 🔹 5️⃣ (opcional) Scroll para a tabela
    // document.getElementById("dataTable")
    //   .scrollIntoView({ behavior: "smooth" });

    // return location.reload();
    
  } catch (err) {
    console.error(err);
    badge.innerText = "Erro";
    badge.className = "badge error";
    alert("Erro ao processar o PDF");
  }
});
