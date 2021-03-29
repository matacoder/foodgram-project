counterFav = document.querySelector("#counter_fav")
const starElements = document.querySelectorAll('[name="favorites"]')

counterFol = document.querySelector("#counter_fol")
const subscribeElements = document.querySelectorAll('[name="subscribe"]')

const setListeners = (elements, counter) => {
    for (let element of elements) {
        element.addEventListener('click', event => {
            let delta = element.dataset.out ? 1 : -1
            counter.innerHTML = parseInt(counter.innerHTML) + delta
        })
    }
}
setListeners(subscribeElements, counterFol)
setListeners(starElements, counterFav)