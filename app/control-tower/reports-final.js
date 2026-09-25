(function () {
    "use strict";

    console.log("RippleTrace Report Table Engine loaded");

    /*
     * IMPORTANT:
     * This file ONLY handles the report popup.
     *
     * It does NOT:
     * - create report buttons
     * - remove report buttons
     * - modify app.js
     * - modify agent execution
     * - modify realtime graph
     * - modify backend
     */

    const reportData = {
        trace: null,
        predict: null,
        recommend: null,
        safeguard: null
    };

    /* =========================================================
       NORMALIZE CAP RESPONSE
       ========================================================= */

    function normalizeResponse(data) {

        /*
         * CAP action returns:
         *
         * {
         *   value: "{\"disruption\":...}"
         * }
         *
         * OR directly:
         *
         * "{\"disruption\":...}"
         *
         * OR already parsed object.
         */

        if (data === null || data === undefined) {
            return null;
        }

        if (typeof data === "string") {
            try {
                return JSON.parse(data);
            } catch (e) {
                console.warn(
                    "Report response was a string but not JSON",
                    data
                );

                return {
                    raw: data
                };
            }
        }

        if (
            typeof data === "object" &&
            typeof data.value === "string"
        ) {
            try {
                return JSON.parse(data.value);
            } catch (e) {
                return data;
            }
        }

        return data;
    }


    /* =========================================================
       CAPTURE REAL AGENT RESPONSES
       ========================================================= */

    const originalFetch = window.fetch;

    window.fetch = async function () {

        const response =
            await originalFetch.apply(this, arguments);

        try {

            const request = arguments[0];

            let url = "";

            if (typeof request === "string") {
                url = request;
            } else if (request && request.url) {
                url = request.url;
            }

            let agent = null;

            if (url.includes("triggerCascade")) {
                agent = "trace";
            }

            else if (url.includes("triggerPrediction")) {
                agent = "predict";
            }

            else if (url.includes("triggerMitigation")) {
                agent = "recommend";
            }

            else if (url.includes("triggerSafeguard")) {
                agent = "safeguard";
            }

            if (agent) {

                const clone = response.clone();

                clone.json()
                    .then(function (data) {

                        const normalized =
                            normalizeResponse(data);

                        reportData[agent] = normalized;

                    })
                    .catch(function (error) {

                        console.warn(
                            "Could not capture report response:",
                            error
                        );

                    });
            }

        } catch (error) {

            console.warn(
                "Report capture error:",
                error
            );

        }

        return response;
    };


    /* =========================================================
       AGENT DETECTION
       ========================================================= */

    function getAgentFromText(text) {

        const value =
            String(text || "").toLowerCase();

        if (
            value.includes("trace") &&
            value.includes("report")
        ) {
            return "trace";
        }

        if (
            value.includes("predict") &&
            value.includes("report")
        ) {
            return "predict";
        }

        if (
            value.includes("recommend") &&
            value.includes("report")
        ) {
            return "recommend";
        }

        if (
            value.includes("safeguard") &&
            value.includes("report")
        ) {
            return "safeguard";
        }

        return null;
    }


    /* =========================================================
       FIND AGENT CARD
       ========================================================= */

    function findAgentCard(button) {

        let element = button;

        while (
            element &&
            element !== document.body
        ) {

            const text =
                (element.innerText || "")
                    .toLowerCase();

            if (
                text.includes("trace agent") ||
                text.includes("predict agent") ||
                text.includes("recommend agent") ||
                text.includes("safeguard agent")
            ) {
                return element;
            }

            element =
                element.parentElement;
        }

        return null;
    }


    /* =========================================================
       FALLBACK: READ EXISTING AGENT OUTPUT
       ========================================================= */

    function getOutputFromCard(card) {

        if (!card) {
            return "";
        }

        const selectors = [
            ".agent-output",
            ".output-box",
            "[class*='agent-output']",
            "[class*='output-box']"
        ];

        for (const selector of selectors) {

            const nodes =
                card.querySelectorAll(selector);

            for (const node of nodes) {

                const text =
                    (
                        node.innerText ||
                        node.textContent ||
                        ""
                    ).trim();

                if (text) {
                    return text;
                }
            }
        }

        return "";
    }


    /* =========================================================
       TRY TO RECOVER JSON FROM OUTPUT
       ========================================================= */

    function extractOutputJSON(text) {

        if (!text) {
            return null;
        }

        const clean =
            text.trim();

        /*
         * Direct JSON
         */

        try {
            return JSON.parse(clean);
        } catch (e) {
            // Continue with fallback.
        }

        /*
         * Look for the first { ... } block.
         */

        const firstBrace =
            clean.indexOf("{");

        const lastBrace =
            clean.lastIndexOf("}");

        if (
            firstBrace !== -1 &&
            lastBrace > firstBrace
        ) {

            const possibleJSON =
                clean.substring(
                    firstBrace,
                    lastBrace + 1
                );

            try {
                return JSON.parse(possibleJSON);
            } catch (e) {
                // Not valid JSON.
            }
        }

        return null;
    }


    /* =========================================================
       BUILD REPORT ROWS
       ========================================================= */

    function buildRows(agent, data) {

        const rows = [];

        function add(
            queryId,
            itemName,
            tier,
            status,
            risk,
            leadTime,
            inventory,
            detail
        ) {

            rows.push({
                queryId:
                    queryId ?? "—",

                itemName:
                    itemName ?? "—",

                tier:
                    tier ?? "—",

                status:
                    status ?? "—",

                risk:
                    risk ?? "—",

                leadTime:
                    leadTime ?? "—",

                inventory:
                    inventory ?? "—",

                detail:
                    detail ?? "—"
            });
        }


        /* =====================================================
           TRACE AGENT
           ===================================================== */

        if (agent === "trace") {

            const disruption =
                data?.disruption || {};

            const nodes =
                data?.affectedNodes || [];

            if (nodes.length) {

                nodes.forEach(function (node) {

                    add(

                        disruption.id ||
                        "—",

                        node.name ||
                        "—",

                        node.tier ??
                        "—",

                        node.status ||
                        "Affected",

                        node.status === "Critical"
                            ? "HIGH"
                            : "—",

                        "—",

                        "—",

                        (
                            node.nodeType ||
                            "Supply Chain Node"
                        ) +
                        " • Confidence " +
                        (
                            node.confidence ??
                            "—"
                        ) + "%"
                    );

                });

            } else {

                add(

                    disruption.id ||
                    "—",

                    disruption.type ||
                    "Maritime Delay",

                    "—",

                    disruption.severity ||
                    "—",

                    disruption.severity ||
                    "—",

                    disruption.delayDays != null
                        ? disruption.delayDays +
                          " days"
                        : "—",

                    "—",

                    disruption.location ||
                    "—"
                );
            }
        }


        /* =====================================================
           PREDICT AGENT
           ===================================================== */

        else if (agent === "predict") {

            const disruption =
                data?.disruption || {};

            const impact =
                data?.impact || {};

            add(

                disruption.id ||
                "—",

                impact.component ||
                "—",

                "—",

                impact.risk ||
                disruption.severity ||
                "—",

                impact.risk ||
                disruption.severity ||
                "—",

                impact.leadTime != null
                    ? impact.leadTime + " days"
                    : "—",

                impact.inventory != null
                    ? impact.inventory + " days"
                    : "—",

                (
                    impact.factory ||
                    "—"
                ) +
                " • Stockout gap: " +
                (
                    impact.stockoutGap ??
                    "—"
                ) +
                " days"
            );
        }


        /* =====================================================
           RECOMMENDATION AGENT
           ===================================================== */

        else if (agent === "recommend") {

            const disruption =
                data?.disruption || {};

            const recommendation =
                data?.recommendation || {};

            const alternatives =
                data?.alternatives || [];

            const list = [
                recommendation,
                ...alternatives
            ];

            list.forEach(function (item, index) {

                if (
                    !item ||
                    typeof item !== "object"
                ) {
                    return;
                }

                add(

                    disruption.id ||
                    "—",

                    item.component ||
                    "—",

                    "Supplier",

                    index === 0
                        ? "RECOMMENDED"
                        : "ALTERNATIVE",

                    item.riskLevel ||
                    item.risk ||
                    "—",

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


        /* =====================================================
           SAFEGUARD AGENT
           ===================================================== */

        else if (agent === "safeguard") {

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


        /* =====================================================
           GENERIC FALLBACK
           ===================================================== */

        if (!rows.length) {

            add(

                data?.disruption?.id ||
                "—",

                agent.toUpperCase() +
                " Agent",

                "—",

                "COMPLETED",

                "—",

                "—",

                "—",

                "Report data available"
            );
        }

        return rows;
    }


    /* =========================================================
       ESCAPE HTML
       ========================================================= */

    function escapeHTML(value) {

        return String(
            value ?? ""
        )
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }


    /* =========================================================
       POPUP
       ========================================================= */

    function showReport(button) {

        const agent =
            getAgentFromText(
                button.innerText ||
                button.textContent
            );

        if (!agent) {
            return;
        }

        /*
         * Prefer the REAL backend response.
         */

        let data =
            reportData[agent];


        /*
         * Fallback to visible agent output.
         */

        if (!data) {

            const card =
                findAgentCard(button);

            const output =
                getOutputFromCard(card);

            data =
                extractOutputJSON(output);

            if (data) {
                reportData[agent] = data;
            }
        }


        if (!data) {

            alert(
                "Run the " +
                agent.toUpperCase() +
                " Agent first."
            );

            return;
        }


        /*
         * Remove only our previous popup.
         */

        const old =
            document.querySelector(
                ".rippletrace-report-overlay"
            );

        if (old) {
            old.remove();
        }


        const rows =
            buildRows(
                agent,
                data
            );


        const titles = {

            trace:
                "TRACE AGENT REPORT",

            predict:
                "PREDICT AGENT REPORT",

            recommend:
                "RECOMMENDATION AGENT REPORT",

            safeguard:
                "SAFEGUARD AGENT REPORT"
        };


        const subtitles = {

            trace:
                "Multi-tier dependency analysis",

            predict:
                "Inventory & stockout prediction",

            recommend:
                "Mitigation recommendation",

            safeguard:
                "Human approval & decision"
        };


        const overlay =
            document.createElement("div");

        overlay.className =
            "rippletrace-report-overlay";


        overlay.innerHTML = `

            <div class="rippletrace-report-modal">

                <div class="rippletrace-report-header">

                    <div>

                        <div class="rippletrace-report-title">
                            ${escapeHTML(titles[agent])}
                        </div>

                        <div class="rippletrace-report-subtitle">
                            ${escapeHTML(subtitles[agent])}
                        </div>

                    </div>

                    <button
                        type="button"
                        class="rippletrace-report-close"
                        aria-label="Close report"
                    >
                        ×
                    </button>

                </div>


                <div class="rippletrace-report-content">

                    <div class="rippletrace-report-table-wrap">

                        <table class="rippletrace-report-table">

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

                                ${rows.map(function (row) {

                                    return `

                                        <tr>

                                            <td>
                                                ${escapeHTML(row.queryId)}
                                            </td>

                                            <td>
                                                ${escapeHTML(row.itemName)}
                                            </td>

                                            <td>
                                                ${escapeHTML(row.tier)}
                                            </td>

                                            <td>
                                                <span class="rippletrace-report-badge">
                                                    ${escapeHTML(row.status)}
                                                </span>
                                            </td>

                                            <td>
                                                ${escapeHTML(row.risk)}
                                            </td>

                                            <td>
                                                ${escapeHTML(row.leadTime)}
                                            </td>

                                            <td>
                                                ${escapeHTML(row.inventory)}
                                            </td>

                                            <td>
                                                ${escapeHTML(row.detail)}
                                            </td>

                                        </tr>

                                    `;

                                }).join("")}

                            </tbody>

                        </table>

                    </div>

                </div>


                <div class="rippletrace-report-footer">

                    <span>
                        RippleTrace • Agent Execution Report
                    </span>

                    <button
                        type="button"
                        class="rippletrace-report-footer-close"
                    >
                        Close
                    </button>

                </div>

            </div>
        `;


        document.body.appendChild(
            overlay
        );


        /* =====================================================
           CLOSE BUTTONS
           ===================================================== */

        overlay
            .querySelector(
                ".rippletrace-report-close"
            )
            .addEventListener(
                "click",
                function () {
                    overlay.remove();
                }
            );


        overlay
            .querySelector(
                ".rippletrace-report-footer-close"
            )
            .addEventListener(
                "click",
                function () {
                    overlay.remove();
                }
            );


        overlay.addEventListener(
            "click",
            function (event) {

                if (
                    event.target === overlay
                ) {
                    overlay.remove();
                }

            }
        );


        function escapeHandler(event) {

            if (event.key === "Escape") {

                overlay.remove();

                document.removeEventListener(
                    "keydown",
                    escapeHandler
                );
            }
        }


        document.addEventListener(
            "keydown",
            escapeHandler
        );
    }


    function showAllAgentReport(results) {

        const agents = [
            ["trace", "TRACE AGENT"],
            ["predict", "PREDICT AGENT"],
            ["recommend", "RECOMMENDATION AGENT"],
            ["safeguard", "SAFEGUARD AGENT"]
        ];

        const rows = agents.flatMap(function ([agent, label]) {
            return buildRows(agent, results[agent]).map(function (row) {
                return { agent: label, ...row };
            });
        });

        const old = document.querySelector(".rippletrace-report-overlay");
        if (old) old.remove();

        const overlay = document.createElement("div");
        overlay.className = "rippletrace-report-overlay";
        overlay.innerHTML = `
            <div class="rippletrace-report-modal">
                <div class="rippletrace-report-header">
                    <div>
                        <div class="rippletrace-report-title">ALL AGENT REPORTS</div>
                        <div class="rippletrace-report-subtitle">Sequential execution results and governed mitigation decision</div>
                    </div>
                    <button type="button" class="rippletrace-report-close" aria-label="Close report">×</button>
                </div>
                <div class="rippletrace-report-content">
                    <div class="rippletrace-report-table-wrap">
                        <table class="rippletrace-report-table">
                            <thead><tr>
                                <th>Agent</th><th>Query ID</th><th>Item Name</th><th>Tier</th>
                                <th>Status</th><th>Risk</th><th>Lead Time</th><th>Inventory</th><th>Detail</th>
                            </tr></thead>
                            <tbody>${rows.map(function (row) { return `
                                <tr>
                                    <td>${escapeHTML(row.agent)}</td>
                                    <td>${escapeHTML(row.queryId)}</td>
                                    <td>${escapeHTML(row.itemName)}</td>
                                    <td>${escapeHTML(row.tier)}</td>
                                    <td><span class="rippletrace-report-badge">${escapeHTML(row.status)}</span></td>
                                    <td>${escapeHTML(row.risk)}</td>
                                    <td>${escapeHTML(row.leadTime)}</td>
                                    <td>${escapeHTML(row.inventory)}</td>
                                    <td>${escapeHTML(row.detail)}</td>
                                </tr>`; }).join("")}</tbody>
                        </table>
                    </div>
                </div>
                <div class="rippletrace-report-footer">
                    <span>RippleTrace • All Agent Execution Report</span>
                    <button type="button" class="rippletrace-report-footer-close">Close</button>
                </div>
            </div>`;

        document.body.appendChild(overlay);

        const close = function () { overlay.remove(); };
        overlay.querySelector(".rippletrace-report-close").addEventListener("click", close);
        overlay.querySelector(".rippletrace-report-footer-close").addEventListener("click", close);
        overlay.addEventListener("click", function (event) {
            if (event.target === overlay) close();
        });
        document.addEventListener("keydown", function escapeHandler(event) {
            if (event.key === "Escape") {
                close();
                document.removeEventListener("keydown", escapeHandler);
            }
        });
    }

    window.showAllAgentReport = showAllAgentReport;


    /* =========================================================
       EXISTING REPORT BUTTON HANDLER
       ========================================================= */

    document.addEventListener(
        "click",
        function (event) {

            let target =
                event.target;

            while (
                target &&
                target !== document.body
            ) {

                const text =
                    (
                        target.innerText ||
                        target.textContent ||
                        ""
                    ).trim().toLowerCase();

                if (
                    text === "view trace report" ||
                    text === "view predict report" ||
                    text === "view recommendation report" ||
                    text === "view safeguard report" ||
                    (
                        text.includes("view") &&
                        text.includes("report")
                    )
                ) {

                    /*
                     * Stop ONLY the old report popup/action.
                     *
                     * The actual agent buttons are untouched.
                     */

                    event.preventDefault();
                    event.stopPropagation();
                    event.stopImmediatePropagation();

                    showReport(target);

                    return;
                }

                target =
                    target.parentElement;
            }

        },
        true
    );


    /* =========================================================
       POPUP CSS
       ========================================================= */

    const style =
        document.createElement("style");

    style.id =
        "rippletrace-report-popup-style";


    style.textContent = `

        .rippletrace-report-overlay {

            position: fixed;

            inset: 0;

            z-index: 999999;

            display: flex;

            align-items: center;

            justify-content: center;

            padding: 30px;

            background:
                rgba(2, 8, 15, 0.82);

            backdrop-filter:
                blur(7px);

        }


        .rippletrace-report-modal {

            width: min(
                1250px,
                calc(100vw - 60px)
            );

            max-height:
                calc(100vh - 60px);

            display: flex;

            flex-direction: column;

            overflow: hidden;

            background:
                #07111c;

            border:
                1px solid #2a4055;

            border-radius:
                8px;

            box-shadow:
                0 30px 90px
                rgba(0, 0, 0, 0.65);

        }


        .rippletrace-report-header {

            display: flex;

            align-items: center;

            justify-content: space-between;

            padding:
                20px 24px;

            background:
                #0b1724;

            border-bottom:
                1px solid #26394c;

        }


        .rippletrace-report-title {

            color:
                #ffffff;

            font-size:
                18px;

            font-weight:
                700;

            letter-spacing:
                0.2px;

        }


        .rippletrace-report-subtitle {

            margin-top:
                5px;

            color:
                #8198ad;

            font-size:
                12px;

        }


        .rippletrace-report-close {

            width:
                34px;

            height:
                34px;

            border:
                1px solid #354b60;

            border-radius:
                5px;

            background:
                #101f2e;

            color:
                #ffffff;

            font-size:
                22px;

            cursor:
                pointer;

        }


        .rippletrace-report-close:hover {

            background:
                #193047;

        }


        .rippletrace-report-content {

            padding:
                20px 24px;

            overflow:
                auto;

        }


        .rippletrace-report-table-wrap {

            width:
                100%;

            overflow-x:
                auto;

            border:
                1px solid #26394c;

            border-radius:
                6px;

        }


        .rippletrace-report-table {

            width:
                100%;

            min-width:
                950px;

            border-collapse:
                collapse;

            font-family:
                Arial,
                sans-serif;

            font-size:
                12px;

        }


        .rippletrace-report-table th {

            padding:
                12px 13px;

            text-align:
                left;

            white-space:
                nowrap;

            background:
                #102235;

            color:
                #8fb9dc;

            border-bottom:
                1px solid #2b4054;

            font-size:
                10px;

            font-weight:
                700;

            text-transform:
                uppercase;

            letter-spacing:
                0.7px;

        }


        .rippletrace-report-table td {

            padding:
                12px 13px;

            vertical-align:
                top;

            background:
                #08131f;

            color:
                #d7e3ed;

            border-bottom:
                1px solid #1d2d3d;

            line-height:
                1.45;

        }


        .rippletrace-report-table tr:hover td {

            background:
                #0e1d2b;

        }


        .rippletrace-report-table td:first-child {

            color:
                #91a9bd;

            font-weight:
                600;

        }


        .rippletrace-report-badge {

            display:
                inline-block;

            padding:
                4px 8px;

            border-radius:
                12px;

            background:
                #12283b;

            color:
                #75b9f4;

            font-size:
                10px;

            font-weight:
                700;

            white-space:
                nowrap;

        }


        .rippletrace-report-footer {

            display:
                flex;

            align-items:
                center;

            justify-content:
                space-between;

            padding:
                13px 24px;

            background:
                #0b1724;

            border-top:
                1px solid #26394c;

            color:
                #6f8598;

            font-size:
                10px;

        }


        .rippletrace-report-footer-close {

            padding:
                8px 17px;

            border:
                1px solid #3a5268;

            border-radius:
                4px;

            background:
                transparent;

            color:
                #dbe7f0;

            cursor:
                pointer;

        }


        .rippletrace-report-footer-close:hover {

            background:
                #15293b;

        }


        @media (max-width: 800px) {

            .rippletrace-report-overlay {

                padding:
                    12px;

            }

            .rippletrace-report-modal {

                width:
                    calc(100vw - 24px);

                max-height:
                    calc(100vh - 24px);

            }

            .rippletrace-report-header {

                padding:
                    16px;

            }

            .rippletrace-report-content {

                padding:
                    12px;

            }

        }

    `;


    document.head.appendChild(
        style
    );

})();
