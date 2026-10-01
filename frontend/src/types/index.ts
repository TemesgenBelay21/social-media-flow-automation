export type User = {
  id: number;
  name: string;
  email: string;
  is_active: boolean;
  timezone: string;
  created_at: string;
};

export type AuthState = {
  user: User | null;
  token: string | null;
};
