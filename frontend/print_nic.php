<?php
include_once("db_connect.php");
$regs = 0;
$records = array();
if (isset($_GET['date']) && isset($_GET['vmname']) && isset($_GET['mac']) && isset($_GET['connected']) && isset($_GET['netlabel'])&&isset($_GET['ipv4'])&&isset($_GET['sortby_nic'])&&isset($_GET['order_nic']))
{


	$date = $_GET['date'];
	$vmname= $_GET['vmname'];
	$mac = $_GET['mac'];
	$connected = $_GET['connected'];
	$netlabel= $_GET['netlabel'];
	$ipv4= $_GET['ipv4'];
	$sortby_nic= $_GET['sortby_nic'];
	$order_nic= $_GET['order_nic'];

	$params[] = $date;
	$params[] = $vmname;
	$params[] = $mac;
	$params[] = $connected;
	$params[] = $netlabel;
	$params[] = $ipv4;
	$params[] = $sortby_nic;
	$params[] = $order_nic;

	$num = 0;
	foreach ($params as $value) {
		
	    if ($value!='') $num++;
	}

	$query = "select datetime,host,vmname,mac,connected,netlabel,prefix,ipv4 FROM nicinfo WHERE datetime LIKE '" . $date ."%'"  ;
	if ($num>0){
		$query = $query . " AND ";



		if ($connected!='2')	$query = $query . "connected=$connected AND ";	
		if ($vmname!='0')	$query = $query . "vmname LIKE '%" . $vmname ."%'" . " AND ";	
		if ($mac!='0')	$query = $query . "mac LIKE '%" . $mac ."%'" . " AND ";	
		if ($netlabel!='0')	$query = $query . "netlabel LIKE '%" . $netlabel ."%'" . " AND ";	
		if ($ipv4!='0')	$query = $query . "ipv4 LIKE '%" . $ipv4 ."%'" . " AND ";

		if ($sortby_nic=='0')
			$query  = substr($query,0,-4);
		if ($sortby_nic!='0' && $order_nic == '1')
			$query  = substr($query,0,-4) . " ORDER BY $sortby_nic;";
		if ($sortby_nic!='0' && $order_nic == '0')
			$query  = substr($query,0,-4) . " ORDER BY $sortby_nic DESC;";
	}

	$regs=mysqli_query($conn,$query); // 

	//**формируем таблицу вывода** 
	if (!isset($_GET["export"])){
		echo '<table border=1>';
		echo '<tr align="center">';
		echo '<th>'.'#'.'</th>';
		echo '<th>'.'datetime'.'</th>';
		echo '<th>'.'host'.'</th>';
		echo '<th>'.'vmname'.'</th>';
		echo '<th>'.'mac'.'</th>';
		echo '<th>'.'connected'.'</th>';
		echo '<th>'.'netlabel'.'</th>';
		echo '<th>'.'prefix'.'</th>';
		echo '<th>'.'ipv4'.'</th>';
		echo '</tr>';
	}




	if ($regs) {
	    $num = mysqli_num_rows($regs);      
	    $i = 0;
	    while ($i < $num) {
			
	       $vms[$i] = mysqli_fetch_assoc($regs); 
			if ($vms[$i])
			{			
								
				if (!isset($_GET["export"])){
	                        echo "<tr>";
	                        echo "<td>".($i+1)."</td>\n";
	                        echo "<td>".$vms[$i]['datetime']."</td>\n";
	                        echo "<td>".$vms[$i]['host']."</td>\n";
	                        echo "<td>".$vms[$i]['vmname']."</td>\n";
	                        echo "<td>".$vms[$i]['mac']."</td>\n";
	                        echo "<td>".$vms[$i]['connected']."</td>\n";
	                        echo "<td>".$vms[$i]['netlabel']."</td>\n";
	                        echo "<td>".$vms[$i]['prefix']."</td>\n";
	                        echo "<td>".$vms[$i]['ipv4']."</td>\n";
	                        echo "</tr>";
				}
			$records[] = $vms[$i];

			}
				
	       $i++;

		}	

	}
	else {
		echo 'pusto';
	}

	if (isset($_GET["export"]))
	{
		$delimiter = ';';
		$enclosure = '"';
		$csv_file = "kitools_".date('Ymd') . ".csv";			
		header("Content-Type: text/csv");
		header("Content-Disposition: attachment; filename=\"$csv_file\"");	
		$fh = fopen( 'php://output', 'w' );


		
		$is_coloumn = true;
		if(!empty($records)) {
		  foreach($records as $record) {
			if($is_coloumn) {		  	  
			  fputcsv($fh, array_keys($record), $delimiter, $enclosure);
			  $is_coloumn = false;
			}
				
			 fputcsv($fh, array_values($record), $delimiter, $enclosure);	  }
		   fclose($fh);
		}
		exit;  
	}


}

