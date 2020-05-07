function post(formData, url) {
    return fetch(url, {
        method: 'POST',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        body: formData,
    }).then(response => response.json()).catch(error => error.json())
}

function get(url) {
    return fetch(url, {
        method: 'GET',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
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
                    row.querySelectorAll('[data-item-row-field]').forEach((field) => {
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

function constructTableData(response) {
    let UUIDlocation;
    let columnCount = 0;

    function countColumn(column) {
        if (column === 'uuid' && isNaN(UUIDlocation) ) UUIDlocation = columnCount;
        columnCount++;
    }

    const data = {"data": []};

    for (let i = 0; i < response.length; i++) {
        data.data[i] = [];
        data.headings = [];
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

        const config = {
            data,
            filters: {},
            columns: [
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
        makeRowLink(dataTable.table)
    });
    dataTable.on('datatable.update', () => {
        makeRowLink(dataTable.table)
    });
    dataTable.on('datatable.sort', () => {
        makeRowLink(dataTable.table)
    });
    dataTable.on('datatable.page', () => {
        makeRowLink(dataTable.table)
    });
}

function makeRowLink(table) {
    const base = (table.hasAttribute('data-row-link-base') ? table.getAttribute('data-row-link-base') : '');
    table.querySelectorAll('[data-row]').forEach((row) => {
        row.addEventListener('click', () => {
            window.location.href = base + '/' + row.getAttribute('data-row');
        });
    });
}

window.addEventListener('DOMContentLoaded', () => {
    create();
    initTables();
});
