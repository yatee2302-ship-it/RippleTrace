
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
