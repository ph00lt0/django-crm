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

const clientChoice = new Choices('[data-choices-client]', {searchPlaceholderValue: 'Type to search'});
const firstItemChoice = new Choices('[data-choices-items]', {searchPlaceholderValue: 'Type to search'});
