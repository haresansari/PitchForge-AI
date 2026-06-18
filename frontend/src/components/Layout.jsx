import { Sparkles } from "lucide-react";
import { Link, NavLink } from "react-router-dom";

export function Shell({ children }) {
  return <main className="min-h-screen overflow-hidden">{children}</main>;
}

export function Navbar() {
  return (
    <header className="section-shell fixed left-1/2 top-4 z-50 -translate-x-1/2">
      <nav className="glass flex items-center justify-between rounded-lg px-4 py-3">
        <Link to="/" className="flex items-center gap-2 font-bold tracking-tight">
          <span className="grid h-9 w-9 place-items-center rounded-md bg-white text-ink">
            <Sparkles size={18} />
          </span>
          PitchForge AI
        </Link>
        <div className="flex items-center gap-2 text-sm text-slate-300">
          <NavLink className="rounded-md px-3 py-2 hover:bg-white/10" to="/">
            Home
          </NavLink>
          <NavLink className="rounded-md px-3 py-2 hover:bg-white/10" to="/dashboard">
            Dashboard
          </NavLink>
        </div>
      </nav>
    </header>
  );
}
