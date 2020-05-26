function post(formData, url) {
    return fetch(url, {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json'},
        body: formData,
    }).then(response => response.json()).catch(error => error.json())
}

function update(attr, value, url) {
    const formData = new FormData();

    formData.append(attr, value);

    return fetch(url, {
        method: 'PUT',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: formData,
    }).then(response => response.json())
        .catch(error => error.json())
}

function deleteRow(url) {
    fetch(url, {
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
    }).then(response => response.json())
        .catch(error => error.json())
}

function get(url) {
    return fetch(url, {
        method: 'GET',
    }).then(response => response.json()).catch(error => error.json())
}

function initCreateForm() {
    document.querySelectorAll('[data-create-form]').forEach((form) => {
        watchItems(form);
        const url = form.querySelector('[data-url]').getAttribute('data-url');
        const formData = new FormData();
        const dataForm = {};
        form.querySelector('[data-submit]').addEventListener('click', async () => {
            form.querySelectorAll('[data-field]').forEach((field) => {
                formData.append(field.getAttribute('name'), field.value);
                dataForm[field.getAttribute('name')] = field.value;
            });
            const details = {};
            const items = [];
            // for all form rows with items
            form.querySelectorAll('[data-sub-row]').forEach((row) => {
                // for all selected items in item row
                row.querySelectorAll('[data-item]').forEach((item) => {
                    const itemsItem = {};
                    itemsItem['item'] = item.getAttribute('data-value');
                    // fields connected to data-item
                    row.querySelectorAll('[data-sub-item-field]').forEach((field) => {
                        itemsItem[field.getAttribute('name')] = field.value;
                    });
                    items.push(itemsItem)
                });
                // add sub fields not connected to data-item
                row.querySelectorAll('[data-sub-field]').forEach((field) => {
                    details[field.getAttribute('name')] = field.value;
                });
            });
            if (Object.keys(items).length > 0) dataForm['items'] = items;
            if (Object.keys(details).length > 0) dataForm['details'] = details;
            addMessage(await post(JSON.stringify(dataForm), url));
        });
    });
}

// update forms are to add items to existing invoices and bills
function initUpdateForm() {
    document.querySelectorAll('[data-update-form]').forEach((form) => {
        watchItems(form);
        const base = form.querySelector('[data-url]').getAttribute('data-url');
        const formData = new FormData();
        const dataForm = {};
        form.querySelector('[data-submit]').addEventListener('click', async () => {
            const url = base + '/' + form.querySelector('[data-item-pk]').value;
            form.querySelectorAll('[data-field]').forEach((field) => {
                formData.append(field.getAttribute('name'), field.value);
                dataForm[field.getAttribute('name')] = field.value;
            });
            addMessage(await post(JSON.stringify(dataForm), url));
        });
    });
}

function watchItems(form) {
    if (!form.querySelector('[data-add-sub-row]')) return;
    form.querySelector('[data-add-sub-row]').addEventListener('click', () => {
        const clone = form.querySelector('[data-sub-template]').content.cloneNode(true);
        const choicesElm = clone.querySelector('[data-choices]');
        initChoices(choicesElm);
        form.querySelector('[data-subs]').appendChild(clone);
    });
}

function initChoices(choicesElm) {
    const choices = new Choices(choicesElm, {
        addItems: true,
        searchPlaceholderValue: 'Type to search',
    });
    if (!choicesElm.hasAttribute('data-url')) return;
    choices.setChoices(async () => {
        const response = await get(choicesElm.getAttribute('data-url'));
        const items = [];
        response.forEach( (item)=> {
            if (item['name'] && item['uuid'])  items.push({"value": item['uuid'], "label": item['name']});
            if (item['name'] && item['pk'])
                items.push({"value": item['pk'], "selected": item['selected'], "label": item['name']});
            if (item['description']) items.push({"value": item['uuid'], "label": item['description']});
        });
        return items;
    });
}

