import { NextResponse } from 'next/server';
import { tasks } from '@/lib/mock-data';

export async function GET() {
  return NextResponse.json(tasks);
}

export async function POST(req: Request) {
  const data = await req.json();
  return NextResponse.json({
    id: String(Date.now()),
    title: data.title,
    status: data.status ?? 'open',
    deadline: data.deadline,
    restaurantId: data.restaurantId
  }, { status: 201 });
}
