<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from './api'
import ApplicationCard from './components/ApplicationCard.vue'
import ApplicationForm from './components/ApplicationForm.vue'
import type {
  ApplicationInput,
  ApplicationStats,
  ApplicationStatus,
  JobApplication,
} from './types'

const applications = ref<JobApplication[]>([])
const stats = ref<ApplicationStats>({
  total: 0,
  applied: 0,
  interview: 0,
  assessment: 0,
  offer: 0,
  rejected: 0,
})

const loading = ref(true)
const saving = ref(false)
const error = ref('')
const search = ref('')
const statusFilter = ref<ApplicationStatus | 'All'>('All')
const showForm = ref(false)
const editing = ref<JobApplication | null>(null)

const statuses: Array<ApplicationStatus | 'All'> = [
  'All',
  'Applied',
  'Interview',
  'Assessment',
  'Offer',
  'Rejected',
]

const visibleApplications = computed(() => {
  const query = search.value.trim().toLowerCase()

  return applications.value.filter((application) => {
    const matchesStatus =
      statusFilter.value === 'All' || application.status === statusFilter.value
    const matchesSearch =
      !query ||
      application.company.toLowerCase().includes(query) ||
      application.role.toLowerCase().includes(query)

    return matchesStatus && matchesSearch
  })
})

async function loadData() {
  loading.value = true
  error.value = ''

  try {
    const [applicationData, statsData] = await Promise.all([
      api.listApplications(),
      api.getStats(),
    ])
    applications.value = applicationData
    stats.value = statsData
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : 'Unable to load ApplyFlow.'
  } finally {
    loading.value = false
  }
}

function startCreate() {
  editing.value = null
  showForm.value = true
}

function startEdit(application: JobApplication) {
  editing.value = application
  showForm.value = true
}

function closeForm() {
  showForm.value = false
  editing.value = null
}

async function saveApplication(payload: ApplicationInput) {
  saving.value = true
  error.value = ''

  try {
    if (editing.value) {
      await api.updateApplication(editing.value.id, payload)
    } else {
      await api.createApplication(payload)
    }

    closeForm()
    await loadData()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : 'Unable to save application.'
  } finally {
    saving.value = false
  }
}

async function removeApplication(id: number) {
  if (!window.confirm('Delete this application?')) return

  error.value = ''
  try {
    await api.deleteApplication(id)
    await loadData()
  } catch (reason) {
    error.value = reason instanceof Error ? reason.message : 'Unable to delete application.'
  }
}

onMounted(loadData)
</script>

<template>
  <main class="app-shell">
    <header class="topbar">
      <a class="brand" href="#">
        <span class="brand-mark">A</span>
        <span>ApplyFlow</span>
      </a>
      <button class="primary-button" type="button" @click="startCreate">
        + Add application
      </button>
    </header>

    <section class="hero">
      <p class="eyebrow">JOB SEARCH COMMAND CENTER</p>
      <h1>Keep every opportunity moving.</h1>
      <p>
        Track applications, interviews, assessments, and offers without losing your next step.
      </p>
    </section>

    <section class="stats-grid" aria-label="Application statistics">
      <article>
        <span>Total</span>
        <strong>{{ stats.total }}</strong>
      </article>
      <article>
        <span>Applied</span>
        <strong>{{ stats.applied }}</strong>
      </article>
      <article>
        <span>Interviews</span>
        <strong>{{ stats.interview }}</strong>
      </article>
      <article>
        <span>Assessments</span>
        <strong>{{ stats.assessment }}</strong>
      </article>
      <article>
        <span>Offers</span>
        <strong>{{ stats.offer }}</strong>
      </article>
    </section>

    <section class="workspace">
      <div class="workspace-heading">
        <div>
          <p class="eyebrow">PIPELINE</p>
          <h2>Your applications</h2>
        </div>
        <span>{{ visibleApplications.length }} shown</span>
      </div>

      <div class="toolbar">
        <input
          v-model="search"
          class="search-input"
          type="search"
          placeholder="Search company or role..."
        />
        <div class="filters" aria-label="Filter by status">
          <button
            v-for="status in statuses"
            :key="status"
            type="button"
            :class="{ active: statusFilter === status }"
            @click="statusFilter = status"
          >
            {{ status }}
          </button>
        </div>
      </div>

      <p v-if="error" class="error-banner">{{ error }}</p>

      <div v-if="loading" class="empty-state">
        <strong>Loading applications…</strong>
      </div>

      <div v-else-if="visibleApplications.length" class="applications-list">
        <ApplicationCard
          v-for="application in visibleApplications"
          :key="application.id"
          :application="application"
          @edit="startEdit"
          @remove="removeApplication"
        />
      </div>

      <div v-else class="empty-state">
        <strong>No applications here yet.</strong>
        <p>Add your first opportunity or change the current filters.</p>
        <button class="primary-button" type="button" @click="startCreate">
          Track an application
        </button>
      </div>
    </section>

    <div v-if="showForm" class="modal-backdrop" @click.self="closeForm">
      <div class="modal">
        <div v-if="saving" class="saving-overlay">Saving…</div>
        <ApplicationForm
          :application="editing"
          @save="saveApplication"
          @cancel="closeForm"
        />
      </div>
    </div>
  </main>
</template>
