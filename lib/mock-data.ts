export const restaurants = [
  { id: '1', name: 'Клёво Ростов', city: 'Ростов-на-Дону', revenue: 1850000, laborCost: 12.8, foodCost: 33.2 },
  { id: '2', name: 'Клёво Сахалин', city: 'Южно-Сахалинск', revenue: 1320000, laborCost: 11.4, foodCost: 30.1 },
  { id: '3', name: 'Клёво Сочи', city: 'Сочи', revenue: 2210000, laborCost: 14.6, foodCost: 36.4 }
];

export const tasks = [
  { id: 't1', title: 'Проверить ФОТ', status: 'open', deadline: '2026-05-07', restaurantId: '1' },
  { id: 't2', title: 'Проверить списания', status: 'in_progress', deadline: '2026-05-08', restaurantId: '2' },
  { id: 't3', title: 'Проверить закупочные цены', status: 'overdue', deadline: '2026-05-03', restaurantId: '3' }
];
