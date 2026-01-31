<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { 
            font-family: Arial, sans-serif; 
            max-width: 800px; 
            margin: 0 auto; 
            padding: 20px;
            background-color: #f5f5f5;
        }
        .dashboard-container {
            background: white;
            padding: 40px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 2px solid #eee;
        }
        .welcome {
            color: #333;
            margin: 0;
        }
        .logout-btn {
            padding: 10px 20px;
            background: #d32f2f;
            color: white;
            text-decoration: none;
            border-radius: 4px;
            font-weight: bold;
        }
        .logout-btn:hover {
            background: #b71c1c;
        }
        .user-info {
            background: #e3f2fd;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 30px;
        }
        .user-info h2 {
            margin-top: 0;
            color: #1976d2;
        }
        .info-item {
            margin-bottom: 10px;
            display: flex;
            align-items: center;
        }
        .info-label {
            font-weight: bold;
            color: #555;
            width: 120px;
        }
        .info-value {
            color: #333;
        }
        .success-message {
            background: #e8f5e8;
            color: #2e7d32;
            padding: 20px;
            border-radius: 6px;
            text-align: center;
            font-size: 18px;
            font-weight: bold;
        }
        .features {
            margin-top: 30px;
        }
        .feature-box {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 6px;
            margin-bottom: 15px;
        }
        .feature-title {
            font-weight: bold;
            color: #007cba;
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="dashboard-container">
        <div class="header">
            <h1 class="welcome">Welcome to your Dashboard!</h1>
            <a href="index.php?action=logout" class="logout-btn">Logout</a>
        </div>
        
        <?php if ($user): ?>
        <div class="user-info">
            <h2>Your Account Information</h2>
            <div class="info-item">
                <span class="info-label">Username:</span>
                <span class="info-value"><?= htmlspecialchars($user['username']) ?></span>
            </div>
        </div>
        <?php endif; ?>
    </div>
</body>
</html>