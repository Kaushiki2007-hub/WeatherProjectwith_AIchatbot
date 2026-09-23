document.addEventListener("DOMContentLoaded", () => {

    const canvas = document.getElementById("chart");

    if (!canvas) {
        console.error("Canvas not found");
        return;
    }

    const ctx = canvas.getContext("2d");

    const times = [];
    const temps = [];

    document.querySelectorAll(".forecast-item").forEach(item => {

        const time = item.querySelector(".forecast-time")?.innerText.trim();
        const temp = parseFloat(
            item.querySelector(".forecast-temperatureValue")?.innerText
        );

        if (time && !isNaN(temp)) {
            times.push(time);
            temps.push(temp);
        }

    });

    if (times.length === 0) {
        console.error("No forecast data found.");
        return;
    }

    const gradient = ctx.createLinearGradient(0, 0, 0, 250);
    gradient.addColorStop(0, "rgba(59,130,246,0.5)");
    gradient.addColorStop(1, "rgba(59,130,246,0)");

    new Chart(ctx, {

        type: "line",

        data: {
            labels: times,
            datasets: [{
                label: "Temperature (°C)",
                data: temps,

                fill: true,
                backgroundColor: gradient,

                borderColor: "#38bdf8",
                borderWidth: 4,

                pointRadius: 6,
                pointHoverRadius: 8,
                pointBackgroundColor: "#ffffff",
                pointBorderColor: "#38bdf8",
                pointBorderWidth: 3,

                tension: 0.45
            }]
        },

        options: {

            responsive: true,
            maintainAspectRatio: false,
            layout:{
                padding:{
                    left:10,
                    right:20,
                    top:10,
                    bottom:10
                }
            },

            animation: {
                duration: 1500
            },

            plugins: {
                legend: {
                    display: false
                }
            },

            layout:{
                padding:{
                    left:15,
                    right:15,
                    top:15,
                    bottom:10
                }
            },
            
            scales: {

                x: {
                    display: true,
                    ticks: {
                        color: "#ffffff",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    },
                    grid: {
                        color: "rgba(255,255,255,.08)"
                    }
                },

                y: {
                    display: true,
                    beginAtZero: false,
                    ticks: {
                        color: "#ffffff",
                        font: {
                            size: 14,
                            weight: "bold"
                        }
                    },
                    grid: {
                        color: "rgba(255,255,255,.08)"
                    }
                }

            }

        }

    });

});