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

    // Add event listener for sign-up button after DOM is loaded
    const signUpButton = document.getElementById("submit");
    if (signUpButton) {
        signUpButton.addEventListener("click", function (event) {
            event.preventDefault();
            signUp();
        });
    }
});

// const homeUrl = "{{ url_for('home') }}";
// const signInUrl = "{{ url_for('signin') }}";

import { initializeApp } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-app.js";
import { getAuth, createUserWithEmailAndPassword, signInWithEmailAndPassword } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-auth.js";
import { getFirestore, doc, setDoc } from "https://www.gstatic.com/firebasejs/10.10.0/firebase-firestore.js";

const firebaseConfig = {
    apiKey: "AIzaSyDrCUw__5Lf772A7hDeB4_2Invdf5Q80Mk",
    authDomain: "register-87e34.firebaseapp.com",
    projectId: "register-87e34",
    storageBucket: "register-87e34.firebasestorage.app",
    messagingSenderId: "173212056067",
    appId: "1:173212056067:web:49d7eebb1a4933f91f6c36"
  };
  


// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

document.addEventListener("DOMContentLoaded", function () {
    const submitButton = document.getElementById("submit");

    submitButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Prevent page reload

        const name = document.getElementById("name").value;
        const email = document.getElementById("email").value;
        const password = document.getElementById("password").value;

        console.log("Signing up:", email, password);

        try {
            const userCredential = await createUserWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            
            // Store user data in Firestore
            await setDoc(doc(db, "users", user.uid), {
                name: name,
                email: email,
                uid: user.uid,
                
            });

            alert("You are Signed Up!");
            console.log("User registered:", user);
            // window.location.href = "/signup.html";
            // window.location.href = "{{ url_for('signin') }}";
            window.location.href = signInUrl;
        } catch (error) {
            console.error("Error:", error.code, error.message);
            alert("Error: " + error.message);
        }
    });
});


//SignIn

document.addEventListener("DOMContentLoaded", function () {
    const signInButton = document.getElementById("signIn");

    signInButton.addEventListener("click", async function (event) {
        event.preventDefault(); // Prevent page reload

        const semail = document.getElementById("semail").value;
        const spassword = document.getElementById("spassword").value;

        console.log("Signing in:", semail);  // ✅ Fixed variable name

        try {
            const userCredential = await signInWithEmailAndPassword(auth, semail, spassword);
            const user = userCredential.user;

            alert("Sign-In Successful!");
            console.log("User signed in:", user);

            // Use the global variable homeUrl (passed from Flask)
            window.location.href = homeUrl;

        } catch (error) {
            console.error("Error:", error.code, error.message);
            alert("Error: " + error.message);
        }
    });
});
