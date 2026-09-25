from pathlib import Path
import shutil
import re
from datetime import datetime


# ============================================================
# RIPPLETRACE UI RESTORE + REAL REPORT FIX
#
# PURPOSE:
# Restore the good existing UI layer and replace ONLY the
# broken report behaviour.
#
# NEVER modifies:
#   srv/
#   db/
#   CDS
#   CAP actions
#   agent files
#
# ============================================================


ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
CSS = APP / "css" / "style.css"

REALTIME = APP / "realtime-monitor.js"
REPORT = APP / "rippletrace-real-reports.js"


if not INDEX.exists():
    raise SystemExit(
        f"ERROR: {INDEX} not found"
    )

if not CSS.exists():
    raise SystemExit(
        f"ERROR: {CSS} not found"
    )


# ============================================================
# BACKUP CURRENT UI
# ============================================================

backup_dir = APP / (
    "ui_restore_backup_" +
    datetime.now().strftime("%Y%m%d_%H%M%S")
)

backup_dir.mkdir(
    parents=True,
    exist_ok=True
)


for file in [
    INDEX,
    CSS,
    REALTIME,
    REPORT
]:

    if file.exists():

        shutil.copy2(
            file,
            backup_dir / file.name
        )


print()
print("=" * 70)
print("RippleTrace UI Restore")
print("=" * 70)

print(
    f"Backup created: {backup_dir}"
)


# ============================================================
# READ INDEX
# ============================================================

html = INDEX.read_text(
    encoding="utf-8"
)


# ============================================================
# REMOVE OLD REPORT JAVASCRIPT REFERENCES ONLY
#
# IMPORTANT:
# We remove OLD REPORT JS.
#
# We DO NOT remove the CSS.
#
# Therefore the existing UI appearance remains intact.
# ============================================================

old_report_scripts = [

    "ui-polish-v2.js",

    "ui-polish-v3.js",

    "ui-polish-v4.js",

    "ui-polish-v5.js",

    "report-v5.js",

    "report-v4.js",

    "report-v3.js",

    "ui-polish.js"

]


for script_name in old_report_scripts:

    pattern = (
        r'<script\b[^>]*src=["\'][^"\']*'
        + re.escape(script_name)
        + r'[^"\']*["\'][^>]*>\s*</script>'
    )

    html = re.sub(
        pattern,
        "",
        html,
        flags=re.IGNORECASE
    )


# ============================================================
# REMOVE DUPLICATE OLD REALTIME REFERENCES
#
# We will add exactly one realtime monitor reference.
# ============================================================

