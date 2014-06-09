function getKeys(object) {
	var keys = [];
	for (var key in object) {
		if (object.hasOwnProperty(key)) {
			keys.push(key);
		}
	}
	return keys;
}

function createChartJson(time, series) {
	var chartSeries = getKeys(series).map(function(key) {
		return {"name": key, "data": series[key]}
	})
	var chartJson = {
		"chart": {
			"type":"line",
		},
		"title": {
			"text": 'Power Consumption'
		},
		"xAxis": {
			"categories": time,
			"title": {"text":"Time"}
		},
		"yAxis": {
			"title": {"text":"Power (kW)"}
		},
		"series": chartSeries,
		"credits": {"enabled": false}
	}
	return chartJson
}

function createTable(time, series) {
	var seriesKeys = getKeys(series);
	
	var table = document.createElement('table');
	
	//Create header row
	var header = document.createElement('thead');
	var headerRow = document.createElement('tr');
	var headers = ['Time'].concat(seriesKeys);
	for (var i in headers) {
		var headerData = document.createElement('th');
		headerData.appendChild(document.createTextNode(headers[i]));
		headerRow.appendChild(headerData);
	}
	header.appendChild(headerRow)
	
	//Create body
	var body = document.createElement('tbody')
	
	for (var i in time) {
		var row = document.createElement('tr');
		
		var tableData = document.createElement('td');
		tableData.appendChild(document.createTextNode(time[i]));
		row.appendChild(tableData);
		
		for (var j in seriesKeys) {
			key = seriesKeys[j];
			var tableData = document.createElement('td');
			tableData.appendChild(document.createTextNode(series[key][i]));
			row.appendChild(tableData);
		}
		
		body.appendChild(row);
	}
	
	table.appendChild(header);
	table.appendChild(body);
	return table;
}
