document.addEventListener('DOMContentLoaded', function() {
    let checkboxes = document.querySelectorAll('#logCheckBox');
    const deleteBtn = document.getElementById('deleteLogsBtn');
    const deleteTargetUrl = document.getElementById('deleteLogsBtn').getAttribute('target-url');
    const csrf = document.getElementById('csrf').children[0].value;

    let itemsToDelete = [];

    checkboxes.forEach((cBox) => {
        cBox.addEventListener('change', (e) => {
            if (e.target.checked) {
                let id = e.target.getAttribute('row-id');
                itemsToDelete.push(id);
                console.log(itemsToDelete);
            } else {
                let id = e.target.getAttribute('row-id');
                index = itemsToDelete.indexOf(id);
                itemsToDelete.splice(index, 1);
                console.log(itemsToDelete);
            }
        });
    });


    deleteBtn.addEventListener('click', (e) => {
        if (itemsToDelete.length > 0) {
            fetch(`${deleteTargetUrl}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken':csrf,
                    'Connection': 'keep-alive'
                },
                body: JSON.stringify(itemsToDelete)
            })

            checkboxes.forEach((cBox) => {
                if (cBox.checked) {
                    cBox.parentElement.parentElement.remove();
                }
            });
            
            window.location.reload();
        }
    });
});