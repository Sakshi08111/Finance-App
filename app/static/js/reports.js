// Pie Chart Data
const pieData = {
    labels: JSON.parse(document.getElementById('pieLabels').textContent),
    datasets: [{
        data: JSON.parse(document.getElementById('pieData').textContent),
        backgroundColor: [
            '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
        ]
    }]
};

// Bar Graph Data
const barData = {
    labels: JSON.parse(document.getElementById('barLabels').textContent),
    datasets: [
        {
            label: 'Income',
            data: JSON.parse(document.getElementById('barIncomeData').textContent),
            backgroundColor: '#36A2EB'
        },
        {
            label: 'Expenses',
            data: JSON.parse(document.getElementById('barExpensesData').textContent),
            backgroundColor: '#FF6384'
        }
    ]
};

// Render Pie Chart
const pieCtx = document.getElementById('pieChart').getContext('2d');
new Chart(pieCtx, {
    type: 'pie',
    data: pieData,
    options: {
        responsive: true,  // Make the chart responsive
        maintainAspectRatio: false  // Allow the chart to resize
    }
});

// Render Bar Graph
const barCtx = document.getElementById('barGraph').getContext('2d');
new Chart(barCtx, {
    type: 'bar',
    data: barData,
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive: true,  // Make the chart responsive
        maintainAspectRatio: false  // Allow the chart to resize
    }
});

// Pie Chart (Expenses by Category)
const pieChart = new Chart(document.getElementById('pieChart'), {
    type: 'pie',
    data: {
        labels: categoriesData.labels,
        datasets: [{
            data: categoriesData.values,
            backgroundColor: [
                '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
            ]
        }]
    }
});

// Bar Chart (Monthly Income vs. Expenses)
const barChart = new Chart(document.getElementById('barChart'), {
    type: 'bar',
    data: {
        labels: monthlyData.labels,
        datasets: [
            {
                label: 'Income',
                data: monthlyData.income,
                backgroundColor: '#36A2EB'
            },
            {
                label: 'Expenses',
                data: monthlyData.expenses,
                backgroundColor: '#FF6384'
            }
        ]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        }
    }
});