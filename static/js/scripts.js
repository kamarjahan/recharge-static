document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rechargeForm');
    const ordersTable = document.getElementById('ordersTable').querySelector('tbody');

    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const operator = form.operator.value;
        const circle = form.circle.value;
        const mobile = form.mobile.value;
        const amount = form.amount.value;
        const orderId = Date.now();

        const newRow = document.createElement('tr');
        newRow.innerHTML = `
            <td>${orderId}</td>
            <td>${operator}</td>
            <td>${circle}</td>
            <td>${mobile}</td>
            <td>${amount}</td>
            <td>Pending</td>
        `;

        ordersTable.appendChild(newRow);
        form.reset();
    });
});
