FROM ubuntu:24.04

RUN apt-get update -y && \
    DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        curl ca-certificates git python3 python3-pip python3-pytest bash && \
    curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN mkdir -p /home/user/app/src/app && chmod -R 0755 /home/user

LABEL Author="any-task-builder"
LABEL Description="Next.js app with WorkOS AuthKit installed, missing sign out action."

WORKDIR /home/user/app

RUN cat > package.json <<'EOF'
{
  "name": "authkit-app",
  "private": true,
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.2.3",
    "react": "^18.3.1",
    "react-dom": "^18.3.1",
    "@workos-inc/authkit-nextjs": "^0.13.0"
  },
  "devDependencies": {
    "typescript": "^5",
    "@types/node": "^20",
    "@types/react": "^18",
    "@types/react-dom": "^18"
  }
}
EOF

RUN cat > src/app/layout.tsx <<'EOF'
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
EOF

RUN cat > src/app/page.tsx <<'EOF'
import { getUser, getSignInUrl } from '@workos-inc/authkit-nextjs';
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
      <form>
        <button type="submit">Sign out</button>
      </form>
    </div>
  );
}
EOF

RUN cat > src/middleware.ts <<'EOF'
import { authkitMiddleware } from '@workos-inc/authkit-nextjs';
export default authkitMiddleware();
export const config = { matcher: ['/', '/((?!_next/|_static/|[\\w-]+\\.\\w+).*)'] };
EOF

RUN cat > next.config.mjs <<'EOF'
/** @type {import('next').NextConfig} */
const nextConfig = {};
export default nextConfig;
EOF

RUN cat > tsconfig.json <<'EOF'
{
  "compilerOptions": {
    "lib": ["dom", "dom.iterable", "esnext"],
    "allowJs": true,
    "skipLibCheck": true,
    "strict": true,
    "noEmit": true,
    "esModuleInterop": true,
    "module": "esnext",
    "moduleResolution": "bundler",
    "resolveJsonModule": true,
    "isolatedModules": true,
    "jsx": "preserve",
    "incremental": true,
    "plugins": [
      {
        "name": "next"
      }
    ],
    "paths": {
      "@/*": ["./src/*"]
    }
  },
  "include": ["next-env.d.ts", "**/*.ts", "**/*.tsx", ".next/types/**/*.ts"],
  "exclude": ["node_modules"]
}
EOF

RUN cd /home/user/app && npm install

CMD ["/bin/bash", "-c", "trap : TERM INT; sleep infinity & wait"]
