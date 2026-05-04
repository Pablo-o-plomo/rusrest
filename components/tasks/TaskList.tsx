const tasks = [
  { title: 'Проверить ФОТ смены', status: 'overdue', assignee: 'Управляющий', deadline: '2026-05-03' },
  { title: 'Разбор food cost', status: 'open', assignee: 'Шеф', deadline: '2026-05-05' }
];

export function TaskList() {
  return (
    <div className="card">
      <h3 className="font-semibold mb-2">Задачи</h3>
      <ul className="space-y-2">
        {tasks.map((task) => (
          <li key={task.title} className="border border-slate-700 rounded p-3">
            <p>{task.title}</p>
            <p className="text-sm text-slate-300">{task.assignee} • дедлайн {task.deadline}</p>
            <p className={task.status === 'overdue' ? 'text-risk text-sm' : 'text-ok text-sm'}>{task.status}</p>
          </li>
        ))}
      </ul>
    </div>
  );
}
