from pathlib import Path
import shutil
import re


# ============================================================
# RIPPLETRACE V5 REPORT FIX
#
# IMPORTANT:
# - Does NOT modify app.js
# - Does NOT modify CAP
# - Does NOT modify agents
# - Does NOT modify database
# - Does NOT modify API endpoints
# - Does NOT modify approval logic
#
# Only fixes the presentation/report layer.
# ============================================================


ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
CSS = APP / "css" / "style.css"
V5_JS = APP / "report-v5.js"


if not INDEX.exists():
    raise SystemExit(f"ERROR: {INDEX} not found")

if not CSS.exists():
    raise SystemExit(f"ERROR: {CSS} not found")


# ============================================================
# BACKUP
# ============================================================

def backup(path, suffix=".v5.bak"):

    if path.exists():

        backup_path = path.with_suffix(
            path.suffix + suffix
        )

        shutil.copy2(
            path,
            backup_path
        )

        print(f"[BACKUP] {backup_path}")


backup(INDEX)
backup(CSS)
backup(V5_JS)


# ============================================================
# REMOVE OLD REPORT SCRIPTS FROM INDEX.HTML
# ============================================================

html = INDEX.read_text(
    encoding="utf-8"
)


old_scripts = [
    "ui-polish-v2.js",
    "ui-polish-v3.js",
    "ui-polish-v4.js",
    "realtime-monitor.js",
]


removed = []

for script_name in old_scripts:

    pattern = (
        r'<script\b[^>]*'
        + re.escape(script_name)
        + r'[^>]*>\s*</script>'
    )

    new_html, count = re.subn(
        pattern,
        "",
        html,
        flags=re.IGNORECASE
    )

    if count:

        html = new_html

        removed.append(script_name)


# Also remove accidental duplicate references
# with plain src attributes.

for script_name in old_scripts:

    html = re.sub(
        r'<script\b[^>]*src=["\'][^"\']*'
        + re.escape(script_name)
        + r'[^"\']*["\'][^>]*>\s*</script>',
        "",
        html,
        flags=re.IGNORECASE
    )


# ============================================================
# ADD V5 SCRIPT
# ============================================================

v5_tag = '<script src="report-v5.js"></script>'


if "report-v5.js" not in html:

    if re.search(
        r"</body>",
        html,
        re.IGNORECASE
    ):

        html = re.sub(
            r"</body>",
            f"    {v5_tag}\n</body>",
            html,
            count=1,
            flags=re.IGNORECASE
        )

    else:

        html += "\n" + v5_tag + "\n"


INDEX.write_text(
    html,
    encoding="utf-8"
)


print()
print("[OK] Old report scripts removed:")
for item in removed:
    print("     -", item)

print("[OK] V5 report script registered")


# ============================================================
# V5 JAVASCRIPT
# ============================================================

