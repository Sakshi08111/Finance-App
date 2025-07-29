function initializeCharts() {
    // Pie Chart (Expenses by Category)
    const pieChartCanvas = document.getElementById('pieChart');
    if (pieChartCanvas) {
        const pieChart = new Chart(pieChartCanvas, {
            type: 'pie',
            data: {
                labels: window.categoriesData.labels,
                datasets: [{
                    data: window.categoriesData.values,
                    backgroundColor: [
                        '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40'
                    ]
                }]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Expenses by Category'
                    }
                }
            }
        });
    } else {
        console.error("Pie chart canvas element not found!");
    }

    // Bar Chart (Monthly Income vs. Expenses)
    const barChartCanvas = document.getElementById('barChart');
    if (barChartCanvas) {
        const barChart = new Chart(barChartCanvas, {
            type: 'bar',
            data: {
                labels: window.monthlyData.labels,
                datasets: [
                    {
                        label: 'Income',
                        data: window.monthlyData.income,
                        backgroundColor: '#36A2EB'
                    },
                    {
                        label: 'Expenses',
                        data: window.monthlyData.expenses,
                        backgroundColor: '#FF6384'
                    }
                ]
            },
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        position: 'top',
                    },
                    title: {
                        display: true,
                        text: 'Monthly Income vs. Expenses'
                    }
                },
                scales: {
                    y: {
                        beginAtZero: true
                    }
                }
            }
        });
    } else {
        console.error("Bar chart canvas element not found!");
    }
}