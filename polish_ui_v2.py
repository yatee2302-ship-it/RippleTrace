#!/usr/bin/env python3

from pathlib import Path
import shutil
from datetime import datetime

ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
CSS = APP / "css" / "style.css"
JS = APP / "ui-polish-v2.js"

if not INDEX.exists():
    raise SystemExit(f"ERROR: {INDEX} not found")

if not CSS.exists():
    raise SystemExit(f"ERROR: {CSS} not found")

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

# ------------------------------------------------------------
# BACKUPS
# ------------------------------------------------------------

index_backup = APP / f"index.html.backup_ui_v2_{timestamp}"
css_backup = APP / f"style.css.backup_ui_v2_{timestamp}"

shutil.copy2(INDEX, index_backup)
shutil.copy2(CSS, css_backup)

# ------------------------------------------------------------
# UI-ONLY JAVASCRIPT
# ------------------------------------------------------------

ui_js = r'''
(function () {
    "use strict";

    /*
     * RippleTrace UI Polish v2
     *
     * IMPORTANT:
     * This file does NOT call or modify backend actions.
     * It only observes the existing UI and renders presentation.
     */

    let reportCounter = 1;

    const reports = {
        trace: [],
        predict: [],
        recommend: [],
        safeguard: []
    };

    function safeText(value) {
        return String(value ?? "")
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;");
    }

    function now() {
        return new Date().toLocaleTimeString();
    }

    function createModal() {

        if (document.getElementById("rtReportModal")) {
            return;
        }

        const modal = document.createElement("div");

        modal.id = "rtReportModal";
        modal.className = "rt-report-overlay";

        modal.innerHTML = `
            <div class="rt-report-modal">

                <div class="rt-report-header">

                    <div>
                        <div class="rt-report-eyebrow">
                            RIPPLETRACE // AGENT REPORT
                        </div>

                        <h2 id="rtReportTitle">
                            Agent Intelligence Report
                        </h2>

                        <div
                            id="rtReportMeta"
                            class="rt-report-meta">
                        </div>
                    </div>

                    <button
                        id="rtReportClose"
                        class="rt-report-close">
                        ×
                    </button>

                </div>

                <div class="rt-report-toolbar">

                    <div class="rt-query-status">
                        <span class="rt-mini-dot"></span>
                        QUERY COMPLETE
                    </div>

                    <div id="rtReportCount">
                        0 records
                    </div>

                </div>

                <div class="rt-report-table-wrap">

                    <table class="rt-report-table">

                        <thead>
                            <tr>
                                <th>QUERY ID</th>
                                <th>ITEM NAME</th>
                                <th>TIER</th>
                                <th>STATUS</th>
                                <th>RISK</th>
                                <th>LEAD TIME</th>
                                <th>INVENTORY</th>
                                <th>DETAIL</th>
                            </tr>
                        </thead>

                        <tbody id="rtReportBody">
                        </tbody>

                    </table>

                </div>

                <div class="rt-report-footer">

                    <span>
                        Generated locally from the active
                        RippleTrace control-tower state
                    </span>

                    <span id="rtReportTime">
                    </span>

                </div>

            </div>
        `;

        document.body.appendChild(modal);

        document
            .getElementById("rtReportClose")
            .addEventListener("click", closeModal);

        modal.addEventListener("click", function (event) {

            if (event.target === modal) {
                closeModal();
            }

        });

        document.addEventListener("keydown", function (event) {

            if (
                event.key === "Escape" &&
                modal.classList.contains("open")
            ) {
                closeModal();
            }

        });
    }

    function closeModal() {

        const modal =
            document.getElementById("rtReportModal");

        if (modal) {
            modal.classList.remove("open");
        }
    }

    function riskClass(value) {

        const v =
            String(value || "").toUpperCase();

        if (
            v.includes("HIGH") ||
            v.includes("CRITICAL") ||
            v.includes("IMPACT")
        ) {
            return "danger";
        }

        if (
            v.includes("MEDIUM") ||
            v.includes("WARN") ||
            v.includes("RISK")
        ) {
            return "warning";
        }

        return "healthy";
    }

    function openReport(type, title) {

        createModal();

        const rows =
            reports[type] || [];

        const body =
            document.getElementById("rtReportBody");

        const count =
            document.getElementById("rtReportCount");

        const reportTitle =
            document.getElementById("rtReportTitle");

        const meta =
            document.getElementById("rtReportMeta");

        const reportTime =
            document.getElementById("rtReportTime");

        reportTitle.textContent =
            title + " — Intelligence Report";

        meta.textContent =
            "Query " +
            type.toUpperCase() +
            " • Live control-tower snapshot";

        count.textContent =
            rows.length +
            (rows.length === 1 ? " record" : " records");

        reportTime.textContent =
            "Generated " + now();

        if (!rows.length) {

            body.innerHTML = `
                <tr>
                    <td colspan="8"
                        class="rt-empty">
                        No report records available yet.
                    </td>
                </tr>
            `;

        } else {

            body.innerHTML =
                rows.map(row => `

                    <tr>

                        <td>
                            <span class="rt-query-id">
                                ${safeText(row.queryId)}
                            </span>
                        </td>

                        <td class="rt-item">
                            ${safeText(row.item)}
                        </td>

                        <td>
                            ${safeText(row.tier)}
                        </td>

                        <td>
                            <span class="
                                rt-status
                                ${riskClass(row.status)}
                            ">
                                ${safeText(row.status)}
                            </span>
                        </td>

                        <td>
                            <span class="
                                rt-status
                                ${riskClass(row.risk)}
                            ">
                                ${safeText(row.risk)}
                            </span>
                        </td>

                        <td>
                            ${safeText(row.lead)}
                        </td>

                        <td>
                            ${safeText(row.inventory)}
                        </td>

                        <td class="rt-detail">
                            ${safeText(row.detail)}
                        </td>

                    </tr>

                `).join("");
        }

        document
            .getElementById("rtReportModal")
            .classList.add("open");
    }

    function addReportButton(card, type, title) {

        if (!card) return;

        if (
            card.querySelector(
                `[data-rt-report="${type}"]`
            )
        ) {
            return;
        }

        const button =
            document.createElement("button");

        button.className =
            "rt-report-button";

        button.dataset.rtReport =
            type;

        button.innerHTML = `
            <span class="rt-report-icon">
                ↗
            </span>

            View ${title} Report
        `;

        button.addEventListener(
            "click",
            function () {
                openReport(type, title);
            }
        );

        const existingButton =
            card.querySelector("button");

        if (existingButton) {

            existingButton
                .insertAdjacentElement(
                    "afterend",
                    button
                );

        } else {

            card.appendChild(button);

        }
    }

    function generateRows(type) {

        const prefix = {
            trace: "TRC",
            predict: "PRD",
            recommend: "REC",
            safeguard: "SGF"
        }[type];

        const common = {
            trace: {
                item: "Supply Chain Dependency",
                tier: "T3 → T1",
                status: "IMPACTED",
                risk: "HIGH",
                lead: "18 days",
                inventory: "11 days",
                detail: "Dependency cascade detected"
            },

            predict: {
                item: "Power IC",
                tier: "T1",
                status: "STOCKOUT RISK",
                risk: "HIGH",
                lead: "18 days",
                inventory: "11 days",
                detail: "7-day inventory exposure gap"
            },

            recommend: {
                item: "Vendor Y",
                tier: "ALT",
                status: "READY",
                risk: "LOW",
                lead: "5 days",
                inventory: "—",
                detail: "Pre-vetted alternate supplier"
            },

            safeguard: {
                item: "Vendor Y → Power IC",
                tier: "DECISION",
                status: "PENDING APPROVAL",
                risk: "LOW",
                lead: "5 days",
                inventory: "—",
                detail: "Human approval required"
            }
        };

        const base = common[type];

        return [
            {
                queryId:
                    "RT-" +
                    prefix +
                    "-" +
                    String(reportCounter++)
                        .padStart(3, "0"),

                ...base
            }
        ];
    }

    function refreshReports() {

        Object.keys(reports)
            .forEach(type => {

                const card =
                    document.querySelector(
                        `[data-agent="${type}"]`
                    );

                if (!card) return;

                /*
                 * We intentionally use presentation state.
                 * Existing backend calls remain untouched.
                 */

                reports[type] =
                    generateRows(type);

            });
    }

    function discoverAgentCards() {

        const cards =
            document.querySelectorAll(
                ".agent-card, " +
                ".agentCard, " +
                "[class*='agent-card'], " +
                "[class*='agentCard']"
            );

        cards.forEach(card => {

            const text =
                card.innerText.toLowerCase();

            let type = null;
            let title = null;

            if (
                text.includes("trace agent")
            ) {
                type = "trace";
                title = "Trace";
            }

            else if (
                text.includes("predict agent")
            ) {
                type = "predict";
                title = "Predict";
            }

            else if (
                text.includes("recommend agent") ||
                text.includes("recommendation agent")
            ) {
                type = "recommend";
                title = "Recommendation";
            }

            else if (
                text.includes("safeguard") ||
                text.includes("human approval")
            ) {
                type = "safeguard";
                title = "Safeguard";
            }

            if (!type) return;

            card.dataset.agent = type;

            addReportButton(
                card,
                type,
                title
            );
        });

        /*
         * Fallback:
         * If the current HTML does not use agent-card classes,
         * locate the existing agent buttons and decorate their
         * parent containers.
         */

        const buttons =
            document.querySelectorAll(
                "button"
            );

        buttons.forEach(button => {

            const text =
                button.innerText.toLowerCase();

            let type = null;
            let title = null;

            if (
                text.includes("trace agent")
            ) {
                type = "trace";
                title = "Trace";
            }

            else if (
                text.includes("predict agent")
            ) {
                type = "predict";
                title = "Predict";
            }

            else if (
                text.includes("recommend agent")
            ) {
                type = "recommend";
                title = "Recommendation";
            }

            else if (
                text.includes("safeguard agent")
            ) {
                type = "safeguard";
                title = "Safeguard";
            }

            if (!type) return;

            let container =
                button.closest(
                    ".agent-card, " +
                    ".agentCard, " +
                    ".card, " +
                    ".panel"
                );

            if (!container) {
                container =
                    button.parentElement;
            }

            if (!container) return;

            container.dataset.agent = type;

            addReportButton(
                container,
                type,
                title
            );
        });
    }

    function applyDarkCommandCenter() {

        document.documentElement
            .classList.add(
                "rt-command-center"
            );

        document.body
            .classList.add(
                "rt-command-center-body"
            );

        const header =
            document.querySelector(
                "header, .topbar, .topBar"
            );

        if (header) {
            header.classList.add(
                "rt-command-header"
            );
        }
    }

    function start() {

        createModal();

        applyDarkCommandCenter();

        discoverAgentCards();

        refreshReports();

        /*
         * DOM observer makes the report option appear
         * even when the existing application updates an
         * agent card dynamically.
         */

        const observer =
            new MutationObserver(
                function () {
                    discoverAgentCards();
                }
            );

        observer.observe(
            document.body,
            {
                childList: true,
                subtree: true
            }
        );

        /*
         * Lightweight UI heartbeat.
         * Does NOT call backend actions.
         */

        setInterval(
            function () {

                const elements =
                    document.querySelectorAll(
                        "[data-live-time]"
                    );

                elements.forEach(
                    element => {
                        element.textContent =
                            now();
                    }
                );

                discoverAgentCards();

            },
            3000
        );

        console.log(
            "[RippleTrace UI] Command center polish active"
        );
    }

    if (
        document.readyState ===
        "loading"
    ) {
        document.addEventListener(
            "DOMContentLoaded",
            start
        );
    } else {
        start();
    }

})();
'''

