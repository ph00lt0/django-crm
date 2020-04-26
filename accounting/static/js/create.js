function post(formData, url) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData,
    }).then(response => response.json()).catch(error => error.json())
}

function create() {
    document.querySelectorAll('[data-create-form]').forEach((form) => {
        watchItems(form);
        const url = form.querySelector('[data-url]').getAttribute('data-url');
        const formData = new FormData();
        form.querySelector('[data-submit]').addEventListener('click', async () => {
            form.querySelectorAll('[data-field]').forEach((field) => {
                formData.append(field.getAttribute('name'), field.value)
            });
            const items = {};
            form.querySelectorAll('[data-item]').forEach((item) => {
                const pk = item.querySelector('[data-item-pk]').value;
                const amount = item.querySelector('[data-item-amount]').value;
                const price = item.querySelector('[data-item-price]').value;
                items[pk] = {
                    "amount": amount,
                    "price": price,
                }
            });
            if (Object.keys(items).length) formData.append('items', JSON.stringify(items));
            addMessage(await post(formData, url));
        });
    });
}

function watchItems(form) {
    form.querySelector('[data-add-item]').addEventListener('click', () => {
        const clone = form.querySelector('[data-item-template]').content.cloneNode(true);
        form.querySelector('[data-items]').appendChild(clone);
    });
}

window.addEventListener('DOMContentLoaded', () => {
    create();
});
