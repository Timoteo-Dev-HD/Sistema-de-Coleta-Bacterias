function formatDate(dateString) {
  if (!dateString) return "—";

  const date = new Date(dateString);

  if (isNaN(date.getTime())) return "—";

  return date.toLocaleDateString("pt-BR");
}


