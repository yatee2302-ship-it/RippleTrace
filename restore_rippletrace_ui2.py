from pathlib import Path
from datetime import datetime
import re
import shutil

# ============================================================
# RippleTrace - VIDEO UI FORMAT + AGENT DIGIT VISIBILITY FIX
# ============================================================
#
# PURPOSE:
#   Make the existing RippleTrace UI visually match the
#   uploaded screencast.
#
# IMPORTANT:
#   - Does NOT modify app.js
#   - Does NOT modify CAP backend
#   - Does NOT modify CDS
#   - Does NOT modify database
#   - Does NOT modify agent execution logic
#   - Does NOT replace the realtime graph
#   - Does NOT replace the existing page
#   - Only adds visual CSS + digit visibility helper
#
# ============================================================


ROOT = Path.home() / "RippleTrace"

APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"

STYLE = APP / "style.css"

FIX_JS = APP / "video-ui-fix.js"


# ------------------------------------------------------------
# Validate project
# ------------------------------------------------------------

if not ROOT.exists():
    raise SystemExit(
        f"\nRippleTrace project not found:\n{ROOT}\n"
    )

if not INDEX.exists():
    raise SystemExit(
        f"\nindex.html not found:\n{INDEX}\n"
    )

if not STYLE.exists():
    raise SystemExit(
        f"\nstyle.css not found:\n{STYLE}\n"
    )


print()
print("=" * 70)
print(" RippleTrace - VIDEO UI FORMAT FIX")
print("=" * 70)
print()


# ------------------------------------------------------------
# Backup
# ------------------------------------------------------------

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

BACKUP = APP / f"backup_video_ui_{timestamp}"

BACKUP.mkdir(
    parents=True,
    exist_ok=True
)

for file in [
    INDEX,
    STYLE,
]:

    if file.exists():

        shutil.copy2(
            file,
            BACKUP / file.name
        )

print("[OK] Backup created:")
print(f"     {BACKUP}")
print()


# ------------------------------------------------------------
# Read existing files
# ------------------------------------------------------------

html = INDEX.read_text(
    encoding="utf-8"
)

css = STYLE.read_text(
    encoding="utf-8"
)


# ------------------------------------------------------------
# Remove previous version of THIS fix only
# ------------------------------------------------------------

css_start_marker = (
    "/* =========================================================="
)

css_end_marker = (
    "/* END RIPPLETRACE VIDEO UI FIX */"
)

start_position = css.find(
    css_start_marker
)

# Only remove the block if it contains our marker.
if (
    start_position != -1
    and
    "RIPPLETRACE VIDEO UI FIX" in
    css[start_position:start_position + 300]
):

    end_position = css.find(
        css_end_marker,
        start_position
    )

    if end_position != -1:

        end_position += len(
            css_end_marker
        )

        css = (
            css[:start_position]
            +
            css[end_position:]
        )

        print(
            "[OK] Previous video UI CSS removed"
        )


# ------------------------------------------------------------
# VIDEO MATCHING CSS
# ------------------------------------------------------------