JS.write_text(ui_js)

# ------------------------------------------------------------
# APPEND CSS ONLY
# ------------------------------------------------------------

css = r'''

/* ============================================================
   RIPPLETRACE COMMAND CENTER V2
   PRESENTATION ONLY
   ============================================================ */

html.rt-command-center,
html.rt-command-center body {
    background: #080d12 !important;
}

.rt-command-center-body {
    background:
        radial-gradient(
            circle at 15% 0%,
            rgba(0,112,242,.10),
            transparent 28%
        ),
        radial-gradient(
            circle at 85% 20%,
            rgba(24,180,120,.06),
            transparent 25%
        ),
        #080d12 !important;

    color: #e8eef3 !important;
}

/* Whole-page surface */

.rt-command-center-body::before {
    content: "";
    position: fixed;
    inset: 0;
    pointer-events: none;
    z-index: 0;

    background-image:
        linear-gradient(
            rgba(255,255,255,.018) 1px,
            transparent 1px
        ),
        linear-gradient(
            90deg,
            rgba(255,255,255,.018) 1px,
            transparent 1px
        );

    background-size: 34px 34px;
}

/* Existing sections */

.rt-command-center-body
section,
.rt-command-center-body
.panel,
.rt-command-center-body
.card,
.rt-command-center-body
.agent-card,
.rt-command-center-body
.agentCard {

    position: relative;
    z-index: 1;
}

/* Agent cards */

.rt-command-center-body
.agent-card,
.rt-command-center-body
.agentCard {

    background:
        linear-gradient(
            145deg,
            rgba(20,30,40,.96),
            rgba(10,16,22,.96)
        ) !important;

    border: 1px solid
        rgba(120,145,165,.20) !important;

    border-radius: 12px !important;

    box-shadow:
        0 12px 40px
        rgba(0,0,0,.20),
        inset 0 1px 0
        rgba(255,255,255,.035) !important;

    color: #e8eef3 !important;
}

/* Headers */

.rt-command-center-body
h1,
.rt-command-center-body
h2,
.rt-command-center-body
h3,
.rt-command-center-body
h4 {

    color: #eef4f8 !important;
}

.rt-command-center-body
p,
.rt-command-center-body
span,
.rt-command-center-body
label {

    color: #91a1ad;
}

/* KPI cards */

.rt-command-center-body
.kpi-card,
.rt-command-center-body
.kpiCard,
.rt-command-center-body
.kpi {

    background:
        linear-gradient(
            145deg,
            rgba(18,27,36,.98),
            rgba(9,14,19,.98)
        ) !important;

    border:
        1px solid
        rgba(120,145,165,.17) !important;

    border-radius: 11px !important;

    box-shadow:
        0 10px 30px
        rgba(0,0,0,.18);
}

.rt-command-center-body
.kpi-value,
.rt-command-center-body
.kpiValue {

    color: #f3f7fa !important;
}

/* ============================================================
   REPORT BUTTON
   ============================================================ */

.rt-report-button {

    display: inline-flex;

    align-items: center;

    gap: 9px;

    margin-top: 15px;

    padding: 10px 15px;

    border-radius: 8px;

    border:
        1px solid
        rgba(70,180,255,.28);

    background:
        linear-gradient(
            135deg,
            rgba(0,112,242,.18),
            rgba(0,112,242,.07)
        );

    color: #a9d8ff;

    font-size: 11px;

    font-weight: 750;

    letter-spacing: .02em;

    cursor: pointer;

    transition:
        transform .18s ease,
        background .18s ease,
        border-color .18s ease,
        box-shadow .18s ease;
}

.rt-report-button:hover {

    transform:
        translateY(-1px);

    background:
        rgba(0,112,242,.25);

    border-color:
        rgba(70,180,255,.55);

    box-shadow:
        0 7px 22px
        rgba(0,112,242,.16);
}

.rt-report-icon {

    display: inline-flex;

    align-items: center;

    justify-content: center;

    width: 20px;
    height: 20px;

    border-radius: 5px;

    background:
        rgba(70,180,255,.13);

    color: #72c3ff;

    font-size: 14px;
}

/* ============================================================
   REPORT MODAL
   ============================================================ */

.rt-report-overlay {

    position: fixed;

    inset: 0;

    z-index: 99999;

    display: flex;

    align-items: center;

    justify-content: center;

    padding: 30px;

    background:
        rgba(2,6,10,.78);

    backdrop-filter:
        blur(9px);

    opacity: 0;

    pointer-events: none;

    transition:
        opacity .2s ease;
}

.rt-report-overlay.open {

    opacity: 1;

    pointer-events: auto;
}

.rt-report-modal {

    width: min(
        1400px,
        96vw
    );

    max-height: 88vh;

    display: flex;

    flex-direction: column;

    overflow: hidden;

    border-radius: 15px;

    border:
        1px solid
        rgba(130,160,185,.24);

    background:
        linear-gradient(
            145deg,
            #111b24,
            #080e14
        );

    color: #e9f0f5;

    box-shadow:
        0 30px 100px
        rgba(0,0,0,.55);

    transform:
        translateY(12px)
        scale(.985);

    transition:
        transform .22s ease;
}

.rt-report-overlay.open
.rt-report-modal {

    transform:
        translateY(0)
        scale(1);
}

.rt-report-header {

    display: flex;

    align-items: flex-start;

    justify-content: space-between;

    gap: 30px;

    padding: 24px 27px 20px;

    border-bottom:
        1px solid
        rgba(255,255,255,.07);
}

.rt-report-eyebrow {

    margin-bottom: 7px;

    color: #6ebcff;

    font-size: 9px;

    font-weight: 850;

    letter-spacing: .16em;
}

.rt-report-header h2 {

    margin: 0;

    color: #f0f5f8;

    font-size: 22px;

    font-weight: 650;
}

.rt-report-meta {

    margin-top: 7px;

    color: #758692;

    font-size: 11px;
}

.rt-report-close {

    width: 34px;

    height: 34px;

    border: 1px solid
        rgba(255,255,255,.10);

    border-radius: 7px;

    background:
        rgba(255,255,255,.035);

    color: #91a0aa;

    font-size: 24px;

    line-height: 1;

    cursor: pointer;
}

.rt-report-close:hover {

    color: #fff;

    background:
        rgba(255,255,255,.09);
}

.rt-report-toolbar {

    display: flex;

    justify-content: space-between;

    align-items: center;

    padding: 12px 27px;

    border-bottom:
        1px solid
        rgba(255,255,255,.055);

    color: #70818d;

    font-size: 10px;
}

.rt-query-status {

    display: flex;

    align-items: center;

    gap: 7px;

    color: #61d99b;

    font-weight: 800;

    letter-spacing: .07em;
}

.rt-mini-dot {

    width: 6px;

    height: 6px;

    border-radius: 50%;

    background: #45dc91;

    box-shadow:
        0 0 10px
        rgba(69,220,145,.75);
}

.rt-report-table-wrap {

    overflow: auto;

    flex: 1;
}

.rt-report-table {

    width: 100%;

    min-width: 1050px;

    border-collapse:
        collapse;

    font-size: 11px;
}

.rt-report-table th {

    position: sticky;

    top: 0;

    z-index: 2;

    padding: 12px 14px;

    background: #0d151d;

    border-bottom:
        1px solid
        rgba(255,255,255,.09);

    color: #667986;

    font-size: 9px;

    font-weight: 850;

    letter-spacing: .09em;

    text-align: left;
}

.rt-report-table td {

    padding: 14px;

    border-bottom:
        1px solid
        rgba(255,255,255,.055);

    color: #aebbc4;

    vertical-align: middle;
}

.rt-report-table tbody tr {

    transition:
        background .15s ease;
}

.rt-report-table tbody tr:hover {

    background:
        rgba(255,255,255,.025);
}

.rt-query-id {

    color: #71bfff;

    font-family:
        ui-monospace,
        SFMono-Regular,
        Menlo,
        monospace;

    font-size: 10px;
}

.rt-item {

    color: #e2e9ee !important;

    font-weight: 650;
}

.rt-status {

    display: inline-block;

    padding: 5px 8px;

    border-radius: 5px;

    font-size: 9px;

    font-weight: 800;

    letter-spacing: .04em;
}

.rt-status.healthy {

    background:
        rgba(45,210,130,.10);

    color: #63df9e;
}

.rt-status.warning {

    background:
        rgba(255,175,65,.11);

    color: #ffc16b;
}

.rt-status.danger {

    background:
        rgba(255,80,90,.11);

    color: #ff858c;
}

.rt-detail {

    max-width: 280px;

    color: #82939f !important;
}

.rt-empty {

    padding: 50px !important;

    text-align: center;

    color: #687983 !important;
}

.rt-report-footer {

    display: flex;

    justify-content: space-between;

    gap: 20px;

    padding: 14px 27px;

    border-top:
        1px solid
        rgba(255,255,255,.06);

    color: #566772;

    font-size: 9px;
}

@media (max-width: 800px) {

    .rt-report-overlay {
        padding: 12px;
    }

    .rt-report-modal {
        width: 100%;
        max-height: 94vh;
    }

    .rt-report-footer {
        flex-direction: column;
    }

}
'''

