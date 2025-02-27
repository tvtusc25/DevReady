// Load Ace Editor
document.addEventListener("DOMContentLoaded", function () {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/python"); // Default language: Python
    editor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        wrap: true,
        minLines: 15,
        maxLines: 15
    });

    // Language Selector
    var languageSelector = document.getElementById("language-selector");
    languageSelector.addEventListener("change", function () {
        var selectedLanguage = languageSelector.value;
        var mode = "ace/mode/" + selectedLanguage;
        editor.session.setMode(mode);
    });

    // Run Button (Unimplemented)
    document.getElementById("run-btn").addEventListener("click", function () {
        var code = editor.getValue();
        var language = languageSelector.value;
        document.getElementById("output").innerHTML = `<pre>Running ${language} code:\n\n${code}</pre>`;
    });
});