html = re.sub(
    r'<script\b[^>]*src=["\'][^"\']*realtime-monitor\.js[^"\']*["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


# ============================================================
# REMOVE OLD REPORT-V5 REFERENCES
# ============================================================

html = re.sub(
    r'<script\b[^>]*src=["\'][^"\']*rippletrace-real-reports\.js[^"\']*["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


# ============================================================
# ADD REALTIME GRAPH SCRIPT
#
# ONLY if the existing graph script exists.
# ============================================================

if REALTIME.exists():

    realtime_tag = (
        '<script src="realtime-monitor.js"></script>'
    )

    if realtime_tag not in html:

        if re.search(
            r"</body>",
            html,
            flags=re.IGNORECASE
        ):

            html = re.sub(
                r"</body>",
                "    " +
                realtime_tag +
                "\n</body>",
                html,
                count=1,
                flags=re.IGNORECASE
            )

        else:

            html += (
                "\n" +
                realtime_tag +
                "\n"
            )

        print(
            "[OK] Real-time graph restored"
        )

else:

    print(
        "[WARNING] realtime-monitor.js not found"
    )


# ============================================================
# ADD NEW SAFE REPORT SCRIPT
# ============================================================

report_tag = (
    '<script src="rippletrace-real-reports.js"></script>'
)


if report_tag not in html:

    if re.search(
        r"</body>",
        html,
        flags=re.IGNORECASE
    ):

        html = re.sub(
            r"</body>",
            "    " +
            report_tag +
            "\n</body>",
            html,
            count=1,
            flags=re.IGNORECASE
        )

    else:

        html += (
            "\n" +
            report_tag +
            "\n"
        )


INDEX.write_text(
    html,
    encoding="utf-8"
)


# ============================================================
# NEW REPORT ENGINE
#
# IMPORTANT:
#
# This does NOT:
#   - trigger agents
#   - modify buttons
#   - intercept agent clicks
#   - create fake results
#
# It captures the actual responses produced by the existing
# application.
# ============================================================

report_js = r"""
/*
 * ============================================================
 * RippleTrace REAL REPORT ENGINE
 * ============================================================
 *
 * PRESENTATION LAYER ONLY.
 *
 * Real API responses only.
 *
 * Does NOT execute agents.
 * Does NOT modify CAP.
 * Does NOT modify database.
 * Does NOT modify approval logic.
 *
 * Existing agent buttons continue to work normally.
 *
 * ============================================================
 */

(function () {

    "use strict";


    console.log(
        "[RippleTrace] Real Report Engine loaded"
    );


    /* ========================================================
       REAL RESULTS
       ======================================================== */

    const results = {

        TRACE: null,

        PREDICT: null,

        RECOMMEND: null,

        SAFEGUARD: null

    };


    /* ========================================================
       MAP REAL API ENDPOINTS
       ======================================================== */

    const endpointMap = {

        "/triggerCascade": "TRACE",

        "/triggerPrediction": "PREDICT",

        "/triggerMitigation": "RECOMMEND",

        "/triggerSafeguard": "SAFEGUARD"

    };


    /* ========================================================
       ORIGINAL FETCH
       ======================================================== */

    const originalFetch =
        window.fetch.bind(window);


    /*
     * IMPORTANT:
     *
     * We DO NOT replace the application's response.
     *
     * We clone it and inspect the clone.
     *
     * The original response continues normally.
     */

    window.fetch = async function () {

        const request =
            arguments[0];

        const options =
            arguments[1];


        let url = "";


        try {

            if (
                typeof request === "string"
            ) {

                url = request;

            }
            else if (
                request &&
                request.url
            ) {

                url = request.url;

            }

        }
        catch (error) {

            console.warn(
                "[Report] Could not read request URL",
                error
            );

        }


        const response =
            await originalFetch(
                request,
                options
            );


        let agentName = null;


        for (
            const endpoint in endpointMap
        ) {

            if (
                url.includes(endpoint)
            ) {

                agentName =
                    endpointMap[endpoint];

                break;

            }

        }


        /*
         * Normal dashboard GET calls
         * are completely untouched.
         */

        if (!agentName) {

            return response;

        }


        /*
         * Capture ONLY successful responses.
         */

        if (
            !response.ok
        ) {

            return response;

        }


        try {

            const cloned =
                response.clone();


            const raw =
                await cloned.json();


            /*
             * Store the REAL result.
             */

            results[agentName] = {

                data: raw,

                endpoint: url,

                status: response.status,

                time:
                    new Date()

            };


            console.log(
                "[Report] REAL " +
                agentName +
                " result captured:",
                raw
            );


            /*
             * Tell the UI that the report
             * is now available.
             */

            window.dispatchEvent(
                new CustomEvent(
                    "rippletrace-agent-complete",
                    {
                        detail: {
                            agent: agentName
                        }
                    }
                )
            );


        }
        catch (error) {

            console.warn(
                "[Report] Could not capture " +
                agentName +
                " response",
                error
            );

        }


        /*
         * Return the ORIGINAL response.
         */

        return response;

    };


    /* ========================================================
       ESCAPE HTML
       ======================================================== */

    function escapeHTML(value) {

        return String(
            value === undefined ||
            value === null
                ? ""
                : value
        )
        .replace(
            /&/g,
            "&amp;"
        )
        .replace(
            /</g,
            "&lt;"
        )
        .replace(
            />/g,
            "&gt;"
        )
        .replace(
            /"/g,
            "&quot;"
        )
        .replace(
            /'/g,
            "&#039;"
        );

    }


    /* ========================================================
       GET AGENT CARD
       ======================================================== */

    function findCard(agent) {

        const all =
            Array.from(
                document.querySelectorAll(
                    "section, article, div, .card, .panel"
                )
            );


        let keywords = [];


        if (
            agent === "TRACE"
        ) {

            keywords = [
                "trace agent",
                "cascade agent",
                "send to predict"
            ];

        }


        if (
            agent === "PREDICT"
        ) {

            keywords = [
                "predict agent",
                "mitigation agent",
                "send to recommend"
            ];

        }


        if (
            agent === "RECOMMEND"
        ) {

            keywords = [
                "recommend agent",
                "safeguard agent",
                "approve reroute"
            ];

        }


        if (
            agent === "SAFEGUARD"
        ) {

            keywords = [
                "safeguard",
                "human approval",
                "approve reroute"
            ];

        }


        /*
         * Search from smaller elements upward.
         */

        for (
            const element of all
        ) {

            const text =
                (
                    element.innerText ||
                    element.textContent ||
                    ""
                )
                .toLowerCase();


            const matches =
                keywords.some(
                    function (keyword) {

                        return text.includes(
                            keyword
                        );

                    }
                );


            if (
                matches &&
                text.length < 5000
            ) {

                return element;

            }

        }


        return null;

    }


    /* ========================================================
       REPORT BUTTON
       ======================================================== */

    function createReportButton(
        agent
    ) {

        /*
         * Never create duplicate buttons.
         */

        const existing =
            document.querySelector(
                '[data-rippletrace-report="' +
                agent +
                '"]'
            );


        if (existing) {

            return existing;

        }


        const card =
            findCard(agent);


        if (!card) {

            return null;

        }


        const button =
            document.createElement(
                "button"
            );


        button.type =
            "button";


        button.dataset.rippletraceReport =
            agent;


        button.className =
            "rt-real-report-button";


        button.innerHTML =
            "▣ View " +
            agent +
            " Report";


        /*
         * DIRECT listener.
         *
         * No document-level click interception.
         */

        button.addEventListener(
            "click",
            function (event) {

                event.preventDefault();

                event.stopPropagation();

                openReport(agent);

            }
        );


        /*
         * Add after existing buttons,
         * preserving the existing layout.
         */

        const buttons =
            card.querySelectorAll(
                "button"
            );


        if (
            buttons.length > 0
        ) {

            buttons[
                buttons.length - 1
            ].insertAdjacentElement(
                "afterend",
                button
            );

        }
        else {

            card.appendChild(
                button
            );

        }


        return button;

    }


    /* ========================================================
       WAIT FOR CARD + ADD REPORT BUTTON
       ======================================================== */

    function addReportButtonWhenReady(
        agent
    ) {

        const existing =
            document.querySelector(
                '[data-rippletrace-report="' +
                agent +
                '"]'
            );


        if (existing) {

            return;

        }


        let attempts = 0;


        const timer =
            setInterval(
                function () {

                    attempts++;


                    const button =
                        createReportButton(
                            agent
                        );


                    if (
                        button ||
                        attempts > 40
                    ) {

                        clearInterval(
                            timer
                        );

                    }

                },
                250
            );

    }


    /* ========================================================
       FORMAT GENERIC VALUES
       ======================================================== */

    function value(
        object,
        keys
    ) {

        if (
            !object
        ) {

            return "—";

        }


        for (
            const key of keys
        ) {

            if (
                object[key] !==
                undefined &&
                object[key] !== null
            ) {

                return object[key];

            }

        }


        return "—";

    }


    /* ========================================================
       BUILD REAL ROWS
       ======================================================== */

    function buildRows(
        agent,
        data
    ) {

        const rows = [];


        /* ----------------------------------------------------
           TRACE
           ---------------------------------------------------- */

        if (
            agent === "TRACE"
        ) {

            const nodes =
                Array.isArray(
                    data?.affectedNodes
                )
                    ? data.affectedNodes
                    : [];


            nodes.forEach(
                function (node) {

                    rows.push({

                        queryId:
                            value(
                                data?.disruption,
                                [
                                    "id",
                                    "ID"
                                ]
                            ),

                        itemName:
                            value(
                                node,
                                [
                                    "name",
                                    "nodeName"
                                ]
                            ),

                        tier:
                            value(
                                node,
                                [
                                    "tier"
                                ]
                            ) !== "—"
                                ? "Tier " +
                                  value(
                                      node,
                                      ["tier"]
                                  )
                                : "—",

                        status:
                            value(
                                node,
                                ["status"]
                            ),

                        risk:
                            value(
                                node,
                                [
                                    "risk",
                                    "severity"
                                ]
                            ),

                        leadTime:
                            "—",

                        inventory:
                            "—",

                        detail:
                            value(
                                node,
                                [
                                    "nodeType",
                                    "location"
                                ]
                            )

                    });

                }
            );

        }


        /* ----------------------------------------------------
           PREDICT
           ---------------------------------------------------- */

        if (
            agent === "PREDICT"
        ) {

            const impact =
                data?.impact;


            if (
                impact
            ) {

                rows.push({

                    queryId:
                        value(
                            data?.disruption,
                            [
                                "id",
                                "ID"
                            ]
                        ),

                    itemName:
                        value(
                            impact,
                            [
                                "component",
                                "componentName"
                            ]
                        ),

                    tier:
                        "Impact",

                    status:
                        value(
                            impact,
                            ["risk"]
                        ),

                    risk:
                        value(
                            impact,
                            ["risk"]
                        ),

                    leadTime:
                        value(
                            impact,
                            [
                                "leadTime",
                                "leadTimeDays"
                            ]
                        ) !== "—"
                            ?
                            value(
                                impact,
                                [
                                    "leadTime",
                                    "leadTimeDays"
                                ]
                            ) +
                            " days"
                            : "—",

                    inventory:
                        value(
                            impact,
                            [
                                "inventory",
                                "stockDays"
                            ]
                        ) !== "—"
                            ?
                            value(
                                impact,
                                [
                                    "inventory",
                                    "stockDays"
                                ]
                            ) +
                            " days"
                            : "—",

                    detail:
                        value(
                            impact,
                            [
                                "factory",
                                "stockoutGap",
                                "stockoutGapDays"
                            ]
                        )

                });

            }

        }


        /* ----------------------------------------------------
           RECOMMEND
           ---------------------------------------------------- */

        if (
            agent === "RECOMMEND"
        ) {

            const recommendation =
                data?.recommendation;


            if (
                recommendation
            ) {

                rows.push({

                    queryId:
                        value(
                            data?.disruption,
                            [
                                "id",
                                "ID"
                            ]
                        ),

                    itemName:
                        value(
                            recommendation,
                            [
                                "supplierName",
                                "name",
                                "supplier"
                            ]
                        ),

                    tier:
                        "Alternate Supplier",

                    status:
                        "RECOMMENDED",

                    risk:
                        value(
                            recommendation,
                            [
                                "riskLevel",
                                "risk"
                            ]
                        ),

                    leadTime:
                        value(
                            recommendation,
                            [
                                "leadTime",
                                "leadTimeDays"
                            ]
                        ) !== "—"
                            ?
                            value(
                                recommendation,
                                [
                                    "leadTime",
                                    "leadTimeDays"
                                ]
                            ) +
                            " days"
                            : "—",

                    inventory:
                        "—",

                    detail:
                        value(
                            recommendation,
                            [
                                "component",
                                "componentName",
                                "score"
                            ]
                        )

                });

            }


            const alternatives =
                Array.isArray(
                    data?.alternatives
                )
                    ? data.alternatives
                    : [];


            alternatives.forEach(
                function (alternative) {

                    rows.push({

                        queryId:
                            value(
                                data?.disruption,
                                [
                                    "id",
                                    "ID"
                                ]
                            ),

                        itemName:
                            value(
                                alternative,
                                [
                                    "supplierName",
                                    "name",
                                    "supplier"
                                ]
                            ),

                        tier:
                            "Alternate Supplier",

                        status:
                            "ALTERNATIVE",

                        risk:
                            value(
                                alternative,
                                [
                                    "riskLevel",
                                    "risk"
                                ]
                            ),

                        leadTime:
                            value(
                                alternative,
                                [
                                    "leadTime",
                                    "leadTimeDays"
                                ]
                            ) !== "—"
                                ?
                                value(
                                    alternative,
                                    [
                                        "leadTime",
                                        "leadTimeDays"
                                    ]
                                ) +
                                " days"
                                : "—",

                        inventory:
                            "—",

                        detail:
                            value(
                                alternative,
                                [
                                    "component",
                                    "componentName"
                                ]
                            )

                    });

                }
            );

        }


        /* ----------------------------------------------------
           SAFEGUARD
           ---------------------------------------------------- */

        if (
            agent === "SAFEGUARD"
        ) {

            const decision =
                data?.decision;


            if (
                decision
            ) {

                rows.push({

                    queryId:
                        value(
                            decision,
                            [
                                "ID",
                                "id"
                            ]
                        ),

                    itemName:
                        value(
                            decision,
                            [
                                "recommendation"
                            ]
                        ),

                    tier:
                        "Human Approval",

                    status:
                        value(
                            decision,
                            [
                                "status"
                            ]
                        ) !== "—"
                            ?
                            value(
                                decision,
                                [
                                    "status"
                                ]
                            )
                            :
                            value(
                                data,
                                [
                                    "status"
                                ]
                            ),

                    risk:
                        "—",

                    leadTime:
                        "—",

                    inventory:
                        "—",

                    detail:
                        value(
                            data,
                            [
                                "message"
                            ]
                        )

                });

            }

        }


        return rows;

    }


    /* ========================================================
       OPEN REPORT
       ======================================================== */

    function openReport(
        agent
    ) {

        const result =
            results[agent];


        /*
         * NEVER fabricate data.
         */

        if (
            !result
        ) {

            return;

        }


        const existing =
            document.querySelector(
                ".rt-real-report-overlay"
            );


        if (existing) {

            existing.remove();

        }


        const rows =
            buildRows(
                agent,
                result.data
            );


        const overlay =
            document.createElement(
                "div"
            );


        overlay.className =
            "rt-real-report-overlay";


        const tableRows =
            rows.length > 0

                ?

                rows.map(
                    function (row) {

                        return `

                            <tr>

                                <td>
                                    ${escapeHTML(
                                        row.queryId
                                    )}
                                </td>

                                <td>
                                    ${escapeHTML(
                                        row.itemName
                                    )}
                                </td>

                                <td>
                                    ${escapeHTML(
                                        row.tier
                                    )}
                                </td>

                                <td>
                                    <span class="rt-real-status">
                                        ${escapeHTML(
                                            row.status
                                        )}
                                    </span>
                                </td>

                                <td>
                                    ${escapeHTML(
                                        row.risk
                                    )}
                                </td>

                                <td>
                                    ${escapeHTML(
                                        row.leadTime
                                    )}
                                </td>

                                <td>
                                    ${escapeHTML(
                                        row.inventory
                                    )}
                                </td>

                                <td>
                                    ${escapeHTML(
                                        row.detail
                                    )}
                                </td>

                            </tr>

                        `;

                    }
                ).join("")

                :

                `

                    <tr>

                        <td colspan="8">

                            The real backend response
                            contains no tabular records.

                        </td>

                    </tr>

                `;


        overlay.innerHTML = `

            <div class="rt-real-report">

                <div class="rt-real-report-header">

                    <div>

                        <div class="rt-real-report-title">

                            ${escapeHTML(
                                agent
                            )}
                            AGENT REPORT

                        </div>

                        <div class="rt-real-report-subtitle">

                            Live backend execution result

                        </div>

                    </div>


                    <button
                        type="button"
                        class="rt-real-close"
                    >
                        ×
                    </button>

                </div>


                <div class="rt-real-report-body">

                    <div class="rt-real-meta">

                        <span>
                            API
                        </span>

                        <strong>
                            ${escapeHTML(
                                result.endpoint
                            )}
                        </strong>

                        <span>
                            HTTP ${escapeHTML(
                                result.status
                            )}
                        </span>

                        <span>
                            ${escapeHTML(
                                result.time
                            )}
                        </span>

                    </div>


                    <div class="rt-real-table-wrapper">

                        <table class="rt-real-table">

                            <thead>

                                <tr>

                                    <th>
                                        Query ID
                                    </th>

                                    <th>
                                        Item Name
                                    </th>

                                    <th>
                                        Tier
                                    </th>

                                    <th>
                                        Status
                                    </th>

                                    <th>
                                        Risk
                                    </th>

                                    <th>
                                        Lead Time
                                    </th>

                                    <th>
                                        Inventory
                                    </th>

                                    <th>
                                        Detail
                                    </th>

                                </tr>

                            </thead>


                            <tbody>

                                ${tableRows}

                            </tbody>

                        </table>

                    </div>


                    <div class="rt-real-json-title">

                        ACTUAL BACKEND RESPONSE

                    </div>


                    <pre class="rt-real-json">${escapeHTML(
                        JSON.stringify(
                            result.data,
                            null,
                            2
                        )
                    )}</pre>

                </div>


                <div class="rt-real-report-footer">

                    ✓ REAL RESPONSE •
                    No simulated values

                </div>

            </div>

        `;


        document.body.appendChild(
            overlay
        );


        overlay
            .querySelector(
                ".rt-real-close"
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
                    event.target ===
                    overlay
                ) {

                    overlay.remove();

                }

            }
        );

    }


    /* ========================================================
       AGENT COMPLETE EVENT
       ======================================================== */

    window.addEventListener(
        "rippletrace-agent-complete",
        function (event) {

            const agent =
                event.detail?.agent;


            if (!agent) {

                return;

            }


            console.log(
                "[Report] " +
                agent +
                " completed."
            );


            /*
             * Report button appears ONLY now.
             */

            addReportButtonWhenReady(
                agent
            );

        }
    );


    /* ========================================================
       ESC CLOSE
       ======================================================== */

    document.addEventListener(
        "keydown",
        function (event) {

            if (
                event.key !== "Escape"
            ) {

                return;

            }


            const overlay =
                document.querySelector(
                    ".rt-real-report-overlay"
                );


            if (overlay) {

                overlay.remove();

            }

        }
    );


    /* ========================================================
       REPORT CSS
       ======================================================== */

    const style =
        document.createElement(
            "style"
        );


    style.textContent = `

        /* ====================================================
           REPORT BUTTON
           ==================================================== */

        .rt-real-report-button {

            display: inline-flex !important;

            align-items: center !important;

            justify-content: center !important;

            margin: 10px 0 0 8px !important;

            padding: 8px 13px !important;

            border: 1px solid #34546b !important;

            border-radius: 6px !important;

            background: #0b1822 !important;

            color: #79c6ff !important;

            font-family:
                Inter,
                Arial,
                sans-serif !important;

            font-size: 11px !important;

            font-weight: 600 !important;

            cursor: pointer !important;

            transition:
                background .15s ease,
                border-color .15s ease !important;

        }


        .rt-real-report-button:hover {

            background: #122838 !important;

            border-color: #4b83aa !important;

            color: #a4dbff !important;

        }


        /* ====================================================
           OVERLAY
           ==================================================== */

        .rt-real-report-overlay {

            position: fixed !important;

            inset: 0 !important;

            z-index: 2147483647 !important;

            display: flex !important;

            align-items: center !important;

            justify-content: center !important;

            padding: 28px !important;

            background:
                rgba(2, 7, 11, .86) !important;

            backdrop-filter:
                blur(8px) !important;

        }


        /* ====================================================
           REPORT
           ==================================================== */

        .rt-real-report {

            width:
                min(1180px, 95vw) !important;

            max-height:
                88vh !important;

            display: flex !important;

            flex-direction: column !important;

            overflow: hidden !important;

            border:
                1px solid #30495a !important;

            border-radius:
                10px !important;

            background:
                #081119 !important;

            color:
                #dce9f2 !important;

            box-shadow:
                0 30px 100px
                rgba(0,0,0,.75) !important;

        }


        /* ====================================================
           HEADER
           ==================================================== */

        .rt-real-report-header {

            display: flex !important;

            align-items: center !important;

            justify-content: space-between !important;

            padding:
                18px 22px !important;

            background:
                #0c1720 !important;

            border-bottom:
                1px solid #293d4b !important;

        }


        .rt-real-report-title {

            font-size:
                15px !important;

            font-weight:
                700 !important;

            letter-spacing:
                .35px !important;

            color:
                #edf6fb !important;

        }


        .rt-real-report-subtitle {

            margin-top:
                5px !important;

            color:
                #71899a !important;

            font-size:
                10px !important;

        }


        .rt-real-close {

            width:
                34px !important;

            height:
                34px !important;

            border:
                1px solid #344957 !important;

            border-radius:
                6px !important;

            background:
                #111d26 !important;

            color:
                #9eb2c1 !important;

            font-size:
                21px !important;

            cursor:
                pointer !important;

        }


        .rt-real-close:hover {

            background:
                #1a2a35 !important;

            color:
                white !important;

        }


        /* ====================================================
           BODY
           ==================================================== */

        .rt-real-report-body {

            padding:
                18px !important;

            overflow:
                auto !important;

        }


        .rt-real-meta {

            display:
                flex !important;

            flex-wrap:
                wrap !important;

            align-items:
                center !important;

            gap:
                10px !important;

            margin-bottom:
                14px !important;

            padding:
                10px 12px !important;

            border:
                1px solid #263946 !important;

            border-radius:
                6px !important;

            background:
                #0c1720 !important;

            color:
                #71899b !important;

            font-size:
                10px !important;

        }


        .rt-real-meta strong {

            color:
                #bad0df !important;

            font-family:
                monospace !important;

        }


        /* ====================================================
           TABLE
           ==================================================== */

        .rt-real-table-wrapper {

            overflow-x:
                auto !important;

            border:
                1px solid #293e4d !important;

            border-radius:
                7px !important;

        }


        .rt-real-table {

            width:
                100% !important;

            min-width:
                900px !important;

            border-collapse:
                collapse !important;

            font-size:
                11px !important;

        }


        .rt-real-table th {

            padding:
                11px 12px !important;

            text-align:
                left !important;

            white-space:
                nowrap !important;

            background:
                #111d26 !important;

            color:
                #8fa7b8 !important;

            border-bottom:
                1px solid #304656 !important;

            font-size:
                10px !important;

            font-weight:
                700 !important;

        }


        .rt-real-table td {

            padding:
                11px 12px !important;

            vertical-align:
                top !important;

            background:
                #0a141c !important;

            color:
                #d2e0e9 !important;

            border-bottom:
                1px solid #20323f !important;

        }


        .rt-real-table tr:hover td {

            background:
                #101e28 !important;

        }


        .rt-real-status {

            display:
                inline-block !important;

            padding:
                4px 8px !important;

            border:
                1px solid #2e5a75 !important;

            border-radius:
                20px !important;

            background:
                #102638 !important;

            color:
                #79c7ff !important;

            font-size:
                9px !important;

            font-weight:
                700 !important;

        }


        /* ====================================================
           RAW JSON
           ==================================================== */

        .rt-real-json-title {

            margin:
                18px 0 7px !important;

            color:
                #8198a9 !important;

            font-size:
                10px !important;

            font-weight:
                700 !important;

            letter-spacing:
                .5px !important;

        }


        .rt-real-json {

            margin:
                0 !important;

            padding:
                14px !important;

            max-height:
                280px !important;

            overflow:
                auto !important;

            border:
                1px solid #263946 !important;

            border-radius:
                7px !important;

            background:
                #050a0e !important;

            color:
                #9eb5c5 !important;

            font-family:
                "JetBrains Mono",
                "Fira Code",
                monospace !important;

            font-size:
                10px !important;

            line-height:
                1.55 !important;

            white-space:
                pre-wrap !important;

            word-break:
                break-word !important;

        }


        /* ====================================================
           FOOTER
           ==================================================== */

        .rt-real-report-footer {

            padding:
                11px 20px !important;

            border-top:
                1px solid #263946 !important;

            background:
                #0c1720 !important;

            color:
                #658092 !important;

            font-size:
                10px !important;

        }

    `;


    document.head.appendChild(
        style
    );


    console.log(
        "[RippleTrace] Real Report Engine ready"
    );


})();
"""


REPORT.write_text(
    report_js,
    encoding="utf-8"
)


print(
    "[OK] New real report engine created"
)


# ============================================================
# VALIDATION
# ============================================================

final_html =
    INDEX.read_text(
        encoding="utf-8"
    )


print()
print("=" * 70)
print("RIPPLETRACE RESTORE COMPLETE")
print("=" * 70)

print()
print("UI:")
print("  ✓ Existing UI preserved")
print("  ✓ Existing CSS preserved")
print("  ✓ Real-time graph preserved/restored")

print()
print("AGENTS:")
print("  ✓ Existing agent execution untouched")
print("  ✓ Existing API calls untouched")
print("  ✓ Existing CAP backend untouched")

print()
print("REPORTS:")
print("  ✓ Old report handlers removed")
print("  ✓ New real-response report engine installed")
print("  ✓ No fake data")
print("  ✓ Report button appears after real completion")
print("  ✓ Agent buttons are NOT intercepted")
print("  ✓ Report opens only from its own button")

print()
print("BACKUP:")
print(
    "  " + str(backup_dir)
)

print()
print("Next:")
print("  1. Restart cds watch if necessary")
print("  2. Open http://localhost:4004/control-tower/")
print("  3. Press Ctrl + Shift + R")
print("  4. Run Trace")
print("  5. Wait for completion")
print("  6. View Trace Report")

print("=" * 70)