video_css = r"""

/* ============================================================
   RIPPLETRACE VIDEO UI FIX
   ============================================================ */


/* ------------------------------------------------------------
   ROOT / PAGE
   ------------------------------------------------------------ */

html,
body {

    background:
        #03080d !important;

    color:
        #e7edf5;

}


body {

    min-height:
        100vh;

    margin:
        0;

    font-family:
        Inter,
        "Segoe UI",
        Arial,
        sans-serif;

}


/* ------------------------------------------------------------
   SUBTLE COMMAND CENTER GRID
   ------------------------------------------------------------ */

body {

    background-image:

        linear-gradient(
            rgba(255,255,255,0.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,0.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            #03080d,
            #02070b
        ) !important;

    background-size:
        24px 24px,
        24px 24px,
        100% 100%;

}


/* ------------------------------------------------------------
   TOP SAP-STYLE HEADER
   ------------------------------------------------------------ */

.topbar,
.header,
.navbar,
.app-header {

    background:
        #ffffff !important;

    color:
        #1f2937 !important;

    border-bottom:
        1px solid #d9dee5 !important;

}


/* Keep brand text readable */

.topbar *,
.header *,
.navbar *,
.app-header * {

    color:
        inherit;

}


/* ------------------------------------------------------------
   MAIN CONTENT WIDTH
   ------------------------------------------------------------ */

main,
.main-content,
.page,
.page-content,
.dashboard,
#app {

    max-width:
        1480px;

}


/* ------------------------------------------------------------
   PAGE TITLE AREA
   ------------------------------------------------------------ */

.page-header,
.dashboard-header {

    color:
        #eef4fb !important;

}


/* Main title */

.page-header h1,
.dashboard-header h1,
.page-title {

    color:
        #f1f5f9 !important;

    font-weight:
        700;

}


/* Blue highlighted Command Center text */

.page-header .accent,
.dashboard-header .accent,
.command-center-accent {

    color:
        #087cff !important;

}


/* Subtitle */

.page-header p,
.dashboard-header p,
.page-subtitle {

    color:
        #8995a3 !important;

}


/* ------------------------------------------------------------
   KPI CARDS
   ------------------------------------------------------------ */

.kpi-card,
.metric-card,
.summary-card {

    background:
        #091118 !important;

    border:
        1px solid #1d2a35 !important;

    color:
        #e8eef5 !important;

    border-radius:
        10px;

}


.kpi-card *,
.metric-card *,
.summary-card * {

    color:
        inherit;

}


.kpi-card .value,
.metric-card .value,
.summary-card .value,
.kpi-value {

    color:
        #f2f6fa !important;

    font-size:
        28px;

    font-weight:
        700;

}


.kpi-card .label,
.metric-card .label,
.summary-card .label {

    color:
        #8c98a6 !important;

}


/* ------------------------------------------------------------
   ACTIVE DISRUPTION
   ------------------------------------------------------------ */

.disruption-banner,
.active-disruption,
.disruption-card {

    background:
        #091118 !important;

    border:
        1px solid #26333f !important;

    color:
        #eaf0f6 !important;

}


.disruption-banner *,
.active-disruption *,
.disruption-card * {

    color:
        inherit;

}


.disruption-banner .severity,
.active-disruption .severity {

    color:
        #ff3131 !important;

}


/* ------------------------------------------------------------
   RISK / MITIGATION PANELS
   ------------------------------------------------------------ */

.risk-card,
.risk-overview,
.mitigation-card,
.mitigation-readiness {

    background:
        #091118 !important;

    border:
        1px solid #24313d !important;

    color:
        #e8eef5 !important;

}


.risk-card *,
.risk-overview *,
.mitigation-card *,
.mitigation-readiness * {

    color:
        inherit;

}


/* ------------------------------------------------------------
   MULTI-TIER DEPENDENCY NETWORK
   ------------------------------------------------------------ */

.network-card,
.network-panel,
.dependency-network,
.graph-panel {

    background:
        #071018 !important;

    border:
        1px solid #263440 !important;

    color:
        #e8eef5 !important;

}


.network-card *,
.network-panel *,
.dependency-network *,
.graph-panel * {

    color:
        inherit;

}


/* Network node cards */

.network-node,
.node-card,
.graph-node {

    background:
        #f8fafc !important;

    color:
        #17202a !important;

    border:
        1px solid #d9e0e7 !important;

}


.network-node *,
.node-card *,
.graph-node * {

    color:
        #17202a !important;

}


/* ------------------------------------------------------------
   AGENT COMMAND CENTER
   ------------------------------------------------------------ */

.agent-command-center,
.agent-section,
.agents-section,
.command-center {

    color:
        #e8eef5 !important;

}


/* Agent heading */

.agent-command-center h2,
.agent-section h2,
.agents-section h2,
.command-center h2 {

    color:
        #edf3f8 !important;

}


/* Agent subtitle */

.agent-command-center p,
.agent-section p,
.agents-section p,
.command-center p {

    color:
        #8e99a6;

}


/* ------------------------------------------------------------
   AGENT CARDS - EXACT VIDEO LOOK
   ------------------------------------------------------------ */

.agent-card,
.agent-panel,
.agent-box {

    background:
        #ffffff !important;

    color:
        #26313b !important;

    border:
        1px solid #dce1e6 !important;

    border-radius:
        7px !important;

    box-shadow:
        0 2px 8px rgba(0,0,0,0.12) !important;

    overflow:
        hidden;

}


/* Everything inside agent cards */

.agent-card *,
.agent-panel *,
.agent-box * {

    color:
        #26313b;

}


/* ------------------------------------------------------------
   AGENT COLORED LEFT BORDERS
   ------------------------------------------------------------ */

.agent-card:nth-of-type(1),
.agent-panel:nth-of-type(1),
.agent-box:nth-of-type(1) {

    border-left:
        4px solid #087cff !important;

}


.agent-card:nth-of-type(2),
.agent-panel:nth-of-type(2),
.agent-box:nth-of-type(2) {

    border-left:
        4px solid #7957ff !important;

}


.agent-card:nth-of-type(3),
.agent-panel:nth-of-type(3),
.agent-box:nth-of-type(3) {

    border-left:
        4px solid #19a974 !important;

}


.agent-card:nth-of-type(4),
.agent-panel:nth-of-type(4),
.agent-box:nth-of-type(4) {

    border-left:
        4px solid #ff8a00 !important;

}


/* ------------------------------------------------------------
   AGENT NUMBER BOXES
   ------------------------------------------------------------ */

/*
   THIS IS THE IMPORTANT FIX.

   In the video:
       01
       02
       03
       04

   are present but nearly invisible.

   Force them to be dark and visible.
*/


.agent-card .step-number,
.agent-card .agent-number,
.agent-card .agent-index,
.agent-card .step-index,
.agent-card .number,
.agent-card .index,

.agent-panel .step-number,
.agent-panel .agent-number,
.agent-panel .agent-index,
.agent-panel .step-index,
.agent-panel .number,
.agent-panel .index,

.agent-box .step-number,
.agent-box .agent-number,
.agent-box .agent-index,
.agent-box .step-index,
.agent-box .number,
.agent-box .index {

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    min-width:
        34px !important;

    width:
        34px !important;

    height:
        34px !important;

    background:
        #eef2f6 !important;

    color:
        #475569 !important;

    opacity:
        1 !important;

    visibility:
        visible !important;

    font-size:
        12px !important;

    font-weight:
        700 !important;

    line-height:
        1 !important;

    border-radius:
        4px !important;

}


/* ------------------------------------------------------------
   FORCE 01 / 02 / 03 / 04 TO BE VISIBLE
   ------------------------------------------------------------ */

.agent-card .rt-visible-agent-digit,
.agent-panel .rt-visible-agent-digit,
.agent-box .rt-visible-agent-digit {

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    background:
        #eef2f6 !important;

    color:
        #334155 !important;

    opacity:
        1 !important;

    visibility:
        visible !important;

    font-weight:
        700 !important;

}


/* ------------------------------------------------------------
   AGENT TITLES
   ------------------------------------------------------------ */

.agent-card h3,
.agent-card h4,
.agent-panel h3,
.agent-panel h4,
.agent-box h3,
.agent-box h4 {

    color:
        #26313b !important;

    opacity:
        1 !important;

    font-weight:
        700 !important;

}


/* Specific agent title visibility */

.agent-card .agent-title,
.agent-card .title,
.agent-panel .agent-title,
.agent-panel .title {

    color:
        #27313a !important;

    opacity:
        1 !important;

}


/* ------------------------------------------------------------
   AGENT SUBTITLES
   ------------------------------------------------------------ */

.agent-card .subtitle,
.agent-card .agent-subtitle,
.agent-panel .subtitle,
.agent-panel .agent-subtitle {

    color:
        #7a8692 !important;

    opacity:
        1 !important;

}


/* ------------------------------------------------------------
   AGENT STATUS BADGES
   ------------------------------------------------------------ */

.agent-card .status,
.agent-card .status-badge,
.agent-panel .status,
.agent-panel .status-badge {

    opacity:
        1 !important;

    visibility:
        visible !important;

    color:
        #475569 !important;

}


/* ------------------------------------------------------------
   AGENT METRIC BOXES
   ------------------------------------------------------------ */

.agent-card .metric,
.agent-card .metric-box,
.agent-card .agent-metric,
.agent-card .stat,

.agent-panel .metric,
.agent-panel .metric-box,
.agent-panel .agent-metric,
.agent-panel .stat,

.agent-box .metric,
.agent-box .metric-box,
.agent-box .agent-metric,
.agent-box .stat {

    background:
        #f6f8fa !important;

    border:
        1px solid #dce2e7 !important;

    color:
        #27313b !important;

    opacity:
        1 !important;

}


/* Metric labels */

.agent-card .metric-label,
.agent-card .label,
.agent-panel .metric-label,
.agent-panel .label {

    color:
        #7a8793 !important;

    opacity:
        1 !important;

    font-size:
        10px !important;

    letter-spacing:
        .08em;

    text-transform:
        uppercase;

}


/* Metric values */

.agent-card .metric-value,
.agent-card .value,
.agent-card .stat-value,

.agent-panel .metric-value,
.agent-panel .value,
.agent-panel .stat-value,

.agent-box .metric-value,
.agent-box .value,
.agent-box .stat-value {

    color:
        #26313b !important;

    opacity:
        1 !important;

    visibility:
        visible !important;

    font-size:
        18px !important;

    font-weight:
        700 !important;

}


/* ------------------------------------------------------------
   AGENT OUTPUT
   ------------------------------------------------------------ */

.agent-card .agent-output,
.agent-card .output,
.agent-panel .agent-output,
.agent-panel .output,
.agent-box .agent-output,
.agent-box .output {

    background:
        #f7f9fa !important;

    border:
        1px solid #dce2e7 !important;

    color:
        #35414c !important;

    opacity:
        1 !important;

}


/* Output labels */

.agent-card .output-label,
.agent-panel .output-label {

    color:
        #84909b !important;

    opacity:
        1 !important;

}


/* Output text */

.agent-card .output-text,
.agent-card .output-content,
.agent-panel .output-text,
.agent-panel .output-content {

    color:
        #34404b !important;

    opacity:
        1 !important;

}


/* ------------------------------------------------------------
   ACTION BUTTONS
   ------------------------------------------------------------ */

.agent-card button,
.agent-panel button,
.agent-box button {

    opacity:
        1;

}


/* Primary agent button */

.agent-card .primary,
.agent-card .primary-button,
.agent-panel .primary,
.agent-panel .primary-button {

    background:
        #087cff !important;

    color:
        #ffffff !important;

    border:
        1px solid #087cff !important;

}


/* Secondary / report */

.agent-card .secondary,
.agent-card .report-button,
.agent-panel .secondary,
.agent-panel .report-button {

    background:
        #edf6ff !important;

    color:
        #0871d8 !important;

    border:
        1px solid #b8d8f4 !important;

}


/* ------------------------------------------------------------
   AGENT PROGRESS INDICATOR 01 02 03 04
   ------------------------------------------------------------ */

.agent-progress,
.agent-steps,
.progress-steps {

    color:
        #e7edf4 !important;

}


.agent-progress .step,
.agent-steps .step,
.progress-steps .step {

    opacity:
        1 !important;

    visibility:
        visible !important;

}


/* ------------------------------------------------------------
   REPORT MODAL - MATCH VIDEO
   ------------------------------------------------------------ */

.rt-report-overlay,
.report-overlay {

    background:
        rgba(0, 0, 0, 0.72) !important;

    backdrop-filter:
        blur(8px);

}


.rt-report-panel,
.report-modal,
.report-panel {

    background:
        #071018 !important;

    color:
        #e5edf5 !important;

    border:
        1px solid #30404d !important;

    border-radius:
        8px !important;

    box-shadow:
        0 25px 80px rgba(0,0,0,.65) !important;

}


.rt-report-panel *,
.report-modal *,
.report-panel * {

    color:
        inherit;

}


/* Report table */

.rt-report-table,
.report-table {

    background:
        #09141d !important;

    color:
        #e6edf5 !important;

    border:
        1px solid #263844 !important;

}


.rt-report-table th,
.rt-report-table td,
.report-table th,
.report-table td {

    border-color:
        #293945 !important;

    color:
        #dbe5ed !important;

}


/* ------------------------------------------------------------
   GENERAL VISIBILITY FIX
   ------------------------------------------------------------ */

.agent-card [style*="opacity"],
.agent-panel [style*="opacity"],
.agent-box [style*="opacity"] {

    /*
       Don't allow the old white-on-white effect.
    */

    opacity:
        1 !important;

}


/* ------------------------------------------------------------
   END RIPPLETRACE VIDEO UI FIX
   ------------------------------------------------------------ */

"""


