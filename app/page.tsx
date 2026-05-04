import Link from 'next/link';
import { RestaurantCard } from '@/components/restaurants/RestaurantCard';

const restaurants = [
  { id: '1', name: 'Basilico', revenue: 1450000, avgCheck: 1250, laborCostPct: 31, foodCostPct: 37, writeOffs: 92000, openTasks: 8, overdueTasks: 2 }
];

export default function DashboardPage() {
  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">Restaurant Ops Map</h1>
      <p className="text-slate-300">Операционная система: метрики → задачи → уведомления → подтверждения.</p>
      <div className="grid md:grid-cols-2 gap-4">
        {restaurants.map((restaurant) => (
          <Link href={`/restaurants/${restaurant.id}`} key={restaurant.id}><RestaurantCard data={restaurant} /></Link>
        ))}
      </div>
    </section>
  );
}
