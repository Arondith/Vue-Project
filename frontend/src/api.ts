import type {
  ApplicationInput,
  ApplicationStats,
  JobApplication,
} from './types'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options?.headers,
    },
    ...options,
  })

  if (!response.ok) {
    let message = 'Request failed'
    try {
      const payload = (await response.json()) as { detail?: string; error?: string }
      message = payload.detail || payload.error || message
    } catch {
      // Keep the generic error when the response is not JSON.
    }
    throw new Error(message)
  }

  if (response.status === 204) {
    return undefined as T
  }

  return response.json() as Promise<T>
}

export const api = {
  listApplications(): Promise<JobApplication[]> {
    return request<JobApplication[]>('/api/applications')
  },

  createApplication(payload: ApplicationInput): Promise<JobApplication> {
    return request<JobApplication>('/api/applications', {
      method: 'POST',
      body: JSON.stringify(payload),
    })
  },

  updateApplication(
    id: number,
    payload: ApplicationInput,
  ): Promise<JobApplication> {
    return request<JobApplication>(`/api/applications/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    })
  },

  deleteApplication(id: number): Promise<void> {
    return request<void>(`/api/applications/${id}`, {
      method: 'DELETE',
    })
  },

  getStats(): Promise<ApplicationStats> {
    return request<ApplicationStats>('/api/stats')
  },
}
