document.addEventListener("DOMContentLoaded", function () {
    const startDate = document.getElementById("startDate");
    const endDate = document.getElementById("endDate");

    // Set max date to today
    const today = new Date().toISOString().split("T")[0];
    startDate.max = today;
    endDate.max = today;

    startDate.addEventListener("change", function () {
        if (startDate.value) {
            // Ensure start date does not exceed today
            if (startDate.value > today) {
                startDate.value = today;
            }
            // Set min for end date
            endDate.min = new Date(new Date(startDate.value).getTime() + 86400000).toISOString().split("T")[0];
        }
    });

    endDate.addEventListener("change", function () {
        if (endDate.value) {
            // Ensure end date does not exceed today
            if (endDate.value > today) {
                endDate.value = today;
            }
            // Ensure end date is after start date
            if (startDate.value && endDate.value <= startDate.value) {
                endDate.value = "";
            }
        }
    });
});