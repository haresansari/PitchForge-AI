const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const response = await fetch(`${API_URL}${path}`, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed with status ${response.status}`);
  }

  return response.json();
}

export const api = {
  generatePitch(payload) {
    return request("/generate-pitch", {
      method: "POST",
      body: JSON.stringify(payload),
    });
  },
  getPitch(pitchId) {
    return request(`/pitch/${pitchId}`);
  },
  generateScore(pitchId) {
    return request("/generate-score", {
      method: "POST",
      body: JSON.stringify({ pitch_id: pitchId }),
    });
  },
  generateSwot(pitchId) {
    return request("/generate-swot", {
      method: "POST",
      body: JSON.stringify({ pitch_id: pitchId }),
    });
  },
  generateCompetitors(pitchId) {
    return request("/generate-competitors", {
      method: "POST",
      body: JSON.stringify({ pitch_id: pitchId }),
    });
  },
  generateValuation(pitchId) {
    return request("/generate-valuation", {
      method: "POST",
      body: JSON.stringify({ pitch_id: pitchId }),
    });
  },
  history() {
    return request("/history?limit=12");
  },
  async exportPdf(pitchId, filename = "pitchforge-report.pdf") {
    const response = await fetch(`${API_URL}/export-pdf`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ pitch_id: pitchId }),
    });

    if (!response.ok) throw new Error("PDF export failed");
    const blob = await response.blob();
    const url = URL.createObjectURL(blob);
    const anchor = document.createElement("a");
    anchor.href = url;
    anchor.download = filename;
    anchor.click();
    URL.revokeObjectURL(url);
  },
};
