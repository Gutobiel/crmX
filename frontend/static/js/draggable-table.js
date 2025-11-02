document.addEventListener('DOMContentLoaded', function () {
    const containers = document.querySelectorAll('.tabela-container')

    containers.forEach(container => {
        let isDown = false
        let startX
        let scrollLeft

        container.style.cursor = 'grab'

        container.addEventListener('mousedown', (e) => {
            isDown = true
            startX = e.pageX - container.offsetLeft
            scrollLeft = container.scrollLeft
            container.style.cursor = 'grabbing'
            e.preventDefault()
        })

        container.addEventListener('mouseleave', () => {
            isDown = false
            container.style.cursor = 'grab'
        })

        container.addEventListener('mouseup', () => {
            isDown = false
            container.style.cursor = 'grab'
        })

        container.addEventListener('mousemove', (e) => {
            if (!isDown) return
            e.preventDefault()
            const x = e.pageX - container.offsetLeft
            const walk = (x - startX) * 2
            container.scrollLeft = scrollLeft - walk
        })
    })
})
