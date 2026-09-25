from pathlib import Path
import shutil
import re

ROOT = Path.home() / "RippleTrace"
APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"
CSS = APP / "css" / "style.css"
JS = APP / "ui-polish-v4.js"


# =========================================================
# SAFETY
# =========================================================

if not APP.exists():
    raise SystemExit(f"ERROR: {APP} not found")

if not INDEX.exists():
    raise SystemExit(f"ERROR: {INDEX} not found")

if not CSS.exists():
    raise SystemExit(f"ERROR: {CSS} not found")


# =========================================================
# BACKUPS
# =========================================================

def backup(path):
    if path.exists():
        backup_path = path.with_suffix(path.suffix + ".v4.bak")
        shutil.copy2(path, backup_path)
        print(f"[BACKUP] {backup_path}")


backup(INDEX)
backup(CSS)
backup(JS)


# =========================================================
# V4 DARK COMMAND CENTER CSS
# =========================================================

dark_css = r"""

/* =========================================================
   RIPPLETRACE V4
   FINAL DARK COMMAND CENTER VISUAL PATCH

   VISUAL ONLY.
   NO APPLICATION / BACKEND LOGIC MODIFIED.
   ========================================================= */


/* ---------------------------------------------------------
   GLOBAL
   --------------------------------------------------------- */

html,
body {
    background: #05090d !important;
    color: #e6eef6 !important;
}


/* ---------------------------------------------------------
   MAIN AGENT COMMAND CENTER
   --------------------------------------------------------- */

#agent-command-center,
.agent-command-center,
.agent-section,
.agents-section {
    background: #070d13 !important;
    color: #e6eef6 !important;
}


/* ---------------------------------------------------------
   AGENT CARDS
   --------------------------------------------------------- */

/*
   Catch the common card containers used by the dashboard.
*/

.agent-card,
.agent-panel,
.agent-container,
.agent-block,
.agent-item,
.agent-box {
    background: #0b1219 !important;

    color: #dce7f1 !important;

    border: 1px solid #263746 !important;

    border-radius: 8px !important;

    box-shadow:
        0 10px 28px rgba(0, 0, 0, .28),
        inset 0 1px 0 rgba(255,255,255,.025) !important;

    overflow: hidden !important;

    margin-bottom: 12px !important;
}


/* ---------------------------------------------------------
   AGENT CARD HEADER
   --------------------------------------------------------- */

.agent-card header,
.agent-card .agent-header,
.agent-card .card-header,
.agent-card .header,
.agent-panel header,
.agent-panel .header {
    background: #0d161f !important;

    color: #e8f1f8 !important;

    border-bottom: 1px solid #263746 !important;
}


/* ---------------------------------------------------------
   AGENT TITLES
   --------------------------------------------------------- */

.agent-card h1,
.agent-card h2,
.agent-card h3,
.agent-card h4,
.agent-card h5,
.agent-card strong,
.agent-card .agent-title,
.agent-card .title,
.agent-card .name {

    color: #edf5fb !important;

    opacity: 1 !important;
}


/* Agent number */

.agent-card .step,
.agent-card .number,
.agent-card .agent-number {

    background: #17232e !important;

    color: #9db3c5 !important;

    border: 1px solid #2c4050 !important;
}


/* ---------------------------------------------------------
   AGENT DESCRIPTION
   --------------------------------------------------------- */

.agent-card p,
.agent-card .description,
.agent-card .subtitle,
.agent-card .agent-description {

    color: #9cafbf !important;

    opacity: 1 !important;
}


/* ---------------------------------------------------------
   GENERAL TEXT INSIDE AGENT CARDS
   --------------------------------------------------------- */

.agent-card span,
.agent-card label,
.agent-card div {

    color: inherit;
}


/* ---------------------------------------------------------
   METRIC / DATA BOXES
   --------------------------------------------------------- */

.agent-card .metric,
.agent-card .metric-box,
.agent-card .stat,
.agent-card .stat-box,
.agent-card .field,
.agent-card .data-field,
.agent-card .info-box,
.agent-card .value-box {

    background: #111b24 !important;

    color: #dce8f2 !important;

    border: 1px solid #293b4a !important;

    border-radius: 6px !important;
}


/* Metric labels */

.agent-card .metric-label,
.agent-card .label,
.agent-card .field-label,
.agent-card .stat-label {

    color: #8298aa !important;

    opacity: 1 !important;
}


/* Metric values */

.agent-card .metric-value,
.agent-card .value,
.agent-card .stat-value,
.agent-card .field-value {

    color: #edf5fb !important;

    font-weight: 600 !important;

    opacity: 1 !important;
}


/* ---------------------------------------------------------
   IMPORTANT:
   HIDE ALL EXISTING AGENT OUTPUT CONTAINERS
   --------------------------------------------------------- */

.agent-output,
.output-box,
.agent-card .agent-output,
.agent-card .output-box,
[class*="agent-output"],
[class*="output-box"],
[class*="agent_output"],
[class*="output_box"] {

    display: none !important;

    visibility: hidden !important;

    height: 0 !important;

    min-height: 0 !important;

    max-height: 0 !important;

    margin: 0 !important;

    padding: 0 !important;

    border: 0 !important;

    overflow: hidden !important;
}


/* ---------------------------------------------------------
   BUTTON AREA
   --------------------------------------------------------- */

.agent-card button,
.agent-panel button {

    min-height: 34px !important;

    border-radius: 6px !important;

    font-size: 11px !important;

    font-weight: 600 !important;

    letter-spacing: .2px !important;

    transition:
        background .18s ease,
        border-color .18s ease,
        transform .18s ease !important;
}


/* Primary action */

.agent-card button.primary,
.agent-card .primary-button,
.agent-card button[id*="send"],
.agent-card button[id*="Send"] {

    background: #087cf5 !important;

    color: #ffffff !important;

    border: 1px solid #087cf5 !important;
}


/* Hover */

.agent-card button:hover:not(:disabled) {

    transform: translateY(-1px) !important;

    border-color: #168cff !important;
}


/* Disabled */

.agent-card button:disabled {

    background: #111920 !important;

    color: #607487 !important;

    border-color: #293946 !important;

    opacity: .9 !important;
}


/* Report button */

.agent-card button[class*="report"],
.agent-card button[id*="report"],
.agent-card button[class*="Report"],
.agent-card button[id*="Report"] {

    background: #101c27 !important;

    color: #73b8ff !important;

    border: 1px solid #2b526f !important;
}


/* ---------------------------------------------------------
   AGENT STATUS BADGES
   --------------------------------------------------------- */

.agent-card .status,
.agent-card .badge,
.agent-card .agent-status {

    background: #14202a !important;

    color: #9fb4c6 !important;

    border: 1px solid #304454 !important;

    border-radius: 20px !important;

    padding: 4px 9px !important;

    font-size: 9px !important;

    font-weight: 700 !important;

    letter-spacing: .4px !important;
}


/* ---------------------------------------------------------
   LOCKED / READY / COMPLETED
   --------------------------------------------------------- */

.agent-card [class*="locked"],
.agent-card [class*="LOCKED"] {

    color: #7c91a3 !important;

    background: #111a22 !important;
}


.agent-card [class*="ready"],
.agent-card [class*="READY"] {

    color: #62aefc !important;

    background: #102338 !important;
}


.agent-card [class*="completed"],
.agent-card [class*="COMPLETED"] {

    color: #55d69a !important;

    background: #10251d !important;
}


/* ---------------------------------------------------------
   HUMAN APPROVAL SECTION
   --------------------------------------------------------- */

.agent-card .approval,
.agent-card .approval-box,
.agent-card [class*="approval"] {

    background: #111a21 !important;

    color: #dce7ef !important;

    border-color: #3b4650 !important;

    border-radius: 7px !important;
}


/* Approval heading */

.agent-card .approval h3,
.agent-card .approval strong {

    color: #f0a35a !important;
}


/* ---------------------------------------------------------
   APPROVE BUTTON
   --------------------------------------------------------- */

.agent-card button[id*="approve"],
.agent-card button[class*="approve"] {

    background: #2e8b62 !important;

    color: #ffffff !important;

    border-color: #3da978 !important;
}


/* ---------------------------------------------------------
   REJECT BUTTON
   --------------------------------------------------------- */

.agent-card button[id*="reject"],
.agent-card button[class*="reject"] {

    background: transparent !important;

    color: #ff8d8d !important;

    border-color: #9f4444 !important;
}


/* ---------------------------------------------------------
   AGENT SECTION SPACING
   --------------------------------------------------------- */

.agent-card {

    padding: 0 !important;
}


.agent-card .content,
.agent-card .body,
.agent-card .agent-body {

    padding: 18px 20px !important;

    background: #0b1219 !important;
}


/* ---------------------------------------------------------
   FORM / INPUT ELEMENTS
   --------------------------------------------------------- */

.agent-card input,
.agent-card textarea,
.agent-card select {

    background: #101a23 !important;

    color: #e1ebf4 !important;

    border: 1px solid #2b3d4c !important;
}


/* ---------------------------------------------------------
   SCROLLBAR
   --------------------------------------------------------- */

.agent-card ::-webkit-scrollbar,
.rt-v3-modal ::-webkit-scrollbar {

    width: 7px;

    height: 7px;
}


.agent-card ::-webkit-scrollbar-track,
.rt-v3-modal ::-webkit-scrollbar-track {

    background: #080e13;
}


.agent-card ::-webkit-scrollbar-thumb,
.rt-v3-modal ::-webkit-scrollbar-thumb {

    background: #304252;

    border-radius: 10px;
}


/* ---------------------------------------------------------
   REPORT BUTTONS
   --------------------------------------------------------- */

[class*="view"][class*="report"],
[id*="report"] {

    color: #75bcff !important;
}


/* ---------------------------------------------------------
   REPORT MODAL
   --------------------------------------------------------- */

.rt-v3-overlay {

    background: rgba(1, 5, 9, .82) !important;

    backdrop-filter: blur(8px) !important;
}


.rt-v3-modal {

    width: min(1180px, 94vw) !important;

    max-height: 88vh !important;

    background: #081018 !important;

    color: #dce8f3 !important;

    border: 1px solid #304454 !important;

    border-radius: 10px !important;

    box-shadow:
        0 30px 100px rgba(0,0,0,.7) !important;
}


.rt-v3-header {

    background: #0d1720 !important;

    border-bottom: 1px solid #293b4a !important;

    padding: 17px 20px !important;
}


.rt-v3-title {

    color: #f0f6fb !important;

    font-size: 15px !important;

    letter-spacing: .3px !important;
}


.rt-v3-subtitle {

    color: #758b9d !important;
}


.rt-v3-content {

    background: #081018 !important;

    padding: 18px !important;
}


.rt-v3-table-wrap {

    border: 1px solid #293b4a !important;

    border-radius: 7px !important;
}


.rt-v3-table th {

    background: #111c25 !important;

    color: #8ca1b2 !important;

    border-color: #293b4a !important;

    font-size: 10px !important;

    letter-spacing: .5px !important;
}


.rt-v3-table td {

    background: #0b141c !important;

    color: #d2dfe9 !important;

    border-color: #1f303d !important;
}


.rt-v3-table tr:hover td {

    background: #101d27 !important;
}


/* ---------------------------------------------------------
   RESPONSIVE ALIGNMENT
   --------------------------------------------------------- */

@media (max-width: 900px) {

    .agent-card .body,
    .agent-card .agent-body,
    .agent-card .content {

        padding: 14px !important;
    }

    .agent-card {

        margin-bottom: 10px !important;
    }
}

"""


