const startButton = document.getElementById('start-button')
const url = window.location.href

startButton.addEventListener('click', () => {
    const testId = startButton.dataset.testId
    // Относительный переход — не хардкодим полный URL
    window.location.pathname = window.location.pathname.replace(/lesson\/\d+/, `test/${testId}`)
})