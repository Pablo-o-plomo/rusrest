import { MetricCard } from '@/components/MetricCard';
import { TaskList } from '@/components/TaskList';
import { restaurants, tasks } from '@/lib/mock-data';
import { notFound } from 'next/navigation';

export default function RestaurantDetailPage({ params }: { params: { id: string } }) {
  const restaurant = restaurants.find((r) => r.id === params.id);
  if (!restaurant) notFound();

  const restaurantTasks = tasks.filter((t) => t.restaurantId === restaurant.id);

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-bold">{restaurant.name}</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <MetricCard title="Выручка" value={`${restaurant.revenue.toLocaleString('ru-RU')} ₽`} />
        <MetricCard title="ФОТ %" value={`${restaurant.laborCost}%`} />
      </div>
      <button className="rounded bg-white px-3 py-2 text-sm font-medium text-black">Создать задачу</button>
      <TaskList tasks={restaurantTasks.map((t) => ({ ...t, deadline: t.deadline }))} />
    </section>
  );
}
