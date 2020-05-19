function getCookie(name) {
  var value = "; " + document.cookie;
  var parts = value.split("; " + name + "=");
  if (parts.length == 2) return parts.pop().split(";").shift();
}

function addMessage(response) {
    const message = document.createElement("li");
    message.classList.add(response.status);
    message.innerText = response.message;
    document.querySelector('[data-messages]').prepend(message);
}

document.querySelectorAll('[data-choices]').forEach( (selector) => {
    new Choices(selector, {searchPlaceholderValue: 'Type to search'})
});