# ------------------------------------------------------------
# Append CSS
# ------------------------------------------------------------

css = css.rstrip()

css += "\n\n" + video_css.strip() + "\n"

STYLE.write_text(
    css,
    encoding="utf-8"
)

print(
    "[OK] Video-matching CSS added"
)


# ------------------------------------------------------------
# JavaScript helper
# ------------------------------------------------------------
#
# This searches the EXISTING agent cards and makes elements
# containing exactly 01, 02, 03 or 04 visible.
#
# It does NOT create agents.
# It does NOT execute agents.
# It does NOT change backend calls.
# ------------------------------------------------------------

fix_js = r"""
/*
 * ============================================================
 * RippleTrace - Video UI Digit Visibility Helper
 * ============================================================
 *
 * Visual-only.
 *
 * It does NOT:
 *   - execute agents
 *   - call APIs
 *   - modify app.js
 *   - modify backend
 *   - modify realtime graph logic
 *
 * It only ensures 01 / 02 / 03 / 04 are visible.
 * ============================================================
 */

(function () {

    "use strict";

    console.log(
        "RippleTrace video UI visibility fix loaded"
    );


    function fixAgentDigits() {

        const possibleCards =
            document.querySelectorAll(
                ".agent-card, " +
                ".agent-panel, " +
                ".agent-box, " +
                "[class*='agent-card'], " +
                "[class*='agent-panel']"
            );


        possibleCards.forEach(
            function (card) {

                const elements =
                    card.querySelectorAll("*");


                elements.forEach(
                    function (element) {

                        const text =
                            (
                                element.textContent ||
                                ""
                            ).trim();


                        /*
                         * Only target elements whose
                         * complete visible text is:
                         *
                         * 01
                         * 02
                         * 03
                         * 04
                         */

                        if (
                            text === "01" ||
                            text === "02" ||
                            text === "03" ||
                            text === "04"
                        ) {

                            /*
                             * Don't touch buttons,
                             * paragraphs or large containers.
                             */

                            const tag =
                                element.tagName
                                    .toLowerCase();


                            if (
                                tag === "button" ||
                                tag === "p" ||
                                tag === "h1" ||
                                tag === "h2" ||
                                tag === "h3" ||
                                tag === "h4"
                            ) {
                                return;
                            }


                            element.classList.add(
                                "rt-visible-agent-digit"
                            );

                        }

                    }
                );

            }
        );

    }


    /*
     * Run once immediately.
     */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            fixAgentDigits
        );

    } else {

        fixAgentDigits();

    }


    /*
     * Agent cards can change after API
     * responses, so observe DOM additions.
     */

    const observer =
        new MutationObserver(
            function () {

                fixAgentDigits();

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


FIX_JS.write_text(
    fix_js.strip() + "\n",
    encoding="utf-8"
)

print(
    "[OK] video-ui-fix.js created"
)


# ------------------------------------------------------------
# Remove duplicate reference to our helper
# ------------------------------------------------------------

html = re.sub(
    r'<script[^>]+src=["\'][^"\']*video-ui-fix\.js["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


# ------------------------------------------------------------
# Add helper exactly once
# ------------------------------------------------------------

script_tag = (
    '<script src="video-ui-fix.js"></script>'
)


if re.search(
    r"</body>",
    html,
    flags=re.IGNORECASE
):

    html = re.sub(
        r"</body>",
        "    " +
        script_tag +
        "\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html += "\n" + script_tag + "\n"


# ------------------------------------------------------------
# IMPORTANT:
# Write the current cleaned HTML.
# This is the corrected final_html section.
# ------------------------------------------------------------

final_html = html

INDEX.write_text(
    final_html,
    encoding="utf-8"
)


# ------------------------------------------------------------
# Validation
# ------------------------------------------------------------

final_html_check = INDEX.read_text(
    encoding="utf-8"
)

script_count = len(
    re.findall(
        r"video-ui-fix\.js",
        final_html_check,
        flags=re.IGNORECASE
    )
)


css_marker_count = final_html_check.count(
    "video-ui-fix.js"
)


print()
print("=" * 70)
print(" VALIDATION")
print("=" * 70)

print(
    f"index.html exists          : {INDEX.exists()}"
)

print(
    f"style.css exists           : {STYLE.exists()}"
)

print(
    f"video-ui-fix.js exists     : {FIX_JS.exists()}"
)

print(
    f"video-ui-fix.js references : {script_count}"
)


if script_count == 1:

    print(
        "[OK] Visual helper loaded exactly once"
    )

else:

    print(
        "[WARNING] Check video-ui-fix.js reference"
    )


print()
print("=" * 70)
print(" COMPLETE")
print("=" * 70)

print()
print("UNCHANGED:")
print("  - app.js")
print("  - CAP backend")
print("  - CDS")
print("  - database")
print("  - agent execution")
print("  - realtime graph logic")
print()
print("CHANGED:")
print("  - visual formatting only")
print("  - agent digit visibility")
print("  - video-style white agent cards")
print("  - dark command-center background")
print("  - metric visibility")
print("  - report modal visual styling")
print()
print(f"Backup: {BACKUP}")
print()
print("Now restart CAP and hard refresh:")
print()
print("  cd ~/RippleTrace")
print("  npm start")
print()
print("Then Firefox:")
print("  Ctrl + Shift + R")
print()
