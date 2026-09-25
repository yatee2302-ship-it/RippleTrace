from pathlib import Path
from datetime import datetime
import re
import shutil

# ============================================================
# RippleTrace - SAFE UI RESTORE + REAL REPORTS
# ============================================================
# IMPORTANT:
# - Does NOT touch backend
# - Does NOT modify app.js
# - Preserves realtime-monitor.js
# - Removes only old report/polish layers
# - Keeps the existing dark/live graph UI
# - Adds reports only after REAL agent responses
# ============================================================

ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
STYLE = APP / "style.css"
APP_JS = APP / "app.js"

REALTIME_JS = APP / "realtime-monitor.js"
REPORT_JS = APP / "reports-final.js"

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
BACKUP = APP / f"backup_safe_restore_{timestamp}"

print("\n============================================================")
print(" RippleTrace SAFE UI RESTORE")
print("============================================================\n")

if not ROOT.exists():
    raise SystemExit(f"RippleTrace project not found: {ROOT}")

if not INDEX.exists():
    raise SystemExit(f"index.html not found: {INDEX}")

# ------------------------------------------------------------
# 1. BACKUP CURRENT UI
# ------------------------------------------------------------

BACKUP.mkdir(parents=True, exist_ok=True)

for file in [
    INDEX,
    STYLE,
    APP_JS,
    REALTIME_JS,
]:
    if file.exists():
        shutil.copy2(file, BACKUP / file.name)

print(f"[OK] Backup created:")
print(f"     {BACKUP}\n")


# ------------------------------------------------------------
# 2. REMOVE OLD REPORT/POLISH SCRIPT REFERENCES
# ------------------------------------------------------------

html = INDEX.read_text(encoding="utf-8")

old_scripts = [
    "ui-polish.js",
    "ui-polish-v2.js",
    "ui-polish-v3.js",
    "ui-polish-v4.js",
    "ui-polish-v5.js",
    "report-v5.js",
    "rippletrace-real-reports.js",
    "reports-final.js",
]

for script_name in old_scripts:
    pattern = rf'<script[^>]+src=["\'][^"\']*{re.escape(script_name)}["\'][^>]*>\s*</script>'
    html, count = re.subn(
        pattern,
        "",
        html,
        flags=re.IGNORECASE
    )

    if count:
        print(f"[REMOVED] {script_name}")


# ------------------------------------------------------------
# 3. REMOVE REPORT-ONLY CSS BLOCKS
# ------------------------------------------------------------

if STYLE.exists():

    css = STYLE.read_text(encoding="utf-8")

    report_markers = [
        "RIPPLETRACE REPORT V5",
        "RippleTrace Report V5",
        "RIPPLETRACE REAL REPORT",
        "RIPPLETRACE REPORT",
        "REAL REPORT MODAL",
    ]

    for marker in report_markers:

        while True:

            start = css.find(marker)

            if start == -1:
                break

            # Find the beginning of the nearest comment
            comment_start = css.rfind("/*", 0, start)

            if comment_start == -1:
                comment_start = start

            # Try to find the next closing comment
            comment_end = css.find("*/", start)

            if comment_end != -1:
                comment_end += 2
            else:
                comment_end = len(css)

            # Remove the marked comment
            css = css[:comment_start] + css[comment_end:]

            print(f"[REMOVED CSS] {marker}")

    STYLE.write_text(css, encoding="utf-8")


# ------------------------------------------------------------
# 4. ENSURE REALTIME GRAPH SCRIPT EXISTS
# ------------------------------------------------------------

