import { useState } from "react";
import { api } from "../services/api";

export function usePitchGeneration() {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function generate(payload) {
    setLoading(true);
    setError("");
    try {
      const pitch = await api.generatePitch(payload);
      const pitchId = pitch.pitch_id;
      await Promise.allSettled([
        api.generateScore(pitchId),
        api.generateSwot(pitchId),
        api.generateCompetitors(pitchId),
        api.generateValuation(pitchId),
      ]);
      return pitchId;
    } catch (err) {
      setError(err.message || "Unable to generate pitch.");
      return null;
    } finally {
      setLoading(false);
    }
  }

  return { generate, loading, error };
}
