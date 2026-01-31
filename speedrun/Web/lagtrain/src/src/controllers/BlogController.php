<?php

require_once '../models/Blog.php';

class BlogController {
    private $blogModel;
    
    public function __construct() {
        $this->blogModel = new Blog();
    }
    
    public function showPost($id) {
        $id = ($id);
        $post = $this->blogModel->getPost($id);
        if ($post) {
            $this->renderView('404', []);
        } else {
            $this->renderView('404', []);
        }
    }
    
    public function showAllPosts() {
        $search = $_GET['search'] ?? '';
        $searchTag = $_GET['search_tag'] ?? '';
        $searchCategory = $_GET['search_category'] ?? '';
        $category = $_GET['category'] ?? '';
        
        if ($search || $searchTag || $searchCategory) {
            $posts = $this->blogModel->searchPosts($search, $searchTag, $searchCategory);
        } elseif ($category) {
            $posts = $this->blogModel->getPostsByCategory($category);
        } else {
            $posts = $this->blogModel->getAllPosts();
        }
        
        $categories = $this->blogModel->getAllCategories();
        $this->renderView('posts', ['posts' => $posts, 'categories' => $categories, 'search' => $search, 'searchTag' => $searchTag, 'searchCategory' => $searchCategory, 'category' => $category]);
    }
    
    private function renderView($viewName, $data = []) {
        extract($data);
        include "../views/{$viewName}.php";
    }
}
?>