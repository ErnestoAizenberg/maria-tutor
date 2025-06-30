// main/static/src/tailwind.config.js
module.exports = {
  content: [
    // Пути ОТНОСИТЕЛЬНО этого конфига!
    "../../../templates/**/*.html",  // Шаблоны Django
    "../../../**/templates/**/*.html"  // Если шаблоны в других приложениях
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
