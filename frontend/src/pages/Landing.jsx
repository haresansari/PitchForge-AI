import { motion } from "framer-motion";
import { ArrowRight, BarChart3, FileDown, LineChart, ShieldCheck, Sparkles, Wand2 } from "lucide-react";
import { Link } from "react-router-dom";
import { Button } from "../components/Button";
import { Navbar, Shell } from "../components/Layout";
import { Page, Reveal } from "../components/Motion";

const features = [
  ["AI Pitch Builder", "Generate investor-ready pitch sections from a raw idea in seconds.", Wand2],
  ["Startup Score Engine", "Evaluate innovation, demand, scalability, and investor appeal.", BarChart3],
  ["Market Intelligence", "SWOT, competitor analysis, and valuation ranges in one workflow.", LineChart],
  ["Exportable Reports", "Download polished PDF reports for judges, mentors, or investors.", FileDown],
];

const benefits = ["Founder-ready narratives", "Accelerator demo workflows", "Hackathon judging proof", "Investor summary clarity"];

export default function Landing() {
  return (
    <Shell>
      <Navbar />
      <Page>
        <section className="section-shell flex min-h-screen items-center pt-28">
          <div className="grid w-full gap-12 lg:grid-cols-[1.02fr_0.98fr] lg:items-center">
            <div>
              <motion.div
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                className="mb-5 inline-flex items-center gap-2 rounded-full border border-white/10 bg-white/10 px-3 py-2 text-sm text-slate-300"
              >
                <Sparkles size={16} className="text-mint" />
                Transform Startup Ideas Into Investor-Ready Business Pitches
              </motion.div>
              <h1 className="max-w-4xl text-balance text-5xl font-extrabold leading-[1.02] tracking-normal text-white md:text-7xl">
                PitchForge AI
              </h1>
              <p className="mt-6 max-w-2xl text-lg leading-8 text-slate-300">
                A premium SaaS workspace for founders, students, incubators, and hackathon teams to
                turn raw startup concepts into structured pitch reports with scoring, SWOT,
                competitors, valuation, history, and PDF export.
              </p>
              <div className="mt-8 flex flex-col gap-3 sm:flex-row">
                <Link to="/dashboard">
                  <Button>
                    Generate Pitch <ArrowRight size={18} />
                  </Button>
                </Link>
                <a href="#features">
                  <Button variant="secondary">Explore Platform</Button>
                </a>
              </div>
            </div>

            <motion.div
              initial={{ opacity: 0, scale: 0.96 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="glass rounded-lg p-5"
            >
              <div className="rounded-md border border-white/10 bg-ink/70 p-5">
                <div className="flex items-center justify-between border-b border-white/10 pb-4">
                  <div>
                    <p className="text-sm text-slate-400">Live Pitch Report</p>
                    <h2 className="text-2xl font-bold">FounderDeck OS</h2>
                  </div>
                  <span className="rounded-md bg-mint/20 px-3 py-2 text-sm text-mint">92 Appeal</span>
                </div>
                <div className="mt-5 grid gap-3">
                  {["Problem", "Solution", "Business Model", "Investor Summary"].map((item, index) => (
                    <motion.div
                      key={item}
                      initial={{ opacity: 0, x: 20 }}
                      animate={{ opacity: 1, x: 0 }}
                      transition={{ delay: 0.2 + index * 0.08 }}
                      className="rounded-md border border-white/10 bg-white/5 p-4"
                    >
                      <p className="text-xs uppercase tracking-[0.18em] text-slate-500">{item}</p>
                      <div className="mt-3 h-2 w-full rounded-full bg-white/10" />
                      <div className="mt-2 h-2 w-3/4 rounded-full bg-white/10" />
                    </motion.div>
                  ))}
                </div>
              </div>
            </motion.div>
          </div>
        </section>

        <section id="features" className="section-shell py-20">
          <Reveal>
            <div className="mb-10 max-w-2xl">
              <p className="text-sm font-semibold uppercase tracking-[0.22em] text-mint">Platform</p>
              <h2 className="mt-3 text-3xl font-bold md:text-5xl">Everything a pitch sprint needs.</h2>
            </div>
          </Reveal>
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
            {features.map(([title, copy, Icon], index) => (
              <Reveal key={title} delay={index * 0.06}>
                <div className="glass h-full rounded-lg p-5 transition hover:-translate-y-1 hover:border-mint/40">
                  <Icon className="text-mint" size={24} />
                  <h3 className="mt-5 text-lg font-semibold">{title}</h3>
                  <p className="mt-3 text-sm leading-6 text-slate-300">{copy}</p>
                </div>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="section-shell py-16">
          <div className="grid gap-8 lg:grid-cols-[0.85fr_1.15fr] lg:items-center">
            <Reveal>
              <div>
                <p className="text-sm font-semibold uppercase tracking-[0.22em] text-coral">Benefits</p>
                <h2 className="mt-3 text-3xl font-bold md:text-5xl">Built for credible startup storytelling.</h2>
              </div>
            </Reveal>
            <div className="grid gap-3 sm:grid-cols-2">
              {benefits.map((benefit) => (
                <Reveal key={benefit}>
                  <div className="flex items-center gap-3 rounded-lg border border-white/10 bg-white/5 p-4">
                    <ShieldCheck className="text-gold" size={20} />
                    <span className="font-medium">{benefit}</span>
                  </div>
                </Reveal>
              ))}
            </div>
          </div>
        </section>

        <section className="section-shell py-20">
          <Reveal>
            <div className="glass rounded-lg p-6 md:p-8">
              <div className="grid gap-6 md:grid-cols-3">
                {["Enter idea, industry, and revenue model", "Generate pitch, scores, SWOT, competitors", "Download and reuse investor-ready report"].map((step, index) => (
                  <div key={step} className="rounded-md border border-white/10 bg-ink/50 p-5">
                    <span className="text-sm text-mint">0{index + 1}</span>
                    <h3 className="mt-4 text-lg font-semibold">{step}</h3>
                  </div>
                ))}
              </div>
            </div>
          </Reveal>
        </section>

        <section className="section-shell py-16">
          <div className="grid gap-4 md:grid-cols-3">
            {[
              ["Aisha K.", "Incubator Lead", "PitchForge makes first mentor sessions much sharper because teams arrive with structure."],
              ["Mateo R.", "Founder", "The investor summary and competitor view helped us explain the wedge without rambling."],
              ["Nina P.", "Hackathon Judge", "It turns rough ideas into something teams can actually defend on stage."],
            ].map(([name, role, quote]) => (
              <Reveal key={name}>
                <blockquote className="glass h-full rounded-lg p-5">
                  <p className="leading-7 text-slate-200">"{quote}"</p>
                  <footer className="mt-5 text-sm text-slate-400">{name} - {role}</footer>
                </blockquote>
              </Reveal>
            ))}
          </div>
        </section>

        <section className="section-shell pb-20 pt-10">
          <Reveal>
            <div className="rounded-lg border border-white/10 bg-white p-8 text-ink md:p-10">
              <h2 className="text-3xl font-extrabold md:text-5xl">Forge the pitch before the room goes quiet.</h2>
              <p className="mt-4 max-w-2xl text-slate-700">
                Generate a full business pitch, score it, compare the market, and export a report.
              </p>
              <Link className="mt-6 inline-flex" to="/dashboard">
                <Button className="bg-ink text-white hover:bg-slate-800">
                  Open Dashboard <ArrowRight size={18} />
                </Button>
              </Link>
            </div>
          </Reveal>
        </section>
      </Page>
    </Shell>
  );
}
