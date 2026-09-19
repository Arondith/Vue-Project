export type ApplicationStatus =
  | 'Applied'
  | 'Interview'
  | 'Assessment'
  | 'Offer'
  | 'Rejected'

export type WorkSetup = 'Remote' | 'Hybrid' | 'On-site'

export interface ApplicationInput {
  company: string
  role: string
  location: string
  work_setup: WorkSetup
  status: ApplicationStatus
  salary: string
  job_url: string | null
  notes: string
  applied_at: string
}

export interface JobApplication extends ApplicationInput {
  id: number
  created_at: string
  updated_at: string
}

export interface ApplicationStats {
  total: number
  applied: number
  interview: number
  assessment: number
  offer: number
  rejected: number
}
