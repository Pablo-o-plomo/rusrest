import { RestaurantCardData } from '@/lib/types';

function riskColor(value: number, warning: number, critical: number) {
  if (value >= critical) return 'text-risk';
  if (value >= warning) return 'text-warn';
  return 'text-ok';
}

export function RestaurantCard({ data }: { data: RestaurantCardData }) {
  return (
    <article className="card space-y-2">
      <h3 className="text-lg font-semibold">{data.name}</h3>
      <p>Выручка: {data.revenue.toLocaleString('ru-RU')} ₽</p>
      <p>Средний чек: {data.avgCheck} ₽</p>
      <p className={riskColor(data.laborCostPct, 30, 38)}>ФОТ: {data.laborCostPct}%</p>
      <p className={riskColor(data.foodCostPct, 35, 42)}>Food Cost: {data.foodCostPct}%</p>
      <p>Списания: {data.writeOffs.toLocaleString('ru-RU')} ₽</p>
      <p>Открытые задачи: {data.openTasks}</p>
      <p className={data.overdueTasks > 0 ? 'text-risk' : 'text-ok'}>Просроченные: {data.overdueTasks}</p>
    </article>
  );
}
