const formOrderBy = document.querySelector('#form-orderby')
const orderBy = document.querySelector('select')
if (orderBy) {
  orderBy.addEventListener('change', () => {
    formOrderBy.submit()
  })
}