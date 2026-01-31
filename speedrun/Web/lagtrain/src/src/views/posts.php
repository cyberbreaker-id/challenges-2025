<!DOCTYPE html>
<html>
<head>
    <title>My Blog</title>
    <style>
        body { font-family: Arial, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }
        .search-bar { margin-bottom: 30px; padding: 20px; background: #f5f5f5; border-radius: 5px; }
        .search-bar input[type="text"] { padding: 10px; margin-right: 10px; border: 1px solid #ccc; border-radius: 3px; }
        .search-bar select { padding: 10px; margin-right: 10px; border: 1px solid #ccc; border-radius: 3px; }
        .search-bar button { padding: 10px 20px; background: #007cba; color: white; border: none; border-radius: 3px; cursor: pointer; }
        .search-bar button:hover { background: #005a8b; }
        .post-preview { margin-bottom: 30px; border-bottom: 1px solid #eee; padding-bottom: 20px; }
        .post-preview:last-child { border-bottom: none; }
        h2 { margin-bottom: 10px; }
        .meta { color: #666; margin-bottom: 10px; font-size: 14px; }
        .category { background: #007cba; color: white; padding: 2px 8px; border-radius: 3px; font-size: 12px; margin-right: 10px; }
        .tags { color: #666; font-size: 12px; }
        .tag { background: #eee; padding: 2px 6px; border-radius: 3px; margin-right: 5px; }
        .excerpt { color: #444; margin-top: 10px; }
        a { color: #007cba; text-decoration: none; }
        a:hover { text-decoration: underline; }
    </style>
</head>
<body>
    <h1>My Blog</h1>
    
    <div class="search-bar">
        <form method="GET" action="">
            <input type="text" name="search" placeholder="Search posts..." value="<?= htmlspecialchars($search) ?>">
            <select name="category">
                <option value="">All Categories</option>
                <?php foreach ($categories as $cat): ?>
                <option value="<?= htmlspecialchars($cat) ?>" <?= $category === $cat ? 'selected' : '' ?>>
                    <?= htmlspecialchars($cat) ?>
                </option>
                <?php endforeach; ?>
            </select>
            <button type="submit">Search</button>
            <a href="index.php" style="margin-left: 10px;">Clear</a>
        </form>
    </div>
    
    <?php if (empty($posts)): ?>
        <p>No posts found.</p>
    <?php else: ?>
        <?php foreach ($posts as $post): ?>
        <div class="post-preview">
            <h2><a href="?id=<?= ($post['id']) ?>"><?= htmlspecialchars($post['title']) ?></a></h2>
            <div class="meta">
                <span class="category"><?= htmlspecialchars($post['category']) ?></span>
                By <?= htmlspecialchars($post['author']) ?> on <?= htmlspecialchars($post['created_at']) ?>
            </div>
            <?php if (!empty($post['tags'])): ?>
            <div class="tags">
                Tags: 
                <?php foreach (explode(',', $post['tags']) as $tag): ?>
                <span class="tag"><?= htmlspecialchars(trim($tag)) ?></span>
                <?php endforeach; ?>
            </div>
            <?php endif; ?>
            <div class="excerpt">
                <?= htmlspecialchars(substr($post['content'], 0, 200)) ?>...
            </div>
        </div>
        <?php endforeach; ?>
    <?php endif; ?>
</body>
</html>