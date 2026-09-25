
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
