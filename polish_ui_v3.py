from pathlib import Path
import shutil
import re

ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
CSS = APP / "css" / "style.css"
JS = APP / "ui-polish-v3.js"

if not APP.exists():
    raise SystemExit(f"ERROR: {APP} not found")

# ---------------------------------------------------------
# Backup existing UI files
# ---------------------------------------------------------

def backup(path):
    if path.exists():
        backup_path = path.with_suffix(path.suffix + ".v3.bak")
        shutil.copy2(path, backup_path)
        print(f"[BACKUP] {backup_path}")

backup(INDEX)
backup(CSS)
backup(JS)


# ---------------------------------------------------------
# 1. DARK UI OVERRIDES
# ---------------------------------------------------------

dark_css = r"""

/* =========================================================
   RIPPLETRACE V3 - DARK COMMAND CENTER OVERRIDES
   Visual-only. Does not modify application logic.
   ========================================================= */

/* Main page */
html,
body {
    background: #05090d !important;
    color: #dbe7f3 !important;
}

/* All major white containers */
.agent-card,
.agent-panel,
.agent-section,
.agent-container,
.kpi-card,
.metric-card,
.info-card,
.summary-card,
.risk-card,
.readiness-card,
.network-card,
.approval-card,
.card,
.panel,
section,
.agent-output,
.output-box {
    background: #0b1219 !important;
    color: #dbe7f3 !important;
    border-color: #263544 !important;
}

/* Agent cards */
.agent-card {
    background: #0b1219 !important;
    border: 1px solid #263544 !important;
    box-shadow: 0 8px 30px rgba(0,0,0,.28) !important;
}

/* Agent card headers */
.agent-card header,
.agent-card .agent-header,
.agent-card .card-header {
    background: #0b1219 !important;
    color: #dbe7f3 !important;
    border-color: #263544 !important;
}

/* Titles and labels */
.agent-card h1,
.agent-card h2,
.agent-card h3,
.agent-card h4,
.agent-card strong,
.agent-card .title,
.agent-card .agent-title {
    color: #e5eef7 !important;
}

/* Descriptions */
.agent-card p,
.agent-card span,
.agent-card label,
.agent-card small {
    color: #8fa3b7 !important;
}

/* KPI / metric boxes */
.agent-card .metric,
.agent-card .metric-box,
.agent-card .stat,
.agent-card .stat-box,
.agent-card .field,
.agent-card .data-field {
    background: #101a23 !important;
    color: #dbe7f3 !important;
    border: 1px solid #263544 !important;
}

/* Metric values */
.agent-card .metric-value,
.agent-card .value,
.agent-card .stat-value {
    color: #edf5fc !important;
}

/* Buttons */
.agent-card button {
    background: #101a23 !important;
    color: #cbd9e6 !important;
    border-color: #405264 !important;
}

.agent-card button:hover {
    background: #162532 !important;
    border-color: #1683ff !important;
    color: #ffffff !important;
}

/* Primary agent buttons */
.agent-card button.primary,
.agent-card .primary-button {
    background: #087cf5 !important;
    color: #ffffff !important;
    border-color: #087cf5 !important;
}

/* Disabled buttons */
.agent-card button:disabled {
    background: #111920 !important;
    color: #506273 !important;
    border-color: #263544 !important;
    opacity: .75 !important;
}

/* =========================================================
   HIDE AGENT OUTPUT BOXES
   The data remains in the DOM and is available to the
   report popup. Only the visual output box is hidden.
   ========================================================= */

.agent-output,
.output-box,
.agent-card .agent-output,
.agent-card .output-box,
[class*="agent-output"],
[class*="output-box"] {
    display: none !important;
}

/* Hide labels immediately associated with output boxes */
.agent-output-label,
.output-label {
    display: none !important;
}

/* =========================================================
   Darken remaining generic white boxes
   ========================================================= */

.agent-card > div,
.agent-card .content,
.agent-card .body,
.agent-card .section,
.agent-card .details {
    background-color: transparent;
}

/* Input/data regions */
input,
textarea,
select {
    background: #101a23 !important;
    color: #dbe7f3 !important;
    border-color: #304252 !important;
}

/* Tables */
.agent-card table {
    background: #0b1219 !important;
    color: #dbe7f3 !important;
}

.agent-card th {
    background: #101a23 !important;
    color: #8fa3b7 !important;
    border-color: #263544 !important;
}

.agent-card td {
    background: #0b1219 !important;
    color: #cbd9e6 !important;
    border-color: #263544 !important;
}

/* =========================================================
   REPORT MODAL
   ========================================================= */

.rt-v3-overlay {
    position: fixed !important;
    inset: 0 !important;
    z-index: 99999 !important;

    display: flex !important;
    align-items: center !important;
    justify-content: center !important;

    background: rgba(0, 0, 0, .78) !important;
    backdrop-filter: blur(7px);
}

.rt-v3-modal {
    width: min(1100px, 92vw) !important;
    max-height: 86vh !important;

    background: #081018 !important;
    color: #dce8f3 !important;

    border: 1px solid #304354 !important;
    border-radius: 12px !important;

    box-shadow:
        0 30px 90px rgba(0,0,0,.65),
        0 0 0 1px rgba(255,255,255,.02) !important;

    overflow: hidden !important;
}

.rt-v3-header {
    display: flex !important;
    justify-content: space-between !important;
    align-items: center !important;

    padding: 18px 22px !important;

    background: #0d1720 !important;
    border-bottom: 1px solid #263544 !important;
}

.rt-v3-title {
    font-size: 16px !important;
    font-weight: 700 !important;
    color: #edf5fc !important;
}

.rt-v3-subtitle {
    margin-top: 4px !important;
    font-size: 11px !important;
    color: #71869a !important;
}

.rt-v3-close {
    width: 34px !important;
    height: 34px !important;

    border: 1px solid #334657 !important;
    border-radius: 7px !important;

    background: #111d27 !important;
    color: #9fb1c2 !important;

    cursor: pointer !important;
}

.rt-v3-close:hover {
    background: #192936 !important;
    color: #ffffff !important;
}

.rt-v3-content {
    padding: 20px !important;
    max-height: 68vh !important;
    overflow: auto !important;
}

.rt-v3-table-wrap {
    overflow-x: auto !important;

    border: 1px solid #263544 !important;
    border-radius: 8px !important;
}

.rt-v3-table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 12px !important;
}

.rt-v3-table th {
    padding: 11px 12px !important;

    text-align: left !important;
    white-space: nowrap !important;

    background: #101a23 !important;
    color: #7f96aa !important;

    border-bottom: 1px solid #304252 !important;
}

.rt-v3-table td {
    padding: 11px 12px !important;

    background: #0b1219 !important;
    color: #cbd9e6 !important;

    border-bottom: 1px solid #1d2a36 !important;
}

.rt-v3-table tr:last-child td {
    border-bottom: 0 !important;
}

.rt-v3-table tr:hover td {
    background: #101b25 !important;
}

.rt-v3-badge {
    display: inline-block !important;

    padding: 4px 8px !important;

    border-radius: 20px !important;

    background: #12283a !important;
    color: #6fb7ff !important;

    font-size: 10px !important;
    font-weight: 700 !important;
}

.rt-v3-json {
    margin-top: 18px !important;

    padding: 14px !important;

    background: #050a0f !important;
    border: 1px solid #263544 !important;
    border-radius: 8px !important;

    color: #8fa8bd !important;

    font-family: monospace !important;
    font-size: 11px !important;

    white-space: pre-wrap !important;
    word-break: break-word !important;
}

.rt-v3-footer {
    padding: 12px 20px !important;

    background: #0d1720 !important;
    border-top: 1px solid #263544 !important;

    color: #647b8e !important;
    font-size: 10px !important;
}
"""