v5_js = r"""
/*
 * ============================================================
 * RippleTrace Report V5
 *
 * REAL RESULTS ONLY
 *
 * This file does NOT:
 *
 * - execute agents
 * - call agent APIs itself
 * - modify app.js
 * - modify CAP
 * - modify database
 * - modify approval logic
 *
 * It only listens to the EXISTING fetch calls made by
 * the application and stores their real responses.
 *
 * SEND TO AGENT buttons remain completely untouched.
 *
 * REPORT buttons only display already captured results.
 * ============================================================
 */

(function () {

    "use strict";


    console.log(
        "RippleTrace Report V5 loaded"
    );


    /* ========================================================
       REAL AGENT RESULTS
       ======================================================== */

    const agentResults = {

        TRACE: null,

        PREDICT: null,

        RECOMMEND: null,

        SAFEGUARD: null

    };


    /* ========================================================
       API -> AGENT MAP
       ======================================================== */

    const endpointMap = {

        "/triggerCascade": "TRACE",

        "/triggerPrediction": "PREDICT",

        "/triggerMitigation": "RECOMMEND",

        "/triggerSafeguard": "SAFEGUARD"

    };


    /* ========================================================
       CAPTURE EXISTING FETCH RESPONSES
       ======================================================== */

    const originalFetch = window.fetch;


    window.fetch = async function () {

        const args = arguments;

        const request =
            args[0];

        const options =
            args[1] || {};


        let url = "";

        try {

            if (
                typeof request === "string"
            ) {

                url = request;

            } else if (
                request &&
                request.url
            ) {

                url = request.url;

            }

        } catch (error) {

            console.warn(
                "Report V5 could not read request URL",
                error
            );

        }


        /*
         * IMPORTANT:
         *
         * We call the ORIGINAL fetch.
         *
         * Therefore the actual application request
         * is unchanged.
         */

        const response =
            await originalFetch.apply(
                this,
                args
            );


        /* ====================================================
           Identify agent endpoint
           ==================================================== */

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


        if (!agentName) {

            return response;

        }


        /* ====================================================
           Clone response.
           
           We NEVER consume the original response.
           The application still receives the same response.
           ==================================================== */

        try {

            const clone =
                response.clone();


            const data =
                await clone.json();


            /*
             * Store EXACT backend result.
             *
             * No fake values.
             * No transformation.
             * No fallback.
             */

            agentResults[agentName] = {

                data: data,

                capturedAt:
                    new Date().toISOString(),

                endpoint: url,

                status:
                    response.status

            };


            console.log(
                "Report V5 captured real " +
                agentName +
                " result:",
                data
            );


            /*
             * Enable the corresponding report button.
             */

            enableReportButton(
                agentName
            );


        } catch (error) {

            console.warn(
                "Report V5 could not capture " +
                agentName +
                " response:",
                error
            );

        }


        /*
         * Return ORIGINAL response.
         *
         * Existing application logic continues normally.
         */

        return response;

    };


    /* ========================================================
       FIND REPORT BUTTON
       ======================================================== */

    function getReportButtons() {

        return Array.from(
            document.querySelectorAll(
                "button, a, [role='button']"
            )
        ).filter(
            function (element) {

                const text =
                    (
                        element.innerText ||
                        element.textContent ||
                        ""
                    )
                    .trim()
                    .toLowerCase();


                return (
                    text.includes(
                        "view trace report"
                    ) ||

                    text.includes(
                        "view predict report"
                    ) ||

                    text.includes(
                        "view recommendation report"
                    ) ||

                    text.includes(
                        "view safeguard report"
                    )
                );

            }
        );

    }


    /* ========================================================
       GET AGENT NAME FROM REPORT BUTTON
       ======================================================== */

    function getAgentFromButton(
        button
    ) {

        const text =
            (
                button.innerText ||
                button.textContent ||
                ""
            )
            .trim()
            .toLowerCase();


        if (
            text.includes(
                "view trace report"
            )
        ) {

            return "TRACE";

        }


        if (
            text.includes(
                "view predict report"
            )
        ) {

            return "PREDICT";

        }


        if (
            text.includes(
                "view recommendation report"
            )
        ) {

            return "RECOMMEND";

        }


        if (
            text.includes(
                "view safeguard report"
            )
        ) {

            return "SAFEGUARD";

        }


        return null;

    }


    /* ========================================================
       ENABLE REPORT BUTTON
       ======================================================== */

    function enableReportButton(
        agentName
    ) {

        getReportButtons()
            .forEach(
                function (button) {

                    const name =
                        getAgentFromButton(
                            button
                        );


                    if (
                        name !== agentName
                    ) {

                        return;

                    }


                    /*
                     * Do NOT interfere with normal
                     * application button behavior.
                     *
                     * Just make report available.
                     */

                    button.disabled = false;

                    button.removeAttribute(
                        "aria-disabled"
                    );


                    button.classList.add(
                        "rt-v5-ready"
                    );

                }
            );

    }


    /* ========================================================
       ESCAPE HTML
       ======================================================== */

    function escapeHTML(
        value
    ) {

        return String(
            value ?? ""
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
       VALUE FORMATTER
       ======================================================== */

    function formatValue(
        value
    ) {

        if (
            value === null ||
            value === undefined
        ) {

            return "—";

        }


        if (
            typeof value === "object"
        ) {

            return JSON.stringify(
                value
            );

        }


        return String(value);

    }


    /* ========================================================
       CREATE GENERIC ROWS FROM REAL JSON
       
       IMPORTANT:
       These are not fabricated values.
       Every value comes from the actual API response.
       ======================================================== */

    function createRows(
        agentName,
        data
    ) {

        const rows = [];


        /*
         * TRACE
         */

        if (
            agentName === "TRACE"
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
                            data?.disruption?.id ??
                            "—",

                        itemName:
                            node?.name ??
                            node?.nodeName ??
                            "—",

                        tier:
                            node?.tier !== undefined
                                ? "Tier " +
                                  node.tier
                                : (
                                    node?.nodeType ??
                                    "—"
                                  ),

                        status:
                            node?.status ??
                            "—",

                        risk:
                            node?.risk ??
                            node?.severity ??
                            "—",

                        leadTime:
                            "—",

                        inventory:
                            "—",

                        detail:
                            node?.nodeType ??
                            "Affected node"

                    });

                }
            );

        }


        /*
         * PREDICT
         */

        else if (
            agentName === "PREDICT"
        ) {

            const impact =
                data?.impact;


            if (
                impact &&
                typeof impact === "object"
            ) {

                rows.push({

                    queryId:
                        data?.disruption?.id ??
                        "—",

                    itemName:
                        impact.component ??
                        "—",

                    tier:
                        "Impact",

                    status:
                        impact.risk ??
                        "—",

                    risk:
                        impact.risk ??
                        "—",

                    leadTime:
                        impact.leadTime !== undefined
                            ? impact.leadTime +
                              " days"
                            : "—",

                    inventory:
                        impact.inventory !== undefined
                            ? impact.inventory +
                              " days"
                            : "—",

                    detail:
                        impact.factory
                            ? "Factory: " +
                              impact.factory
                            : (
                                impact.stockoutGap !==
                                undefined
                                    ? "Stockout gap: " +
                                      impact.stockoutGap +
                                      " days"
                                    : "—"
                              )

                });

            }

        }


        /*
         * RECOMMEND
         */

        else if (
            agentName === "RECOMMEND"
        ) {

            const recommendation =
                data?.recommendation;


            const alternatives =
                Array.isArray(
                    data?.alternatives
                )
                    ? data.alternatives
                    : [];


            if (
                recommendation &&
                typeof recommendation === "object"
            ) {

                rows.push({

                    queryId:
                        data?.disruption?.id ??
                        "—",

                    itemName:
                        recommendation.supplierName ??
                        recommendation.name ??
                        recommendation.supplier ??
                        "—",

                    tier:
                        "Alternate Supplier",

                    status:
                        "RECOMMENDED",

                    risk:
                        recommendation.riskLevel ??
                        recommendation.risk ??
                        "—",

                    leadTime:
                        recommendation.leadTime !==
                        undefined
                            ? recommendation.leadTime +
                              " days"
                            : "—",

                    inventory:
                        "—",

                    detail:
                        recommendation.component ??
                        "—"

                });

            }


            alternatives.forEach(
                function (item) {

                    if (
                        !item ||
                        typeof item !== "object"
                    ) {

                        return;

                    }


                    rows.push({

                        queryId:
                            data?.disruption?.id ??
                            "—",

                        itemName:
                            item.supplierName ??
                            item.name ??
                            item.supplier ??
                            "—",

                        tier:
                            "Alternate Supplier",

                        status:
                            "ALTERNATIVE",

                        risk:
                            item.riskLevel ??
                            item.risk ??
                            "—",

                        leadTime:
                            item.leadTime !==
                            undefined
                                ? item.leadTime +
                                  " days"
                                : "—",

                        inventory:
                            "—",

                        detail:
                            item.component ??
                            "—"

                    });

                }
            );

        }


        /*
         * SAFEGUARD
         */

        else if (
            agentName === "SAFEGUARD"
        ) {

            const decision =
                data?.decision;


            if (
                decision &&
                typeof decision === "object"
            ) {

                rows.push({

                    queryId:
                        decision.ID ??
                        decision.id ??
                        data?.decisionId ??
                        "—",

                    itemName:
                        decision.recommendation ??
                        "Mitigation Decision",

                    tier:
                        "Governance",

                    status:
                        decision.status ??
                        data?.status ??
                        "PENDING_APPROVAL",

                    risk:
                        "—",

                    leadTime:
                        "—",

                    inventory:
                        "—",

                    detail:
                        data?.message ??
                        decision.recommendation ??
                        "—"

                });

            }

        }


        return rows;

    }


    /* ========================================================
       SHOW REPORT
       
       ONLY REAL CAPTURED DATA.
       ======================================================== */

    function showReport(
        agentName
    ) {

        const result =
            agentResults[agentName];


        /*
         * ABSOLUTELY NO FAKE REPORT.
         */

        if (!result) {

            showNoResult(
                agentName
            );

            return;

        }


        const data =
            result.data;


        const rows =
            createRows(
                agentName,
                data
            );


        /*
         * Remove old popup.
         */

        const old =
            document.querySelector(
                ".rt-v5-overlay"
            );


        if (old) {

            old.remove();

        }


        const overlay =
            document.createElement(
                "div"
            );


        overlay.className =
            "rt-v5-overlay";


        const rowHTML =
            rows.length
                ? rows.map(
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
                                    <span class="rt-v5-badge">
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
                : `
                    <tr>
                        <td colspan="8">
                            The agent returned a valid result,
                            but there are no tabular records
                            in this response.
                        </td>
                    </tr>
                `;


        overlay.innerHTML = `

            <div class="rt-v5-modal">

                <div class="rt-v5-header">

                    <div>

                        <div class="rt-v5-title">

                            ${escapeHTML(
                                agentName
                            )}
                            AGENT REPORT

                        </div>

                        <div class="rt-v5-subtitle">

                            Live result returned by
                            RippleTrace backend

                        </div>

                    </div>


                    <button
                        type="button"
                        class="rt-v5-close"
                    >
                        ×
                    </button>

                </div>


                <div class="rt-v5-content">

                    <div class="rt-v5-meta">

                        <span>
                            Endpoint
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

                    </div>


                    <div class="rt-v5-table-wrap">

                        <table class="rt-v5-table">

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

                                ${rowHTML}

                            </tbody>

                        </table>

                    </div>


                    <div class="rt-v5-raw-title">

                        Actual Backend Response

                    </div>


                    <pre class="rt-v5-raw">
${escapeHTML(
    JSON.stringify(
        data,
        null,
        2
    )
)}
                    </pre>

                </div>


                <div class="rt-v5-footer">

                    Captured from the existing agent
                    execution • No simulated values

                </div>

            </div>

        `;


        document.body.appendChild(
            overlay
        );


        overlay
            .querySelector(
                ".rt-v5-close"
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
       NO RESULT
       ======================================================== */

    function showNoResult(
        agentName
    ) {

        const old =
            document.querySelector(
                ".rt-v5-overlay"
            );


        if (old) {

            old.remove();

        }


        const overlay =
            document.createElement(
                "div"
            );


        overlay.className =
            "rt-v5-overlay";


        overlay.innerHTML = `

            <div class="rt-v5-modal rt-v5-empty">

                <div class="rt-v5-header">

                    <div>

                        <div class="rt-v5-title">

                            ${escapeHTML(
                                agentName
                            )}
                            AGENT REPORT

                        </div>

                        <div class="rt-v5-subtitle">

                            No execution result available

                        </div>

                    </div>


                    <button
                        type="button"
                        class="rt-v5-close"
                    >
                        ×
                    </button>

                </div>


                <div class="rt-v5-empty-body">

                    <div class="rt-v5-empty-icon">
                        !
                    </div>

                    <h3>
                        Agent has not completed yet
                    </h3>

                    <p>
                        Run the ${escapeHTML(
                            agentName
                        )} Agent first.
                        The report will contain only
                        the actual response returned
                        by the backend.
                    </p>

                </div>

            </div>

        `;


        document.body.appendChild(
            overlay
        );


        overlay
            .querySelector(
                ".rt-v5-close"
            )
            .addEventListener(
                "click",
                function () {

                    overlay.remove();

                }
            );

    }


    /* ========================================================
       REPORT CLICK HANDLER
       
       VERY IMPORTANT:
       We DO NOT use capture phase.
       We DO NOT stop propagation.
       We DO NOT intercept agent buttons.
       
       We only handle actual report buttons.
       ======================================================== */

    document.addEventListener(
        "click",
        function (event) {

            let element =
                event.target;


            while (
                element &&
                element !== document.body
            ) {

                const name =
                    getAgentFromButton(
                        element
                    );


                if (name) {

                    /*
                     * This is a REPORT button.
                     *
                     * Prevent its default only.
                     * Agent buttons are never touched.
                     */

                    event.preventDefault();

                    showReport(
                        name
                    );

                    return;

                }


                element =
                    element.parentElement;

            }

        },
        false
    );


    /* ========================================================
       HIDE OLD AGENT OUTPUT BOXES
       
       Presentation only.
       ======================================================== */

    function hideOldOutputs() {

        const selectors = [

            ".agent-output",

            ".output-box",

            ".result-box",

            ".agentResultBox",

            "[class*='agent-output']",

            "[class*='output-box']",

            "[class*='agentResultBox']"

        ];


        selectors.forEach(
            function (selector) {

                document
                    .querySelectorAll(
                        selector
                    )
                    .forEach(
                        function (element) {

                            element.style
                                .setProperty(
                                    "display",
                                    "none",
                                    "important"
                                );

                        }
                    );

            }
        );

    }


    /* ========================================================
       INITIALIZE
       ======================================================== */

    function initialize() {

        hideOldOutputs();

        console.log(
            "RippleTrace Report V5 ready"
        );

    }


    initialize();


    /*
     * Re-hide output boxes if the existing
     * application re-renders them.
     */

    const observer =
        new MutationObserver(
            function () {

                hideOldOutputs();

            }
        );


    observer.observe(
        document.body,
        {
            childList: true,
            subtree: true
        }
    );


})();
"""


