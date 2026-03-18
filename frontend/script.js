// Substitua pela URL da sua API no Render, se for diferente
const API_BASE_URL = "https://plant-recognition-ai.onrender.com";

const imageInput = document.getElementById("imageInput");
const identifyButton = document.getElementById("identifyButton");
const previewContainer = document.getElementById("previewContainer");
const previewImage = document.getElementById("previewImage");
const statusEl = document.getElementById("status");
const resultSection = document.getElementById("resultSection");
const plantNameEl = document.getElementById("plantName");
const confidenceEl = document.getElementById("confidence");
const plantDetailsEl = document.getElementById("plantDetails");

let selectedFile = null;

// Quando o usuário escolhe uma imagem
imageInput.addEventListener("change", () => {
  const file = imageInput.files[0];
  if (!file) return;

  selectedFile = file;
  identifyButton.disabled = false;

  // Mostrar pré-visualização
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewContainer.style.display = "block";
  };
  reader.readAsDataURL(file);

  statusEl.textContent = "Imagem pronta para análise.";
  resultSection.style.display = "none";
});

// Quando clica em "Identificar planta"
identifyButton.addEventListener("click", async () => {
  if (!selectedFile) {
    statusEl.textContent = "Selecione uma imagem primeiro.";
    return;
  }

  identifyButton.disabled = true;
  statusEl.textContent = "Analisando imagem, aguarde...";

  const formData = new FormData();
  formData.append("file", selectedFile);

  try {
    const response = await fetch(`${API_BASE_URL}/identify`, {
      method: "POST",
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Erro na API: ${response.status}`);
    }

    const data = await response.json();

    plantNameEl.textContent = data.planta || "Desconhecida";
    confidenceEl.textContent = data.confianca || "";

    plantDetailsEl.innerHTML = "";

    if (data.dados && typeof data.dados === "object") {
      for (const [key, value] of Object.entries(data.dados)) {
        const p = document.createElement("p");
        p.innerHTML = `<strong>${key}:</strong> ${value}`;
        plantDetailsEl.appendChild(p);
      }
    } else {
      const p = document.createElement("p");
      p.textContent = "Nenhuma informação adicional encontrada para esta planta.";
      plantDetailsEl.appendChild(p);
    }

    resultSection.style.display = "block";
    statusEl.textContent = "Análise concluída.";

  } catch (error) {
    console.error(error);
    statusEl.textContent = "Erro ao identificar a planta. Tente novamente.";
    resultSection.style.display = "none";
  } finally {
    identifyButton.disabled = false;
  }
});
