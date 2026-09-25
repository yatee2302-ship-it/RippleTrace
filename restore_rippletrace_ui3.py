from pathlib import Path
from datetime import datetime
import shutil
import re


# ============================================================
# RIPPLETRACE - FINAL VIDEO UI RESTORE
# ============================================================
#
# VISUAL ONLY
#
# DOES NOT MODIFY:
#   app.js
#   realtime-monitor.js
#   CAP backend
#   CDS
#   database
#   agent execution
#
# DOES:
#   - preserve current dashboard
#   - preserve realtime graph
#   - remove old report CSS layers
#   - remove old polish script references
#   - restore video-style visual hierarchy
#   - make 01 / 02 / 03 / 04 visible
#   - make agent cards white
#   - keep surrounding command center dark
#   - keep reports-final.js
#
# ============================================================


ROOT = Path.home() / "RippleTrace"

APP = ROOT / "app" / "control-tower"

INDEX = APP / "index.html"

STYLE = APP / "css" / "style.css"

REALTIME = APP / "realtime-monitor.js"

REPORTS = APP / "reports-final.js"

VIDEO_CSS = APP / "video-ui-exact.css"

VIDEO_JS = APP / "video-ui-digits.js"


# ============================================================
# CHECK PROJECT
# ============================================================

print()
print("=" * 72)
print(" RippleTrace - FINAL VIDEO UI RESTORE")
print("=" * 72)
print()

if not ROOT.exists():
    raise SystemExit(
        f"RippleTrace project not found:\n{ROOT}"
    )

if not INDEX.exists():
    raise SystemExit(
        f"index.html not found:\n{INDEX}"
    )

if not STYLE.exists():
    raise SystemExit(
        f"style.css not found:\n{STYLE}"
    )


# ============================================================
# BACKUP
# ============================================================

timestamp = datetime.now().strftime(
    "%Y%m%d_%H%M%S"
)

BACKUP = APP / f"backup_video_final_{timestamp}"

BACKUP.mkdir(
    parents=True,
    exist_ok=True
)


for source in [
    INDEX,
    STYLE,
    REALTIME,
    REPORTS,
]:

    if source.exists():

        shutil.copy2(
            source,
            BACKUP / source.name
        )


print("[OK] Backup created:")
print(f"     {BACKUP}")
print()


# ============================================================
# READ HTML
# ============================================================

html = INDEX.read_text(
    encoding="utf-8"
)


# ============================================================
# REMOVE OLD POLISH / REPORT SCRIPT REFERENCES
#
# IMPORTANT:
# Files are NOT deleted.
# They are simply no longer loaded by index.html.
# ============================================================

OLD_SCRIPTS = [
    "ui-polish.js",
    "ui-polish-v2.js",
    "ui-polish-v3.js",
    "ui-polish-v4.js",
    "ui-polish-v5.js",
    "report-v5.js",
]


for script_name in OLD_SCRIPTS:

    pattern = (
        r'<script\b[^>]*'
        r'src\s*=\s*["\'][^"\']*'
        + re.escape(script_name)
        + r'["\'][^>]*>'
        r'\s*</script>'
    )

    html, count = re.subn(
        pattern,
        "",
        html,
        flags=re.IGNORECASE
    )

    if count:

        print(
            f"[REMOVED FROM HTML] {script_name}"
        )


# ============================================================
# REMOVE DUPLICATE VIDEO CSS / JS REFERENCES
# ============================================================

html = re.sub(
    r'<link\b[^>]*href\s*=\s*["\'][^"\']*video-ui-exact\.css["\'][^>]*>',
    "",
    html,
    flags=re.IGNORECASE
)

