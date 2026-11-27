import type { LoginPayload, RegisterPayload } from "./types";

export function validateRegister(p: RegisterPayload): string | null {
  if (p.full_name.trim().length < 4) return "Full name must be at least 4 characters.";
  if (!p.shop_name.trim()) return "Shop name is required.";
  if (!/^\S+@\S+\.\S+$/.test(p.email.trim())) return "Please enter a valid email.";
  if (p.password.length < 8) return "Password must be at least 8 characters.";
  if (p.password !== p.confirm_password) return "Passwords do not match.";
  return null;
}

export function validateLogin(p: LoginPayload): string | null {
  if (!/^\S+@\S+\.\S+$/.test(p.email.trim())) return "Please enter a valid email.";
  if (p.password.length < 8) return "Password must be at least 8 characters.";
  return null;
}