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
