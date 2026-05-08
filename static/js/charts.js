/**
 * charts.js — ApexCharts qrafik inisializasiyası
 * LMS Platform | analytics/dashboard.html
 *
 * Gözlənilən data atributları #revenue-chart elementdə:
 *   data-revenue  — JSON array (aylıq gəlir rəqəmləri)
 *   data-bookings — JSON array (aylıq dərs sayları)
 *   data-labels   — JSON array (ay adları)
 */

document.addEventListener('DOMContentLoaded', function () {
    var el = document.querySelector('#revenue-chart');
    if (!el) return;

    var revenueData  = JSON.parse(el.dataset.revenue  || '[0,0,0,0,0,0]');
    var bookingsData = JSON.parse(el.dataset.bookings || '[0,0,0,0,0,0]');
    var labels       = JSON.parse(el.dataset.labels   || '["Yan","Fev","Mar","Apr","May","İyn"]');

    new ApexCharts(el, {
        chart: {
            type: 'area',
            height: 300,
            toolbar: { show: false },
            fontFamily: 'Inter,sans-serif',
            zoom: { enabled: false }
        },
        series: [
            { name: 'Gəlir (AZN)', data: revenueData },
            { name: 'Dərslər',     data: bookingsData }
        ],
        colors: ['#6366f1', '#10b981'],
        stroke: { width: [2.5, 2], curve: 'smooth' },
        fill: {
            type: 'gradient',
            gradient: { shadeIntensity: 1, opacityFrom: 0.15, opacityTo: 0.01, stops: [0, 90, 100] }
        },
        xaxis: {
            categories: labels,
            labels: { style: { fontSize: '11px', colors: '#94a3b8', fontWeight: 500 } },
            axisBorder: { show: false },
            axisTicks: { show: false }
        },
        yaxis: {
            labels: { style: { fontSize: '11px', colors: '#94a3b8' } },
            min: 0,
            forceNiceScale: true
        },
        grid: {
            borderColor: '#f1f5f9',
            strokeDashArray: 4,
            xaxis: { lines: { show: false } },
            padding: { left: 8, right: 8 }
        },
        legend: { show: false },
        dataLabels: { enabled: false },
        tooltip: {
            theme: 'light',
            style: { fontSize: '12px' },
            y: {
                formatter: function (v, o) {
                    return o.seriesIndex === 0 ? v + ' AZN' : v + ' dərs';
                }
            }
        },
        markers: { size: 0, hover: { size: 5 } },
        noData: {
            text: 'Hələ məlumat yoxdur',
            style: { fontSize: '14px', color: '#94a3b8' }
        }
    }).render();
});
