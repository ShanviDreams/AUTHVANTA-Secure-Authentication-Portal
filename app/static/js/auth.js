document.addEventListener(
    "DOMContentLoaded",
    function () {

        const passwordInput =
            document.getElementById("password");

        if (!passwordInput) {
            return;
        }

        passwordInput.addEventListener(
            "input",
            function () {

                const password =
                    passwordInput.value;

                const hasLength =
                    password.length >= 8;

                const hasUppercase =
                    /[A-Z]/.test(password);

                const hasLowercase =
                    /[a-z]/.test(password);

                const hasNumber =
                    /[0-9]/.test(password);

                const hasSpecial =
                    /[^A-Za-z0-9]/.test(password);

                const isStrong =
                    hasLength &&
                    hasUppercase &&
                    hasLowercase &&
                    hasNumber &&
                    hasSpecial;

                passwordInput.dataset.strong =
                    isStrong ? "true" : "false";
            }
        );
    }
);