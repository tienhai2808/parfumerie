const inputQuantities = document.querySelectorAll('.quantity');
const divUpdate = document.querySelector('.div-update-cart');

if (inputQuantities.length > 0) {
  inputQuantities.forEach((input) => {
    input.addEventListener('change', () => {
      let isChanged = false;
      inputQuantities.forEach((input) => {
        if (input.getAttribute('old') != input.value) {
          isChanged = true;
        }
      });
      if (isChanged) {
        divUpdate.classList.remove('d-none');
      } else {
        divUpdate.classList.add('d-none');
      }
    });
  });
} 

const btnUpdate = document.querySelector('.btn-update')
const formData = document.querySelector('[form-data]')
if (btnUpdate) {
  btnUpdate.addEventListener('click', () => {
    const data = []
    inputQuantities.forEach((input) => {
      data.push({
        product_id: input.getAttribute('data-id'),
        quantity: input.value
      })
    })
    formData.querySelector('[hidden]').value = JSON.stringify(data);
    formData.submit()
  })
}

const btnRemoves = document.querySelectorAll('.btn-remove')
const formDelete = document.querySelector('[form-delete]')
if (btnRemoves.length > 0) {
  btnRemoves.forEach((btn) => {
    btn.addEventListener('click', () => {
      formDelete.querySelector('[hidden]').value = btn.getAttribute('product-id')
      formDelete.submit()
    })
  })
}
