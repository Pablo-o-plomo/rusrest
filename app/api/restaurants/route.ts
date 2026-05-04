import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  const restaurants = await prisma.restaurant.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(restaurants);
}

export async function POST(req: Request) {
  const data = await req.json();
  const restaurant = await prisma.restaurant.create({
    data: {
      name: data.name,
      city: data.city,
      revenue: Number(data.revenue),
      laborCost: Number(data.laborCost)
    }
  });

  if (restaurant.laborCost > 12) {
    await prisma.task.create({
      data: {
        title: 'Снизить ФОТ',
        status: 'open',
        deadline: new Date(Date.now() + 3 * 24 * 60 * 60 * 1000),
        restaurantId: restaurant.id
      }
    });
  }

  return NextResponse.json(restaurant, { status: 201 });
}
