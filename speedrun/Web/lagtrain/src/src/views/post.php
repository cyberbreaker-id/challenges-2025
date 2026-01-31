<!DOCTYPE html>
<html>
<head>
    <title><?= htmlspecialchars($post['title']) ?></title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .post { margin-bottom: 30px; }
        .meta { color: #666; margin-bottom: 20px; }
        .category { background: #007cba; color: white; padding: 4px 12px; border-radius: 3px; font-size: 14px; margin-right: 15px; }
        .tags { color: #666; font-size: 14px; margin-top: 10px; }
        .tag { background: #eee; padding: 4px 8px; border-radius: 3px; margin-right: 8px; }
        .content { line-height: 1.6; margin-top: 20px; }
        .back-link { margin-top: 30px; }
        a { color: #007cba; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <div class="post">
        <h1><?= htmlspecialchars($post['title']) ?></h1>
        <div class="meta">
            <span class="category"><?= htmlspecialchars($post['category']) ?></span>
            <strong>Author:</strong> <?= htmlspecialchars($post['author']) ?> | 
            <strong>Posted:</strong> <?= htmlspecialchars($post['created_at']) ?>
        </div>
        <?php if (!empty($post['tags'])): ?>
        <div class="tags">
            <strong>Tags:</strong> 
            <?php foreach (explode(',', $post['tags']) as $tag): ?>
            <span class="tag"><?= htmlspecialchars(trim($tag)) ?></span>
            <?php endforeach; ?>
        </div>
        <?php endif; ?>
        <div class="content">
            <?= nl2br(htmlspecialchars($post['content'])) ?>
        </div>
        <div class="back-link">
            <a href="index.php">← Back to all posts</a>
        </div>
    </div>
</body>
</html>