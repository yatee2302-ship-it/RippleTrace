sap.ui.define([
    "sap/ui/core/mvc/Controller",
    "sap/m/MessageToast",
    "sap/m/MessageBox"
], function (Controller, MessageToast, MessageBox) {
    "use strict";

    return Controller.extend("rippletrace.controller.App", {

        onInit: function () {
            console.log("RippleTrace Control Tower started");

            this._state = {
                traceDone: false,
                predictionDone: false,
                recommendationDone: false,
                safeguardDone: false,
                decisionId: null
            };

            this.loadDashboard();
        },

        // =========================================================
        // HTTP HELPERS
        // =========================================================

        getJSON: async function (endpoint) {
            const url = window.location.origin + "/api/risk/" + endpoint;

            const response = await fetch(url, {
                method: "GET",
                headers: {
                    "Accept": "application/json"
                }
            });

            if (!response.ok) {
                throw new Error(
                    "GET " + endpoint + " failed: " +
                    response.status + " " + response.statusText
                );
            }

            return response.json();
        },

        postAction: async function (action, body) {
            const url = window.location.origin + "/api/risk/" + action;

            console.log("Calling:", url, body);

            const response = await fetch(url, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "Accept": "application/json"
                },
                body: JSON.stringify(body || {})
            });

            const text = await response.text();

            console.log("Action response:", text);

            if (!response.ok) {
                throw new Error(
                    action + " failed: " +
                    response.status + " " +
                    text
                );
            }

            try {
                return JSON.parse(text);
            } catch (e) {
                return {
                    value: text
                };
            }
        },

        parseAgentResult: function (response) {
            if (!response) {
                return {};
            }

            let value = response.value;

            if (typeof value === "string") {
                try {
                    return JSON.parse(value);
                } catch (e) {
                    return {
                        message: value
                    };
                }
            }

            return value || response;
        },

        // =========================================================
        // DASHBOARD
        // =========================================================

        loadDashboard: async function () {
            try {
                const [
                    suppliers,
                    components,
                    inventory,
                    disruptions,
                    nodes
                ] = await Promise.all([
                    this.getJSON("Suppliers"),
                    this.getJSON("Components"),
                    this.getJSON("Inventory"),
                    this.getJSON("Disruptions"),
                    this.getJSON("SupplyChainNodes")
                ]);

                const supplierData = suppliers.value || [];
                const componentData = components.value || [];
                const inventoryData = inventory.value || [];
                const disruptionData = disruptions.value || [];
                const nodeData = nodes.value || [];

                this._dashboardData = {
                    suppliers: supplierData,
                    components: componentData,
                    inventory: inventoryData,
                    disruptions: disruptionData,
                    nodes: nodeData
                };

                this.setText("supplierCount", supplierData.length);
                this.setText("componentCount", componentData.length);
                this.setText("inventoryCount", inventoryData.length);
                this.setText("disruptionCount", disruptionData.length);
                this.setText("nodeCount", nodeData.length);

                const activeDisruption = disruptionData.find(function (d) {
                    return d.status === "ACTIVE";
                }) || disruptionData[0];

                if (activeDisruption) {
                    this.setText(
                        "disruptionTitle",
                        activeDisruption.title || activeDisruption.name || "Active disruption"
                    );

                    this.setText(
                        "disruptionLocation",
                        activeDisruption.location || "Supply Network"
                    );

                    this.setText(
                        "disruptionSeverity",
                        activeDisruption.severity || activeDisruption.riskLevel || "HIGH"
                    );

                    this.setText(
                        "disruptionDuration",
                        activeDisruption.durationDays
                            ? activeDisruption.durationDays + " days"
                            : "Active"
                    );
                }

                // Initial states
                this.setStatus("traceStatus", "Ready");
                this.setStatus("predictionStatus", "Locked");
                this.setStatus("recommendationStatus", "Locked");
                this.setStatus("safeguardStatus", "Locked");

                this.setButtonEnabled("traceButton", true);
                this.setButtonEnabled("predictButton", false);
                this.setButtonEnabled("recommendButton", false);
                this.setButtonEnabled("safeguardButton", false);
                this.setButtonEnabled("approvalButton", false);
                this.setButtonEnabled("rejectButton", false);

                console.log("Dashboard data loaded", {
                    suppliers: supplierData.length,
                    components: componentData.length,
                    inventory: inventoryData.length,
                    disruptions: disruptionData.length,
                    nodes: nodeData.length
                });

            } catch (error) {
                console.error("Dashboard loading failed:", error);

                MessageBox.error(
                    "Unable to load RippleTrace dashboard data.\n\n" +
                    error.message
                );
            }
        },

        // =========================================================
        // TRACE AGENT
        // =========================================================

        onTrace: async function () {
            console.log("TRACE AGENT ACTIVATED");

            if (this._state.traceDone) {
                MessageToast.show("Trace Agent already completed.");
                return;
            }

            try {
                this.setStatus("traceStatus", "Running...");
                this.setText("traceResult", "Tracing multi-tier dependencies...");
                this.setButtonEnabled("traceButton", false);

                const response = await this.postAction(
                    "triggerCascade",
                    {
                        disruptionId: "DIS001"
                    }
                );

                console.log("TRACE RESPONSE:", response);

                const result = this.parseAgentResult(response);

                console.log("TRACE RESULT:", result);

                const affectedNodes =
                    result.affectedNodes ||
                    result.nodes ||
                    [];

                const affectedCount =
                    result.affectedCount ||
                    affectedNodes.length ||
                    0;

                this.setStatus("traceStatus", "Completed");

                this.setText(
                    "traceCount",
                    affectedCount + " nodes affected"
                );

                this.setText(
                    "traceSummary",
                    result.summary ||
                    result.message ||
                    "Cascade traced successfully across the supply network."
                );

                this.setText(
                    "traceResult",
                    this.formatResult(result)
                );

                this._state.traceDone = true;

                this.setButtonEnabled("predictButton", true);
                this.setStatus("predictionStatus", "Ready");

                MessageToast.show(
                    "Trace Agent completed — " +
                    affectedCount +
                    " nodes affected."
                );

            } catch (error) {
                console.error("TRACE ERROR:", error);

                this.setStatus("traceStatus", "Failed");
                this.setText(
                    "traceResult",
                    "Trace failed: " + error.message
                );

                this.setButtonEnabled("traceButton", true);

                MessageBox.error(
                    "Trace Agent failed.\n\n" +
                    error.message
                );
            }
        },

        // =========================================================
        // PREDICTION AGENT
        // =========================================================

        onPredict: async function () {
            console.log("PREDICTION AGENT ACTIVATED");

            if (!this._state.traceDone) {
                MessageBox.warning(
                    "Complete the Trace Agent before running Prediction."
                );
                return;
            }

            if (this._state.predictionDone) {
                MessageToast.show("Prediction Agent already completed.");
                return;
            }

            try {
                this.setStatus("predictionStatus", "Running...");
                this.setText(
                    "predictionResult",
                    "Calculating inventory exposure and stockout risk..."
                );

                this.setButtonEnabled("predictButton", false);

                const response = await this.postAction(
                    "triggerPrediction",
                    {
                        disruptionId: "DIS001"
                    }
                );

                console.log("PREDICTION RESPONSE:", response);

                const result = this.parseAgentResult(response);

                console.log("PREDICTION RESULT:", result);

                this.setStatus("predictionStatus", "Completed");

                this.setText(
                    "predictionComponent",
                    result.component || "Power IC"
                );

                this.setText(
                    "predictionFactory",
                    result.factory || "India Electronics Plant"
                );

                this.setText(
                    "inventoryDays",
                    result.inventoryDays ??
                    result.stockDays ??
                    "11"
                );

                this.setText(
                    "leadTimeDays",
                    result.leadTimeDays ??
                    result.normalLeadTimeDays ??
                    "18"
                );

                this.setText(
                    "stockoutGap",
                    result.stockoutGap ??
                    result.exposureDays ??
                    "7"
                );

                this.setText(
                    "riskLevel",
                    result.riskLevel || "HIGH"
                );

                this.setText(
                    "predictionResult",
                    this.formatResult(result)
                );

                this._state.predictionDone = true;

                this.setButtonEnabled("recommendButton", true);
                this.setStatus("recommendationStatus", "Ready");

                MessageToast.show(
                    "Prediction Agent completed."
                );

            } catch (error) {
                console.error("PREDICTION ERROR:", error);

                this.setStatus("predictionStatus", "Failed");

                this.setText(
                    "predictionResult",
                    "Prediction failed: " + error.message
                );

                this.setButtonEnabled("predictButton", true);

                MessageBox.error(
                    "Prediction Agent failed.\n\n" +
                    error.message
                );
            }
        },

        // =========================================================
        // RECOMMENDATION AGENT
        // =========================================================

        onRecommend: async function () {
            console.log("RECOMMENDATION AGENT ACTIVATED");

            if (!this._state.predictionDone) {
                MessageBox.warning(
                    "Complete the Prediction Agent before running Recommendation."
                );
                return;
            }

            if (this._state.recommendationDone) {
                MessageToast.show(
                    "Recommendation Agent already completed."
                );
                return;
            }

            try {
                this.setStatus(
                    "recommendationStatus",
                    "Running..."
                );

                this.setText(
                    "recommendResult",
                    "Evaluating alternate suppliers..."
                );

                this.setButtonEnabled(
                    "recommendButton",
                    false
                );

                const response = await this.postAction(
                    "triggerMitigation",
                    {
                        disruptionId: "DIS001"
                    }
                );

                console.log(
                    "RECOMMENDATION RESPONSE:",
                    response
                );

                const result = this.parseAgentResult(response);

                console.log(
                    "RECOMMENDATION RESULT:",
                    result
                );

                const recommendation =
                    result.recommendation ||
                    result.recommendedSupplier ||
                    result;

                this.setStatus(
                    "recommendationStatus",
                    "Completed"
                );

                this.setText(
                    "recommendedSupplier",
                    recommendation.supplierName ||
                    recommendation.supplier ||
                    "Vendor Y"
                );

                this.setText(
                    "recommendComponent",
                    recommendation.component ||
                    "Power IC"
                );

                this.setText(
                    "recommendLeadTime",
                    recommendation.leadTimeDays ??
                    recommendation.leadTime ??
                    "5"
                );

                this.setText(
                    "recommendRisk",
                    recommendation.riskLevel ||
                    recommendation.risk ||
                    "LOW"
                );

                this.setText(
                    "recommendScore",
                    recommendation.score ??
                    "100"
                );

                this.setText(
                    "preVetted",
                    recommendation.preVetted === false
                        ? "NO"
                        : "YES"
                );

                this.setText(
                    "recommendResult",
                    this.formatResult(result)
                );

                this._state.recommendationDone = true;

                this.setButtonEnabled(
                    "safeguardButton",
                    true
                );

                this.setStatus(
                    "safeguardStatus",
                    "Ready"
                );

                MessageToast.show(
                    "Recommendation Agent completed."
                );

            } catch (error) {
                console.error(
                    "RECOMMENDATION ERROR:",
                    error
                );

                this.setStatus(
                    "recommendationStatus",
                    "Failed"
                );

                this.setText(
                    "recommendResult",
                    "Recommendation failed: " +
                    error.message
                );

                this.setButtonEnabled(
                    "recommendButton",
                    true
                );

                MessageBox.error(
                    "Recommendation Agent failed.\n\n" +
                    error.message
                );
            }
        },

        // =========================================================
        // SAFEGUARD AGENT
        // =========================================================

        onSafeguard: async function () {
            console.log("SAFEGUARD AGENT ACTIVATED");

            if (!this._state.recommendationDone) {
                MessageBox.warning(
                    "Complete the Recommendation Agent first."
                );
                return;
            }

            if (this._state.safeguardDone) {
                MessageToast.show(
                    "Safeguard decision already created."
                );
                return;
            }

            try {
                this.setStatus(
                    "safeguardStatus",
                    "Creating approval request..."
                );

                this.setText(
                    "decisionText",
                    "Safeguard Agent is preparing the mitigation decision for human approval..."
                );

                this.setButtonEnabled(
                    "safeguardButton",
                    false
                );

                const response = await this.postAction(
                    "triggerSafeguard",
                    {
                        disruptionId: "DIS001"
                    }
                );

                console.log(
                    "SAFEGUARD RESPONSE:",
                    response
                );

                const result = this.parseAgentResult(response);

                console.log(
                    "SAFEGUARD RESULT:",
                    result
                );

                // Handle different possible CAP response shapes
                let decisionId =
                    result.decisionId ||
                    result.DecisionId ||
                    result.ID ||
                    result.id ||
                    null;

                let recommendation =
                    result.recommendation ||
                    result.message ||
                    result.description ||
                    "";

                // If backend returned only a decision ID,
                // retrieve the created decision.
                if (!decisionId && typeof result === "string") {
                    decisionId = result;
                }

                // Fallback: find latest pending decision.
                if (!decisionId) {
                    try {
                        const decisions =
                            await this.getJSON(
                                "Decisions?$orderby=createdAt%20desc"
                            );

                        const list =
                            decisions.value || [];

                        const pending =
                            list.find(function (d) {
                                return d.status ===
                                    "PENDING_APPROVAL";
                            });

                        if (pending) {
                            decisionId =
                                pending.ID ||
                                pending.id;

                            recommendation =
                                pending.recommendation ||
                                recommendation;
                        }
                    } catch (lookupError) {
                        console.warn(
                            "Decision lookup failed:",
                            lookupError
                        );
                    }
                }

                this._state.decisionId = decisionId;
                this._state.safeguardDone = true;

                this.setStatus(
                    "safeguardStatus",
                    "PENDING HUMAN APPROVAL"
                );

                this.setText(
                    "decisionText",
                    recommendation ||
                    "Mitigation recommendation generated. Human approval required."
                );

                this.setText(
                    "decisionId",
                    decisionId ||
                    "Decision created"
                );

                this.setText(
                    "decisionStatus",
                    "PENDING_APPROVAL"
                );

                this.setButtonEnabled(
                    "approvalButton",
                    !!decisionId
                );

                this.setButtonEnabled(
                    "rejectButton",
                    true
                );

                MessageToast.show(
                    "Safeguard decision ready for human approval."
                );

            } catch (error) {
                console.error(
                    "SAFEGUARD ERROR:",
                    error
                );

                this.setStatus(
                    "safeguardStatus",
                    "Failed"
                );

                this.setText(
                    "decisionText",
                    "Safeguard failed: " +
                    error.message
                );

                this.setButtonEnabled(
                    "safeguardButton",
                    true
                );

                MessageBox.error(
                    "Safeguard Agent failed.\n\n" +
                    error.message
                );
            }
        },

        // =========================================================
        // HUMAN APPROVAL
        // =========================================================

        onApprove: function () {
            console.log("APPROVE BUTTON CLICKED");

            if (!this._state.safeguardDone) {
                MessageBox.warning(
                    "Run the Safeguard Agent first."
                );
                return;
            }

            if (!this._state.decisionId) {
                MessageBox.error(
                    "No decision ID is available for approval."
                );
                return;
            }

            MessageBox.confirm(
                "Approve the recommended supply-chain mitigation?",
                {
                    title: "Human Approval Required",

                    onClose: async function (action) {
                        if (action !== MessageBox.Action.OK) {
                            return;
                        }

                        await this.approveDecision(
                            this._state.decisionId
                        );
                    }.bind(this)
                }
            );
        },

        approveDecision: async function (decisionId) {
            try {
                this.setStatus(
                    "safeguardStatus",
                    "Approving..."
                );

                this.setButtonEnabled(
                    "approvalButton",
                    false
                );

                this.setButtonEnabled(
                    "rejectButton",
                    false
                );

                const response =
                    await this.postAction(
                        "approveDecision",
                        {
                            decisionId: decisionId,
                            approved: true
                        }
                    );

                console.log(
                    "APPROVAL RESPONSE:",
                    response
                );

                const result =
                    this.parseAgentResult(response);

                this.setText(
                    "decisionStatus",
                    result.status ||
                    "APPROVED"
                );

                this.setStatus(
                    "safeguardStatus",
                    "APPROVED"
                );

                MessageToast.show(
                    "Mitigation decision approved."
                );

            } catch (error) {
                console.error(
                    "APPROVAL ERROR:",
                    error
                );

                this.setStatus(
                    "safeguardStatus",
                    "Approval failed"
                );

                this.setButtonEnabled(
                    "approvalButton",
                    true
                );

                this.setButtonEnabled(
                    "rejectButton",
                    true
                );

                MessageBox.error(
                    "Approval failed.\n\n" +
                    error.message
                );
            }
        },

        // =========================================================
        // REJECT
        // =========================================================

        onReject: function () {
            console.log("REJECT BUTTON CLICKED");

            if (!this._state.safeguardDone) {
                MessageBox.warning(
                    "Run the Safeguard Agent first."
                );
                return;
            }

            MessageBox.confirm(
                "Reject this mitigation recommendation?",
                {
                    title: "Reject Decision",

                    onClose: function (action) {
                        if (action !== MessageBox.Action.OK) {
                            return;
                        }

                        this.setText(
                            "decisionStatus",
                            "REJECTED"
                        );

                        this.setStatus(
                            "safeguardStatus",
                            "REJECTED"
                        );

                        this.setButtonEnabled(
                            "approvalButton",
                            false
                        );

                        this.setButtonEnabled(
                            "rejectButton",
                            false
                        );

                        MessageToast.show(
                            "Mitigation recommendation rejected."
                        );
                    }.bind(this)
                }
            );
        },

        // =========================================================
        // UI HELPERS
        // =========================================================

        setText: function (id, value) {
            const control = this.byId(id);

            if (!control) {
                console.warn(
                    "UI control not found:",
                    id
                );
                return;
            }

            if (control.setText) {
                control.setText(
                    value === null ||
                    value === undefined
                        ? "-"
                        : String(value)
                );
            }
        },

        setStatus: function (id, value) {
            const control = this.byId(id);

            if (!control) {
                console.warn(
                    "Status control not found:",
                    id
                );
                return;
            }

            if (control.setText) {
                control.setText(value);
            }

            // Add CSS state classes where possible
            if (control.removeStyleClass) {
                control.removeStyleClass("statusReady");
                control.removeStyleClass("statusRunning");
                control.removeStyleClass("statusComplete");
                control.removeStyleClass("statusLocked");
                control.removeStyleClass("statusPending");
                control.removeStyleClass("statusFailed");

                const normalized =
                    String(value)
                        .toLowerCase();

                if (normalized.includes("running")) {
                    control.addStyleClass(
                        "statusRunning"
                    );
                } else if (
                    normalized.includes("completed") ||
                    normalized.includes("approved")
                ) {
                    control.addStyleClass(
                        "statusComplete"
                    );
                } else if (
                    normalized.includes("pending")
                ) {
                    control.addStyleClass(
                        "statusPending"
                    );
                } else if (
                    normalized.includes("locked")
                ) {
                    control.addStyleClass(
                        "statusLocked"
                    );
                } else if (
                    normalized.includes("failed")
                ) {
                    control.addStyleClass(
                        "statusFailed"
                    );
                } else {
                    control.addStyleClass(
                        "statusReady"
                    );
                }
            }
        },

        setButtonEnabled: function (id, enabled) {
            const button = this.byId(id);

            if (!button) {
                console.warn(
                    "Button not found:",
                    id
                );
                return;
            }

            button.setEnabled(!!enabled);
        },

        formatResult: function (result) {
            if (!result) {
                return "No result returned.";
            }

            if (typeof result === "string") {
                return result;
            }

            // Show important fields as readable lines.
            const lines = [];

            Object.keys(result).forEach(function (key) {
                const value = result[key];

                if (
                    value === null ||
                    value === undefined
                ) {
                    return;
                }

                if (typeof value === "object") {
                    lines.push(
                        key + ": " +
                        JSON.stringify(value)
                    );
                } else {
                    lines.push(
                        key + ": " + value
                    );
                }
            });

            return lines.join("\n");
        }

    });
});
