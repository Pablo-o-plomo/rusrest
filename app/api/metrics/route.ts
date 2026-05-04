import { NextResponse } from 'next/server';
import { restaurants, tasks } from '@/lib/mock-data';

export async function GET() {
  const totalRevenue = restaurants.reduce((acc, r) => acc + r.revenue, 0);
  const avgLabor = restaurants.reduce((acc, r) => acc + r.laborCost, 0) / restaurants.length;
  const avgFood = restaurants.reduce((acc, r) => acc + r.foodCost, 0) / restaurants.length;
  return NextResponse.json([
    { name: 'revenue', value: totalRevenue },
    { name: 'labor_cost_pct', value: avgLabor },
    { name: 'food_cost_pct', value: avgFood },
    { name: 'open_tasks', value: tasks.filter((t) => t.status !== 'closed').length }
  ]);
}
