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
  const row = recordsData.find(r => r.id === id);

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


function viewRow(id) {
  console.log("ABRINDO MODAL:", id);
  const r = recordsData.find(item => item.id === id);

  if (!r) return;

  // Dados principais
  document.getElementById("m_nome").innerText = r.nome_paciente ?? "—";
  document.getElementById("m_local").innerText = r.local ?? "—";
  document.getElementById("m_material").innerText = r.material_coletada ?? "—";
  document.getElementById("m_micro").innerText = r.microorganismo ?? "—";

  // Datas
  document.getElementById("m_admissao").innerText = formatDate(r.data_admissao);
  document.getElementById("m_coleta").innerText = formatDate(r.data_da_coleta);
  document.getElementById("m_ence").innerText = formatDate(r.data_encerramento);
  document.getElementById("m_insert").innerHTML = formatDate(r.data_criacao);

  // Observações
  document.getElementById("m_obs").innerText = r.observacao ?? "—";

  // Antibiograma
  const tbody = document.getElementById("antibiogramaBody");
  tbody.innerHTML = "";

  const ANTIBIOTICOS = {
    amicacina: "Amicacina",
    ampicilina: "Ampicilina",
    amoxicilina: "Amoxicilina",
    amoxicilina_clavulanato: "Amoxicilina-Clavulanato",
    cefalexina: "Cefalexina",
    cefepime: "Cefepima",
    ceftazidime: "Ceftazidima",
    ceftriaxone: "Ceftriaxona",
    cefuroxime: "Cefuroxima",
    ciprofloxacino: "Ciprofloxacina",
    ertapenem: "Ertapenem",
    gentamicina: "Gentamicina",
    imipenem: "Imipenem",
    levofloxacino: "Levofloxacina",
    meropenem: "Meropenem",
    norfloxacina: "Norfloxacina",
    piperacilina_tazobactam: "Piperacilina-Tazobactam",
    polimixina_b: "Polimixina B",
    trimetoprim_sulfametoxazol: "Trimetoprim-Sulfametoxazol",
    vancomicina: "Vancomicina",
    ceftazidima_avibactam: "Ceftazidima-Avibactam",
    nitrofurantoina: "Nitrofurantoina"
  };

  Object.keys(ANTIBIOTICOS).forEach(key => {
    if (r[key]) {
      const tr = document.createElement("tr");

      tr.innerHTML = `
        <td>${ANTIBIOTICOS[key]}</td>
        <td class="${resultadoClass(r[key])}">
          ${r[key]}
        </td>
      `;

      tbody.appendChild(tr);
    }
  });

  document.getElementById("recordModal").style.display = "flex";
}

function formatDate(date) {
  if (!date) return "—";
  return new Date(date).toLocaleDateString("pt-BR");
}

function resultadoClass(value) {
  if (value.includes("Resistente")) return "resistente";
  if (value.includes("Sensível")) return "sensivel";
  if (value.includes("Intermediário")) return "intermediario";
  return "";
}

function closeModal() {
  document.getElementById("recordModal").style.display = "none";
}


// 🔥 EXPOR FUNÇÕES PARA O HTML
window.viewRow = viewRow;
window.closeModal = closeModal;
window.editRow = editRow;
window.deleteRow = deleteRow;
