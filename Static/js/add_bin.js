document.addEventListener("DOMContentLoaded", function () {
    const form = document.getElementById("bin_form");
    const existingBinSelect = document.getElementById("id_existing_bin");
    const locationFields = ["id_location_name", "id_latitude", "id_longitude"];
    const binTypeField = document.getElementById("id_bin_types");  
    const submitButton = document.getElementById("submit-btn");

    // Get URLs from the form's data attributes
    const addBinUrl = form.getAttribute("data-add-url");
    const editBinUrlTemplate = form.getAttribute("data-edit-url");

    function updateFormAction() {
        const binPk = existingBinSelect.value.trim(); // Ensure valid input

        if (binPk) {
            form.action = editBinUrlTemplate.replace("0", binPk);
            disableLocationFields(true);
        } else {
            form.action = addBinUrl;
            disableLocationFields(false);
        }
    }

    function disableLocationFields(disable) {
        locationFields.forEach(fieldId => {
            let field = document.getElementById(fieldId);
            if (field) {
                field.disabled = disable;
            }
        });
        if (binTypeField) {
            binTypeField.disabled = disable;
        }
    }

    existingBinSelect.addEventListener("change", updateFormAction);
    updateFormAction(); // Ensure correct action on page load
});
