
// Check if the dataContainer element exists
const dataContainer = document.getElementById('dataContainer');

if (dataContainer) {
    // Extract data from the dataContainer element
    const categoriesLabels = dataContainer.getAttribute('data-categories-labels');
    const categoriesValues = dataContainer.getAttribute('data-categories-values');
    const monthlyLabels = dataContainer.getAttribute('data-monthly-labels');
    const monthlyIncome = dataContainer.getAttribute('data-monthly-income');
    const monthlyExpenses = dataContainer.getAttribute('data-monthly-expenses');

    // Validate and parse the data
    if (categoriesLabels && categoriesValues && monthlyLabels && monthlyIncome && monthlyExpenses) {
        window.categoriesData = {
            labels: JSON.parse(categoriesLabels),
            values: JSON.parse(categoriesValues)
        };

        window.monthlyData = {
            labels: JSON.parse(monthlyLabels),
            income: JSON.parse(monthlyIncome),
            expenses: JSON.parse(monthlyExpenses)
        };
    } else {
        console.error("One or more data attributes are missing in the dataContainer element!");
    }
} else {
    console.error("dataContainer element not found!");
}