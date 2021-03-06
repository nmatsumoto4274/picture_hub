//ヒートマップ
       var datas = {
            "1530370800" : 1, // 2018/07/01
            "1530457200" : 3, // 2018/07/02
            "1533049200" : 5, // 2018/08/01
            "1533135600" : 7, // 2018/08/02
            "1546268400" : 10 // 2019/01/01
        };
        var cal = new CalHeatMap();
        var now = new Date();
        cal.init({
            itemSelector: '#sample-heatmap',
            domain: "week",
            data: datas,
            domainLabelFormat: '',
            start: new Date(now.getFullYear(), now.getMonth() - 11),
            cellSize: 10,
            range: 48,
            legend: [1, 3, 5, 7, 10],
        });