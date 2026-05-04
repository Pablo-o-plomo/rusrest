export type RuleInput = { laborCostPct: number; foodCostPct: number; overdueTasks: number };

export function evaluateRules(input: RuleInput) {
  const actions: string[] = [];
  if (input.laborCostPct > 30) actions.push('Создать задачу управляющему: снизить ФОТ');
  if (input.foodCostPct > 32) actions.push('Создать задачу шефу: разобрать food cost');
  if (input.overdueTasks > 0) actions.push('Отправить уведомление о просроченных задачах');
  return actions;
}