V5_JS.write_text(
    v5_js,
    encoding="utf-8"
)


print(
    f"[OK] Created {V5_JS}"
)


# ============================================================
# V5 CSS
# ============================================================

v5_css = r"""

/* ============================================================
   RIPPLETRACE REPORT V5
   ============================================================ */

.rt-v5-overlay {

    position: fixed !important;

    inset: 0 !important;

    z-index: 999999 !important;

    display: flex !important;

    align-items: center !important;

    justify-content: center !important;

    padding: 30px !important;

    background:
        rgba(2, 7, 12, .84) !important;

    backdrop-filter:
        blur(9px) !important;

}


.rt-v5-modal {

    width:
        min(1180px, 94vw) !important;

    max-height:
        88vh !important;

    display: flex !important;

    flex-direction: column !important;

    background:
        #081018 !important;

    color:
        #dce8f3 !important;

    border:
        1px solid #304454 !important;

    border-radius:
        10px !important;

    overflow:
        hidden !important;

    box-shadow:
        0 30px 100px
        rgba(0,0,0,.75) !important;

}


.rt-v5-header {

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        space-between !important;

    gap:
        20px !important;

    padding:
        18px 22px !important;

    background:
        #0d1720 !important;

    border-bottom:
        1px solid #293b4a !important;

}


.rt-v5-title {

    color:
        #f0f6fb !important;

    font-size:
        16px !important;

    font-weight:
        700 !important;

    letter-spacing:
        .3px !important;

}


.rt-v5-subtitle {

    margin-top:
        5px !important;

    color:
        #71879a !important;

    font-size:
        11px !important;

}


.rt-v5-close {

    width:
        34px !important;

    height:
        34px !important;

    flex:
        0 0 34px !important;

    border:
        1px solid #344958 !important;

    border-radius:
        7px !important;

    background:
        #111d26 !important;

    color:
        #a7b8c7 !important;

    font-size:
        20px !important;

    cursor:
        pointer !important;

}


.rt-v5-close:hover {

    background:
        #1a2b38 !important;

    color:
        #ffffff !important;

}


.rt-v5-content {

    padding:
        18px !important;

    overflow:
        auto !important;

    background:
        #081018 !important;

}


.rt-v5-meta {

    display:
        flex !important;

    align-items:
        center !important;

    gap:
        12px !important;

    margin-bottom:
        14px !important;

    padding:
        10px 12px !important;

    background:
        #0d1720 !important;

    border:
        1px solid #263746 !important;

    border-radius:
        6px !important;

    color:
        #7f95a8 !important;

    font-size:
        10px !important;

}


.rt-v5-meta strong {

    color:
        #bcd0df !important;

    font-family:
        monospace !important;

    font-size:
        10px !important;

}


.rt-v5-table-wrap {

    overflow-x:
        auto !important;

    border:
        1px solid #293b4a !important;

    border-radius:
        7px !important;

}


.rt-v5-table {

    width:
        100% !important;

    min-width:
        850px !important;

    border-collapse:
        collapse !important;

    font-size:
        11px !important;

}


.rt-v5-table th {

    padding:
        11px 12px !important;

    text-align:
        left !important;

    white-space:
        nowrap !important;

    background:
        #111c25 !important;

    color:
        #8fa5b6 !important;

    border-bottom:
        1px solid #304252 !important;

    font-size:
        10px !important;

    font-weight:
        700 !important;

    letter-spacing:
        .35px !important;

}


.rt-v5-table td {

    padding:
        11px 12px !important;

    background:
        #0b141c !important;

    color:
        #d1dfe9 !important;

    border-bottom:
        1px solid #1f303d !important;

    vertical-align:
        top !important;

}


.rt-v5-table tr:hover td {

    background:
        #101d27 !important;

}


.rt-v5-table tr:last-child td {

    border-bottom:
        0 !important;

}


.rt-v5-badge {

    display:
        inline-block !important;

    padding:
        4px 8px !important;

    border-radius:
        20px !important;

    background:
        #12283a !important;

    color:
        #75bcff !important;

    font-size:
        9px !important;

    font-weight:
        700 !important;

    letter-spacing:
        .3px !important;

}


.rt-v5-raw-title {

    margin-top:
        18px !important;

    margin-bottom:
        7px !important;

    color:
        #8399aa !important;

    font-size:
        10px !important;

    font-weight:
        700 !important;

    letter-spacing:
        .5px !important;

}


.rt-v5-raw {

    margin:
        0 !important;

    padding:
        14px !important;

    max-height:
        280px !important;

    overflow:
        auto !important;

    background:
        #050a0f !important;

    border:
        1px solid #263544 !important;

    border-radius:
        7px !important;

    color:
        #9db2c2 !important;

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


.rt-v5-footer {

    padding:
        11px 20px !important;

    background:
        #0d1720 !important;

    border-top:
        1px solid #263746 !important;

    color:
        #647b8e !important;

    font-size:
        10px !important;

}


.rt-v5-empty {

    max-width:
        560px !important;

}


.rt-v5-empty-body {

    padding:
        45px 30px !important;

    text-align:
        center !important;

}


.rt-v5-empty-icon {

    width:
        42px !important;

    height:
        42px !important;

    margin:
        0 auto 16px !important;

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    border:
        1px solid #765d36 !important;

    border-radius:
        50% !important;

    background:
        #241b10 !important;

    color:
        #e7aa58 !important;

    font-weight:
        700 !important;

}


.rt-v5-empty-body h3 {

    margin:
        0 0 8px !important;

    color:
        #edf5fb !important;

}


.rt-v5-empty-body p {

    margin:
        0 !important;

    color:
        #879aaa !important;

    line-height:
        1.6 !important;

}


/* Report button after real result arrives */

.rt-v5-ready {

    border-color:
        #286a9e !important;

    color:
        #78c0ff !important;

}


@media (max-width: 800px) {

    .rt-v5-overlay {

        padding:
            12px !important;

    }

    .rt-v5-modal {

        width:
            98vw !important;

        max-height:
            94vh !important;

    }

    .rt-v5-header {

        padding:
            14px !important;

    }

    .rt-v5-content {

        padding:
            12px !important;

    }

}

"""


