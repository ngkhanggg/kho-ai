export type RegisterPayload = {
  full_name: string;
  email: string;
  shop_name: string;
  password: string;
  confirm_password: string;
};

export type RegisterResponse = {
  user_id: string;
  shop_id: string;
  full_name: string;
  email: string;
  created_at: string;
  message: string;
};

export type LoginPayload = {
  email: string;
  password: string;
};

export type LoginResponse = {
  access_token: string;
  token_type: string;
  expires_in: number;
  message: string;
};

export type SessionResponse = {
  user_id: string;
  shop_id: string;
  email: string;
  expires_at: string;
};