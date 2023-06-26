<?php
include_once("db_connect.php");
$regs = 0;
$records = array();
if(isset($_GET['date']) && isset($_GET['cluster']) && isset($_GET['vmname']) && isset($_GET['folder']) && isset($_GET['vmstate'])&&isset($_GET['ip_primary'])&&isset($_GET['vmwtools'])&&isset($_GET['annotation'])&&isset($_GET['sortby'])&&isset($_GET['order']))
{

	$date = $_GET['date'];
	$cluster = $_GET['cluster'];
	$vmname= $_GET['vmname'];
	$folder = $_GET['folder'];
	$vmstate = $_GET['vmstate'];
	$ip_primary= $_GET['ip_primary'];
	$vmwtools= $_GET['vmwtools'];
	$annotation= $_GET['annotation'];
	$sortby= $_GET['sortby'];
	$order= $_GET['order'];


	$params[] = $date;
	$params[] = $cluster;
	$params[] = $vmname;
	$params[] = $folder;
	$params[] = $vmstate;
	$params[] = $ip_primary;
	$params[] = $annotation;
	$params[] = $vmwtools;
	$params[] = $sortby;
	$params[] = $order;

	$num = 0;
	foreach ($params as $value) {
		
	    if ($value!='') $num++;
	}

	$query = "select datetime,vmname,cluster,host,folder,ip_primary,provisioned_space,guest_disk_usage,usage_storage,path,mem,cpu,ostype,state,annotation FROM vminfo WHERE datetime LIKE '" . $date ."%'"  ;

	if ($num>0)
	{
		$query = $query . " AND ";



		if ($cluster!='0')	$query = $query . "cluster='$cluster' AND ";	
		if ($vmname!='0')	$query = $query . "vmname LIKE '%" . $vmname ."%'" . " AND ";	
		if ($folder!='0')	$query = $query . "folder LIKE '%" . $folder ."%'" . " AND ";	
		if ($vmstate!='0')	$query = $query . "state='$vmstate' AND ";	
		if ($ip_primary!='0')	$query = $query . "ip_primary=INET_ATON('$ip_primary')  AND ";	
		if ($annotation!='0')	$query = $query . "annotation LIKE '%" . $annotation ."%'" . " AND ";	
		if ($vmwtools!='0')	$query = $query . "vmwtools='$vmwtools' AND ";	

		if ($sortby=='0')
			$query  = substr($query,0,-4);
		if ($sortby!='0' && $order == '1')
			$query  = substr($query,0,-4) . " ORDER BY $sortby;";
		if ($sortby!='0' && $order == '0')
			$query  = substr($query,0,-4) . " ORDER BY $sortby DESC;";
	}











$regs=mysqli_query($conn,$query); // 


//**формируем таблицу вывода** 
if (!isset($_GET["export"])){
	echo '<table border=1>';
	echo '<tr align="center">';
	echo '<th>'.'#'.'</th>';
	echo '<th>'.'datetime'.'</th>';
	echo '<th>'.'vmname'.'</th>';
	echo '<th>'.'cluster'.'</th>';
	echo '<th>'.'host'.'</th>';
	echo '<th>'.'folder'.'</th>';
	echo '<th>'.'ip_primary'.'</th>';
	echo '<th>'.'prov_space'.'</th>';
	echo '<th>'.'guest_disk'.'</th>';
	echo '<th>'.'usage'.'</th>';
	
	echo '<th>'.'mem'.'</th>';
	echo '<th>'.'cpu'.'</th>';
	echo '<th>'.'ostype'.'</th>';
	echo '<th>'.'state'.'</th>';
	echo '<th>'.'annotation'.'</th>';
	echo '<th>'.'path'.'</th>';
	echo '</tr>';
}



if ($regs) {
    $num = mysqli_num_rows($regs);      
    $i = 0;
    $sum_prov=0;
    $sum_guest=0;
    $sum_usage=0;
    $sum_mem=0;
    $sum_cpu=0;
    while ($i < $num) {
		
       $vms[$i] = mysqli_fetch_assoc($regs); 
		if ($vms[$i])
		{			
			if (!isset($_GET["export"])){
				$sum_prov+=$vms[$i]['provisioned_space'];
			    $sum_guest+=$vms[$i]['guest_disk_usage'];
			    $sum_usage+=$vms[$i]['usage_storage'];
			    $sum_mem+=$vms[$i]['mem'];
			    $sum_cpu+=$vms[$i]['cpu'];
		    	echo "<tr>";	
		    	echo "<td>".($i+1)."</td>\n";
		    	echo "<td>".$vms[$i]['datetime']."</td>\n";
				echo "<td><a href=\"graph.php?vmname=".$vms[$i]['vmname'].'">'.$vms[$i]['vmname']."</a></td>\n";
				echo "<td>".$vms[$i]['cluster']."</td>\n";
				echo "<td>".$vms[$i]['host']."</td>\n";
				echo "<td>".$vms[$i]['folder']."</td>\n";
				echo "<td>".long2ip($vms[$i]['ip_primary'])."</td>\n";
				echo "<td>".$vms[$i]['provisioned_space']."</td>\n";
				echo "<td>".$vms[$i]['guest_disk_usage']."</td>\n";
				echo "<td>".$vms[$i]['usage_storage']."</td>\n";
				
				echo "<td>".$vms[$i]['mem']."</td>\n";
				echo "<td>".$vms[$i]['cpu']."</td>\n";
				echo "<td>".$vms[$i]['ostype']."</td>\n";
				echo "<td>".$vms[$i]['state']."</td>\n";
				echo "<td>".$vms[$i]['annotation']."</td>\n";
				echo "<td>".$vms[$i]['path']."</td>\n";
				echo "</tr>";	
			}
		$records[] = $vms[$i];
		}
			
       $i++;

	}	
	//print sum in the end of table
    echo "<tr><td></td><td></td><td></td><td></td><td></td><td></td><td></td>";
    echo "<td>".$sum_prov."</td>\n";
    echo "<td>".$sum_guest."</td>\n";
    echo "<td>".$sum_usage."</td>\n";
    echo "<td>".$sum_mem."</td>\n";
    echo "<td>".$sum_cpu."</td>\n";
    echo "<td><td><td></td><td></td>";
    echo "</tr>";	
}


//export to csv
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
?>