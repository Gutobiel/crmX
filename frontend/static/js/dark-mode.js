const html = document.documentElement
const toggle = document.getElementById('themeToggle')

toggle.addEventListener('click', (e) => {
  e.preventDefault() // <--- ESSENCIAL
  html.dataset.bsTheme =
    html.dataset.bsTheme === 'light' ? 'dark' : 'light'

  localStorage.setItem('theme', html.dataset.bsTheme)
})

// ao carregar recuperar do storage
const saved = localStorage.getItem('theme')
if (saved) html.dataset.bsTheme = saved
