import { prisma } from '@/lib/prisma';

function rowColor(status: string) {
  if (status === 'overdue') return 'text-red-400';
  if (status === 'closed') return 'text-green-400';
  return 'text-yellow-400';
}

export default async function TasksPage() {
  const tasks = await prisma.task.findMany({ include: { restaurant: true }, orderBy: { deadline: 'asc' } });

  return (
    <section className="space-y-4">
      <h1 className="text-2xl font-bold">Tasks</h1>
      <div className="overflow-x-auto rounded-2xl border border-slate-800 bg-[#171717] p-3">
        <table className="w-full text-sm">
          <thead className="text-slate-400"><tr><th className="text-left">Название</th><th className="text-left">Ресторан</th><th>Статус</th><th>Дедлайн</th></tr></thead>
          <tbody>
            {tasks.map((task) => (
              <tr key={task.id} className="border-t border-slate-800">
                <td className="py-2">{task.title}</td>
                <td>{task.restaurant.name}</td>
                <td className={`text-center ${rowColor(task.status)}`}>{task.status}</td>
                <td className="text-center">{new Date(task.deadline).toLocaleDateString('ru-RU')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
