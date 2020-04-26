function create(formData, updateUrl) {
    return fetch(updateUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData,
    }).then(response => response.json())
        .catch(error => error.json())
}

window.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('[data-create-form]').forEach((form) => {
        const updateUrl = form.querySelector('[data-url]').getAttribute('data-url');
        const formData = new FormData();
        form.querySelector('[data-submit]').addEventListener('click', async () => {
            form.querySelectorAll('[data-field]').forEach((field) => {
                console.log(field.getAttribute('name'));
                formData.append(field.getAttribute('name'), field.value)
            });
            addMessage(await create(formData, updateUrl));
        });
    });
});
