function parseAntibioticoValue(value) {
  if (!value) {
    return { status: "", operador: "<=", mic: "" };
  }

  const match = value.match(/(Sensível|Resistente|Intermediário)\s*(<=|>=|=)?\s*(.*)?/i);

  if (!match) {
    return { status: "", operador: "<=", mic: "" };
  }

  return {
    status: match[1] ?? "",
    operador: match[2] ?? "<=",
    mic: match[3] ?? ""
  };
}


function formatDate(dateString) {
  if (!dateString) return "—";

  const date = new Date(dateString);

  if (isNaN(date.getTime())) return "—";

  return date.toLocaleDateString("pt-BR");
}

function emptyToNull(value) {
  return value === "" ? null : value;
}