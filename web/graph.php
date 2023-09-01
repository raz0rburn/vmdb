
<?php 
include("header.php"); 
echo "<a href=\"index.php\">Главная</a>";
echo "<div id=\"container2\" style=\"height: 500px; min-width: 310px\"></div>";
echo "<div id=\"container3\" style=\"height: 350px; min-width: 310px\"></div>";
?>
<script>

        Highcharts.setOptions({
                                lang: {
                                        loading: 'Загрузка...',
                                        months: ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'],
                                        weekdays: ['Воскресенье', 'Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота'],
                                        shortMonths: ['Янв', 'Фев', 'Март', 'Апр', 'Май', 'Июнь', 'Июль', 'Авг', 'Сент', 'Окт', 'Нояб', 'Дек'],
                                        exportButtonTitle: "Экспорт",
                                        printButtonTitle: "Печать",
                                        rangeSelectorFrom: "С",
                                        rangeSelectorTo: "По",
                                        rangeSelectorZoom: "Период",
                                        downloadPNG: 'Скачать PNG',
                                        downloadJPEG: 'Скачать JPEG',
                                        downloadPDF: 'Скачать PDF',
                                        downloadSVG: 'Скачать SVG',
                                        printChart: 'Напечатать график'
                                }
                });
</script>

<script type="text/javascript">
function getUrlVars() {
        var vars = {};
        var parts = window.location.href.replace(/[?&]+([^=&]+)=([^&]*)/gi, function(m,key,value) {
        vars[key] = value;
        });
return vars;
}

if (getUrlVars()["vmname"])

        var vmname = getUrlVars()["vmname"];


        var url_json = `jsonp.php?vmname=${vmname}`;
        //alert(tablename);

        $.getJSON(url_json, function (data) {

        // split the data set into voltage and current
        var     provisioned_space = [],
                guest_disk_usage = [],
                usage_storage = [],
                mem = [],
                cpu = [],
                dataLength = data.length,

        i = 0;
        for (i; i < dataLength; i += 1) {
                provisioned_space.push([
                        data[i][0] * 1000, // the date
                        data[i][2], // provisioned_space
                ]);

                guest_disk_usage.push([
                        data[i][0] * 1000, // the date
                        data[i][3] // guest_disk_usage
                ]);

                usage_storage.push([
                        data[i][0] * 1000, // the date
                        data[i][4] // usage_storage
                ]);
                mem.push([
                        data[i][0] * 1000, // the date
                        data[i][5] // mem
                ]);

                cpu.push([
                        data[i][0] * 1000, // the date
                        data[i][6] // cpu
                ]);
        }


        // create the chart
        Highcharts.stockChart('container2', {

                rangeSelector: {
                        selected: 6,
                        buttons: [{
                                type: 'minute',
                                count: 10,
                                text: '10м'
                        }, {
                                type: 'hour',
                                count: 1,
                                text: '1час'
                        }, {
                                type: 'hour',
                                count: 6,
                                text: '6час'
                        }, {
                                type: 'day',
                                count: 1,
                                text: '1дн'
                        }, {
                                type: 'week',
                                count: 1,
                                text: 'неделя'
                        }, {
                                type: 'month',
                                count: 1,
                                text: 'мес'
                        }, {
                                type: 'year',
                                count: 1,
                                text: 'год'
                        }, {
                                type: 'all',
                                text: 'Всё'
                        }]
                },

                title: {
                        text: data[0][1]+' (Disk)'
                },

                yAxis: [{
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                                text: 'provisioned_space'
                        },
                        height: '35%',
                        lineWidth: 1,
                        resize: {
                                enabled: true
                        }
                },{
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                                text: 'guest_disk_usage'
                        },
                        top: '40%',
                        height: '35%',
                        offset: 0,
                        lineWidth: 1
                }, {
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                                text: 'usage_storage'
                        },
                        top: '70%',
                        height: '35%',
                        offset: 0,
                        lineWidth: 1
                }],

                tooltip: {
                        split: true
                },

                series: [{
                        type: 'spline',
                        name: 'provisioned_space (GB)',
                        data: provisioned_space,
                        yAxis: 0 
                }, {
                        type: 'spline',
                        name: 'guest_disk_usage (GB)',
                        data: guest_disk_usage,
                        yAxis: 1
                }, {
                        type: 'spline',
                        name: 'usage_storage (GB)',
                        data: usage_storage,
                        yAxis: 2
                }]
        });



        // create the chart
        Highcharts.stockChart('container3', {

                rangeSelector: {
                        selected: 6,
                        buttons: [{
                                type: 'minute',
                                count: 10,
                                text: '10м'
                        }, {
                                type: 'hour',
                                count: 1,
                                text: '1час'
                        }, {
                                type: 'hour',
                                count: 6,
                                text: '6час'
                        }, {
                                type: 'day',
                                count: 1,
                                text: '1дн'
                        }, {
                                type: 'week',
                                count: 1,
                                text: 'неделя'
                        }, {
                                type: 'month',
                                count: 1,
                                text: 'мес'
                        }, {
                                type: 'year',
                                count: 1,
                                text: 'год'
                        }, {
                                type: 'all',
                                text: 'Всё'
                        }]
                },

                title: {
                        text: data[0][1]+' (ram/cpu)'
                },

                yAxis: [{
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                                text: 'Memory (Gb)'
                        },
                        height: '50%',
                        lineWidth: 1,
                        resize: {
                                enabled: true
                        }
                },{
                        labels: {
                                align: 'right',
                                x: -3
                        },
                        title: {
                                text: 'CPU'
                        },
                        top: '52%',
                        height: '20%',
                        offset: 0,
                        lineWidth: 1
                }],

                tooltip: {
                        split: true
                },

                series: [{
                        type: 'spline',
                        name: 'Memory (Gb)',
                        data: mem,
                        yAxis: 0 
                }, {
                        type: 'spline',
                        name: 'CPU',
                        data: cpu,
                        yAxis: 1
                }]
        });
});


</script>
