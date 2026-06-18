export function PitchCard({ title, children, accent = "border-white/10" }) {
  return (
    <section className={`glass rounded-lg border ${accent} p-5`}>
      <h2 className="text-sm font-semibold uppercase tracking-[0.18em] text-slate-400">{title}</h2>
      <div className="mt-4 text-sm leading-7 text-slate-200">{children}</div>
    </section>
  );
}
