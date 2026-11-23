(function () {
    const root = document.documentElement;
    const button = document.getElementById("themeToggle");
    const icon = document.getElementById("themeIcon");
    const label = document.getElementById("themeLabel");

    function applyTheme(theme) {
        const selected = theme === "dark" ? "dark" : "light";
        root.dataset.theme = selected;
        localStorage.setItem("authvanta-theme", selected);

        if (icon) icon.textContent = selected === "dark" ? "☀" : "☾";
        if (label) label.textContent = selected === "dark" ? "Light mode" : "Dark mode";
        if (button) {
            button.setAttribute(
                "aria-label",
                selected === "dark" ? "Switch to light theme" : "Switch to dark theme"
            );
        }
    }

    applyTheme(localStorage.getItem("authvanta-theme") || "light");

    if (button) {
        button.addEventListener("click", function () {
            applyTheme(root.dataset.theme === "dark" ? "light" : "dark");
        });
    }
})();
