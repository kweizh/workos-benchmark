import { getSignInUrl, getSignUpUrl } from '@workos-inc/authkit-nextjs';
import { withAuth } from '@workos-inc/authkit-nextjs';
import Link from 'next/link';
import { signOut } from '@workos-inc/authkit-nextjs';
import { redirect } from 'next/navigation';

export default async function HomePage() {
  const { user } = await withAuth();
  const signInUrl = await getSignInUrl();
  const signUpUrl = await getSignUpUrl();

  return (
    <div className="p-8">
      <h1 className="text-2xl font-bold mb-4">Welcome to AuthKit with Next.js</h1>
      {user ? (
        <div>
          <p className="mb-4">Hello, {user.firstName || user.email}!</p>
          <div className="flex gap-4">
            <Link href="/dashboard" className="text-blue-600 hover:underline">
              Go to Dashboard
            </Link>
            <form action={async () => {
              "use server";
              await signOut();
            }}>
              <button type="submit" className="text-red-600 hover:underline">
                Sign Out
              </button>
            </form>
          </div>
        </div>
      ) : (
        <div className="flex gap-4">
          <Link href={signInUrl} className="bg-blue-600 text-white px-4 py-2 rounded">
            Sign In
          </Link>
          <Link href={signUpUrl} className="bg-gray-600 text-white px-4 py-2 rounded">
            Sign Up
          </Link>
        </div>
      )}
    </div>
  );
}
