document.addEventListener("DOMContentLoaded", () => {
    // Initialize Ace Editor
    const editor = ace.edit("editor");
    editor.setTheme("ace/theme/xcode");
    const template = document.getElementById("editor").dataset.template;
    if (template) editor.setValue(template, -1);
    editor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        wrap: true,
        minLines: 15,
        maxLines: 15,
    });
});
