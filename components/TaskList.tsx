type Task = { id: string; title: string; status: string; deadline: string; restaurantName?: string };

function statusClass(status: string) {
  if (status === 'overdue') return 'text-red-400';
  if (status === 'closed') return 'text-green-400';
  return 'text-yellow-400';
}

export function TaskList({ tasks }: { tasks: Task[] }) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-[#171717] p-4 shadow">
      <h3 className="mb-3 text-lg font-semibold">Задачи</h3>
      <ul className="space-y-3">
        {tasks.map((task) => (
          <li key={task.id} className="rounded-lg border border-slate-800 p-3">
            <div className="flex justify-between gap-2">
              <p>{task.title}</p>
              <p className={`text-sm ${statusClass(task.status)}`}>{task.status}</p>
            </div>
            <p className="text-xs text-slate-400">{task.restaurantName ? `${task.restaurantName} • ` : ''}дедлайн {new Date(task.deadline).toLocaleDateString('ru-RU')}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