# =========================================================
# APPEND CSS
# =========================================================

css_text = CSS.read_text(encoding="utf-8")

marker = "RIPPLETRACE V4"

if marker not in css_text:

    with CSS.open("a", encoding="utf-8") as f:
        f.write("\n\n" + dark_css + "\n")

    print("[OK] V4 dark command-center CSS added")

else:

    print("[SKIP] V4 CSS already installed")


# =========================================================
# V4 JAVASCRIPT
# =========================================================

js_code = r"""
/*
 * RippleTrace UI Polish V4
 *
 * VISUAL ONLY.
 *
 * This script does NOT:
 * - call APIs
 * - change agent execution
 * - change CAP
 * - change database
 * - change approval logic
 *
 * It only removes visible AGENT OUTPUT containers
 * after the dashboard renders them.
 */

(function () {

    "use strict";

    console.log("RippleTrace UI Polish V4 loaded");


    /* =====================================================
       Hide the actual AGENT OUTPUT box
       ===================================================== */

    function hideAgentOutputBoxes() {

        /*
         * First handle known CSS classes.
         */

        const knownSelectors = [
            ".agent-output",
            ".output-box",
            "[class*='agent-output']",
            "[class*='output-box']",
            "[class*='agent_output']",
            "[class*='output_box']"
        ];

        knownSelectors.forEach(function (selector) {

            document
                .querySelectorAll(selector)
                .forEach(function (element) {

                    element.style.setProperty(
                        "display",
                        "none",
                        "important"
                    );

                });

        });


        /*
         * Now handle the actual rendered text.
         *
         * This is the important fallback because the
         * existing dashboard may not use the class names
         * above.
         */

        const elements =
            document.querySelectorAll(
                "div,section,article,fieldset"
            );


        elements.forEach(function (element) {

            const directText =
                Array.from(element.childNodes)
                    .filter(function (node) {
                        return node.nodeType === Node.TEXT_NODE;
                    })
                    .map(function (node) {
                        return node.textContent.trim();
                    })
                    .join(" ")
                    .toUpperCase();


            /*
             * Look for an actual AGENT OUTPUT label.
             */

            if (
                directText === "AGENT OUTPUT" ||
                directText === "AGENT OUTPUT:"
            ) {

                /*
                 * Usually the output label and output text
                 * live inside this parent container.
                 */

                let box = element;

                for (let i = 0; i < 3; i++) {

                    if (!box.parentElement) {
                        break;
                    }

                    const parent = box.parentElement;

                    const parentText =
                        (parent.innerText || "")
                            .trim()
                            .toUpperCase();


                    /*
                     * Don't climb into the entire agent card.
                     */

                    if (
                        parentText.length > 1500 ||
                        parent.querySelector("button")
                    ) {
                        break;
                    }

                    box = parent;
                }


                box.style.setProperty(
                    "display",
                    "none",
                    "important"
                );

                box.style.setProperty(
                    "visibility",
                    "hidden",
                    "important"
                );

                box.style.setProperty(
                    "height",
                    "0",
                    "important"
                );

                box.style.setProperty(
                    "min-height",
                    "0",
                    "important"
                );

                box.style.setProperty(
                    "margin",
                    "0",
                    "important"
                );

                box.style.setProperty(
                    "padding",
                    "0",
                    "important"
                );

                box.style.setProperty(
                    "border",
                    "0",
                    "important"
                );

            }

        });

    }


    /* =====================================================
       Improve readability of extremely faint text
       ===================================================== */

    function improveReadability() {

        const agentCards =
            document.querySelectorAll(
                ".agent-card, .agent-panel, .agent-container"
            );


        agentCards.forEach(function (card) {

            card.style.setProperty(
                "color",
                "#dce7f1",
                "important"
            );


            /*
             * Fix elements that inherited the old light theme.
             */

            card.querySelectorAll(
                "p, label, small"
            ).forEach(function (element) {

                element.style.setProperty(
                    "color",
                    "#91a5b6",
                    "important"
                );

                element.style.setProperty(
                    "opacity",
                    "1",
                    "important"
                );

            });


            card.querySelectorAll(
                "h1,h2,h3,h4,h5,strong"
            ).forEach(function (element) {

                element.style.setProperty(
                    "color",
                    "#edf5fb",
                    "important"
                );

                element.style.setProperty(
                    "opacity",
                    "1",
                    "important"
                );

            });

        });

    }


    /* =====================================================
       Run now
       ===================================================== */

    function applyV4() {

        hideAgentOutputBoxes();

        improveReadability();

    }


    applyV4();


    /* =====================================================
       Reapply after existing app renders agent results
       ===================================================== */

    /*
     * IMPORTANT:
     * The original V4 patch used a MutationObserver plus a
     * 1-second setInterval. Because applyV4() changes element
     * styles, those changes can themselves trigger the
     * MutationObserver repeatedly. That can cause the browser
     * main thread to stay busy and make the page appear to
     * refresh/freeze when the report is opened.
     *
     * Keep the observer, but temporarily disconnect it while
     * applying the visual patch. This prevents a feedback loop.
     */

    let observer = null;
    let applyingV4 = false;
    let applyScheduled = false;

    function safeApplyV4() {

        if (applyingV4 || applyScheduled) {
            return;
        }

        applyScheduled = true;

        window.requestAnimationFrame(function () {

            applyScheduled = false;

            if (applyingV4) {
                return;
            }

            applyingV4 = true;

            if (observer) {
                observer.disconnect();
            }

            try {
                applyV4();
            } finally {

                applyingV4 = false;

                if (observer && document.body) {
                    observer.observe(
                        document.body,
                        {
                            childList: true,
                            subtree: true
                        }
                    );
                }
            }

        });

    }


    observer =
        new MutationObserver(function () {

            /*
             * Only react to actual DOM additions/removals.
             * Do not continuously re-run the patch from its
             * own style changes.
             */

            if (!applyingV4) {
                safeApplyV4();
            }

        });


    if (document.body) {

        observer.observe(
            document.body,
            {
                childList: true,
                subtree: true
            }
        );

    }


    /*
     * Initial application.
     */

    safeApplyV4();


})();
"""