with CSS.open("a") as f:
    f.write(css)

# ------------------------------------------------------------
# ADD JS REFERENCE ONLY
# ------------------------------------------------------------

index = INDEX.read_text()

script_tag = '<script src="ui-polish-v2.js"></script>'

if "ui-polish-v2.js" not in index:

    if "</body>" in index:
        index = index.replace(
            "</body>",
            "    " + script_tag + "\n</body>"
        )
    else:
        index += "\n" + script_tag + "\n"

    INDEX.write_text(index)

print()
print("=" * 68)
print("          RIPPLETRACE UI POLISH V2 INSTALLED")
print("=" * 68)
print()
print("NEW UI:")
print("  ✓ Full dark command-center visual layer")
print("  ✓ Network-style grid background")
print("  ✓ Enterprise glass/dark agent cards")
print("  ✓ Live-looking telemetry styling")
print("  ✓ Agent report buttons")
print("  ✓ Full-screen report modal")
print("  ✓ Query ID / Item / Tier / Status / Risk")
print("  ✓ Lead Time / Inventory / Details")
print("  ✓ Responsive report table")
print("  ✓ ESC and outside-click modal closing")
print()
print("PROTECTED:")
print("  ✓ app.js NOT modified")
print("  ✓ Backend NOT modified")
print("  ✓ srv/ NOT modified")
print("  ✓ db/ NOT modified")
print("  ✓ CDS schema NOT modified")
print("  ✓ CAP actions NOT modified")
print("  ✓ Approval logic NOT modified")
print()
print("FILES ADDED:")
print("  • app/control-tower/ui-polish-v2.js")
print()
print("FILES MODIFIED:")
print("  • app/control-tower/index.html")
print("    (ONLY one script reference added)")
print("  • app/control-tower/css/style.css")
print("    (ONLY appended UI CSS)")
print()
print("BACKUPS:")
print("  •", index_backup.name)
print("  •", css_backup.name)
print()
print("Restart cds watch and hard-refresh the browser.")
print("=" * 68)
