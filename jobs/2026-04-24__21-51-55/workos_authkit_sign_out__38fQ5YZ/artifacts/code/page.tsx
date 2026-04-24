import { getUser, getSignInUrl, signOut } from '@workos-inc/authkit-nextjs';
import Link from 'next/link';

export default async function HomePage() {
  const { user } = await getUser();

  if (!user) {
    const signInUrl = await getSignInUrl();
    return <Link href={signInUrl}>Log in</Link>;
  }

  return (
    <div>
      <p>Welcome back, {user.firstName}!</p>
      <form
        action={async () => {
          'use server';
          await signOut();
        }}
      >
        <button type="submit">Sign out</button>
      </form>
    </div>
  );
}
