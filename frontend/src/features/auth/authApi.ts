import type {
  LoginPayload,
  LoginResponse,
  RegisterPayload,
  RegisterResponse,
  SessionResponse,
} from "./types";

const API_URL = "/api/v1";
const TOKEN_KEY = "access_token";

export const getToken = () => localStorage.getItem(TOKEN_KEY);
export const clearToken = () => localStorage.removeItem(TOKEN_KEY);

export async function register(payload: RegisterPayload): Promise<RegisterResponse> {
  const res = await fetch(`${API_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => null);
    const detail = err?.detail;
    
    if (typeof detail === "string") throw new Error(detail);
    if (Array.isArray(detail)) throw new Error(detail[0]?.msg ?? "Invalid input");
    throw new Error("Something went wrong");
  }

  return res.json();
}

export async function login(payload: LoginPayload): Promise<LoginResponse> {
  const res = await fetch(`${API_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  if (!res.ok) {
    const err = await res.json().catch(() => null);
    const detail = err?.detail;
    if (typeof detail === "string") throw new Error(detail);
    if (Array.isArray(detail)) throw new Error(detail[0]?.msg ?? "Invalid input");
    throw new Error("Something went wrong");
  }

  const data: LoginResponse = await res.json();
  localStorage.setItem(TOKEN_KEY, data.access_token);
  return data;
}

export async function getSession(): Promise<SessionResponse> {
  const res = await fetch(`${API_URL}/auth/session`, {
    headers: { Authorization: `Bearer ${getToken()}` },
  });

  if (!res.ok) {
    const err = await res.json().catch(() => null);
    const detail = err?.detail;
    throw new Error(typeof detail === "string" ? detail : "Something went wrong");
  }

  return res.json();
}

export async function logout(): Promise<void> {
  try {
    await fetch(`${API_URL}/auth/logout`, {
      method: "POST",
      headers: { Authorization: `Bearer ${getToken()}` },
    });
  } finally {
    clearToken();
  }
}