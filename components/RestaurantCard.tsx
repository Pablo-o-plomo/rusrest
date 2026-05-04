import Link from 'next/link';

type Props = { id: string; name: string; city: string; revenue: number; laborCost: number };

function riskClass(laborCost: number) {
  if (laborCost > 14) return 'text-red-400';
  if (laborCost >= 12) return 'text-yellow-400';
  return 'text-green-400';
}

export function RestaurantCard({ id, name, city, revenue, laborCost }: Props) {
  return (
    <Link href={`/restaurants/${id}`} className="block rounded-2xl border border-slate-800 bg-[#171717] p-4 shadow hover:border-slate-700">
      <h3 className="text-lg font-semibold">{name}</h3>
      <p className="text-sm text-slate-400">{city}</p>
      <p className="mt-2 text-sm">Выручка: {revenue.toLocaleString('ru-RU')} ₽</p>
      <p className={`text-sm ${riskClass(laborCost)}`}>ФОТ: {laborCost}%</p>
    </Link>
  );
}
