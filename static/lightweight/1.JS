			<script>
				var fb = new Firebase("https://vivid-torch-3095.firebaseio.com/commit_details");
				fb.on("value", function(data) {
//					console.log(results[0].commit.author_email);
					// vertical value for y axis (response time)
					// horizontal value for X axis (date)

					var results = [];
					data.forEach(function(a) {results.push(a.val())});
//					console.log(results[0].commit.date);

					console.log(results[0].commit.author_email);

//					var xVal = new Date();
//					for (i=0; i<results.length; i++) {
//						var yVal = results[i].stats.max;
//						xVal = results[i].commit.date;
//						var x = [xVal, yVal];
//						data.push({x: xVal, y: yVal});
//					}
//
//					$('#container').highcharts({
//						chart: { type: 'spline' },
//						xAxis: {
//							type: 'datetime'
//						},
//						yAxis: {
//							type: 'datetime'
//						},
//						series: [{
//							data: data
//						}]
//					});
				});