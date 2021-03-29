// Looking for actual counter number on page
counterFav = document.querySelector("#counter_fav")
// Get array of buttons 'Add to favorites' (star icon)
const starElements = document.querySelectorAll('[name="favorites"]')

counterFol = document.querySelector("#counter_fol")
const subscribeElements = document.querySelectorAll('[name="subscribe"]')

// Function to add 'on click' action (listener) on every element of array
const setListeners = (elements, counter) => {
    for (let element of elements) {
        element.addEventListener('click', event => {
            // check if attribute data-out === 'true' and act accordingly
            let delta = element.dataset.out ? 1 : -1
            counter.innerHTML = parseInt(counter.innerHTML) + delta
        })
    }
}
setListeners(subscribeElements, counterFol)
setListeners(starElements, counterFav)