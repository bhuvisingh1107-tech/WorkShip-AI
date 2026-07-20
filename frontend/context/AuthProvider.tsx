'use client';

import { createContext, useContext, useState, useEffect, useCallback, ReactNode } from 'react';
import { supabase } from '@/lib/supabaseClient';

// Known email → role map (fallback when user_metadata.role is not set)
const KNOWN_ROLES: Record<string, string> = {
  'test@workshipai.com': 'Manager',
};

// Role hierarchy for permissions
const ROLE_PERMISSIONS: Record<string, string[]> = {
  Employee: ['/dashboard', '/copilot', '/incidents', '/knowledge', '/settings'],
  Manager: ['/dashboard', '/copilot', '/incidents', '/knowledge', '/company-sales', '/settings'],
  CEO: ['/dashboard', '/copilot', '/incidents', '/knowledge', '/company-sales', '/settings'],
};

export type UserRole = 'Employee' | 'Manager' | 'CEO';

interface AuthContextType {
  user: any;
  role: UserRole | null;
  loading: boolean;
  login: (email: string, password: string, selectedRole: UserRole) => Promise<void>;
  logout: () => Promise<void>;
  canAccess: (path: string) => boolean;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

function resolveRole(user: any): UserRole {
  // 1. Check user_metadata.role (set by Supabase admin or profiles)
  if (user?.user_metadata?.role) {
    return user.user_metadata.role as UserRole;
  }
  // 2. Check app_metadata.role
  if (user?.app_metadata?.role) {
    return user.app_metadata.role as UserRole;
  }
  // 3. Fallback to known email map
  if (user?.email && KNOWN_ROLES[user.email]) {
    return KNOWN_ROLES[user.email] as UserRole;
  }
  // 4. Default to Employee
  return 'Employee';
}

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<any>(null);
  const [role, setRole] = useState<UserRole | null>(null);
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Get initial session
    supabase.auth.getSession().then(({ data: { session } }) => {
      const u = session?.user ?? null;
      setUser(u);
      setRole(u ? resolveRole(u) : null);
      setLoading(false);
    });

    // Listen for auth changes
    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      const u = session?.user ?? null;
      setUser(u);
      setRole(u ? resolveRole(u) : null);
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, []);

  const login = useCallback(async (email: string, password: string, selectedRole: UserRole) => {
    // First authenticate with Supabase
    const { data, error } = await supabase.auth.signInWithPassword({
      email,
      password,
    });
    if (error) throw error;

    // Resolve the actual role
    const actualRole = resolveRole(data.user);

    // Validate selected role matches actual role
    if (selectedRole !== actualRole) {
      // Sign out since role doesn't match
      await supabase.auth.signOut();
      throw new Error(
        `Selected role "${selectedRole}" does not match your account role "${actualRole}".`
      );
    }

    // Role matches — state will be updated by onAuthStateChange listener
  }, []);

  const logout = useCallback(async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    setUser(null);
    setRole(null);
  }, []);

  const canAccess = useCallback(
    (path: string): boolean => {
      if (!role) return false;
      const allowed = ROLE_PERMISSIONS[role];
      if (!allowed) return false;
      return allowed.some((p) => path === p || path.startsWith(p + '/'));
    },
    [role]
  );

  return (
    <AuthContext.Provider value={{ user, role, loading, login, logout, canAccess }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};