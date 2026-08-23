const addMore = document.getElementById("add_more");
const additionalPracticals = document.getElementById("additional_practicals");

const fileInputBtn = document.getElementById("file_input_btn");
const manualInputBtn = document.getElementById("manual_input_btn");

const fileInputSection = document.getElementById("file_input_section");
const manualInputSection = document.getElementById("manual_input_section");

const manualEntry = document.getElementById("manual_entry");


// Add more practicals

addMore.addEventListener("change", function () {

    additionalPracticals.classList.toggle(
        "d-none",
        !this.checked
    );

});


// File input

fileInputBtn.addEventListener("click", function () {

    fileInputSection.classList.remove("d-none");
    manualInputSection.classList.add("d-none");

    fileInputBtn.classList.add("active");
    manualInputBtn.classList.remove("active");

    manualEntry.value = "file";

});


// Manual input

manualInputBtn.addEventListener("click", function () {

    manualInputSection.classList.remove("d-none");
    fileInputSection.classList.add("d-none");

    manualInputBtn.classList.add("active");
    fileInputBtn.classList.remove("active");

    manualEntry.value = "manual";

});