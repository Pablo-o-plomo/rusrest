import { notFound } from 'next/navigation';
import { prisma } from '@/lib/prisma';
import { MetricCard } from '@/components/MetricCard';
import { TaskList } from '@/components/TaskList';
import { revalidatePath } from 'next/cache';

async function createTask(formData: FormData) {
  'use server';
  const restaurantId = String(formData.get('restaurantId'));
  const title = String(formData.get('title'));
  const deadline = new Date(String(formData.get('deadline')));

  await prisma.task.create({ data: { title, status: 'open', deadline, restaurantId } });
  revalidatePath('/tasks');
  revalidatePath(`/restaurants/${restaurantId}`);
}

export default async function RestaurantDetailPage({ params }: { params: { id: string } }) {
  const restaurant = await prisma.restaurant.findUnique({
    where: { id: params.id },
    include: { tasks: { orderBy: { deadline: 'asc' } } }
  });

  if (!restaurant) notFound();

  return (
    <section className="space-y-6">
      <h1 className="text-2xl font-bold">{restaurant.name}</h1>
      <div className="grid gap-4 md:grid-cols-2">
        <MetricCard title="Выручка" value={`${restaurant.revenue.toLocaleString('ru-RU')} ₽`} />
        <MetricCard title="ФОТ %" value={`${restaurant.laborCost}%`} subtitle="Ключевая метрика затрат на персонал" />
      </div>

      <form action={createTask} className="grid gap-3 rounded-2xl border border-slate-800 bg-[#171717] p-4 md:grid-cols-4">
        <input type="hidden" name="restaurantId" value={restaurant.id} />
        <input name="title" required placeholder="Создать задачу" className="rounded bg-[#0f0f0f] p-2 md:col-span-2" />
        <input name="deadline" required type="date" className="rounded bg-[#0f0f0f] p-2" />
        <button className="rounded bg-white px-3 py-2 font-medium text-black">Создать задачу</button>
      </form>

      <TaskList tasks={restaurant.tasks.map((t) => ({ id: t.id, title: t.title, status: t.status, deadline: t.deadline.toISOString() }))} />
    </section>
  );
}
