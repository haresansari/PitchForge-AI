import { Clock, Loader2, Rocket, Sparkles } from "lucide-react";
import { useEffect, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Button } from "../components/Button";
import { Navbar, Shell } from "../components/Layout";
import { Page } from "../components/Motion";
import { usePitchGeneration } from "../hooks/usePitchGeneration";
import { api } from "../services/api";

const examples = [
  "AI platform that helps small clinics reduce patient no-shows with predictive outreach",
  "Marketplace for climate-friendly construction materials with verified supplier data",
  "Personal finance copilot for students entering their first job",
];

export default function Dashboard() {
  const navigate = useNavigate();
  const { generate, loading, error } = usePitchGeneration();
  const [history, setHistory] = useState([]);
  const [form, setForm] = useState({
    startup_idea: examples[0],
    industry: "Healthcare SaaS",
    revenue_model: "Monthly subscription with premium analytics",
  });

  useEffect(() => {
    api.history().then((result) => setHistory(result.data || [])).catch(() => setHistory([]));
  }, []);

  async function onSubmit(event) {
    event.preventDefault();
    const pitchId = await generate(form);
    if (pitchId) navigate(`/results/${pitchId}`);
  }

  function updateField(field, value) {
    setForm((current) => ({ ...current, [field]: value }));
  }

  return (
    <Shell>
      <Navbar />
      <Page>
        <section className="section-shell min-h-screen pt-32 pb-16">
          <div className="grid gap-6 lg:grid-cols-[1fr_380px]">
            <div className="glass rounded-lg p-6 md:p-8">
              <div className="mb-8 flex items-start justify-between gap-6">
                <div>
                  <p className="text-sm font-semibold uppercase tracking-[0.22em] text-mint">Dashboard</p>
                  <h1 className="mt-3 text-3xl font-extrabold md:text-5xl">Generate an investor-ready pitch.</h1>
                  <p className="mt-4 max-w-2xl leading-7 text-slate-300">
                    Describe the startup in plain language. PitchForge will create the pitch, scoring,
                    SWOT, competitor analysis, valuation, and exportable report.
                  </p>
                </div>
                <div className="hidden rounded-md border border-white/10 bg-white/10 p-3 md:block">
                  <Rocket className="text-coral" size={24} />
                </div>
              </div>

              <form className="space-y-5" onSubmit={onSubmit}>
                <label className="block">
                  <span className="text-sm font-medium text-slate-300">Startup Idea</span>
                  <textarea
                    className="mt-2 min-h-40 w-full resize-y rounded-lg border border-white/10 bg-ink/70 px-4 py-4 leading-7 text-white outline-none transition placeholder:text-slate-600 focus:border-mint"
                    value={form.startup_idea}
                    minLength={10}
                    maxLength={1200}
                    onChange={(event) => updateField("startup_idea", event.target.value)}
                    placeholder="What are you building, for whom, and what pain does it solve?"
                    required
                  />
                </label>

                <div className="grid gap-5 md:grid-cols-2">
                  <label className="block">
                    <span className="text-sm font-medium text-slate-300">Industry</span>
                    <input
                      className="mt-2 h-12 w-full rounded-lg border border-white/10 bg-ink/70 px-4 text-white outline-none transition placeholder:text-slate-600 focus:border-mint"
                      value={form.industry}
                      minLength={2}
                      maxLength={120}
                      onChange={(event) => updateField("industry", event.target.value)}
                      placeholder="FinTech, EdTech, ClimateTech"
                      required
                    />
                  </label>
                  <label className="block">
                    <span className="text-sm font-medium text-slate-300">Revenue Model</span>
                    <input
                      className="mt-2 h-12 w-full rounded-lg border border-white/10 bg-ink/70 px-4 text-white outline-none transition placeholder:text-slate-600 focus:border-mint"
                      value={form.revenue_model}
                      minLength={3}
                      maxLength={240}
                      onChange={(event) => updateField("revenue_model", event.target.value)}
                      placeholder="Subscription, marketplace fee, licensing"
                      required
                    />
                  </label>
                </div>

                <div className="flex flex-col gap-3 sm:flex-row sm:items-center">
                  <Button type="submit" disabled={loading}>
                    {loading ? <Loader2 className="animate-spin" size={18} /> : <Sparkles size={18} />}
                    {loading ? "Forging Pitch..." : "Generate Pitch"}
                  </Button>
                  {error && <p className="text-sm text-coral">{error}</p>}
                </div>
              </form>
            </div>

            <aside className="space-y-5">
              <div className="glass rounded-lg p-5">
                <h2 className="flex items-center gap-2 text-lg font-semibold">
                  <Sparkles size={18} className="text-mint" /> Idea Starters
                </h2>
                <div className="mt-4 space-y-3">
                  {examples.map((example) => (
                    <button
                      key={example}
                      type="button"
                      onClick={() => updateField("startup_idea", example)}
                      className="w-full rounded-md border border-white/10 bg-white/5 p-3 text-left text-sm leading-6 text-slate-300 transition hover:border-mint/50 hover:text-white"
                    >
                      {example}
                    </button>
                  ))}
                </div>
              </div>

              <div className="glass rounded-lg p-5">
                <h2 className="flex items-center gap-2 text-lg font-semibold">
                  <Clock size={18} className="text-gold" /> Pitch History
                </h2>
                <div className="mt-4 space-y-3">
                  {history.length === 0 && (
                    <p className="text-sm leading-6 text-slate-400">Previous pitches will appear here after generation.</p>
                  )}
                  {history.map((pitch) => (
                    <Link
                      key={pitch.id}
                      to={`/results/${pitch.id}`}
                      className="block rounded-md border border-white/10 bg-white/5 p-3 transition hover:border-sky/60"
                    >
                      <p className="font-medium">{pitch.startup_name}</p>
                      <p className="mt-1 text-xs text-slate-400">{pitch.industry}</p>
                    </Link>
                  ))}
                </div>
              </div>
            </aside>
          </div>
        </section>
      </Page>
    </Shell>
  );
}
