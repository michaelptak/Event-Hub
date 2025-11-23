// Dark mode toggle functionality

// Check for saved theme preference or default to light mode
const currentTheme = localStorage.getItem('theme') || 'light';

// Apply the theme on page load
if (currentTheme === 'dark') {
  document.documentElement.setAttribute('data-theme', 'dark');
  document.getElementById('darkModeSwitch').checked = true;
}

// Listen for toggle switch changes
$('#darkModeSwitch').change(function() {
  if (this.checked) {
    // Enable dark mode
    document.documentElement.setAttribute('data-theme', 'dark');
    localStorage.setItem('theme', 'dark');
  } else {
    // Enable light mode
    document.documentElement.removeAttribute('data-theme');
    localStorage.setItem('theme', 'light');
  }
});
