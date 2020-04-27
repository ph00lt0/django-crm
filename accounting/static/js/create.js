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
                formData.append(field.getAttribute('name'), field.value);
            });
            const items = {};
            // for all form rows with items
            form.querySelectorAll('[data-item-row]').forEach((row) => {
                // for all selected items in item row
                row.querySelectorAll('[data-item]').forEach((item) => {
                    const pk = item.getAttribute('data-value');
                    items[pk] = {};
                    row.querySelectorAll('[data-item-row-field]').forEach( (field) =>  {
                        items[pk][field.getAttribute('name')] = field.value;
                    });
                });
            });
            if (Object.keys(items).length > 0) formData.append('items', JSON.stringify(items));
            addMessage(await post(formData, url));
        });
    });
}

function watchItems(form) {
    form.querySelector('[data-add-item-row]').addEventListener('click', () => {
        const clone = form.querySelector('[data-item-template]').content.cloneNode(true);
        new Choices(clone.querySelector('[data-choices-items]'), {
            addItems: true,
            searchPlaceholderValue: 'Type to search',
        });
        form.querySelector('[data-items]').appendChild(clone);
    });
}

window.addEventListener('DOMContentLoaded', () => {
    create();
});
