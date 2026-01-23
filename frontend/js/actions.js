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

function editRow(id) {
  const r = recordsData.find(item => item.id === id);
  if (!r) return;

  document.getElementById("e_id").value = r.id;
  document.getElementById("e_nome").value = r.nome_paciente ?? "";
  document.getElementById("e_local").value = r.local ?? "";
  document.getElementById("e_material").value = r.material_coletada ?? "";
  document.getElementById("e_micro").value = r.microorganismo ?? "";

  document.getElementById("e_diagnostico").value = r.diagnostico ?? "";
  document.getElementById("e_desfecho").value = r.desfecho ?? "";
  document.getElementById("e_notificacao").value = r.notificacao ?? "";
  document.getElementById("e_dialise").value = r.dialise ?? "";

  document.getElementById("e_admissao").value = r.data_admissao?.slice(0, 10) ?? "";
  document.getElementById("e_coleta").value = r.data_da_coleta?.slice(0, 10) ?? "";
  document.getElementById("e_encerramento").value = r.data_encerramento?.slice(0, 10) ?? "";

  document.getElementById("e_obs").value = r.observacao ?? "";

  document.getElementById("editModal").style.display = "flex";
}

async function saveEdit() {
  const id = document.getElementById("e_id").value;

  // 🔹 Helper: converte "" → null
  const emptyToNull = (v) => (v === "" ? null : v);

  const payload = {
    // ===== Paciente =====
    nome_paciente: document.getElementById("e_nome").value || null,
    local: document.getElementById("e_local").value || null,
    material_coletada: document.getElementById("e_material").value || null,
    microorganismo: document.getElementById("e_micro").value || null,

    // ===== Clínico =====
    diagnostico: document.getElementById("e_diagnostico").value || null,
    desfecho: document.getElementById("e_desfecho").value || null,
    notificacao: document.getElementById("e_notificacao").value || null,
    dialise: document.getElementById("e_dialise").value || null,

    // ===== Datas (⚠️ CRÍTICO) =====
    data_admissao: emptyToNull(document.getElementById("e_admissao").value),
    data_da_coleta: emptyToNull(document.getElementById("e_coleta").value),
    data_encerramento: emptyToNull(document.getElementById("e_encerramento").value),

    // ===== Observações =====
    observacao: document.getElementById("e_obs").value || null
  };

  try {
    await api.put(`/registry/${id}`, payload);

    closeEditModal();        // 🔒 fecha modal
    await loadRegistries();  // 🔄 atualiza lista

  } catch (err) {
    console.error(err);
    alert("Erro ao salvar alterações do registro");
  }
}


function closeEditModal() {
  document.getElementById("editModal").style.display = "none";
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
window.deleteRow = deleteRow;



window.editRow = editRow;
window.saveEdit = saveEdit;
window.closeEditModal = closeEditModal;
