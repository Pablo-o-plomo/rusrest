import './globals.css';
import type { ReactNode } from 'react';
import { Navbar } from '@/components/Navbar';

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="ru">
      <body className="bg-[#0f0f0f] text-slate-100">
        <main className="mx-auto max-w-6xl p-6">
          <Navbar />
          {children}
        </main>
      </body>
    </html>
  );
}
