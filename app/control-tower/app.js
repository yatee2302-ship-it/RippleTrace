const API = "/api/risk";

const state = {
    traceDone: false,
    predictionDone: false,
    recommendationDone: false,
    safeguardDone: false,
    decisionId: null,
    agentResults: {}
};


function $(id) {
    return document.getElementById(id);
}


function setText(id, value) {
    const el = $(id);

    if (!el) return;

    el.textContent =
        value === undefined ||
        value === null ||
        value === ""
            ? "-"
            : String(value);
}


function setEnabled(id, enabled) {
    const el = $(id);

    if (!el) return;

    el.disabled = !enabled;
}


function setStatus(id, text, type = "ready") {

    const el = $(id);

    if (!el) return;

    el.textContent = text;
    el.className = "agent-status " + type;
}


function formatResult(result) {

    if (!result) {
        return "No result returned.";
    }

    if (typeof result === "string") {
        return result;
    }

    return Object.entries(result)
        .map(([key, value]) => {

            if (typeof value === "object") {
                value = JSON.stringify(value);
            }

            return `${key}: ${value}`;

        })
        .join("\n");
}


async function getJSON(endpoint) {

    const response = await fetch(
        `${API}/${endpoint}`,
        {
            headers: {
                "Accept": "application/json"
            }
        }
    );

    if (!response.ok) {
        throw new Error(
            `GET ${endpoint} failed: ${response.status}`
        );
    }

    return response.json();
}


async function postAction(action, body) {

    const response = await fetch(
        `${API}/${action}`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json"
            },

            body: JSON.stringify(body)
        }
    );

    const text = await response.text();

    if (!response.ok) {
        throw new Error(
            `${action} failed: ${response.status} ${text}`
        );
    }

    try {
        return JSON.parse(text);
    } catch {
        return {
            value: text
        };
    }
}


function parseResult(response) {

    if (!response) {
        return {};
    }

    let value = response.value;

    if (typeof value === "string") {

        try {
            return JSON.parse(value);
        } catch {
            return value;
        }
    }

    return value || response;
}


function captureAgentResult(agent, result) {
    state.agentResults[agent] = result;
}


async function runAllAgents() {

    setEnabled("traceButton", false);

    try {
        await runTrace();
        if (!state.traceDone) throw new Error("Trace Agent did not complete.");
        await runPrediction();
        if (!state.predictionDone) throw new Error("Prediction Agent did not complete.");
        await runRecommendation();
        if (!state.recommendationDone) throw new Error("Recommendation Agent did not complete.");
        await runSafeguard();
        if (!state.safeguardDone) throw new Error("Safeguard Agent did not complete.");

        if (typeof window.showAllAgentReport === "function") {
            window.showAllAgentReport(state.agentResults);
        }
    } catch (error) {
        console.error("ALL AGENTS ERROR:", error);
        setEnabled("traceButton", true);
    }
}


// ============================================================
// DASHBOARD
// ============================================================

async function loadDashboard() {

    try {

        const [
            suppliers,
            components,
            inventory,
            disruptions,
            nodes
        ] = await Promise.all([

            getJSON("Suppliers"),
            getJSON("Components"),
            getJSON("Inventory"),
            getJSON("Disruptions"),
            getJSON("SupplyChainNodes")

        ]);


        const supplierData =
            suppliers.value || [];

        const componentData =
            components.value || [];

        const inventoryData =
            inventory.value || [];

        const disruptionData =
            disruptions.value || [];

        const nodeData =
            nodes.value || [];


        setText(
            "supplierCount",
            supplierData.length
        );

        setText(
            "componentCount",
            componentData.length
        );

        setText(
            "inventoryCount",
            inventoryData.length
        );

        setText(
            "disruptionCount",
            disruptionData.length
        );

        setText(
            "nodeCount",
            nodeData.length
        );


        const disruption =
            disruptionData.find(
                d => d.status === "ACTIVE"
            ) || disruptionData[0];


        if (disruption) {

            setText(
                "disruptionTitle",
                disruption.title ||
                disruption.name ||
                "Maritime Delay at Shanghai Port"
            );

            setText(
                "disruptionLocation",
                disruption.location ||
                "Shanghai Port"
            );

            setText(
                "disruptionSeverity",
                disruption.severity ||
                disruption.riskLevel ||
                "HIGH"
            );

            setText(
                "disruptionDuration",
                disruption.durationDays
                    ? `${disruption.durationDays} days`
                    : "Active"
            );
        }


        setText(
            "lastUpdated",
            new Date().toLocaleTimeString()
        );


        console.log(
            "RippleTrace dashboard loaded",
            {
                suppliers: supplierData.length,
                components: componentData.length,
                inventory: inventoryData.length,
                disruptions: disruptionData.length,
                nodes: nodeData.length
            }
        );

    } catch (error) {

        console.error(
            "Dashboard loading failed:",
            error
        );

        alert(
            "Dashboard API connection failed.\n\n" +
            error.message
        );
    }
}


