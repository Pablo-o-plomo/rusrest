import { Telegraf } from 'telegraf';

export function buildBot(token: string) {
  const bot = new Telegraf(token);
  bot.command('tasks', async (ctx) => ctx.reply('Открытые задачи: 1) Проверить ФОТ 2) Разбор списаний'));
  bot.action('close_task', async (ctx) => ctx.reply('Задача закрыта ✅'));
  return bot;
}
