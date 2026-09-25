const cds = require('@sap/cds');
const runSafeguardAgent = require('./agents/safeguard-agent');
const runMitigationAgent = require('./agents/mitigation-agent');

const runCascadeAgent = require('./agents/cascade-agent');
const runPredictionAgent = require('./agents/prediction-agent');

module.exports = cds.service.impl(async function () {

    // CASCADE AGENT
    this.on('triggerCascade', async (req) => {

        const { disruptionId } = req.data;

        if (!disruptionId) {
            return req.error(400, 'disruptionId is required');
        }

        const result = await runCascadeAgent(disruptionId);

        return JSON.stringify(result);
    });


    // PREDICTION AGENT
    this.on('triggerPrediction', async (req) => {

        const { disruptionId } = req.data;

        if (!disruptionId) {
            return req.error(400, 'disruptionId is required');
        }

        const result = await runPredictionAgent(disruptionId);

        return JSON.stringify(result);
    });
   this.on('triggerMitigation', async (req) => {

    const { disruptionId } = req.data;

    if (!disruptionId) {
        return req.error(
            400,
            'disruptionId is required'
        );
    }

    const result =
        await runMitigationAgent(disruptionId);

    return JSON.stringify(result);
});
    // SAFEGUARD AGENT
this.on('triggerSafeguard', async (req) => {

    const { disruptionId } = req.data;

    if (!disruptionId) {
        return req.error(
            400,
            'disruptionId is required'
        );
    }

    const result =
        await runSafeguardAgent(disruptionId);

    return JSON.stringify(result);
});


// HUMAN APPROVAL
this.on('approveDecision', async (req) => {

    const { decisionId, approved } = req.data;

    if (!decisionId) {
        return req.error(400, 'decisionId is required');
    }

    const newStatus = approved ? 'APPROVED' : 'REJECTED';

    const result = await UPDATE('rippletrace.Decisions')
        .set({
            status: newStatus,
            humanApproved: approved
        })
        .where({ ID: decisionId });

    if (!result) {
        return req.error(404, 'Decision not found');
    }

    return JSON.stringify({
        decisionId,
        status: newStatus,
        humanApproved: approved,
        message: approved
            ? 'Recommendation approved by human.'
            : 'Recommendation rejected by human.'
    });
});
});
