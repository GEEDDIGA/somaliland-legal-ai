<?php
/**
 * WPCode Snippet Fix Script
 * 
 * This script updates the broken JavaScript code in the WordPress WPCode snippet.
 * Upload this file to your WordPress root directory and access it via browser ONCE, then DELETE IT.
 * 
 * URL: https://www.goolle.shop/fix-wpcode-snippet.php
 */

// SECURITY: Delete this file after running
if ($_SERVER['REQUEST_METHOD'] !== 'GET' || !isset($_GET['run'])) {
    die('Access this file via: https://www.goolle.shop/fix-wpcode-snippet.php?run=fix');
}

if ($_GET['run'] !== 'fix') {
    die('Invalid parameter');
}

// Load WordPress
require_once('wp-load.php');

if (!current_user_can('manage_options')) {
    die('You must be logged in as admin');
}

// The fixed JavaScript code
$fixed_code = "const botAnswer = (data && data.answer) ? data.answer : (data && data.error) ? data.error : 'Cilad ayaa dhacday';";

// Get snippet ID 449
$snippet_id = 449;

// Update the snippet in database
global $wpdb;
$table = $wpdb->prefix . 'wpcode_snippets';

$snippet = $wpdb->get_row($wpdb->prepare("SELECT * FROM $table WHERE id = %d", $snippet_id));

if (!$snippet) {
    die('Snippet not found!');
}

$code = $snippet->code;

// Replace the broken line
$broken_pattern = '/const\s+botAnswer\s*=\s*data\.answer\s*\|\|\s*data\.message\s*\|\|\s*[\'"].*?[\'"];?/';
$code = preg_replace($broken_pattern, $fixed_code, $code);

// Update in database
$result = $wpdb->update(
    $table,
    array('code' => $code),
    array('id' => $snippet_id),
    array('%s'),
    array('%d')
);

if ($result !== false) {
    echo '<h1>✅ SUCCESS!</h1>';
    echo '<p>The snippet has been fixed. The chatbot should now work correctly.</p>';
    echo '<p><strong>IMPORTANT: DELETE THIS FILE NOW!</strong></p>';
    echo '<p>Run: <code>rm /path/to/wordpress/fix-wpcode-snippet.php</code></p>';
    echo '<hr>';
    echo '<h2>What was fixed:</h2>';
    echo '<pre>' . htmlspecialchars($fixed_code) . '</pre>';
    echo '<p><a href="https://www.goolle.shop/">Test the chatbot</a></p>';
} else {
    echo '<h1>❌ ERROR</h1>';
    echo '<p>Failed to update the snippet. Error: ' . $wpdb->last_error . '</p>';
}

// Clear WordPress cache
if (function_exists('wp_cache_flush')) {
    wp_cache_flush();
}
?>
