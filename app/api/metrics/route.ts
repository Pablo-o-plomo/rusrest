import { NextResponse } from 'next/server';
import { prisma } from '@/lib/prisma';

export async function GET() {
  const metrics = await prisma.metric.findMany({ orderBy: { createdAt: 'desc' } });
  return NextResponse.json(metrics);
}
