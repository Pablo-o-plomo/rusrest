export async function authorize(email: string, password: string) {
  if (!email || !password) return null;
  return { id: 'demo-user', email };
}
