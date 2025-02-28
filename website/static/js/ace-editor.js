// Load Ace Editor
document.addEventListener("DOMContentLoaded", function () {
    var editor = ace.edit("editor");
    editor.setTheme("ace/theme/xcode");
    editor.session.setMode("ace/mode/python"); // Fixed to Python-only
    editor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        wrap: true,
        minLines: 15,
        maxLines: 15
    });

    // Run Button
    document.getElementById("submit-btn").addEventListener("click", async function () {
        let code = editor.getValue();
    
        let response = await fetch("/run", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ code: code }) // No more "language" field
        });
    
        let result = await response.json();
        document.getElementById("output").innerHTML = result.output 
            ? `<pre>${result.output}</pre>` 
            : `<pre style="color:red;">${result.error}</pre>`;
    });
});