function constructTableData(response) {
    let UUIDlocation;
    let columnCount = 0;

    function countColumn(column) {
        // check if UUID location is not a num since 0 equals false
        columnCount++;
        if (column === 'uuid' && isNaN(UUIDlocation)) UUIDlocation = columnCount;
    }

    const data = {"data": []};
    if (!response.length) {
        response = [response]
    }

    for (let i = 0; i < response.length; i++) {
        data.data[i] = ['a'];
        data.headings = [''];
        // counting for position of column for uuid field. Which is used in the render of init tables
        for (let key in response[i]) {
            let value = response[i][key];
            // if object with details go though it
            if (typeof value === 'object') {
                for (let oKey in value) {
                    data.headings.push(oKey);
                    data.data[i].push(value[oKey]);
                    countColumn(oKey);
                }
            } else {
                data.headings.push(key);
                data.data[i].push(value);
                countColumn(key)
            }
        }
    }
    return [data, UUIDlocation];
}

function initTables() {
    document.querySelectorAll('[data-table]').forEach(async (elm) => {
        if (!elm.hasAttribute('data-url')) {
            return addMessage({'status': 'ERROR', 'message': 'No data url'})
        }
        const response = await get(elm.getAttribute('data-url'));
        if (response.status === "ERROR") return addMessage(response);

        let dataAndUUIDlocation;
        // if response has item rows
        if (response.items) {
            dataAndUUIDlocation = constructTableData(response.items);
        } else {
            dataAndUUIDlocation = constructTableData(response);
        }
        const data = dataAndUUIDlocation[0]; // position in return
        const UUIDlocation = dataAndUUIDlocation[1]; // position in return

        const columns = Array.apply(null, {length: data.headings.length}).map(Number.call, Number);

        const config = {
            data,
            filters: {},
            columns: [
                {
                    select: columns, render: function (data, cell, row) {
                        cell.setAttribute('contenteditable', true);
                        cell.setAttribute('clickable', true);
                        return data
                    }
                },
                {
                    select: 0, render: function (data, cell, row) {
                        cell.setAttribute('contenteditable', false);
                        cell.removeAttribute('clickable');
                        return "<button data-delete>🗑</button>"
                    }
                },
                {
                    // add uuid to row as attribute for linking to other pages
                    select: UUIDlocation, hidden: true, render: function (data, cell, row) {
                        row.setAttribute('data-row', data);
                    }
                }
            ]
        };
        let dataTable = new simpleDatatables.DataTable(elm, config);
        watchTable(dataTable);
    });
}

function watchTable(dataTable) {
    dataTable.on('datatable.init', () => {
        makeRowLink(dataTable.table);
        addTableActions(dataTable.table);
        watchCells(dataTable.table);
    });
    dataTable.on('datatable.update', () => {
        makeRowLink(dataTable.table);
        addTableActions(dataTable.table);
        watchCells(dataTable.table);
    });
    dataTable.on('datatable.sort', () => {
        makeRowLink(dataTable.table);
        addTableActions(dataTable.table);
        watchCells(dataTable.table);
    });
    dataTable.on('datatable.page', () => {
        makeRowLink(dataTable.table);
        addTableActions(dataTable.table);
        watchCells(dataTable.table);
    });
}

function addTableActions(table) {
    const base = table.getAttribute('data-url');
    table.querySelectorAll('[data-delete]').forEach((button) => {
        button.addEventListener('click', () => {
            const url = base + '/' + button.parentElement.parentElement.getAttribute('data-row');
            addMessage(deleteRow(url));
        });
    });
}

function watchCells(table) {
    let updateUrl;
    if (table.hasAttribute('data-update-item-url')) {
        updateUrl = table.getAttribute('data-update-item-url')
    } else {
        updateUrl = table.getAttribute('data-url');
    }

    table.querySelectorAll('[contenteditable]').forEach((input) => {
        input.addEventListener('input', async (e) => {
            const attr = table.querySelectorAll('th')[input.cellIndex].innerText;
            const value = input.innerText;
            const url = updateUrl + '/' + input.parentElement.getAttribute('data-row');
            addMessage(await update(attr, value, url));
        });
    });
}

function makeRowLink(table) {
    const base = (table.hasAttribute('data-row-link-base') ? table.getAttribute('data-row-link-base') : '');
    table.querySelectorAll('[data-row]').forEach((row) => {
        row.addEventListener('click', (e) => {
            if (e.target.attributes.clickable) {
                window.location.href = base + '/' + row.getAttribute('data-row');
            }
        });
    });
}

window.addEventListener('DOMContentLoaded', () => {
    initCreateForm();
    initUpdateForm();
    initTables();
    document.querySelectorAll('[data-choices]').forEach((selector) => {
        initChoices(selector);
    });
});
