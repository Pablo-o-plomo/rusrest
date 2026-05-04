import { ProcessCanvas } from '@/components/canvas/ProcessCanvas';
import { NodePropertiesPanel } from '@/components/canvas/NodePropertiesPanel';
import { MetricsTable } from '@/components/metrics/MetricsTable';
import { TaskList } from '@/components/tasks/TaskList';

export default function RestaurantPage() {
  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">Ресторан • Карточка</h1>
      <div className="flex gap-2 text-sm">
        <span className="card">Карта процессов</span><span className="card">Метрики</span><span className="card">Задачи</span><span className="card">Отчёты</span><span className="card">Боты</span>
      </div>
      <div className="grid grid-cols-1 xl:grid-cols-4 gap-4">
        <div className="xl:col-span-3"><ProcessCanvas /></div>
        <NodePropertiesPanel />
      </div>
      <div className="grid md:grid-cols-2 gap-4">
        <MetricsTable />
        <TaskList />
      </div>
    </div>
  );
}
