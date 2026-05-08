import { ref } from 'vue'

// Module-level ref so all components share the same state
const isDark = ref(localStorage.getItem('darkMode') === 'true')

function applyDark(value) {
  if (value) {
    document.documentElement.classList.add('dark')
  } else {
    document.documentElement.classList.remove('dark')
  }
  localStorage.setItem('darkMode', value)
}

// Apply on first import
applyDark(isDark.value)

export function useDarkMode() {
  function toggle() {
    isDark.value = !isDark.value
    applyDark(isDark.value)
  }

  return { isDark, toggle }
}