if not REALTIME_JS.exists():

    print("[WARNING] realtime-monitor.js does not exist.")

    realtime_code = r"""
/*
 * RippleTrace Realtime Dependency Monitor
 *
 * This file is intentionally kept independent from
 * the agent/report logic.
 */

(function () {

    "use strict";

    console.log("RippleTrace realtime monitor loaded");

    async function loadRealtimeGraph() {

        try {

            const response = await fetch(
                window.location.origin +
                "/api/risk/SupplyChainNodes"
            );

            if (!response.ok) {
                throw new Error(
                    "Realtime graph request failed: " +
                    response.status
                );
            }

            const data = await response.json();

            console.log(
                "Realtime graph nodes:",
                data.value || data
            );

        } catch (error) {

            console.warn(
                "Realtime graph monitor:",
                error
            );

        }

    }

    loadRealtimeGraph();

    setInterval(
        loadRealtimeGraph,
        3000
    );

})();
"""

    REALTIME_JS.write_text(
        realtime_code.strip() + "\n",
        encoding="utf-8"
    )

    print("[CREATED] realtime-monitor.js")

else:

    print("[OK] Existing realtime-monitor.js preserved")


# ------------------------------------------------------------
# 5. ENSURE REALTIME GRAPH IS LOADED EXACTLY ONCE
# ------------------------------------------------------------

