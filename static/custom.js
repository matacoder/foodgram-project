counterFav = document.querySelector("#counter_fav")

const starElements = document.querySelectorAll('[name="favorites"]')

for (let starElement of starElements) {
    starElement.addEventListener('click', event => {
        if (starElement.dataset.out) {
            console.dir(starElement.dataset.out)
            ++counterFav.innerHTML
        } else {
            console.dir(starElement.dataset.out)
            --counterFav.innerHTML
        }
    })
}

// const subscribeElements