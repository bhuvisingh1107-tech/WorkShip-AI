'use client';

import { useEffect } from 'react';
import { useRouter, usePathname } from 'next/navigation';
import { useAuth } from '@/context/AuthProvider';

export default function AuthRedirectHandler() {
  const { user } = useAuth();
  const router = useRouter();
  const pathname = usePathname();

  useEffect(() => {
    const publicPaths = ['/login', '/signup', '/api'];
    const isPublic = publicPaths.some((path) => pathname.startsWith(path));
    if (!user && !isPublic) {
      router.replace('/login');
    }
  }, [user, router, pathname]);

  return null;
}