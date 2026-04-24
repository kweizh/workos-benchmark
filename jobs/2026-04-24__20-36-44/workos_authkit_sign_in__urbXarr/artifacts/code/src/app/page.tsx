import { withAuth, getSignInUrl, getSignUpUrl } from '@workos-inc/authkit-nextjs';
import Link from 'next/link';

export default async function HomePage() {
  const { user } = await withAuth();
  const signInUrl = await getSignInUrl();
  const signUpUrl = await getSignUpUrl();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen py-2">
      <h1 className="text-6xl font-bold text-center">WorkOS AuthKit + Next.js</h1>
      <p className="mt-4 text-2xl text-center">
        The easiest way to add authentication to your Next.js app.
      </p>

      <div className="mt-8 flex gap-4">
        {user ? (
          <div className="flex flex-col items-center gap-4">
            <p className="text-lg">Signed in as <span className="font-semibold">{user.email}</span></p>
            <Link
              href="/dashboard"
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Go to Dashboard
            </Link>
          </div>
        ) : (
          <div className="flex gap-4">
            <Link
              href={signInUrl}
              className="px-6 py-3 bg-blue-600 text-white rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              Sign In
            </Link>
            <Link
              href={signUpUrl}
              className="px-6 py-3 bg-gray-200 text-gray-800 rounded-lg font-semibold hover:bg-gray-300 transition-colors"
            >
              Sign Up
            </Link>
          </div>
        )}
      </div>
    </div>
  );
}
