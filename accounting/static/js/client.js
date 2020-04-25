function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function update(attr, value) {
    const formData = new FormData();
    const updateUrl = document.querySelector('[data-update-url]').getAttribute('data-update-url');

    formData.append('attr', attr);
    formData.append('value', value);

    return fetch(updateUrl, {
        method: 'PUT',
        headers: {
          'X-CSRFToken': getCookie('csrftoken')
         },
        body: formData,
    }).then(response => response.json())
    .catch(error => error.json())
}

window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-auto-update]').forEach((input)=>{
        input.addEventListener('change', async () => {
            const attr = input.getAttribute(name);
            const value = input.value;
            const response = await update(attr, value);
            const message = document.createElement("li");
            message.classList.add(response.status);
            message.innerText = response.message;
            document.querySelector('[data-messages]').prepend(message);
        });
    })
});