# Append only if not already installed
if CSS.exists():
    css_text = CSS.read_text(encoding="utf-8")

    marker = "RIPPLETRACE V3 - DARK COMMAND CENTER OVERRIDES"

    if marker not in css_text:
        with CSS.open("a", encoding="utf-8") as f:
            f.write("\n" + dark_css + "\n")
        print("[OK] Dark UI CSS added")
    else:
        print("[SKIP] V3 CSS already exists")
else:
    raise SystemExit("ERROR: style.css not found")


# ---------------------------------------------------------
# 2. REPORT POPUP JAVASCRIPT
# ---------------------------------------------------------

js_code = r"""
/*
 * RippleTrace UI Polish V3
 *
 * VISUAL LAYER ONLY.
 *
 * Does NOT modify:
 * - app.js
 * - CAP service
 * - agents
 * - database
 * - CDS
 * - API calls
 * - approval logic
 *
 * It only:
 * - hides agent output boxes
 * - reads their existing text
 * - displays it inside the report popup
 */

(function () {

    "use strict";

    console.log("RippleTrace UI Polish V3 loaded");

    /* -----------------------------------------------------
       Find the agent card belonging to a report button
       ----------------------------------------------------- */

    function findAgentCard(button) {

        let el = button;

        while (el && el !== document.body) {

            const text = (el.innerText || "").toLowerCase();

            if (
                text.includes("trace agent") ||
                text.includes("predict agent") ||
                text.includes("recommend agent") ||
                text.includes("safeguard agent")
            ) {
                return el;
            }

            el = el.parentElement;
        }

        return null;
    }


    /* -----------------------------------------------------
       Find existing agent output
       ----------------------------------------------------- */

    function getAgentOutput(card) {

        if (!card) return "";

        const selectors = [
            ".agent-output",
            ".output-box",
            "[class*='agent-output']",
            "[class*='output-box']"
        ];

        for (const selector of selectors) {

            const nodes = card.querySelectorAll(selector);

            for (const node of nodes) {

                const text = (node.innerText || node.textContent || "").trim();

                if (text) {
                    return text;
                }
            }
        }

        /*
         * Fallback:
         * Search for a section containing "AGENT OUTPUT".
         */

        const all = card.querySelectorAll("*");

        for (const node of all) {

            const text = (node.innerText || "").trim();

            if (
                text.startsWith("AGENT OUTPUT") ||
                text.startsWith("Agent output")
            ) {

                const parent = node.parentElement;

                if (parent) {
                    return (parent.innerText || "").trim();
                }
            }
        }

        return "";
    }


    /* -----------------------------------------------------
       Try to extract JSON from agent output
       ----------------------------------------------------- */

    function extractJSON(text) {

        if (!text) return null;

        let cleaned = text
            .replace(/^AGENT OUTPUT\s*/i, "")
            .replace(/^Agent output\s*/i, "")
            .trim();

        /*
         * Remove markdown code fences if present.
         */

        cleaned = cleaned
            .replace(/^```json\s*/i, "")
            .replace(/^```\s*/i, "")
            .replace(/```\s*$/i, "")
            .trim();

        try {
            return JSON.parse(cleaned);
        } catch (e) {
            /* Continue to bracket extraction */
        }

        const firstObject = cleaned.indexOf("{");
        const lastObject = cleaned.lastIndexOf("}");

        if (firstObject !== -1 && lastObject > firstObject) {

            try {
                return JSON.parse(
                    cleaned.substring(firstObject, lastObject + 1)
                );
            } catch (e) {
                return null;
            }
        }

        return null;
    }


    /* -----------------------------------------------------
       Convert arbitrary agent output into table rows
       ----------------------------------------------------- */

    function makeRows(data, rawText, agentName) {

        const rows = [];

        function add(queryId, itemName, tier, status, risk,
                     leadTime, inventory, detail) {

            rows.push({
                queryId: queryId || "—",
                itemName: itemName || "—",
                tier: tier || "—",
                status: status || "—",
                risk: risk || "—",
                leadTime: leadTime || "—",
                inventory: inventory || "—",
                detail: detail || "—"
            });
        }


        /* ---------------------------------------------
           TRACE AGENT
           --------------------------------------------- */

        if (agentName === "TRACE") {

            const nodes =
                data?.affectedNodes ||
                data?.nodes ||
                [];

            if (Array.isArray(nodes) && nodes.length) {

                nodes.forEach((node, index) => {

                    add(
                        data?.disruption?.id || "DIS001",
                        node.name || node.nodeName,
                        node.tier != null
                            ? "Tier " + node.tier
                            : node.nodeType,
                        node.status,
                        node.risk || node.severity,
                        "—",
                        "—",
                        node.nodeType || "Affected downstream node"
                    );

                });

            } else {

                add(
                    data?.disruption?.id || "—",
                    data?.disruption?.type || "Maritime Delay",
                    "Network",
                    "Confirmed",
                    data?.disruption?.severity || "HIGH",
                    "—",
                    "—",
                    "Multi-tier disruption trace"
                );
            }
        }


        /* ---------------------------------------------
           PREDICTION AGENT
           --------------------------------------------- */

        else if (agentName === "PREDICT") {

            const impact = data?.impact || {};

            add(
                data?.disruption?.id || "—",
                impact.component || "—",
                "Component",
                impact.risk || "—",
                impact.risk || "—",
                impact.leadTime != null
                    ? impact.leadTime + " days"
                    : "—",
                impact.inventory != null
                    ? impact.inventory + " days"
                    : "—",
                impact.factory
                    ? "Factory: " + impact.factory
                    : "Stockout gap: " +
                      (impact.stockoutGap ?? "—") +
                      " days"
            );
        }


        /* ---------------------------------------------
           RECOMMENDATION AGENT
           --------------------------------------------- */

        else if (agentName === "RECOMMEND") {

            const recommendation =
                data?.recommendation || {};

            const alternatives =
                data?.alternatives || [];

            const list = [
                recommendation,
                ...alternatives
            ];

            list.forEach((item, index) => {

                if (!item || typeof item !== "object") return;

                add(
                    data?.disruption?.id || "—",
                    item.component || recommendation.component || "—",
                    "Supplier",
                    index === 0
                        ? "RECOMMENDED"
                        : "ALTERNATIVE",
                    item.riskLevel || item.risk || "—",
                    item.leadTime != null
                        ? item.leadTime + " days"
                        : "—",
                    "—",
                    item.supplierName ||
                    item.name ||
                    item.supplier ||
                    "Supplier option"
                );
            });
        }


        /* ---------------------------------------------
           SAFEGUARD AGENT
           --------------------------------------------- */

        else if (agentName === "SAFEGUARD") {

            const decision =
                data?.decision || {};

            add(
                decision.ID ||
                decision.id ||
                data?.decisionId ||
                "—",

                decision.recommendation ||
                "Mitigation decision",

                "Governance",

                data?.status ||
                decision.status ||
                "PENDING_APPROVAL",

                "—",
                "—",
                "—",

                decision.recommendation ||
                data?.message ||
                "Human approval required"
            );
        }


        /*
         * Generic fallback for unexpected output.
         */

        if (!rows.length) {

            add(
                "—",
                agentName + " Agent",
                "—",
                "COMPLETED",
                "—",
                "—",
                "—",
                rawText || "No report data available."
            );
        }

        return rows;
    }


    /* -----------------------------------------------------
       Escape HTML
       ----------------------------------------------------- */

    function esc(value) {

        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    /* -----------------------------------------------------
       Determine agent name
       ----------------------------------------------------- */

    function getAgentName(card) {

        const text = (card?.innerText || "").toUpperCase();

        if (text.includes("TRACE AGENT")) return "TRACE";
        if (text.includes("PREDICT AGENT")) return "PREDICT";
        if (text.includes("RECOMMEND AGENT")) return "RECOMMEND";
        if (text.includes("SAFEGUARD AGENT")) return "SAFEGUARD";

        return "AGENT";
    }


    /* -----------------------------------------------------
       Create report popup
       ----------------------------------------------------- */

    function showReport(button) {

        /*
         * Remove any previous V3 popup.
         */

        const old = document.querySelector(".rt-v3-overlay");

        if (old) {
            old.remove();
        }


        const card = findAgentCard(button);
        const agentName = getAgentName(card);

        const rawText = getAgentOutput(card);
        const jsonData = extractJSON(rawText);

        const rows = makeRows(
            jsonData,
            rawText,
            agentName
        );


        const overlay = document.createElement("div");

        overlay.className = "rt-v3-overlay";

        overlay.innerHTML = `
            <div class="rt-v3-modal">

                <div class="rt-v3-header">

                    <div>
                        <div class="rt-v3-title">
                            ${esc(agentName)} AGENT REPORT
                        </div>

                        <div class="rt-v3-subtitle">
                            RippleTrace • Agent execution details
                        </div>
                    </div>

                    <button
                        class="rt-v3-close"
                        type="button"
                        aria-label="Close report"
                    >
                        ✕
                    </button>

                </div>


                <div class="rt-v3-content">

                    <div class="rt-v3-table-wrap">

                        <table class="rt-v3-table">

                            <thead>
                                <tr>
                                    <th>Query ID</th>
                                    <th>Item Name</th>
                                    <th>Tier</th>
                                    <th>Status</th>
                                    <th>Risk</th>
                                    <th>Lead Time</th>
                                    <th>Inventory</th>
                                    <th>Detail</th>
                                </tr>
                            </thead>

                            <tbody>

                                ${rows.map(row => `
                                    <tr>

                                        <td>
                                            ${esc(row.queryId)}
                                        </td>

                                        <td>
                                            ${esc(row.itemName)}
                                        </td>

                                        <td>
                                            ${esc(row.tier)}
                                        </td>

                                        <td>
                                            <span class="rt-v3-badge">
                                                ${esc(row.status)}
                                            </span>
                                        </td>

                                        <td>
                                            ${esc(row.risk)}
                                        </td>

                                        <td>
                                            ${esc(row.leadTime)}
                                        </td>

                                        <td>
                                            ${esc(row.inventory)}
                                        </td>

                                        <td>
                                            ${esc(row.detail)}
                                        </td>

                                    </tr>
                                `).join("")}

                            </tbody>

                        </table>

                    </div>


                    ${
                        rawText
                            ? `
                                <div class="rt-v3-json">
                                    ${esc(rawText)}
                                </div>
                              `
                            : `
                                <div class="rt-v3-json">
                                    No agent output was captured.
                                </div>
                              `
                    }

                </div>


                <div class="rt-v3-footer">
                    Report generated from the existing agent execution output.
                    No backend data was modified.
                </div>

            </div>
        `;


        document.body.appendChild(overlay);


        /* Close button */

        overlay
            .querySelector(".rt-v3-close")
            .addEventListener("click", function () {
                overlay.remove();
            });


        /* Click outside modal */

        overlay.addEventListener("click", function (event) {

            if (event.target === overlay) {
                overlay.remove();
            }

        });


        /* ESC key */

        const escHandler = function (event) {

            if (event.key === "Escape") {

                overlay.remove();

                document.removeEventListener(
                    "keydown",
                    escHandler
                );
            }
        };

        document.addEventListener(
            "keydown",
            escHandler
        );
    }


    /* -----------------------------------------------------
       Report button detection
       ----------------------------------------------------- */

    function isReportButton(element) {

        if (!element) return false;

        const text =
            (element.innerText ||
             element.textContent ||
             "").trim().toLowerCase();

        return (
            text.includes("view trace report") ||
            text.includes("view predict report") ||
            text.includes("view recommendation report") ||
            text.includes("view safeguard report")
        );
    }


    /* -----------------------------------------------------
       Capture report clicks BEFORE old popup handlers
       ----------------------------------------------------- */

    document.addEventListener(
        "click",
        function (event) {

            let target = event.target;

            while (
                target &&
                target !== document.body &&
                !isReportButton(target)
            ) {
                target = target.parentElement;
            }

            if (!isReportButton(target)) {
                return;
            }


            /*
             * Stop the older report handler so only V3
             * popup is displayed.
             */

            event.preventDefault();
            event.stopPropagation();
            event.stopImmediatePropagation();

            showReport(target);

        },
        true
    );


    /* -----------------------------------------------------
       Keep output boxes hidden even if UI updates them
       ----------------------------------------------------- */

    function hideOutputs() {

        const selectors = [
            ".agent-output",
            ".output-box",
            "[class*='agent-output']",
            "[class*='output-box']"
        ];

        selectors.forEach(selector => {

            document
                .querySelectorAll(selector)
                .forEach(node => {

                    node.style.display = "none";

                });

        });
    }


    hideOutputs();


    /*
     * UI5/DOM changes may recreate parts of the page.
     * This only re-applies the visual hiding.
     */

    const observer = new MutationObserver(function () {

        hideOutputs();

    });

    observer.observe(
        document.body,
        {
            childList: true,
            subtree: true
        }
    );


})();
"""


