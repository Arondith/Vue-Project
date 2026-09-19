<script setup lang="ts">
import type { JobApplication } from '../types'

defineProps<{
  application: JobApplication
}>()

const emit = defineEmits<{
  edit: [application: JobApplication]
  remove: [id: number]
}>()

function formatDate(date: string) {
  return new Intl.DateTimeFormat(undefined, {
    month: 'short',
    day: 'numeric',
    year: 'numeric',
  }).format(new Date(`${date}T00:00:00`))
}
</script>

<template>
  <article class="application-card">
    <div class="card-top">
      <div>
        <div class="company-line">
          <h3>{{ application.role }}</h3>
          <span class="status-pill" :data-status="application.status">
            {{ application.status }}
          </span>
        </div>
        <p class="company">{{ application.company }}</p>
      </div>
      <div class="card-actions">
        <button class="icon-button" type="button" @click="emit('edit', application)">
          Edit
        </button>
        <button class="icon-button danger" type="button" @click="emit('remove', application.id)">
          Delete
        </button>
      </div>
    </div>

    <div class="meta-row">
      <span>{{ application.work_setup }}</span>
      <span v-if="application.location">{{ application.location }}</span>
      <span v-if="application.salary">{{ application.salary }}</span>
      <span>Applied {{ formatDate(application.applied_at) }}</span>
    </div>

    <p v-if="application.notes" class="notes">{{ application.notes }}</p>

    <a
      v-if="application.job_url"
      class="job-link"
      :href="application.job_url"
      target="_blank"
      rel="noreferrer"
    >
      Open job posting ↗
    </a>
  </article>
</template>
