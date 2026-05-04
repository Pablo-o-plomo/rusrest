import { prisma } from '@/lib/prisma';
import { RestaurantCard } from '@/components/RestaurantCard';
import { MetricCard } from '@/components/MetricCard';

export default async function DashboardPage() {
  const restaurants = await prisma.restaurant.findMany({ orderBy: { createdAt: 'desc' } });
  const totalRevenue = restaurants.reduce((acc, item) => acc + item.revenue, 0);
  const avgLabor = restaurants.length ? restaurants.reduce((acc, item) => acc + item.laborCost, 0) / restaurants.length : 0;

  return (
    <section className="space-y-6">
      <h1 className="text-3xl font-bold">Restaurant Ops Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-3">
        <MetricCard title="Ресторанов" value={String(restaurants.length)} />
        <MetricCard title="Суммарная выручка" value={`${totalRevenue.toLocaleString('ru-RU')} ₽`} />
        <MetricCard title="Средний ФОТ" value={`${avgLabor.toFixed(1)}%`} />
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => <RestaurantCard key={r.id} id={r.id} name={r.name} city={r.city} revenue={r.revenue} laborCost={r.laborCost} />)}
      </div>
    </section>
  );
}