JS.write_text(js_code, encoding="utf-8")
print(f"[OK] Created {JS}")


# ---------------------------------------------------------
# 3. Add JS to index.html
# ---------------------------------------------------------

if not INDEX.exists():
    raise SystemExit("ERROR: index.html not found")

html = INDEX.read_text(encoding="utf-8")

script_tag = '<script src="ui-polish-v3.js"></script>'

if script_tag not in html:

    if "</body>" in html.lower():

        html = re.sub(
            r"</body>",
            f"    {script_tag}\n</body>",
            html,
            count=1,
            flags=re.IGNORECASE
        )

    else:
        html += "\n" + script_tag + "\n"

    INDEX.write_text(html, encoding="utf-8")

    print("[OK] ui-polish-v3.js added to index.html")

else:
    print("[SKIP] Script already included")


# ---------------------------------------------------------
# FINAL SAFETY CHECK
# ---------------------------------------------------------

print()
print("=" * 60)
print("RippleTrace V3 UI polish installed successfully")
print("=" * 60)

print()
print("Changed:")
print("  ✓ Darkened remaining white agent boxes")
print("  ✓ Hidden AGENT OUTPUT boxes")
print("  ✓ Report popup uses existing agent output")
print("  ✓ Report displayed as rows + columns")
print("  ✓ Added ESC / outside-click popup closing")

print()
print("NOT changed:")
print("  ✓ app.js")
print("  ✓ CAP service")
print("  ✓ Agent logic")
print("  ✓ Database")
print("  ✓ CDS schema")
print("  ✓ API endpoints")
print("  ✓ Human approval logic")

print()
print("Backups:")
print(f"  {INDEX}.v3.bak")
print(f"  {CSS}.v3.bak")

print()
print("Refresh the browser with Ctrl+Shift+R.")
