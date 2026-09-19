<script setup lang="ts">
import { reactive, ref, watch } from 'vue'
import type {
  ApplicationInput,
  ApplicationStatus,
  JobApplication,
  WorkSetup,
} from '../types'

const props = defineProps<{
  application?: JobApplication | null
}>()

const emit = defineEmits<{
  save: [payload: ApplicationInput]
  cancel: []
}>()

const statuses: ApplicationStatus[] = [
  'Applied',
  'Interview',
  'Assessment',
  'Offer',
  'Rejected',
]

const workSetups: WorkSetup[] = ['Remote', 'Hybrid', 'On-site']

type FormState = Omit<ApplicationInput, 'job_url'> & {
  job_url: string
}

const today = () => new Date().toISOString().slice(0, 10)

const blankForm = (): FormState => ({
  company: '',
  role: '',
  location: '',
  work_setup: 'Remote',
  status: 'Applied',
  salary: '',
  job_url: '',
  notes: '',
  applied_at: today(),
})

const form = reactive<FormState>(blankForm())
const submitted = ref(false)

watch(
  () => props.application,
  (application) => {
    submitted.value = false
    Object.assign(
      form,
      application
        ? {
            company: application.company,
            role: application.role,
            location: application.location,
            work_setup: application.work_setup,
            status: application.status,
            salary: application.salary,
            job_url: application.job_url ?? '',
            notes: application.notes,
            applied_at: application.applied_at,
          }
        : blankForm(),
    )
  },
  { immediate: true },
)

function submit() {
  submitted.value = true
  if (!form.company.trim() || !form.role.trim()) return

  emit('save', {
    ...form,
    company: form.company.trim(),
    role: form.role.trim(),
    location: form.location.trim(),
    salary: form.salary.trim(),
    job_url: form.job_url.trim() || null,
    notes: form.notes.trim(),
  })
}
</script>

<template>
  <form class="application-form" @submit.prevent="submit">
    <div class="form-heading">
      <div>
        <p class="eyebrow">{{ application ? 'EDIT APPLICATION' : 'NEW APPLICATION' }}</p>
        <h2>{{ application ? 'Update opportunity' : 'Track an opportunity' }}</h2>
      </div>
      <button type="button" class="ghost-button" @click="emit('cancel')">Close</button>
    </div>

    <div class="form-grid">
      <label>
        <span>Company *</span>
        <input v-model="form.company" placeholder="Acme Labs" />
        <small v-if="submitted && !form.company.trim()">Company is required.</small>
      </label>

      <label>
        <span>Role *</span>
        <input v-model="form.role" placeholder="Frontend Developer" />
        <small v-if="submitted && !form.role.trim()">Role is required.</small>
      </label>

      <label>
        <span>Status</span>
        <select v-model="form.status">
          <option v-for="status in statuses" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </label>

      <label>
        <span>Work setup</span>
        <select v-model="form.work_setup">
          <option v-for="setup in workSetups" :key="setup" :value="setup">
            {{ setup }}
          </option>
        </select>
      </label>

      <label>
        <span>Location</span>
        <input v-model="form.location" placeholder="Remote / Seattle, WA" />
      </label>

      <label>
        <span>Salary</span>
        <input v-model="form.salary" placeholder="$1,500/month or ₱35,000" />
      </label>

      <label>
        <span>Application date</span>
        <input v-model="form.applied_at" type="date" />
      </label>

      <label>
        <span>Job URL</span>
        <input v-model="form.job_url" type="url" placeholder="https://..." />
      </label>

      <label class="full-width">
        <span>Notes</span>
        <textarea
          v-model="form.notes"
          rows="4"
          placeholder="Interview schedule, recruiter notes, next steps..."
        />
      </label>
    </div>

    <div class="form-actions">
      <button type="button" class="ghost-button" @click="emit('cancel')">Cancel</button>
      <button type="submit" class="primary-button">
        {{ application ? 'Save changes' : 'Add application' }}
      </button>
    </div>
  </form>
</template>
