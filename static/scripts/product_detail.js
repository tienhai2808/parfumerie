const btnBuyNow = document.querySelector('#buy-now')
const btnAddCart = document.querySelector('#add-cart')
const formAction = document.querySelector('[form-action]')

btnBuyNow.addEventListener('click', () => {
  const checkUser = btnBuyNow.getAttribute('user')
  if (!checkUser) {
    window.location.href = '/account/login/'
  } else {
    const quantityProduct = document.querySelector('.quantity')
    formAction.querySelector('input[name="quantity"]').value = quantityProduct.value
    formAction.querySelector('input[name="action"]').value = 'buy-now'
    formAction.submit()
  }
})

btnAddCart.addEventListener('click', () => {
  const checkUser = btnAddCart.getAttribute('user')
  if (!checkUser) {
    window.location.href = '/account/login/'
  } else {
    const quantityProduct = document.querySelector('.quantity')
    formAction.querySelector('input[name="quantity"]').value = quantityProduct.value
    formAction.querySelector('input[name="action"]').value = 'add-cart'
    formAction.submit()
  }
})

const imgMain = document.querySelector('#img-main')
const imgSubs = document.querySelectorAll('#img-sub')
if (imgSubs.length > 0) {
  imgSubs.forEach((img) => {
    img.addEventListener('click', () => {
      imgMain.setAttribute('src', img.getAttribute('src'))
    })
  })
}
