export type RiskColor = 'ok' | 'warn' | 'risk';

export type RestaurantCardData = {
  id: string;
  name: string;
  revenue: number;
  avgCheck: number;
  laborCostPct: number;
  foodCostPct: number;
  writeOffs: number;
  openTasks: number;
  overdueTasks: number;
};
