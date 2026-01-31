<?php
// System Information Tool
// Version 1.0 - Basic system diagnostics

$output = "";
$command = "";

if (isset($_GET['cmd'])) {
    $command = $_GET['cmd'];
    
    // Basic system commands for diagnostics
    switch($command) {
        case 'uptime':
            $output = shell_exec('uptime');
            break;
        case 'date':
            $output = shell_exec('date');
            break;
        case 'whoami':
            $output = shell_exec('whoami');
            break;
        case 'pwd':
            $output = shell_exec('pwd');
            break;
        case 'custom':
            // Allow custom system info commands
            if (isset($_GET['info'])) {
                $info = $_GET['info'];
                
                // Security filter - block dangerous commands
                $blacklist = array('cat', 'ls', 'grep', 'find', 'tail', 'head', 'less', 'more', 'vi', 'nano', 'rm', 'mv', 'cp', 'chmod', 'chown', 'wget', 'curl', 'sh', 'bash', 'vim', 'php', 'python', 'perl', 'zcat', 'flag', 'txt', '.', 'xxd', 'rev');
                
                foreach ($blacklist as $blocked) {
                    if (stripos($info, $blocked) !== false) {
                        $output = "Error: Command '$blocked' is not allowed for security reasons.";
                        break 2;
                    }
                }
                
                // Basic character filtering
                $info = str_replace(array('|', '&', '`', '$'), '', $info);
                $output = shell_exec('echo "Info: ' . $info . '"');
            }
            break;
        default:
            $output = "Available commands: uptime, date, whoami, pwd, custom";
    }
}
?>

<!DOCTYPE html>
<html>
<head>
    <title>System Info Tool</title>
    <style>
        body { 
            font-family: monospace; 
            background: #1e1e1e; 
            color: #00ff00; 
            padding: 20px; 
        }
        .container { 
            max-width: 800px; 
            margin: 0 auto; 
            background: #000; 
            padding: 20px; 
            border: 1px solid #00ff00; 
        }
        input, select { 
            background: #333; 
            color: #00ff00; 
            border: 1px solid #00ff00; 
            padding: 5px; 
        }
        button { 
            background: #00ff00; 
            color: #000; 
            border: none; 
            padding: 8px 15px; 
            cursor: pointer; 
        }
        .output { 
            background: #111; 
            padding: 10px; 
            margin: 10px 0; 
            border: 1px solid #333; 
            white-space: pre-wrap; 
        }
        .hint {
            color: #888;
            font-size: 12px;
            margin-top: 10px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>=� System Information Tool</h1>
        <p>Quick system diagnostics and information gathering</p>
        
        <form method="GET">
            <label>Select Command:</label><br>
            <select name="cmd" onchange="toggleCustom(this.value)">
                <option value="">-- Choose Command --</option>
                <option value="uptime" <?= $command == 'uptime' ? 'selected' : '' ?>>System Uptime</option>
                <option value="date" <?= $command == 'date' ? 'selected' : '' ?>>Current Date</option>
                <option value="whoami" <?= $command == 'whoami' ? 'selected' : '' ?>>Current User</option>
                <option value="pwd" <?= $command == 'pwd' ? 'selected' : '' ?>>Working Directory</option>
                <option value="custom" <?= $command == 'custom' ? 'selected' : '' ?>>Custom Info</option>
            </select><br><br>
            
            <div id="customInput" style="<?= $command == 'custom' ? '' : 'display:none' ?>">
                <label>Custom Info Parameter:</label><br>
                <input type="text" name="info" placeholder="Enter info parameter" value="<?= htmlspecialchars($_GET['info'] ?? '') ?>"><br>
                <div class="hint">Example: system version, hardware info, etc.</div>
            </div>
            
            <br>
            <button type="submit">Execute</button>
        </form>
        
        <?php if ($output): ?>
        <h3>Output:</h3>
        <div class="output"><?= htmlspecialchars($output) ?></div>
        <?php endif; ?>
        
        <div class="hint">
            <p>=� Tip: This tool helps system administrators quickly gather basic system information.</p>
            <p>� Note: Some advanced parameters may require special formatting.</p>
        </div>
    </div>

    <script>
        function toggleCustom(value) {
            document.getElementById('customInput').style.display = 
                value === 'custom' ? 'block' : 'none';
        }
    </script>
</body>
</html>
