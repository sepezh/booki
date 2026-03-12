function removeElementById(id) {
    const element = document.getElementById(id);

    if (element) {
        element.remove();
    }
}

function runScript() {
    const element = document.getElementById('runscript');

    if (element) {
        eval(element.innerHTML)
    }
}

window.onload = (event) => {
    const modalElement = document.getElementById("modalId");
    const myModal = new bootstrap.Modal(modalElement);
    modalElement.addEventListener('hidden.bs.modal', function () {
        document.querySelector('#modalId .modal-title').innerHTML = '';
        document.querySelector('#modalId .modal-body').innerHTML = '';
    });

    document.getElementById('menu-search').addEventListener('click', function (event) {
        event.preventDefault();
        document.querySelector('.search-overlay').classList.remove('d-none');
        document.querySelector('main').classList.add('filter-blur', 'overflow-hidden');
    });

    document.getElementById('close-search-overlay').addEventListener('click', function (event) {
        event.preventDefault();
        document.querySelector('main').classList.remove('filter-blur', 'overflow-hidden');
        document.querySelector('.search-overlay').classList.add('d-none');
    });

    const reserveBtnElement = document.getElementById('reserve');
    if (reserveBtnElement) {
        reserveBtnElement.addEventListener('click', async function () {
            const bookSlug = this.getAttribute('data-book')
            const url = '/ajax/near-libraries?book=' + bookSlug;
            try {
                const response = await fetch(url, {
                    headers: {
                        'accept': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }

                const json = await response.json();
                if ('view' in json && json.view.trim().length > 0 && json.message == 'update_profile') {
                    document.querySelector('#modalId .modal-title').innerHTML = 'System Message';
                    document.querySelector('#modalId .modal-body').innerHTML = json.view;
                    myModal.show();
                }

                if ('view' in json && json.view.trim().length > 0 && json.message == 'success') {
                    document.querySelector('#modalId .modal-title').innerHTML = 'Nearest Libraries';
                    document.querySelector('#modalId .modal-body').innerHTML = json.view;
                    myModal.show();
                }
            } catch (error) {
                console.error(error.message);
            }
        });
    }

    const redirectElements = document.querySelectorAll('.redirect[data-href]');
    if (redirectElements) {
        redirectElements.forEach(elm => elm.addEventListener('click', function (event) {
            event.preventDefault();
            location.href = this.getAttribute('data-href')
        }));
    }

    const showMoreReview = document.getElementById('show-more-review')
    if (showMoreReview) {
        showMoreReview.addEventListener('click', async function () {
            const page = this.getAttribute('data-page');

            const url = '/ajax/load-more-reviews/' + book + '?' + new URLSearchParams({
                'page': page
            });

            try {
                const response = await fetch(url, {
                    headers: {
                        'accept': 'application/json'
                    }
                });
                if (!response.ok) {
                    throw new Error(`Response status: ${response.status}`);
                }

                const json = await response.json();
                if (json.message == 'empty') {
                    this.remove()
                }

                if ('view' in json && json.view.trim().length > 0 && json.message == 'success') {
                    document.getElementById('reviews_list').innerHTML += json.view;
                }
            } catch (error) {
                console.error(error.message);
            }

        });
    }
};