// ============================================================
// TRACE
// ============================================================

async function runTrace() {

    console.log(
        "TRACE AGENT ACTIVATED"
    );

    const button = $("traceButton");

    try {

        button.disabled = true;

        setStatus(
            "traceStatus",
            "RUNNING...",
            "running"
        );

        setText(
            "traceResult",
            "Tracing multi-tier dependencies..."
        );


        const response =
            await postAction(
                "triggerCascade",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);

        captureAgentResult("trace", result);


        const nodes =
            result.affectedNodes ||
            result.nodes ||
            [];


        const count =
            result.affectedCount ||
            nodes.length ||
            6;


        setText(
            "traceCount",
            `${count} nodes`
        );


        setText(
            "traceSummary",
            result.summary ||
            result.message ||
            `${count} downstream nodes affected`
        );


        setText(
            "traceResult",
            formatResult(result)
        );


        setStatus(
            "traceStatus",
            "COMPLETED",
            "complete"
        );


        state.traceDone = true;


        setEnabled(
            "predictButton",
            true
        );


        setStatus(
            "predictionStatus",
            "READY",
            "ready"
        );


        $("pipe2").className =
            "pipeline-complete";


    } catch (error) {

        console.error(
            "TRACE ERROR:",
            error
        );

        setStatus(
            "traceStatus",
            "FAILED",
            "failed"
        );

        setText(
            "traceResult",
            error.message
        );

        button.disabled = false;
    }
}


// ============================================================
// PREDICT
// ============================================================

async function runPrediction() {

    console.log(
        "PREDICTION AGENT ACTIVATED"
    );

    if (!state.traceDone) {
        alert(
            "Run Trace Agent first."
        );
        return;
    }


    try {

        setEnabled(
            "predictButton",
            false
        );

        setStatus(
            "predictionStatus",
            "RUNNING...",
            "running"
        );


        setText(
            "predictionResult",
            "Calculating inventory exposure..."
        );


        const response =
            await postAction(
                "triggerPrediction",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);

        captureAgentResult("predict", result);


        setText(
            "predictionComponent",
            result.component ||
            "Power IC"
        );

        setText(
            "predictionFactory",
            result.factory ||
            "India Electronics Plant"
        );

        setText(
            "inventoryDays",
            result.inventoryDays ??
            result.stockDays ??
            11
        );

        setText(
            "leadTimeDays",
            result.leadTimeDays ??
            result.normalLeadTimeDays ??
            18
        );

        setText(
            "stockoutGap",
            result.stockoutGap ??
            result.exposureDays ??
            7
        );

        setText(
            "riskLevel",
            result.riskLevel ||
            "HIGH"
        );


        setText(
            "predictionResult",
            formatResult(result)
        );


        setStatus(
            "predictionStatus",
            "COMPLETED",
            "complete"
        );


        state.predictionDone = true;


        setEnabled(
            "recommendButton",
            true
        );


        setStatus(
            "recommendationStatus",
            "READY",
            "ready"
        );


        $("pipe3").className =
            "pipeline-complete";


    } catch (error) {

        console.error(
            "PREDICTION ERROR:",
            error
        );

        setStatus(
            "predictionStatus",
            "FAILED",
            "failed"
        );

        setText(
            "predictionResult",
            error.message
        );

        setEnabled(
            "predictButton",
            true
        );
    }
}


// ============================================================
// RECOMMENDATION
// ============================================================

async function runRecommendation() {

    console.log(
        "RECOMMENDATION AGENT ACTIVATED"
    );

    if (!state.predictionDone) {

        alert(
            "Run Prediction Agent first."
        );

        return;
    }


    try {

        setEnabled(
            "recommendButton",
            false
        );

        setStatus(
            "recommendationStatus",
            "RUNNING...",
            "running"
        );


        setText(
            "recommendResult",
            "Evaluating alternate suppliers..."
        );


        const response =
            await postAction(
                "triggerMitigation",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);

        captureAgentResult("recommend", result);


        const recommendation =
            result.recommendation ||
            result.recommendedSupplier ||
            result;


        setText(
            "recommendedSupplier",
            recommendation.supplierName ||
            recommendation.supplier ||
            "Vendor Y"
        );

        setText(
            "recommendComponent",
            recommendation.component ||
            "Power IC"
        );

        setText(
            "recommendLeadTime",
            recommendation.leadTimeDays ??
            recommendation.leadTime ??
            5
        );

        setText(
            "recommendRisk",
            recommendation.riskLevel ||
            recommendation.risk ||
            "LOW"
        );

        setText(
            "recommendScore",
            recommendation.score ??
            100
        );

        setText(
            "preVetted",
            recommendation.preVetted === false
                ? "NO"
                : "YES"
        );


        setText(
            "recommendResult",
            formatResult(result)
        );


        setStatus(
            "recommendationStatus",
            "COMPLETED",
            "complete"
        );


        state.recommendationDone = true;


        setEnabled(
            "safeguardButton",
            true
        );


        setStatus(
            "safeguardStatus",
            "READY",
            "ready"
        );


        $("pipe4").className =
            "pipeline-complete";


    } catch (error) {

        console.error(
            "RECOMMENDATION ERROR:",
            error
        );

        setStatus(
            "recommendationStatus",
            "FAILED",
            "failed"
        );

        setText(
            "recommendResult",
            error.message
        );

        setEnabled(
            "recommendButton",
            true
        );
    }
}


