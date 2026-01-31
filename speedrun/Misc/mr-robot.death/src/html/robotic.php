<?php
$poemsDirectory = __DIR__ . '/poems';

$fileParam = isset($_GET['file']) ? $_GET['file'] : null;

function renderPage($title, $bodyHtml) {
    echo "<!doctype html>\n";
    echo "<html lang=\"en\">\n";
    echo "  <head>\n";
    echo "    <meta charset=\"utf-8\">\n";
    echo "    <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n";
    echo "    <title>" . $title . "</title>\n";
    // Match index.html styles exactly
    echo "    <style>\n";
    echo "      html, body { height: 100%; margin: 0; background: #0a0a0a; }\n";
    echo "      .center { height: 100%; display: flex; align-items: center; justify-content: center; }\n";
    echo "      img { width: 280px; height: auto; filter: drop-shadow(0 0 24px #00e3ff88); }\n";
    echo "    </style>\n";
    echo "  </head>\n";
    echo "  <body>\n";
    echo "    <div class=\"center\">\n";
    echo "      <div style=\"max-width: 760px; padding: 16px; color: #eaeaea;\">\n";
    echo $bodyHtml;
    echo "      </div>\n";
    echo "    </div>\n";
    echo "  </body>\n";
    echo "</html>\n";
}

if ($fileParam === null) {
    $listHtml = "<div style=\"display:flex; gap:16px; align-items:center; margin-bottom:12px;\"><a href=\"/\" style=\"color:#00e3ff; text-decoration:none;\">home</a></div>";
    $listHtml .= "<h1 style=\"margin:0 0 16px; font-size:22px; color:#00e3ff;\">mr robot — poems</h1>";

    if (!is_dir($poemsDirectory)) {
        $listHtml .= "<p style=\"opacity:.8;\">No poems directory found.</p>";
        renderPage('mr robot — poems', $listHtml);
        exit;
    }

    $entries = array_values(array_diff(scandir($poemsDirectory), ['.', '..']));
    if (empty($entries)) {
        $listHtml .= "<p style=\"opacity:.8;\">No poems available.</p>";
    } else {
        $listHtml .= "<p style=\"opacity:.8;\">Click to view a poem:</p><ul>";
        foreach ($entries as $entry) {
            if (is_file($poemsDirectory . '/' . $entry)) {
                $safe = htmlspecialchars($entry, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
                $listHtml .= "<li><a href=\"?file=" . rawurlencode($entry) . "\" style=\"color:#00e3ff; text-decoration:none;\">" . $safe . "</a></li>";
            }
        }
        $listHtml .= "</ul>";
    }

    renderPage('mr robot — poems', $listHtml);
    exit;
}

$foundPath = null;
$path = $poemsDirectory . '/' . $fileParam;
if (is_file($path)) {
    $foundPath = $path;
}

if ($foundPath !== null) {
    $content = @file_get_contents($foundPath);
    $displayName = htmlspecialchars($fileParam, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
    $body = "<div style=\"display:flex; gap:16px; align-items:center; margin-bottom:12px;\"><a href=\"/robotic.php\" style=\"color:#00e3ff; text-decoration:none;\">back</a></div>";
    $body .= "<h1 style=\"margin:0 0 16px; font-size:22px; color:#00e3ff;\">mr robot — " . $displayName . "</h1>";
    $body .= "<pre style=\"white-space:pre-wrap; word-break:break-word; background:#0b0b0b; border:1px solid #1f1f1f; border-radius:8px; padding:16px; overflow:auto; color:#eaeaea;\">" . htmlspecialchars((string)$content, ENT_NOQUOTES | ENT_SUBSTITUTE, 'UTF-8') . "</pre>";
    renderPage('mr robot — view', $body);
    exit;
}

http_response_code(404);
$body = "<div style=\"display:flex; gap:16px; align-items:center; margin-bottom:12px;\"><a href=\"/robotic.php\" style=\"color:#00e3ff; text-decoration:none;\">back</a></div>";
$body .= "<h1 style=\"margin:0 0 16px; font-size:22px; color:#00e3ff;\">mr robot — not found</h1><p style=\"opacity:.8;\">File not found.</p>";
renderPage('mr robot — not found', $body); 