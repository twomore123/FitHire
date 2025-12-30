/**
 * API Client for FitHire Backend
 * Handles authentication and API requests
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: any
  ) {
    super(message);
    this.name = "APIError";
  }
}

async function fetchWithAuth(
  endpoint: string,
  options: RequestInit = {},
  token?: string
): Promise<Response> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const url = `${API_BASE_URL}${endpoint}`;

  const response = await fetch(url, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorDetails;
    try {
      errorDetails = await response.json();
    } catch {
      errorDetails = await response.text();
    }

    throw new APIError(
      errorDetails?.detail || `API request failed: ${response.statusText}`,
      response.status,
      errorDetails
    );
  }

  return response;
}

// Coach API
export const coachAPI = {
  async create(data: any, token: string) {
    const response = await fetchWithAuth("/api/v1/coaches/", {
      method: "POST",
      body: JSON.stringify(data),
    }, token);
    return response.json();
  },

  async get(id: number, token: string) {
    const response = await fetchWithAuth(`/api/v1/coaches/${id}`, {}, token);
    return response.json();
  },

  async list(params: { page?: number; page_size?: number; location_id?: number; role_type?: string; status?: string }, token: string) {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.set("page", params.page.toString());
    if (params.page_size) queryParams.set("page_size", params.page_size.toString());
    if (params.location_id) queryParams.set("location_id", params.location_id.toString());
    if (params.role_type) queryParams.set("role_type", params.role_type);
    if (params.status) queryParams.set("status", params.status);

    const response = await fetchWithAuth(`/api/v1/coaches/?${queryParams}`, {}, token);
    return response.json();
  },

  async update(id: number, data: any, token: string) {
    const response = await fetchWithAuth(`/api/v1/coaches/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }, token);
    return response.json();
  },

  async getMatches(id: number, limit: number = 20, token: string) {
    const response = await fetchWithAuth(`/api/v1/coaches/${id}/matches?limit=${limit}`, {}, token);
    return response.json();
  },
};

// Job API
export const jobAPI = {
  async create(data: any, token: string) {
    const response = await fetchWithAuth("/api/v1/jobs/", {
      method: "POST",
      body: JSON.stringify(data),
    }, token);
    return response.json();
  },

  async get(id: number, token: string) {
    const response = await fetchWithAuth(`/api/v1/jobs/${id}`, {}, token);
    return response.json();
  },

  async list(params: { page?: number; page_size?: number; location_id?: number; role_type?: string; status?: string }, token: string) {
    const queryParams = new URLSearchParams();
    if (params.page) queryParams.set("page", params.page.toString());
    if (params.page_size) queryParams.set("page_size", params.page_size.toString());
    if (params.location_id) queryParams.set("location_id", params.location_id.toString());
    if (params.role_type) queryParams.set("role_type", params.role_type);
    if (params.status) queryParams.set("status", params.status);

    const response = await fetchWithAuth(`/api/v1/jobs/?${queryParams}`, {}, token);
    return response.json();
  },

  async update(id: number, data: any, token: string) {
    const response = await fetchWithAuth(`/api/v1/jobs/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }, token);
    return response.json();
  },

  async delete(id: number, token: string) {
    await fetchWithAuth(`/api/v1/jobs/${id}`, {
      method: "DELETE",
    }, token);
  },

  async getCandidates(id: number, limit: number = 20, token: string) {
    const response = await fetchWithAuth(`/api/v1/jobs/${id}/candidates?limit=${limit}`, {}, token);
    return response.json();
  },
};
