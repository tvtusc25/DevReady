// Load Ace Editor
document.addEventListener("DOMContentLoaded", function () {
    var editor = ace.edit("editor");
    console.log(editor)
    editor.setTheme("ace/theme/xcode");

    // Retrieve the template from the hidden data attribute
    var template = document.getElementById("editor").dataset.template;
    if (template) {
        editor.setValue(template, -1); // -1 prevents cursor moving to the end
    }

    editor.setOptions({
        fontSize: "14px",
        showPrintMargin: false,
        wrap: true,
        minLines: 15,
        maxLines: 15
    });

    const questionId = document.getElementById('question-title')?.dataset?.questionId;


    // Run Button
    document.getElementById("run-btn").addEventListener("click", async function () {
        if (!questionId) {
            alert('No question selected!');
            return;
        }

        const code = editor.getValue();
        const outputDiv = document.getElementById("output");

        try {
            outputDiv.innerHTML = '<p class="text-muted">Running sample tests...</p>';

            const response = await fetch(`/run/${questionId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ code })
            });

            const result = await response.json();
            if (result.error) {
                outputDiv.innerHTML = `<pre class="text-danger">${result.error}</pre>`;
                return;
            }

            const resultHtml = `
                <div class="${result.passed ? 'text-success' : 'text-danger'}">
                    <h6>${result.passed ? 'All Sample Tests Passed! 🎉' : 'Some Sample Tests Failed'}</h6>
                    ${result.results
                    .filter(test => test.input !== 'Hidden')
                    .map(test => `
                            <div class="test-case border rounded p-2 my-2 ${test.passed ? 'border-success' : 'border-danger'}">
                                <div>Input: <code>${test.input}</code></div>
                                <div>Expected: <code>${test.expected}</code></div>
                                <div>Output: <code>${test.actual}</code></div>
                                ${test.error ? `<div class="text-danger">Error: ${test.error}</div>` : ''}
                                <div class="mt-1">
                                    <span class="badge ${test.passed ? 'bg-success' : 'bg-danger'}">
                                        ${test.passed ? 'PASSED' : 'FAILED'}
                                    </span>
                                </div>
                            </div>
                        `).join('')}
                </div>
            `;

            outputDiv.innerHTML = resultHtml;
        } catch (error) {
            outputDiv.innerHTML = `<pre class="text-danger">Error: ${error.message}</pre>`;
        }
    });

    // Submit Button
    document.getElementById("submit-btn").addEventListener("click", async function () {
        if (!questionId) {
            alert('No question selected!');
            return;
        }

        const code = editor.getValue();
        const outputDiv = document.getElementById("output");

        try {
            outputDiv.innerHTML = '<p class="text-muted">Testing solution...</p>';

            const response = await fetch(`/submit/${questionId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ code })
            });

            const result = await response.json();
            const resultHtml = `
                <div class="${result.passed ? 'text-success' : 'text-danger'}">
                    <h6>${result.passed ? 'All Tests Passed!' : 'Some Tests Failed'}</h6>
                    ${result.results
                    .filter(test => test.input !== 'Hidden')
                    .map(test => `
                            <div class="test-case border rounded p-2 my-2 ${test.passed ? 'border-success' : 'border-danger'}">
                                <div>Input: <code>${test.input}</code></div>
                                <div>Expected: <code>${test.expected}</code></div>
                                <div>Output: <code>${test.actual}</code></div>
                                ${test.error ? `<div class="text-danger">Error: ${test.error}</div>` : ''}
                                <div class="mt-1">
                                    <span class="badge ${test.passed ? 'bg-success' : 'bg-danger'}">
                                        ${test.passed ? 'PASSED' : 'FAILED'}
                                    </span>
                                </div>
                            </div>
                        `).join('')}
                </div>
            `;

            outputDiv.innerHTML = resultHtml;
        } catch (error) {
            outputDiv.innerHTML = `<pre class="text-danger">Error: ${error.message}</pre>`;
        }
    });

    document.getElementById("skip-btn").addEventListener("click", function () {
        if (confirm('Are you sure you want to skip this question?')) {
            window.location.reload();
        }
    });
});