JS.write_text(js_code, encoding="utf-8")

print(f"[OK] Created {JS}")


# =========================================================
# ADD SCRIPT TO INDEX
# =========================================================

html = INDEX.read_text(encoding="utf-8")

script_tag = '<script src="ui-polish-v4.js"></script>'


if script_tag not in html:

    if re.search(r"</body>", html, re.IGNORECASE):

        html = re.sub(
            r"</body>",
            f"    {script_tag}\n</body>",
            html,
            count=1,
            flags=re.IGNORECASE
        )

    else:

        html += "\n" + script_tag + "\n"


    INDEX.write_text(
        html,
        encoding="utf-8"
    )

    print("[OK] V4 script added to index.html")

else:

    print("[SKIP] V4 script already included")


# =========================================================
# FINAL
# =========================================================

print()
print("=" * 64)
print("RIPPLETRACE V4 UI PATCH INSTALLED")
print("=" * 64)

print()
print("VISUAL CHANGES:")
print("  ✓ All agent cards dark")
print("  ✓ Inner metric boxes dark")
print("  ✓ Improved text contrast")
print("  ✓ Improved spacing and alignment")
print("  ✓ Hidden visible AGENT OUTPUT boxes")
print("  ✓ Existing report popup preserved")
print("  ✓ Dark report modal preserved")
print("  ✓ Human approval section darkened")

print()
print("UNCHANGED:")
print("  ✓ app.js")
print("  ✓ CAP service")
print("  ✓ Agent logic")
print("  ✓ Database")
print("  ✓ CDS schema")
print("  ✓ API endpoints")
print("  ✓ Approval logic")
print("  ✓ Existing agent sequence")

print()
print("Refresh browser:")
print("  Ctrl + Shift + R")

print()
print("Backups created:")
print(f"  {INDEX}.v4.bak")
print(f"  {CSS}.v4.bak")

print()
print("Done.")
