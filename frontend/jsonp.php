<?php
if(isset($_GET['vmname']))
{

	include_once("db_connect.php");

	date_default_timezone_set( 'Asia/Yakutsk' );
	//echo date('Y-m-d H:i:s');

	$mysqli = new mysqli($servername, $username, $password, $dbname);

	$query = "SELECT `datetime`, `vmname`, `provisioned_space`,`guest_disk_usage`,`usage_storage`,`mem`,`cpu` FROM `vminfo` WHERE vmname LIKE '".$_GET['vmname']."';";

	//$query = "SELECT `datetime`, `vmname`, `provisioned_space`,`guest_disk_usage` FROM `vminfo` WHERE vmname LIKE 'srv318krl04.rcitsakha.ru';";

	$result = $mysqli->query($query);

	while ($record = $result->fetch_row()){
		$all[] =  array( strtotime($record[0]),(string)$record[1], (float)$record[2], (float)$record[3], (float)$record[4], (float)$record[5], (int)$record[6]);
	}
	echo json_encode($all);

	$mysqli->close();
}
?>
