import { NextResponse } from 'next/server';
import { restaurants } from '@/lib/mock-data';

export async function GET() {
  return NextResponse.json(restaurants);
}

export async function POST(req: Request) {
  const data = await req.json();
  return NextResponse.json({
    id: String(Date.now()),
    name: data.name,
    city: data.city,
    revenue: Number(data.revenue ?? 0),
    laborCost: Number(data.laborCost ?? 0)
  }, { status: 201 });
}
