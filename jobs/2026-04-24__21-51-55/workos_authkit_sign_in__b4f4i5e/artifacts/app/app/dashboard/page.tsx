import { getSignInUrl } from '@workos-inc/authkit-nextjs';
import { withAuth } from '@workos-inc/authkit-nextjs';
import { redirect } from 'next/navigation';
import Link from 'next/link';

export default async function DashboardPage() {
  const { user } = await withAuth();

  if (!user) {
    const signInUrl = await getSignInUrl();
    redirect(signInUrl);
  }

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <p className="mb-4">This is a protected route.</p>
      <div className="bg-gray-100 p-4 rounded mb-4">
        <pre>{JSON.stringify(user, null, 2)}</pre>
      </div>
      <Link href="/" className="text-blue-600 hover:underline">
        Back to Home
      </Link>
    </div>
  );
}
