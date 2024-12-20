document.querySelectorAll('label').forEach((label) => {
  if (label.textContent.trim() === 'Password-based authentication:') {
    label.remove()
  }
})

const pwHt = document.querySelector('#id_usable_password_helptext')
if (pwHt) {
  pwHt.remove()
}

const uPw = document.querySelector('#id_usable_password')
if (uPw) {
  uPw.remove()
}

const btnAdd = document.querySelector('.btn-add')
const divAdd = document.querySelector('.add-address')
const btnCancel = document.querySelector('[btn-x]')
if (btnAdd) {
  btnAdd.addEventListener('click', () => {
    if (divAdd.classList.contains('d-none')) {
      divAdd.classList.remove('d-none')
    }
  })
}
if (btnCancel) {
  btnCancel.addEventListener('click', () => {
    if (!divAdd.classList.contains('d-none')) {
      divAdd.classList.add('d-none')
    }
  })
} 

const btnUpdate = document.querySelector('.btn-update')
const divInfo = document.querySelector('.add-info')
const btnRemove = document.querySelector('[btn-remove]')
if (btnUpdate) {
  btnUpdate.addEventListener('click', () => {
    if (divInfo.classList.contains('d-none')) {
      divInfo.classList.remove('d-none')
    }
  })
}
if (btnRemove) {
  btnRemove.addEventListener('click', () => {
    if (!divInfo.classList.contains('d-none')) {
      divInfo.classList.add('d-none')
    }
  })
}

const btnDeletes = document.querySelectorAll('.btn-delete')
const formDelete = document.querySelector('[form-delete]')
if (btnDeletes.length > 0) {
  btnDeletes.forEach((btn) => {
    btn.addEventListener('click', () => {
      const confirmDelete = confirm('Xác nhận xóa địa chỉ này?')
      if (confirmDelete) {
        formDelete.querySelector('[hidden]').value = btn.getAttribute('id')
        formDelete.submit()
      }
    })
  })
}