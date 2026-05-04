import Link from 'next/link';

export function Navbar() {
  const linkClass = 'text-sm text-slate-300 hover:text-white transition';
  return (
    <nav className="mb-6 flex items-center gap-6 rounded-xl border border-slate-800 bg-[#151515] px-4 py-3 shadow-sm">
      <Link className={linkClass} href="/">Dashboard</Link>
      <Link className={linkClass} href="/restaurants">Restaurants</Link>
      <Link className={linkClass} href="/tasks">Tasks</Link>
    </nav>
  );
}
