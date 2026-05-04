import { MetricCard } from '@/components/MetricCard';
import { RestaurantCard } from '@/components/RestaurantCard';
import { restaurants, tasks } from '@/lib/mock-data';

export default function DashboardPage() {
  const totalRevenue = restaurants.reduce((acc, r) => acc + r.revenue, 0);
  const avgLabor = restaurants.reduce((acc, r) => acc + r.laborCost, 0) / restaurants.length;
  const avgFood = restaurants.reduce((acc, r) => acc + r.foodCost, 0) / restaurants.length;

  return (
    <section className="space-y-6">
      <h1 className="text-3xl font-bold">Restaurant Ops Dashboard</h1>
      <div className="grid gap-4 md:grid-cols-4">
        <MetricCard title="Выручка" value={`${totalRevenue.toLocaleString('ru-RU')} ₽`} />
        <MetricCard title="ФОТ %" value={`${avgLabor.toFixed(1)}%`} />
        <MetricCard title="Food Cost %" value={`${avgFood.toFixed(1)}%`} />
        <MetricCard title="Открытые задачи" value={String(tasks.filter((t) => t.status !== 'closed').length)} />
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => <RestaurantCard key={r.id} id={r.id} name={r.name} city={r.city} revenue={r.revenue} laborCost={r.laborCost} />)}
      </div>
    </section>
  );
}
