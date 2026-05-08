<script setup>
import { RouterView } from 'vue-router'
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import { useDarkMode } from '@/composables/useDarkMode.js';

// Ensure dark class is applied on app load
useDarkMode();
</script>

<template>
  <AppHeader />
  <main>
    <RouterView />
  </main>
  <AppFooter />
</template>

<style>
body {
  padding-top: 75px;
}

/* ── Global dark mode overrides ── */
html.dark body {
  background-color: #111827;
  color: #f9fafb;
}

html.dark .detail-card,
html.dark .edit-card,
html.dark .match-card,
html.dark .profile-card,
html.dark .register-card,
html.dark .login-card,
html.dark .convo-item,
html.dark .thread-header,
html.dark .thread-input {
  background-color: #1f2937 !important;
  color: #f9fafb !important;
}

html.dark .conversations-panel {
  background-color: #111827 !important;
  border-color: #374151 !important;
}

html.dark .thread-messages {
  background-color: #111827 !important;
}

html.dark input,
html.dark select,
html.dark textarea {
  background-color: #374151 !important;
  color: #f9fafb !important;
  border-color: #4b5563 !important;
}

html.dark input::placeholder,
html.dark textarea::placeholder {
  color: #9ca3af !important;
}

html.dark .bio,
html.dark .location,
html.dark .username,
html.dark .tagline,
html.dark .last-msg,
html.dark .convo-name {
  color: #d1d5db !important;
}

html.dark .no-data { color: #6b7280 !important; }

html.dark .btn-cancel {
  background: #374151 !important;
  color: #d1d5db !important;
  border-color: #4b5563 !important;
}

html.dark .filter-input,
html.dark .filter-select {
  background-color: #374151 !important;
  color: #f9fafb !important;
  border-color: #4b5563 !important;
}

html.dark .theirs .bubble {
  background: #374151 !important;
  color: #f9fafb !important;
}

html.dark h1, html.dark h2, html.dark h3 {
  color: #a5b4fc !important;
}
</style>
