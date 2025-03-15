document.addEventListener("DOMContentLoaded", function () {
    const signInForm = document.querySelector(".sign-in-container");
    const signUpForm = document.querySelector(".sign-up-container");

    document.getElementById("showSignUp").addEventListener("click", function (event) {
        event.preventDefault();
        signInForm.classList.add("hidden");
        signUpForm.classList.remove("hidden");
    });

    document.getElementById("showSignIn").addEventListener("click", function (event) {
        event.preventDefault();
        signUpForm.classList.add("hidden");
        signInForm.classList.remove("hidden");
    });
});
