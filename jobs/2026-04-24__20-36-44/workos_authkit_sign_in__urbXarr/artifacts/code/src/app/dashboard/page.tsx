import { withAuth, getSignInUrl, signOut } from '@workos-inc/authkit-nextjs';
import { redirect } from 'next/navigation';

export default async function DashboardPage() {
  const { user } = await withAuth();

  if (!user) {
    const signInUrl = await getSignInUrl();
    redirect(signInUrl);
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-4xl font-bold">Dashboard</h1>
      <p className="mt-4 text-xl">Welcome, {user.firstName || user.email}!</p>
      <pre className="mt-4 p-4 bg-gray-100 rounded overflow-auto max-w-full">
        {JSON.stringify(user, null, 2)}
      </pre>
      <form
        action={async () => {
          'use server';
          await signOut();
        }}
      >
        <button
          type="submit"
          className="mt-4 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
        >
          Sign Out
        </button>
      </form>
    </div>
  );
}
