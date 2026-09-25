(function () {
    "use strict";

    const palette = {
        cyan: "#4de1d1",
        blue: "#55a9ff",
        amber: "#f7b955",
        red: "#ff6673"
    };

    function setupNetworkCanvas() {
        const network = document.querySelector(".rt-network");
        if (!network || document.getElementById("rtDepthCanvas")) return;

        const canvas = document.createElement("canvas");
        canvas.id = "rtDepthCanvas";
        canvas.setAttribute("aria-hidden", "true");
        network.prepend(canvas);

        const context = canvas.getContext("2d");
        let width = 0;
        let height = 0;
        let depth = 0;
        let pointerX = 0;
        let pointerY = 0;

        function resize() {
            const ratio = Math.min(window.devicePixelRatio || 1, 2);
            width = network.clientWidth;
            height = network.clientHeight;
            canvas.width = width * ratio;
            canvas.height = height * ratio;
            canvas.style.width = width + "px";
            canvas.style.height = height + "px";
            context.setTransform(ratio, 0, 0, ratio, 0, 0);
        }

        function draw() {
            if (!width || !height) return;
            depth += 0.006;
            context.clearRect(0, 0, width, height);

            const centerX = width * 0.5 + pointerX * 12;
            const centerY = height * 0.52 + pointerY * 8;
            const rings = [0.22, 0.38, 0.56, 0.78];

            context.save();
            context.translate(centerX, centerY);
            context.rotate(-0.12 + Math.sin(depth) * 0.02);
            context.strokeStyle = "rgba(77, 225, 209, .12)";
            context.lineWidth = 1;

            rings.forEach(function (scale, index) {
                context.beginPath();
                context.ellipse(0, 0, width * scale, height * scale * 0.28, 0, 0, Math.PI * 2);
                context.stroke();
                context.strokeStyle = index % 2
                    ? "rgba(85, 169, 255, .08)"
                    : "rgba(77, 225, 209, .12)";
            });

            for (let index = 0; index < 34; index += 1) {
                const angle = index * 2.399 + depth;
                const orbit = 0.18 + (index % 7) * 0.09;
                const x = Math.cos(angle) * width * orbit;
                const y = Math.sin(angle) * height * orbit * 0.28;
                const glow = 1.5 + (Math.sin(depth * 4 + index) + 1) * 1.2;
                const color = index % 9 === 0
                    ? palette.red
                    : index % 4 === 0 ? palette.amber : palette.cyan;

                context.beginPath();
                context.fillStyle = color;
                context.globalAlpha = 0.18 + (index % 4) * 0.08;
                context.shadowBlur = 12;
                context.shadowColor = color;
                context.arc(x, y, glow, 0, Math.PI * 2);
                context.fill();
            }

            context.restore();
            context.globalAlpha = 1;
            requestAnimationFrame(draw);
        }

        network.addEventListener("pointermove", function (event) {
            const bounds = network.getBoundingClientRect();
            pointerX = (event.clientX - bounds.left) / bounds.width - 0.5;
            pointerY = (event.clientY - bounds.top) / bounds.height - 0.5;
        });
        network.addEventListener("pointerleave", function () {
            pointerX = 0;
            pointerY = 0;
        });
        window.addEventListener("resize", resize);
        resize();
        draw();
    }

    function setupSurfaceDepth() {
        document.querySelectorAll(".kpi, .panel, .disruption, .agent").forEach(function (surface) {
            surface.addEventListener("pointermove", function (event) {
                const bounds = surface.getBoundingClientRect();
                const x = (event.clientX - bounds.left) / bounds.width - 0.5;
                const y = (event.clientY - bounds.top) / bounds.height - 0.5;
                surface.style.setProperty("--tilt-x", (y * -1.4).toFixed(2) + "deg");
                surface.style.setProperty("--tilt-y", (x * 1.4).toFixed(2) + "deg");
            });
            surface.addEventListener("pointerleave", function () {
                surface.style.setProperty("--tilt-x", "0deg");
                surface.style.setProperty("--tilt-y", "0deg");
            });
        });
    }

    function boot() {
        setupSurfaceDepth();
        setupNetworkCanvas();
        if (!document.getElementById("rtDepthCanvas")) {
            setTimeout(setupNetworkCanvas, 700);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", boot);
    } else {
        boot();
    }
}());