html = re.sub(
    r'<script\b[^>]*src\s*=\s*["\'][^"\']*video-ui-digits\.js["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


# ============================================================
# ADD FINAL VIDEO CSS
# ============================================================

css_tag = (
    '<link rel="stylesheet" '
    'href="video-ui-exact.css">'
)


if re.search(
    r"</head>",
    html,
    flags=re.IGNORECASE
):

    html = re.sub(
        r"</head>",
        "    " + css_tag + "\n</head>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html = css_tag + "\n" + html


# ============================================================
# ADD DIGIT VISIBILITY SCRIPT
# ============================================================

js_tag = (
    '<script src="video-ui-digits.js"></script>'
)


if re.search(
    r"</body>",
    html,
    flags=re.IGNORECASE
):

    html = re.sub(
        r"</body>",
        "    " + js_tag + "\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html += "\n" + js_tag + "\n"


# ============================================================
# ENSURE REALTIME GRAPH IS LOADED EXACTLY ONCE
# ============================================================

html = re.sub(
    r'<script\b[^>]*src\s*=\s*["\'][^"\']*realtime-monitor\.js["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


realtime_tag = (
    '<script src="realtime-monitor.js"></script>'
)


if re.search(
    r"</body>",
    html,
    flags=re.IGNORECASE
):

    html = re.sub(
        r"</body>",
        "    " + realtime_tag + "\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html += "\n" + realtime_tag + "\n"


# ============================================================
# ENSURE REAL REPORT ENGINE IS LOADED
# ============================================================

html = re.sub(
    r'<script\b[^>]*src\s*=\s*["\'][^"\']*reports-final\.js["\'][^>]*>\s*</script>',
    "",
    html,
    flags=re.IGNORECASE
)


report_tag = (
    '<script src="reports-final.js"></script>'
)


if re.search(
    r"</body>",
    html,
    flags=re.IGNORECASE
):

    html = re.sub(
        r"</body>",
        "    " + report_tag + "\n</body>",
        html,
        count=1,
        flags=re.IGNORECASE
    )

else:

    html += "\n" + report_tag + "\n"


# ============================================================
# WRITE HTML
# ============================================================

final_html = html

INDEX.write_text(
    final_html,
    encoding="utf-8"
)


# ============================================================
# FINAL VIDEO CSS
# ============================================================

VIDEO_CSS_CONTENT = r"""
/* ============================================================
   RIPPLETRACE VIDEO UI - FINAL VISUAL LAYER
   ============================================================ */


/* ============================================================
   PAGE
   ============================================================ */

html,
body {

    background:
        #050a0f !important;

    color:
        #e8eef4 !important;

}


body {

    min-height:
        100vh;

    background-image:

        linear-gradient(
            rgba(255,255,255,.025) 1px,
            transparent 1px
        ),

        linear-gradient(
            90deg,
            rgba(255,255,255,.025) 1px,
            transparent 1px
        ) !important;

    background-size:
        24px 24px,
        24px 24px;

}


/* ============================================================
   MAIN PAGE
   ============================================================ */

main,
#app,
.dashboard,
.main-content,
.page-content {

    background:
        transparent !important;

}


/* ============================================================
   HEADINGS
   ============================================================ */

h1,
h2,
h3 {

    letter-spacing:
        -.01em;

}


/* ============================================================
   KPI AREA
   ============================================================ */

.kpi-card,
.metric-card,
.summary-card {

    background:
        #0b1219 !important;

    border:
        1px solid #202d38 !important;

    color:
        #e8eef4 !important;

    border-radius:
        9px !important;

}


.kpi-card *,
.metric-card *,
.summary-card * {

    opacity:
        1 !important;

}


.kpi-card .value,
.metric-card .value,
.summary-card .value,
.kpi-value {

    color:
        #f5f8fb !important;

    font-weight:
        700 !important;

}


/* ============================================================
   DARK INFORMATION PANELS
   ============================================================ */

.risk-card,
.risk-overview,
.mitigation-card,
.mitigation-readiness,
.network-card,
.network-panel,
.graph-panel,
.dependency-network {

    background:
        #091118 !important;

    border:
        1px solid #25323d !important;

    color:
        #e7edf3 !important;

    border-radius:
        9px !important;

}


/* ============================================================
   REALTIME GRAPH
   ============================================================ */

.network-card,
.network-panel,
.graph-panel,
.dependency-network {

    overflow:
        hidden !important;

}


/*
   DO NOT style SVG paths aggressively.
   realtime-monitor.js owns the graph.
*/


/* ============================================================
   AGENT COMMAND CENTER
   ============================================================ */

#agent-command-center,
.agent-command-center,
.agent-section,
.agents-section,
.command-center {

    background:
        transparent !important;

    color:
        #edf2f7 !important;

}


/* ============================================================
   AGENT GRID
   ============================================================ */

.agent-grid,
.agents-grid {

    display:
        grid;

    grid-template-columns:
        repeat(
            4,
            minmax(
                0,
                1fr
            )
        );

    gap:
        16px;

}


@media (max-width: 1200px) {

    .agent-grid,
    .agents-grid {

        grid-template-columns:
            repeat(
                2,
                minmax(
                    0,
                    1fr
                )
            );

    }

}


@media (max-width: 700px) {

    .agent-grid,
    .agents-grid {

        grid-template-columns:
            1fr;

    }

}


/* ============================================================
   AGENT CARDS
   ============================================================ */

.agent-card,
.agent-panel,
.agent-box {

    background:
        #ffffff !important;

    color:
        #25313b !important;

    border:
        1px solid #dce2e7 !important;

    border-radius:
        8px !important;

    box-shadow:
        0 2px 10px
        rgba(
            0,
            0,
            0,
            .16
        ) !important;

    opacity:
        1 !important;

}


/* Everything inside agent cards */

.agent-card *,
.agent-panel *,
.agent-box * {

    opacity:
        1 !important;

}


/* ============================================================
   AGENT CARD LEFT ACCENTS
   ============================================================ */

.agent-card:nth-child(1),
.agent-panel:nth-child(1),
.agent-box:nth-child(1) {

    border-left:
        4px solid #087cff !important;

}


.agent-card:nth-child(2),
.agent-panel:nth-child(2),
.agent-box:nth-child(2) {

    border-left:
        4px solid #7557ff !important;

}


.agent-card:nth-child(3),
.agent-panel:nth-child(3),
.agent-box:nth-child(3) {

    border-left:
        4px solid #19a974 !important;

}


.agent-card:nth-child(4),
.agent-panel:nth-child(4),
.agent-box:nth-child(4) {

    border-left:
        4px solid #f28b20 !important;

}


/* ============================================================
   AGENT HEADERS
   ============================================================ */

.agent-card h1,
.agent-card h2,
.agent-card h3,
.agent-card h4,
.agent-panel h1,
.agent-panel h2,
.agent-panel h3,
.agent-panel h4,
.agent-box h1,
.agent-box h2,
.agent-box h3,
.agent-box h4 {

    color:
        #26313a !important;

    opacity:
        1 !important;

}


/* ============================================================
   AGENT SUBTITLE
   ============================================================ */

.agent-card p,
.agent-card .subtitle,
.agent-card .description,
.agent-card .agent-description,
.agent-panel p,
.agent-panel .subtitle,
.agent-panel .description {

    color:
        #74818c !important;

    opacity:
        1 !important;

}


/* ============================================================
   AGENT NUMBER
   ============================================================ */

.agent-card .step,
.agent-card .number,
.agent-card .agent-number,
.agent-card .step-number,
.agent-card .agent-index,
.agent-card .step-index,

.agent-panel .step,
.agent-panel .number,
.agent-panel .agent-number,
.agent-panel .step-number,
.agent-panel .agent-index,
.agent-panel .step-index,

.agent-box .step,
.agent-box .number,
.agent-box .agent-number,
.agent-box .step-number,
.agent-box .agent-index,
.agent-box .step-index {

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    width:
        34px !important;

    min-width:
        34px !important;

    height:
        34px !important;

    min-height:
        34px !important;

    padding:
        0 !important;

    margin:
        0 !important;

    background:
        #edf1f5 !important;

    color:
        #344454 !important;

    border:
        1px solid #d6dde4 !important;

    border-radius:
        5px !important;

    font-size:
        12px !important;

    font-weight:
        800 !important;

    line-height:
        34px !important;

    text-align:
        center !important;

    opacity:
        1 !important;

    visibility:
        visible !important;

}


/* ============================================================
   FORCE DIGITS CREATED BY JS
   ============================================================ */

.rt-visible-agent-digit {

    display:
        flex !important;

    align-items:
        center !important;

    justify-content:
        center !important;

    width:
        34px !important;

    height:
        34px !important;

    min-width:
        34px !important;

    min-height:
        34px !important;

    background:
        #edf1f5 !important;

    color:
        #263746 !important;

    border:
        1px solid #d3dce4 !important;

    border-radius:
        5px !important;

    font-size:
        12px !important;

    font-weight:
        800 !important;

    opacity:
        1 !important;

    visibility:
        visible !important;

}


/* ============================================================
   AGENT METRICS
   ============================================================ */

.agent-card .metric,
.agent-card .metric-box,
.agent-card .stat,
.agent-card .stat-box,
.agent-card .field,
.agent-card .data-field,
.agent-card .info-box,
.agent-card .value-box,

.agent-panel .metric,
.agent-panel .metric-box,
.agent-panel .stat,
.agent-panel .stat-box {

    background:
        #f7f9fa !important;

    border:
        1px solid #dce3e8 !important;

    color:
        #27333c !important;

    border-radius:
        5px !important;

}


/* ============================================================
   METRIC LABELS
   ============================================================ */

.agent-card .metric-label,
.agent-card .label,
.agent-card .field-label,
.agent-card .stat-label,

.agent-panel .metric-label,
.agent-panel .label,
.agent-panel .field-label,
.agent-panel .stat-label {

    color:
        #7a8792 !important;

    opacity:
        1 !important;

    font-size:
        10px !important;

    font-weight:
        600 !important;

    text-transform:
        uppercase;

}


/* ============================================================
   METRIC VALUES
   ============================================================ */

.agent-card .metric-value,
.agent-card .value,
.agent-card .stat-value,
.agent-card .field-value,

.agent-panel .metric-value,
.agent-panel .value,
.agent-panel .stat-value,
.agent-panel .field-value {

    color:
        #25313a !important;

    font-size:
        18px !important;

    font-weight:
        750 !important;

    opacity:
        1 !important;

    visibility:
        visible !important;

}


/* ============================================================
   OUTPUT
   ============================================================ */

.agent-output,
.output-box,
.agent-card .agent-output,
.agent-card .output-box,
.agent-panel .agent-output,
.agent-panel .output-box {

    background:
        #f7f9fa !important;

    border:
        1px solid #dce3e8 !important;

    color:
        #35414d !important;

    opacity:
        1 !important;

}


/* ============================================================
   STATUS
   ============================================================ */

.agent-card .status,
.agent-card .badge,
.agent-card .agent-status,
.agent-panel .status,
.agent-panel .badge,
.agent-panel .agent-status {

    opacity:
        1 !important;

    visibility:
        visible !important;

}


/* ============================================================
   BUTTONS
   ============================================================ */

.agent-card button,
.agent-panel button,
.agent-box button {

    opacity:
        1 !important;

    visibility:
        visible !important;

}


/* Primary */

.agent-card button.primary,
.agent-card .primary-button,
.agent-panel button.primary,
.agent-panel .primary-button {

    background:
        #087cff !important;

    color:
        #ffffff !important;

    border-color:
        #087cff !important;

}


/* Secondary */

.agent-card button.secondary,
.agent-card .secondary-button,
.agent-panel button.secondary,
.agent-panel .secondary-button {

    background:
        #edf5fc !important;

    color:
        #086dcc !important;

    border:
        1px solid #bfd7ec !important;

}


/* ============================================================
   REPORT BUTTON
   ============================================================ */

.agent-card [data-rippletrace-report],
.agent-panel [data-rippletrace-report] {

    background:
        #edf5fc !important;

    color:
        #086dcc !important;

    border:
        1px solid #bfd7ec !important;

    border-radius:
        5px !important;

}


/* ============================================================
   REPORT MODAL
   ============================================================ */

#rt-report-modal {

    position:
        fixed;

    inset:
        0;

    z-index:
        99999;

}


#rt-report-modal .rt-report-overlay {

    position:
        absolute;

    inset:
        0;

    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    background:
        rgba(
            0,
            0,
            0,
            .74
        ) !important;

    backdrop-filter:
        blur(
            8px
        );

}


#rt-report-modal .rt-report-panel {

    width:
        min(
            900px,
            90vw
        );

    max-height:
        85vh;

    overflow:
        auto;

    background:
        #09131c !important;

    color:
        #e8eef5 !important;

    border:
        1px solid #30404c !important;

    border-radius:
        9px !important;

    padding:
        24px !important;

    box-shadow:
        0 30px 90px
        rgba(
            0,
            0,
            0,
            .7
        ) !important;

}


/* ============================================================
   END
   ============================================================ */
"""


VIDEO_CSS.write_text(
    VIDEO_CSS_CONTENT.strip() + "\n",
    encoding="utf-8"
)


print(
    "[OK] video-ui-exact.css created"
)


# ============================================================
# DIGIT VISIBILITY JAVASCRIPT
# ============================================================

VIDEO_JS_CONTENT = r"""
/*
 * RippleTrace - Agent Digit Visibility
 *
 * Visual only.
 */

(function () {

    "use strict";

    console.log(
        "RippleTrace agent digit visibility active"
    );


    function scanAgentCards() {

        const cards =
            document.querySelectorAll(
                ".agent-card, " +
                ".agent-panel, " +
                ".agent-box, " +
                "[class*='agent-card']"
            );


        cards.forEach(
            function (card) {

                const elements =
                    card.querySelectorAll(
                        "*"
                    );


                elements.forEach(
                    function (element) {

                        const value =
                            (
                                element.textContent ||
                                ""
                            ).trim();


                        if (
                            value === "01" ||
                            value === "02" ||
                            value === "03" ||
                            value === "04"
                        ) {

                            /*
                             * Do not modify actual buttons
                             * or large text containers.
                             */

                            const tag =
                                element.tagName
                                    .toLowerCase();


                            if (
                                tag === "button" ||
                                tag === "h1" ||
                                tag === "h2" ||
                                tag === "h3" ||
                                tag === "h4" ||
                                tag === "p"
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
     * Initial scan
     */

    if (
        document.readyState ===
        "loading"
    ) {

        document.addEventListener(
            "DOMContentLoaded",
            scanAgentCards
        );

    } else {

        scanAgentCards();

    }


    /*
     * Scan again when agent cards are
     * updated dynamically.
     */

    const observer =
        new MutationObserver(
            function () {

                scanAgentCards();

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


VIDEO_JS.write_text(
    VIDEO_JS_CONTENT.strip() + "\n",
    encoding="utf-8"
)


print(
    "[OK] video-ui-digits.js created"
)


# ============================================================
# VALIDATION
# ============================================================

final_html = INDEX.read_text(
    encoding="utf-8"
)


realtime_count = len(
    re.findall(
        r"realtime-monitor\.js",
        final_html,
        flags=re.IGNORECASE
    )
)


reports_count = len(
    re.findall(
        r"reports-final\.js",
        final_html,
        flags=re.IGNORECASE
    )
)


css_count = len(
    re.findall(
        r"video-ui-exact\.css",
        final_html,
        flags=re.IGNORECASE
    )
)


digit_js_count = len(
    re.findall(
        r"video-ui-digits\.js",
        final_html,
        flags=re.IGNORECASE
    )
)


print()
print("=" * 72)
print(" FINAL VALIDATION")
print("=" * 72)

print(
    f"index.html               : {INDEX.exists()}"
)

print(
    f"style.css                : {STYLE.exists()}"
)

print(
    f"realtime-monitor.js      : {REALTIME.exists()}"
)

print(
    f"reports-final.js         : {REPORTS.exists()}"
)

print(
    f"video-ui-exact.css       : {VIDEO_CSS.exists()}"
)

print(
    f"video-ui-digits.js       : {VIDEO_JS.exists()}"
)

print()

print(
    f"Realtime script refs     : {realtime_count}"
)

print(
    f"Report script refs       : {reports_count}"
)

print(
    f"Video CSS refs           : {css_count}"
)

print(
    f"Digit JS refs            : {digit_js_count}"
)


# ============================================================
# SAFETY CHECKS
# ============================================================

if realtime_count != 1:

    print(
        "\n[WARNING] realtime-monitor.js "
        "is not loaded exactly once."
    )

else:

    print(
        "[OK] Real-time graph preserved."
    )


if reports_count != 1:

    print(
        "[WARNING] reports-final.js "
        "is not loaded exactly once."
    )

else:

    print(
        "[OK] Real report engine preserved."
    )


if css_count == 1:

    print(
        "[OK] Video CSS loaded exactly once."
    )


if digit_js_count == 1:

    print(
        "[OK] Digit visibility helper loaded exactly once."
    )


print()
print("=" * 72)
print(" COMPLETE")
print("=" * 72)

print()
print("UNCHANGED:")
print("  app.js")
print("  realtime-monitor.js")
print("  CAP backend")
print("  CDS")
print("  database")
print("  agent execution")
print()
print("PRESERVED:")
print("  real-time dependency graph")
print("  existing agent flow")
print("  existing reports engine")
print()
print("FIXED:")
print("  video-style dark command center")
print("  white agent cards")
print("  agent colored accents")
print("  visible 01 / 02 / 03 / 04")
print("  visible agent metrics")
print("  visible output sections")
print()
print("Backup:")
print(f"  {BACKUP}")
print()
print("Now restart:")
print()
print("  cd ~/RippleTrace")
print("  npm start")
print()
print("Then hard refresh Firefox:")
print()
print("  Ctrl + Shift + R")
print()
