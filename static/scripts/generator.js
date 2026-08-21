const addMore = document.getElementById("add_more");
const additionalPracticals = document.getElementById("additional_practicals");

addMore.addEventListener("change", function () {
    additionalPracticals.classList.toggle(
        "d-none",
        !this.checked
    );
});