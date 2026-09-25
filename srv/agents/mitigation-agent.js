const cds = require('@sap/cds');

const runPredictionAgent = require('./prediction-agent');

module.exports = async function runMitigationAgent(disruptionId) {

    const db = await cds.connect.to('db');

    const { AlternateSuppliers, Suppliers } =
        cds.entities('rippletrace');

    // Get prediction first
    const prediction = await runPredictionAgent(disruptionId);

    const componentName = prediction.impact.component;
    const stockoutGapDays =
        prediction.impact.stockoutGapDays;

    // Find component
    const component = await db.run(
        SELECT.one
            .from('rippletrace_Components')
            .where({ name: componentName })
    );

    if (!component) {
        throw new Error(
            `Component not found: ${componentName}`
        );
    }

    // Find alternate suppliers
    const alternatives = await db.run(
        SELECT.from(AlternateSuppliers)
            .where({ component_ID: component.ID })
    );

    if (!alternatives.length) {
        return {
            status: 'NO_ALTERNATIVE',
            recommendation: null,
            reason: 'No alternate supplier available'
        };
    }

    // Score alternatives
    const scored = alternatives.map(candidate => {

        const leadTime = Number(candidate.leadTimeDays);
        const costIndex = Number(candidate.costIndex);

        let score = 0;

        // Can the supplier cover the exposure?
        if (leadTime <= stockoutGapDays) {
            score += 50;
        }

        // Prefer lower risk
        if (candidate.riskLevel === 'LOW') {
            score += 25;
        } else if (candidate.riskLevel === 'MEDIUM') {
            score += 10;
        }

        // Prefer pre-vetted suppliers
        if (candidate.preVetted) {
            score += 20;
        }

        // Prefer reasonable cost
        if (costIndex <= 1.20) {
            score += 5;
        }

        return {
            ID: candidate.ID,
            supplier_ID: candidate.supplier_ID,
            component_ID: candidate.component_ID,
            leadTimeDays: leadTime,
            costIndex: costIndex,
            riskLevel: candidate.riskLevel,
            preVetted: candidate.preVetted,
            score
        };
    });

    // Highest score first
    scored.sort((a, b) => b.score - a.score);

    const recommended = scored[0];

    // Get supplier name
    const supplier = await db.run(
        SELECT.one
            .from('rippletrace_Suppliers')
            .where({ ID: recommended.supplier_ID })
    );

    return {

        disruption: prediction.disruption,

        risk: {
            level: prediction.impact.riskLevel,
            stockoutGapDays
        },

        recommendation: {
            supplier: supplier?.name || recommended.supplier_ID,
            supplierId: recommended.supplier_ID,
            component: componentName,
            leadTimeDays: recommended.leadTimeDays,
            costIndex: recommended.costIndex,
            riskLevel: recommended.riskLevel,
            preVetted: recommended.preVetted,
            score: recommended.score
        },

        alternatives: scored
    };
};
