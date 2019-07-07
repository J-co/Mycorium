
<html>
	<head>
	<title>Mighty Mycorium</title>
	</head>
<body>

<form action="DHT11_MakeMeasurement.php" method="get">
  <input type="submit" value="Run DHT11 Measurement">
</form>

	
<form action="humidifier_on.php" method="get">
  <input type="submit" value="Turn on humidifier">
</form>	

<form action="humidifier_off.php" method="get">
  <input type="submit" value="Turn off humidifier">
</form>

<input type="submit" class="button" name="insert" value="insert" />

<script src="jquery-3.4.1.min.js">
	$(document).ready(function(){
    $('.button').click(function(){
        //var clickBtnValue = $(this).val();
        var ajaxurl = 'humidifier_on.php',
        data =  {};
        $.post(ajaxurl, data, function (response) {
            // Response div goes here.
            alert("action performed successfully");
        });
    });

});
</script>
	
	
<?php
$hostname = 'localhost';
$username = 'monitor';
$password = 'raspberry';

try {
    $dbh = new PDO("mysql:host=$hostname;dbname=mycorium", $username, $password);

    /*** The SQL SELECT statement ***/
    $sth = $dbh->prepare("
       SELECT  `ttime`, `temperature`,`humidity`  FROM  `DHT11`
    ");
    $sth->execute();

    /* Fetch all of the remaining rows in the result set */
    $result = $sth->fetchAll(PDO::FETCH_ASSOC);

    /*** close the database connection ***/
    $dbh = null;
    
}
catch(PDOException $e)
    {
        echo $e->getMessage();
    }

$json_data = json_encode($result); 
?>


</body>

</html>


<html>
  <head>
    <!--Load the AJAX API-->
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script src="https://momentjs.com/downloads/moment.js"></script>
    <script type="text/javascript">

      google.charts.load('current', {'packages':['annotatedtimeline']});
      google.charts.setOnLoadCallback(drawChart);
      

     // Get the data
    <?php echo "db_data=".$json_data.";" ?>

    var DHT11DataArray = [];
    
    db_data.forEach(function(d) {
      
      var momentDate = moment(d.ttime, 'YYYY-MM-DD HH:mm:ss');
      var jsDate = momentDate.toDate();
      DHT11DataArray.push([jsDate,+d.temperature,+d.humidity]);
      
    });


    function drawChart() {

      var data = new google.visualization.DataTable();
      data.addColumn('datetime','Time');
      data.addColumn('number','Temperature');
      data.addColumn('number','Humidity');

      data.addRows(DHT11DataArray);
      
      //var dateFormatter = new google.visualization.DateFormat({pattern: 'yyyy-MM-dd HH:mm:ss'});
      //dateFormatter.format(data, 0);
      var options = {
        chart: {
          title: 'Temperature and Humidity'
        },
        width: 900,
        height: 500,
        series: {
          // Gives each series an axis name that matches the Y-axis below.
          0: {axis: 'Temperature'},
          1: {axis: 'Humidity'}
        },
        axes: {
          // Adds labels to each axis; they don't have to match the axis names.
          y: {
            Temperature: {label: 'Temperature [Celsius]'},
            Humidity: {label: 'Humidity [%]'}
          }
        }

      };

      var chart = new google.visualization.AnnotatedTimeLine(document.getElementById('linechart_material'));

      chart.draw(data, options);
    }
    </script>
  </head>

  <body>
    <!--Div that will hold the pie chart-->
    <div id="linechart_material" style='width: 700px; height: 240px;'></div>
  </body>
</html>
