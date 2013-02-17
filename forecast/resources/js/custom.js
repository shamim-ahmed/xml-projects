$(document).ready(function() {
	$(".tablesorter.forecasttable").tablesorter({
        sortInitialOrder: 'desc',
		headers : {
			1 : {
				sorter : false
			}
		}
	});
	
	$(".tablesorter.eventtable").tablesorter({
        sortInitialOrder: 'desc',
		headers : {
			1 : {
				sorter : false
			},
			2 : {
				sorter : false
			}
		}
	});
});