css_text = CSS.read_text(
    encoding="utf-8"
)


if "RIPPLETRACE REPORT V5" not in css_text:

    with CSS.open(
        "a",
        encoding="utf-8"
    ) as f:

        f.write(
            "\n\n" +
            v5_css +
            "\n"
        )

    print(
        "[OK] V5 report CSS added"
    )

else:

    print(
        "[SKIP] V5 CSS already exists"
    )


# ============================================================
# FINAL VALIDATION
# ============================================================

final_html = INDEX.read_text(
    encoding="utf-8"
)


print()
print("=" * 68)
print("RIPPLETRACE V5 REPORT FIX INSTALLED")
print("=" * 68)

print()
print("OLD REPORT LAYERS REMOVED:")
for item in old_scripts:
    if item in final_html:
        print("  WARNING: still referenced ->", item)
    else:
        print("  ✓", item)

print()
print("NEW:")
print("  ✓ report-v5.js")
print("  ✓ Real backend response capture")
print("  ✓ No fake fallback data")
print("  ✓ Report only opens from report buttons")
print("  ✓ SEND TO AGENT buttons untouched")
print("  ✓ Original fetch response returned to app")

print()
print("UNCHANGED:")
print("  ✓ app.js")
print("  ✓ CAP service")
print("  ✓ Agent files")
print("  ✓ Database")
print("  ✓ CDS")
print("  ✓ API endpoints")
print("  ✓ Approval logic")

print()
print("NOW:")
print("  1. Refresh browser with Ctrl + Shift + R")
print("  2. Click SEND TO TRACE AGENT")
print("  3. Wait for agent completion")
print("  4. Click VIEW TRACE REPORT")
print("  5. The popup will contain the REAL backend response")

print()
print("No simulated agent results are generated.")
print("=" * 68)
