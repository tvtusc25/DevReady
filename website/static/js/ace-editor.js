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

    // Run Button 
    document.getElementById("submit-btn").addEventListener("click", async function () {
        let code = editor.getValue();
        let language = document.getElementById("language-selector").value;
    
        let response = await fetch("/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code, language: language })
        });
    
        let result = await response.json();
        document.getElementById("output").innerHTML = result.output 
            ? `<pre>${result.output}</pre>` 
            : `<pre style="color:red;">${result.error}</pre>`;
    });
    
});
