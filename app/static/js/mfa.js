document.addEventListener(
    "DOMContentLoaded",
    function () {

        const codeInput =
            document.getElementById("code");

        if (!codeInput) {
            return;
        }

        codeInput.addEventListener(
            "input",
            function () {

                codeInput.value =
                    codeInput.value
                        .replace(/\D/g, "")
                        .slice(0, 6);
            }
        );
    }
);