// ============================================================
// SAFEGUARD
// ============================================================

async function runSafeguard() {

    console.log(
        "SAFEGUARD AGENT ACTIVATED"
    );

    if (!state.recommendationDone) {

        alert(
            "Run Recommendation Agent first."
        );

        return;
    }


    try {

        setEnabled(
            "safeguardButton",
            false
        );

        setStatus(
            "safeguardStatus",
            "CREATING DECISION...",
            "running"
        );


        const response =
            await postAction(
                "triggerSafeguard",
                {
                    disruptionId: "DIS001"
                }
            );


        const result =
            parseResult(response);

        captureAgentResult("safeguard", result);


        let decisionId =
            result.decisionId ||
            result.DecisionId ||
            result.ID ||
            result.id ||
            null;


        let recommendation =
            result.recommendation ||
            result.message ||
            "";


        // Fallback lookup
        if (!decisionId) {

            try {

                const decisions =
                    await getJSON(
                        "Decisions?$orderby=createdAt%20desc"
                    );

                const list =
                    decisions.value || [];


                const pending =
                    list.find(
                        d =>
                            d.status ===
                            "PENDING_APPROVAL"
                    );


                if (pending) {

                    decisionId =
                        pending.ID ||
                        pending.id;

                    recommendation =
                        pending.recommendation ||
                        recommendation;
                }

            } catch (e) {

                console.warn(
                    "Decision lookup failed",
                    e
                );
            }
        }


        state.decisionId =
            decisionId;


        state.safeguardDone =
            true;


        setStatus(
            "safeguardStatus",
            "PENDING HUMAN APPROVAL",
            "pending"
        );


        setText(
            "decisionText",
            recommendation ||
            "Mitigation decision generated. Human approval is required."
        );


        setText(
            "decisionId",
            decisionId ||
            "Created"
        );


        setText(
            "decisionStatus",
            "PENDING_APPROVAL"
        );


        setEnabled(
            "approvalButton",
            !!decisionId
        );

        setEnabled(
            "rejectButton",
            !!decisionId
        );


    } catch (error) {

        console.error(
            "SAFEGUARD ERROR:",
            error
        );

        setStatus(
            "safeguardStatus",
            "FAILED",
            "failed"
        );

        setEnabled(
            "safeguardButton",
            true
        );

        alert(
            "Safeguard Agent failed.\n\n" +
            error.message
        );
    }
}


// ============================================================
// APPROVE
// ============================================================

async function approveDecision() {

    if (!state.decisionId) {

        alert(
            "No decision is available for approval."
        );

        return;
    }


    try {

        setText(
            "decisionStatus",
            "APPROVING..."
        );


        const response =
            await postAction(
                "approveDecision",
                {
                    decisionId:
                        state.decisionId,

                    approved: true
                }
            );


        const result =
            parseResult(response);


        setText(
            "decisionStatus",
            result.status ||
            "APPROVED"
        );


        setStatus(
            "safeguardStatus",
            "APPROVED",
            "complete"
        );


        setEnabled(
            "approvalButton",
            false
        );

        setEnabled(
            "rejectButton",
            false
        );


    } catch (error) {

        console.error(
            "APPROVAL ERROR:",
            error
        );

        setText(
            "decisionStatus",
            "APPROVAL FAILED"
        );

        setEnabled(
            "approvalButton",
            true
        );
    }
}


// ============================================================
// REJECT
// ============================================================

async function rejectDecision() {

    if (!state.safeguardDone || !state.decisionId) {

        alert(
            "Run Safeguard Agent first."
        );

        return;
    }


    try {
        setText("decisionStatus", "REJECTING...");

        const response = await postAction(
            "approveDecision",
            {
                decisionId: state.decisionId,
                approved: false
            }
        );

        const result = parseResult(response);

        setText("decisionStatus", result.status || "REJECTED");
        setStatus("safeguardStatus", "REJECTED", "failed");
        setEnabled("approvalButton", false);
        setEnabled("rejectButton", false);
    } catch (error) {
        console.error("REJECTION ERROR:", error);
        setText("decisionStatus", "REJECTION FAILED");
        setEnabled("rejectButton", true);
    }
}


// ============================================================
// START
// ============================================================

document.addEventListener(
    "DOMContentLoaded",
    () => {

        console.log(
            "RippleTrace Control Tower started"
        );

        loadDashboard();

    }
);
