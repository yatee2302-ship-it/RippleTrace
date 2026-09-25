
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
