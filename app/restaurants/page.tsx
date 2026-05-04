import { RestaurantCard } from '@/components/RestaurantCard';
import { restaurants } from '@/lib/mock-data';

export default function RestaurantsPage() {
  return (
    <section className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold">Restaurants</h1>
        <button className="rounded bg-white px-3 py-2 text-sm font-medium text-black">Добавить ресторан</button>
      </div>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => <RestaurantCard key={r.id} id={r.id} name={r.name} city={r.city} revenue={r.revenue} laborCost={r.laborCost} />)}
      </div>
    </section>
  );
}
