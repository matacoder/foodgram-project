counterFav = document.querySelector("#counter_fav")

const starElements = document.querySelectorAll('[name="favorites"]')


for (let starElement of starElements) {
    starElement.addEventListener('click', event => {
        if (starElement.dataset.out) {
            ++counterFav.innerHTML
        } else {
            --counterFav.innerHTML
        }
    })
}

counterFol = document.querySelector("#counter_fol")
const subscribeElements = document.querySelectorAll('[name="subscribe"]')


for (let subscribeElement of subscribeElements) {
    subscribeElement.addEventListener('click', event => {
        if (subscribeElement.dataset.out) {
            ++counterFol.innerHTML
        } else {
            --counterFol.innerHTML
        }
    })
}