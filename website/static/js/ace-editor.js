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

    // Get question ID
    const questionElem = document.getElementById("question-title");
    const questionId = questionElem ? questionElem.dataset.questionId : null;
    if (!questionId) return alert("No question selected!");

    // Execute code via API
    async function executeCode(endpoint, outputId, isSubmission = false) {
        const code = editor.getValue();
        const outputDiv = document.getElementById(outputId);
        outputDiv.innerHTML = '<p class="text-muted">Processing...</p>';

        try {
            const res = await fetch(`/${endpoint}/${questionId}`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                credentials: "include",
                body: JSON.stringify({ code }),
            });
            const result = await res.json();
            if (result.error) {
                outputDiv.innerHTML = `<pre class="text-danger">${result.error}</pre>`;
                return;
            }
            isSubmission ? displaySubmissionResults(result.results) : displayRunResults(result.results);
        } catch (error) {
            outputDiv.innerHTML = `<pre class="text-danger">Error: ${error.message}</pre>`;
        }
    }

    // Update sample test case buttons based on run results
    function displayRunResults(results) {
        const buttons = document.querySelectorAll("#test-case-buttons button");
        if (!results || results.length === 0) {
            document.getElementById("actual-output").innerHTML =
                `<pre class="text-danger">Error: No test results found.</pre>`;
            return;
        }
        results.forEach((test, i) => {
            if (i < buttons.length) {
                const btn = buttons[i];
                btn.className = test.passed ? "btn btn-success" : "btn btn-danger";
                btn.onclick = () => showTestCase(test.expected, test.input, test.actual, btn);
            }
        });
        // Automatically show the first test case result
        showTestCase(results[0].expected, results[0].input, results[0].actual, buttons[0]);
    }

    // Needs logic to show unpassed cases beyond sample !!!!!
    // Update test case buttons based on submission results
    function displaySubmissionResults(results) {
        const buttons = document.querySelectorAll("#test-case-buttons button");
        if (!results || results.length === 0) {
            document.getElementById("actual-output").innerHTML =
                `<pre class="text-danger">Error: No test results found.</pre>`;
            return;
        }
        results.forEach((test, i) => {
            if (i < buttons.length) {
                const btn = buttons[i];
                btn.className = test.passed ? "btn btn-success" : "btn btn-danger";
                btn.onclick = () => showTestCase(test.expected, test.input, test.actual, btn);
            }
        });
        // Automatically show the first test case result
        showTestCase(results[0].expected, results[0].input, results[0].actual, buttons[0]);
    }

    // Display a single test case result
    function showTestCase(expected, input, actual, activeButton) {
        document.getElementById("expected-text").innerHTML = `<strong>${expected}</strong>`;
        document.getElementById("input-text").innerHTML = `<strong>${input}</strong>`;
      
        let actualOutput = "";
        let isError = false;
      
        // Check if 'actual' is an error object (has an 'error' property)
        if (actual && typeof actual === "object" && actual.error) {
          actualOutput = actual.error;
          isError = true;
        } else if (actual === undefined || actual === null) {
          actualOutput = "None";
        } else if (typeof actual === "string") {
          actualOutput = `"${actual}"`;
        } else {
          actualOutput = JSON.stringify(actual);
        }
      
        // If it's an error, show in red without bold; otherwise, bold the output.
        if (isError) {
          document.getElementById("actual-output").innerHTML = `<span style="color: red">${actualOutput}</span>`;
        } else {
          document.getElementById("actual-output").innerHTML = `<strong>${actualOutput}</strong>`;
        }
      
        document.querySelectorAll("#test-case-buttons button").forEach(btn => {
          btn.classList.remove("btn-primary", "active");
        });
        activeButton.classList.add("btn-primary", "active");
      }      

    // Bind button events
    document.getElementById("run-btn").addEventListener("click", () =>
        executeCode("run", "actual-output")
    );
    document.getElementById("submit-btn").addEventListener("click", () =>
        executeCode("submit", "actual-output", true)
    );
    document.getElementById("skip-btn").addEventListener("click", () => {
        if (confirm("Are you sure you want to skip this question?")) window.location.reload();
    });
});