# Remove all realtime-monitor script tags first
html = re.sub(
    r'<script[^>]+src=["\'][^"\']*realtime-monitor\.js["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)

# Add it once before </body>
realtime_tag = '<script src="realtime-monitor.js"></script>'

if re.search(r"</body>", html, flags=re.IGNORECASE):

    html = re.sub(
        r"</body>",
        f"    {realtime_tag}\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html += "\n" + realtime_tag + "\n"

print("[OK] realtime-monitor.js loaded exactly once")


# ------------------------------------------------------------
# 6. CREATE SAFE REAL REPORT ENGINE
# ------------------------------------------------------------

report_code = r"""
/*
 * ============================================================
 * RippleTrace - FINAL REAL REPORT ENGINE
 * ============================================================
 *
 * IMPORTANT:
 * - Does NOT modify agent buttons
 * - Does NOT intercept clicks
 * - Does NOT preventDefault()
 * - Does NOT stopPropagation()
 * - Does NOT create fake results
 * - Reports are generated ONLY from real API responses
 * - Realtime graph remains untouched
 * ============================================================
 */

(function () {

    "use strict";

    console.log(
        "RippleTrace real report engine loaded"
    );

    const originalFetch = window.fetch;

    let latestResults = {
        TRACE: null,
        PREDICT: null,
        RECOMMEND: null,
        SAFEGUARD: null
    };


    // --------------------------------------------------------
    // Capture REAL backend responses
    // --------------------------------------------------------

    window.fetch = async function (...args) {

        const response = await originalFetch.apply(
            this,
            args
        );

        try {

            const request = args[0];

            let url = "";

            if (typeof request === "string") {
                url = request;
            } else if (request && request.url) {
                url = request.url;
            }

            const method =
                args[1] &&
                args[1].method
                    ? args[1].method.toUpperCase()
                    : "GET";


            if (
                method === "POST" &&
                url.includes("/api/risk/")
            ) {

                const cloned = response.clone();

                cloned.json()
                    .then(data => {

                        if (
                            url.includes(
                                "triggerCascade"
                            )
                        ) {

                            latestResults.TRACE = data;

                            console.log(
                                "REAL TRACE REPORT DATA:",
                                data
                            );

                            createReportButton(
                                "TRACE",
                                data
                            );

                        }

                        else if (
                            url.includes(
                                "triggerPrediction"
                            )
                        ) {

                            latestResults.PREDICT = data;

                            console.log(
                                "REAL PREDICT REPORT DATA:",
                                data
                            );

                            createReportButton(
                                "PREDICT",
                                data
                            );

                        }

                        else if (
                            url.includes(
                                "triggerMitigation"
                            )
                        ) {

                            latestResults.RECOMMEND = data;

                            console.log(
                                "REAL RECOMMENDATION REPORT DATA:",
                                data
                            );

                            createReportButton(
                                "RECOMMEND",
                                data
                            );

                        }

                        else if (
                            url.includes(
                                "triggerSafeguard"
                            )
                        ) {

                            latestResults.SAFEGUARD = data;

                            console.log(
                                "REAL SAFEGUARD REPORT DATA:",
                                data
                            );

                            createReportButton(
                                "SAFEGUARD",
                                data
                            );

                        }

                    })
                    .catch(() => {
                        // Ignore non-JSON responses
                    });
            }

        } catch (error) {

            console.warn(
                "Report capture warning:",
                error
            );

        }

        return response;
    };


    // --------------------------------------------------------
    // Create ONLY our own report button
    // --------------------------------------------------------

    function createReportButton(
        agent,
        data
    ) {

        if (!data) {
            return;
        }

        const buttonId =
            "rt-report-" +
            agent.toLowerCase();


        // Remove previous report button
        const oldButton =
            document.getElementById(buttonId);

        if (oldButton) {
            oldButton.remove();
        }


        const button =
            document.createElement("button");

        button.id = buttonId;

        button.type = "button";

        button.textContent =
            "View " +
            formatAgentName(agent) +
            " Report";


        button.setAttribute(
            "data-rippletrace-report",
            agent
        );


        // ----------------------------------------------------
        // IMPORTANT:
        // Listener belongs ONLY to this button
        // ----------------------------------------------------

        button.addEventListener(
            "click",
            function () {

                openReport(
                    agent,
                    latestResults[agent]
                );

            }
        );


        // ----------------------------------------------------
        // Try to place button in matching agent card
        // without touching existing buttons
        // ----------------------------------------------------

        const card =
            findAgentCard(agent);


        if (card) {

            const container =
                document.createElement("div");

            container.className =
                "rt-report-container";

            container.appendChild(button);

            card.appendChild(container);

        } else {

            // Safe fallback:
            // add to report area at bottom
            const fallback =
                document.createElement("div");

            fallback.className =
                "rt-report-fallback";

            fallback.appendChild(button);

            document.body.appendChild(
                fallback
            );

        }

    }


    // --------------------------------------------------------
    // Find agent card WITHOUT modifying its controls
    // --------------------------------------------------------

    function findAgentCard(agent) {

        const cards =
            document.querySelectorAll(
                ".agent-card, " +
                ".agent-panel, " +
                ".agent, " +
                ".card"
            );


        let keywords = [];

        if (agent === "TRACE") {

            keywords = [
                "trace",
                "cascade"
            ];

        } else if (agent === "PREDICT") {

            keywords = [
                "predict"
            ];

        } else if (agent === "RECOMMEND") {

            keywords = [
                "recommend",
                "mitigation"
            ];

        } else if (agent === "SAFEGUARD") {

            keywords = [
                "safeguard"
            ];

        }


        for (const card of cards) {

            const text =
                (
                    card.innerText ||
                    ""
                ).toLowerCase();


            for (const keyword of keywords) {

                if (text.includes(keyword)) {
                    return card;
                }

            }

        }

        return null;

    }


    // --------------------------------------------------------
    // Agent names
    // --------------------------------------------------------

    function formatAgentName(agent) {

        const names = {

            TRACE: "Trace",

            PREDICT: "Prediction",

            RECOMMEND: "Recommendation",

            SAFEGUARD: "Safeguard"

        };

        return names[agent] || agent;

    }


    // --------------------------------------------------------
    // Report Modal
    // --------------------------------------------------------

    function openReport(
        agent,
        data
    ) {

        if (!data) {

            console.warn(
                "No real report data available"
            );

            return;

        }


        const existing =
            document.getElementById(
                "rt-report-modal"
            );

        if (existing) {
            existing.remove();
        }


        const modal =
            document.createElement("div");

        modal.id =
            "rt-report-modal";


        const overlay =
            document.createElement("div");

        overlay.className =
            "rt-report-overlay";


        const panel =
            document.createElement("div");

        panel.className =
            "rt-report-panel";


        const title =
            document.createElement("h2");

        title.textContent =
            formatAgentName(agent) +
            " Agent Report";


        const subtitle =
            document.createElement("div");

        subtitle.className =
            "rt-report-subtitle";

        subtitle.textContent =
            "Live result returned by RippleTrace backend";


        const table =
            document.createElement("table");

        table.className =
            "rt-report-table";


        const tbody =
            document.createElement("tbody");


        const rows =
            flattenObject(
                data
            );


        rows.forEach(
            row => {

                const tr =
                    document.createElement("tr");


                const key =
                    document.createElement("td");

                key.textContent =
                    row.key;


                const value =
                    document.createElement("td");

                value.textContent =
                    row.value;


                tr.appendChild(key);

                tr.appendChild(value);

                tbody.appendChild(tr);

            }
        );


        table.appendChild(tbody);


        const close =
            document.createElement("button");

        close.type = "button";

        close.className =
            "rt-report-close";

        close.textContent =
            "Close";


        close.addEventListener(
            "click",
            function () {
                modal.remove();
            }
        );


        panel.appendChild(title);

        panel.appendChild(subtitle);

        panel.appendChild(table);

        panel.appendChild(close);

        overlay.appendChild(panel);

        modal.appendChild(overlay);

        document.body.appendChild(modal);


        overlay.addEventListener(
            "click",
            function (event) {

                if (
                    event.target === overlay
                ) {

                    modal.remove();

                }

            }
        );

    }


    // --------------------------------------------------------
    // Convert real JSON response to table rows
    // --------------------------------------------------------

    function flattenObject(
        object,
        prefix = ""
    ) {

        const rows = [];


        if (
            object === null ||
            object === undefined
        ) {

            return rows;

        }


        if (
            typeof object !== "object"
        ) {

            rows.push({
                key: prefix || "Result",
                value: String(object)
            });

            return rows;

        }


        if (Array.isArray(object)) {

            object.forEach(
                (item, index) => {

                    const child =
                        flattenObject(
                            item,
                            prefix +
                            "[" +
                            index +
                            "]"
                        );

                    rows.push(
                        ...child
                    );

                }
            );

            return rows;

        }


        Object.entries(object)
            .forEach(
                ([key, value]) => {

                    const fullKey =
                        prefix
                            ? prefix +
                              "." +
                              key
                            : key;


                    if (
                        value !== null &&
                        typeof value === "object"
                    ) {

                        rows.push(
                            ...flattenObject(
                                value,
                                fullKey
                            )
                        );

                    } else {

                        rows.push({

                            key: fullKey,

                            value:
                                value === null
                                    ? "—"
                                    : String(value)

                        });

                    }

                }
            );


        return rows;

    }


    // --------------------------------------------------------
    // Minimal report CSS
    // This does NOT replace existing UI CSS.
    // --------------------------------------------------------

    const style =
        document.createElement("style");

    style.textContent = `

        .rt-report-container {
            margin-top: 12px;
        }

        .rt-report-container button,
        .rt-report-fallback button {

            border: 1px solid rgba(255,255,255,.18);

            background: rgba(255,255,255,.06);

            color: inherit;

            padding: 8px 14px;

            border-radius: 7px;

            cursor: pointer;

            font-size: 13px;

            transition:
                background .2s ease,
                transform .2s ease;

        }

        .rt-report-container button:hover,
        .rt-report-fallback button:hover {

            background:
                rgba(255,255,255,.12);

            transform:
                translateY(-1px);

        }

        .rt-report-fallback {

            position: fixed;

            right: 24px;

            bottom: 24px;

            z-index: 9998;

        }

        .rt-report-overlay {

            position: fixed;

            inset: 0;

            z-index: 99999;

            display: flex;

            align-items: center;

            justify-content: center;

            background:
                rgba(0,0,0,.72);

            backdrop-filter:
                blur(8px);

        }

        .rt-report-panel {

            width: min(
                900px,
                90vw
            );

            max-height: 85vh;

            overflow: auto;

            padding: 24px;

            border-radius: 14px;

            background:
                #10151d;

            border:
                1px solid rgba(255,255,255,.14);

            box-shadow:
                0 30px 80px rgba(0,0,0,.55);

            color:
                #f2f5f8;

        }

        .rt-report-panel h2 {

            margin:
                0 0 6px;

        }

        .rt-report-subtitle {

            opacity:
                .65;

            margin-bottom:
                18px;

            font-size:
                13px;

        }

        .rt-report-table {

            width:
                100%;

            border-collapse:
                collapse;

        }

        .rt-report-table td {

            padding:
                10px 12px;

            border-bottom:
                1px solid
                rgba(255,255,255,.08);

            vertical-align:
                top;

        }

        .rt-report-table td:first-child {

            width:
                32%;

            font-weight:
                600;

            opacity:
                .8;

        }

        .rt-report-close {

            margin-top:
                20px;

            padding:
                9px 18px;

            border:
                1px solid
                rgba(255,255,255,.18);

            border-radius:
                7px;

            background:
                rgba(255,255,255,.08);

            color:
                inherit;

            cursor:
                pointer;

        }

    `;

    document.head.appendChild(style);


})();
"""


REPORT_JS.write_text(
    report_code.strip() + "\n",
    encoding="utf-8"
)

print("[CREATED] reports-final.js")


# ------------------------------------------------------------
# 7. ADD FINAL REPORT SCRIPT
# ------------------------------------------------------------

# Remove any existing reports-final reference
html = re.sub(
    r'<script[^>]+src=["\'][^"\']*reports-final\.js["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)

report_tag = '<script src="reports-final.js"></script>'

if re.search(
    r"</body>",
    html,
    flags=re.IGNORECASE
):

    html = re.sub(
        r"</body>",
        f"    {report_tag}\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html += "\n" + report_tag + "\n"

print("[OK] reports-final.js loaded exactly once")


# ------------------------------------------------------------
# 8. WRITE FINAL HTML
# ------------------------------------------------------------

final_html = INDEX.read_text(
    encoding="utf-8"
)

# The previous versions may have changed the in-memory HTML.
# Re-apply the intended final HTML content here.
#
# We use the current cleaned HTML variable rather than
# rebuilding the dashboard.

final_html = html

INDEX.write_text(
    final_html,
    encoding="utf-8"
)


# ------------------------------------------------------------
# 9. FINAL VALIDATION
# ------------------------------------------------------------

final_content = INDEX.read_text(
    encoding="utf-8"
)


realtime_count = len(
    re.findall(
        r"realtime-monitor\.js",
        final_content,
        flags=re.IGNORECASE
    )
)

report_count = len(
    re.findall(
        r"reports-final\.js",
        final_content,
        flags=re.IGNORECASE
    )
)


print("\n============================================================")
print(" VALIDATION")
print("============================================================")

print(
    f"realtime-monitor.js references : {realtime_count}"
)

print(
    f"reports-final.js references     : {report_count}"
)

print(
    f"app.js exists                  : {APP_JS.exists()}"
)

print(
    f"realtime-monitor.js exists     : {REALTIME_JS.exists()}"
)

print(
    f"reports-final.js exists        : {REPORT_JS.exists()}"
)


if realtime_count != 1:

    print(
        "\n[WARNING] realtime-monitor.js should appear exactly once."
    )

else:

    print(
        "[OK] Realtime graph script preserved."
    )


if report_count != 1:

    print(
        "[WARNING] reports-final.js should appear exactly once."
    )

else:

    print(
        "[OK] Real report engine installed."
    )


print("\n============================================================")
print(" DONE")
print("============================================================")

print("\nBackend files were NOT changed.")
print("app.js was NOT changed.")
print("Existing realtime graph was preserved.")
print("Only report/polish layers were cleaned.")
print("\nRestart your CAP server and hard-refresh the browser:")
print("  Ctrl + Shift + R")
print()
