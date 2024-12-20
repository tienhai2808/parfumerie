const checkboxes = document.querySelectorAll('input[type="checkbox"]');
const btnNewAddress = document.querySelector('#newaddress');
const formNewAddress = document.querySelector('.form-newaddress');

if (checkboxes.length > 0) {
  checkboxes[0].checked = true; 
  if (btnNewAddress && formNewAddress) {
    if (btnNewAddress.checked) {
      formNewAddress.classList.remove('d-none');
    } else {
      formNewAddress.classList.add('d-none');
    }
  }
  checkboxes.forEach(checkbox => {
    checkbox.addEventListener('change', (e) => {
      if (e.target.checked) {
        checkboxes.forEach(cb => {
          if (cb !== e.target) {
            cb.checked = false;
          }
        });
        if (btnNewAddress && formNewAddress) {
          if (btnNewAddress.checked) {
            formNewAddress.classList.remove('d-none');
            formNewAddress.querySelectorAll('input').forEach((input) => {
              input.setAttribute('required', true)
            })
          } else {
            formNewAddress.classList.add('d-none');
            formNewAddress.querySelectorAll('input').forEach((input) => {
              input.removeAttribute('required')
            })
          }
        }
      }
      const isAnyChecked = Array.from(checkboxes).some(cb => cb.checked);
      if (!isAnyChecked) {
        e.target.checked = true;
      }
    });
  });
}

const selectMethod = document.querySelector('#payment-method')
const divBanking = document.querySelector('.banking')
if (selectMethod) {
  selectMethod.addEventListener('change', () => {
    if (selectMethod.value === 'bank') {
      if (divBanking.classList.contains('d-none')) {
        divBanking.classList.remove('d-none')
      }
    } else {
      if (!divBanking.classList.contains('d-none')) {
        divBanking.classList.add('d-none')
      }
    }
  })
}

const btnPayment = document.querySelector('.btn-payment')
if (btnPayment) {
  btnPayment.addEventListener('click', () => {
    
  })
}