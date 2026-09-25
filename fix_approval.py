#!/usr/bin/env python3

from pathlib import Path
import shutil
from datetime import datetime

PROJECT = Path.home() / "RippleTrace"
SERVICE = PROJECT / "srv" / "risk-service.js"

if not SERVICE.exists():
    raise SystemExit(f"ERROR: {SERVICE} not found.")

source = SERVICE.read_text()

old = """// HUMAN APPROVAL
this.on('approveDecision', async (req) => {

    const { decisionId, approved } = req.data;

    if (!decisionId) {
        return req.error(
            400,
            'decisionId is required'
        );
    }

    const db = await cds.connect.to('db');

    const { Decisions } =
        cds.entities('rippletrace');

    const decision =
        await db.run(
            SELECT.one
                .from(Decisions)
                .where({ ID: decisionId })
        );

    if (!decision) {
        return req.error(
            404,
            'Decision not found'
        );
    }

    const newStatus =
        approved ? 'APPROVED' : 'REJECTED';

    await db.run(
        UPDATE(Decisions)
            .set({
                status: newStatus,
                humanApproved: approved
            })
            .where({ ID: decisionId })
    );

    return JSON.stringify({
        decisionId,
        status: newStatus,
        humanApproved: approved,
        message: approved
            ? 'Recommendation approved by human.'
            : 'Recommendation rejected by human.'
    });
});"""

new = """// HUMAN APPROVAL
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
});"""

if old not in source:
    raise SystemExit(
        "ERROR: Expected HUMAN APPROVAL block was not found.\n"
        "No files were changed."
    )

timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
backup = SERVICE.with_name(f"risk-service.js.backup_{timestamp}")

shutil.copy2(SERVICE, backup)
SERVICE.write_text(source.replace(old, new))

print("=" * 60)
print("RippleTrace Approval Fix")
print("=" * 60)
print("Changed ONLY:")
print("  srv/risk-service.js")
print()
print("Created backup:")
print(f"  {backup}")
print()
print("UI files were NOT modified.")
print("CDS schema was NOT modified.")
print("CSV data was NOT modified.")
print("package.json was NOT modified.")
print("=" * 60)
