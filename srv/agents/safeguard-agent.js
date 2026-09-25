const cds = require('@sap/cds');

const runMitigationAgent =
    require('./mitigation-agent');

module.exports = async function runSafeguardAgent(disruptionId) {

    const db = await cds.connect.to('db');

    const {
        Decisions,
        RiskAssessments
    } = cds.entities('rippletrace');

    // Get mitigation recommendation
    const mitigation =
        await runMitigationAgent(disruptionId);

    if (!mitigation.recommendation) {
        return {
            status: 'NO_RECOMMENDATION',
            message: 'No mitigation recommendation available'
        };
    }

    const recommendation =
        mitigation.recommendation;

    // Create a risk assessment
    const riskId = cds.utils.uuid();

    await db.run(
        INSERT.into(RiskAssessments).entries({
            ID: riskId,
            riskScore: 100,
            stockoutGapDays:
                mitigation.risk.stockoutGapDays,
            confidence: 95,
            status: 'PENDING_APPROVAL'
        })
    );

    // Create human approval decision
    const decisionId = cds.utils.uuid();

    await db.run(
        INSERT.into(Decisions).entries({
            ID: decisionId,
            risk_ID: riskId,
            recommendation:
                `Switch to ${recommendation.supplier} for ${recommendation.component}. ` +
                `Lead time ${recommendation.leadTimeDays} days, ` +
                `risk level ${recommendation.riskLevel}.`,
            alternate_ID:mitigation.alternatives[0].ID,
            status: 'PENDING_APPROVAL',
            humanApproved: false
        })
    );

    return {
        status: 'PENDING_APPROVAL',

        decision: {
            id: decisionId,
            riskId: riskId,
            recommendation:
                recommendation.supplier,
            component:
                recommendation.component,
            leadTimeDays:
                recommendation.leadTimeDays,
            riskLevel:
                recommendation.riskLevel,
            score:
                recommendation.score,
            humanApproved: false
        },

        message:
            'Recommendation created. Human approval required.'
    };
};
