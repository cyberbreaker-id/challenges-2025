<?php
ini_set('display_errors', 'Off'); error_reporting(0);
if( isset( $_POST[ 'Submit' ]  ) ) {
	$target = trim($_REQUEST[ 'ip' ]);

	$substitutions = array(
		'||' => '',
		'&'  => '',
		';'  => '',
		'| ' => '',
		'$'  => '',
		'('  => '',
		')'  => '',
		'`'  => '',
	);

	$target = str_replace( array_keys( $substitutions ), $substitutions, $target );
    $cmd = shell_exec( 'ping -c 4 ' . $target );

	$html .= "<pre>{$cmd}</pre>";
}
echo highlight_file(__FILE__);
?>