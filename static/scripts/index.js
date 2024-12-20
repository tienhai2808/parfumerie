const divMessages = document.querySelectorAll('.message')
if (divMessages.length > 0) {
  divMessages.forEach((mess) => {
    const closeMess = mess.querySelector('.close-mess')
    closeMess.addEventListener('click', () => {
      mess.remove()
    })
  })
}