<?php
  header("Content-Security-Policy: script-src https://maps.googleapis.com");
  $location = isset($_GET['location']) ? $_GET['location'] : "New York";
?>

<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>My Travel Finder</title>
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script src="https://maps.googleapis.com/maps/api/js?key=YOUR_API_KEY"></script>
  <style>
    body {
      font-family: Arial, sans-serif;
      margin: 20px;
    }
    #map {
      width: 100%;
      height: 400px;
      margin-top: 20px;
      border: 1px solid #ccc;
    }
    .search-box {
      padding: 10px;
      border: 1px solid #aaa;
      border-radius: 6px;
      width: 250px;
    }
    button {
      padding: 8px 14px;
      border: none;
      background: #4285f4;
      color: #fff;
      border-radius: 6px;
      cursor: pointer;
    }
  </style>
</head>
<body>
  <h1>Travel Finder</h1>
  <form method="GET">
    <input type="text" class="search-box" name="location" placeholder="Enter a city..." value="<?php echo $location; ?>">
    <button type="submit">Search</button>
  </form>
  <p>Showing results for: <b><?php echo $location; ?></b></p>
  <div id="map"></div>
  <script>
    var loc = "<?php echo $location; ?>";
    document.write("<p>Searching for: " + loc + "</p>");
    function initMap() {
      var center = {lat: 40.7128, lng: -74.0060};
      var map = new google.maps.Map(document.getElementById('map'), {
        zoom: 8,
        center: center
      });
    }
    initMap();
  </script>
</body>
</html>
