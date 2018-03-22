<?php

define('EMAIL_FOR_REPORTS', '');
define('RECAPTCHA_PRIVATE_KEY', '@privatekey@');
define('FINISH_URI', 'http://');
define('FINISH_ACTION', 'message');
define('FINISH_MESSAGE', 'Thanks for filling out my form!');
define('UPLOAD_ALLOWED_FILE_TYPES', 'doc, docx, xls, csv, txt, rtf, html, zip, jpg, jpeg, png, gif');

define('_DIR_', str_replace('\\', '/', dirname(__FILE__)) . '/');
require_once _DIR_ . '/handler.php';

?>

<?php if (frmd_message()): ?>
<link rel="stylesheet" href="<?php echo dirname($form_path); ?>/formoid-metro-cyan.css" type="text/css" />
<span class="alert alert-success"><?php echo FINISH_MESSAGE; ?></span>
<?php else: ?>
<!-- Start Formoid form-->
<link rel="stylesheet" href="<?php echo dirname($form_path); ?>/formoid-metro-cyan.css" type="text/css" />
<script type="text/javascript" src="<?php echo dirname($form_path); ?>/jquery.min.js"></script>
<form class="formoid-metro-cyan" style="background-color:#f5f0ff;font-size:11px;font-family:'Open Sans','Helvetica Neue','Helvetica',Arial,Verdana,sans-serif;color:#666666;max-width:480px;min-width:150px" method="post"><div class="title"><h2>Submit Your Post</h2></div>
	<div class="element-input<?php frmd_add_class("input"); ?>" title="Thitl"><label class="title">Title<span class="required">*</span></label><input class="large" type="text" name="input" required="required"/></div>
	<div class="element-textarea<?php frmd_add_class("textarea"); ?>" title="Post"><label class="title">Post<span class="required">*</span></label><textarea class="large" name="textarea" cols="20" rows="5" required="required"></textarea></div>
	<div class="element-input<?php frmd_add_class("input1"); ?>" title="Seperate with commas ','"><label class="title">Tags</label><input class="large" type="text" name="input1" /></div>
	<div class="element-url<?php frmd_add_class("url"); ?>" title="Enter your website"><label class="title">Website</label><input class="large" type="url" name="url" value="http://" /></div>
<div class="submit"><input type="submit" value="Submit"/></div></form><script type="text/javascript" src="<?php echo dirname($form_path); ?>/formoid-metro-cyan.js"></script>

<!-- Stop Formoid form-->
<?php endif; ?>

<?php frmd_end_form(); ?>