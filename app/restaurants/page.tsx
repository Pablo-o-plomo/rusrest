import { prisma } from '@/lib/prisma';
import { RestaurantCard } from '@/components/RestaurantCard';
import { revalidatePath } from 'next/cache';

async function createRestaurant(formData: FormData) {
  'use server';
  const name = String(formData.get('name') || '');
  const city = String(formData.get('city') || '');
  const revenue = Number(formData.get('revenue') || 0);
  const laborCost = Number(formData.get('laborCost') || 0);

  const restaurant = await prisma.restaurant.create({ data: { name, city, revenue, laborCost } });

  if (laborCost > 12) {
    await prisma.task.create({
      data: {
        title: 'Снизить ФОТ',
        status: 'open',
        deadline: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
        restaurantId: restaurant.id
      }
    });
  }

  revalidatePath('/');
  revalidatePath('/restaurants');
}

export default async function RestaurantsPage() {
  const restaurants = await prisma.restaurant.findMany({ orderBy: { createdAt: 'desc' } });

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-bold">Restaurants</h1>
      <form action={createRestaurant} className="grid gap-3 rounded-2xl border border-slate-800 bg-[#171717] p-4 md:grid-cols-5">
        <input name="name" required placeholder="Название" className="rounded bg-[#0f0f0f] p-2" />
        <input name="city" required placeholder="Город" className="rounded bg-[#0f0f0f] p-2" />
        <input name="revenue" required type="number" step="0.01" placeholder="Выручка" className="rounded bg-[#0f0f0f] p-2" />
        <input name="laborCost" required type="number" step="0.1" placeholder="ФОТ %" className="rounded bg-[#0f0f0f] p-2" />
        <button className="rounded bg-white px-3 py-2 font-medium text-black">Добавить ресторан</button>
      </form>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {restaurants.map((r) => <RestaurantCard key={r.id} id={r.id} name={r.name} city={r.city} revenue={r.revenue} laborCost={r.laborCost} />)}
      </div>
    </section>
  );
}
