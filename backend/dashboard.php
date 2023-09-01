<!DOCTYPE html>
<?php 

include("header.php"); 
?>
<html>
	
<head>
	<title>
		Приборная панель
	</title>
</head>

<body style="text-align:center;">
	
	<h1 style="color:green;">
		Dashboard
	</h1>
	<a href="index.php">Форма поиска ВМ</a>
	<h4>
		Нажмите button1 - 5etaj, button2 - COD для обновления
	</h4>

	<?php
	
		if(isset($_POST['button1'])) {
			
			$command = escapeshellcmd("/usr/bin/python3 /opt/vmware-api/snaplist.py 'Apparatnaya: ' '/opt/vmware-api/config-5etaj.txt' >> /opt/vmware-api/log");
			$output = shell_exec($command);
			//echo $output;
		}
		if(isset($_POST['button2'])) {
			$command = escapeshellcmd("/usr/bin/python3 /opt/vmware-api/snaplist.py 'COD: ' '/opt/vmware-api/config.txt' >> /opt/vmware-api/log");
			$output = shell_exec($command);
			//echo $output;
		}
	?>
	
	<form method="post">
		<input type="submit" name="button1"
				value="Аппаратная"/>
		
		<input type="submit" name="button2"
				value="ЦОД"/>
	</form>
	<div align="left">
		<a>Snaphot list:</a>

	</div>

	<?php
		include_once 'db_connect.php';

		$query="SELECT iteration FROM snapinfo ORDER BY id DESC LIMIT 1";
		$result = $conn->query($query);
		$row = $result->fetch_array(MYSQLI_ASSOC);
		//echo $row['iteration'];

		$query="SELECT * FROM snapinfo WHERE iteration='".$row['iteration']."'";
		$result=$conn->query($query);
		$i = 0;
		echo '<table border=1>';
		echo '<tr align="left">';
		echo '<th>'.'#'.'</th>';
		echo '<th>'.'datetime'.'</th>';
		echo '<th>'.'dc_name'.'</th>';
		echo '<th>'.'vm_name'.'</th>';
		echo '<th>'.'snap_name'.'</th>';
		echo '<th>'.'snap_size'.'</th>';
		echo '<th>'.'snap_count'.'</th>';
		echo '<th>'.'iteration'.'</th>';

		 while ($row[$i]=$result->fetch_array(MYSQLI_ASSOC)) { 
		echo "<tr>";	
		echo "<td>".($i+1)."</td>\n";
		echo "<td>".$row[$i]['datetime']."</td>\n";
		echo "<td>".$row[$i]['dc_name']."</td>\n";
		echo "<td>".$row[$i]['vm_name']."</td>\n";
		echo "<td>".$row[$i]['snap_name']."</td>\n";
		echo "<td>".$row[$i]['snap_size']."</td>\n";
		echo "<td>".$row[$i]['snap_count']."</td>\n";
		echo "<td>".$row[$i]['iteration']."</td>\n";
		echo "</tr>";

		$i++;
		}
			echo "</table>";
		?>
		

	<div align="left">
		<a>Datastore list:</a>
	</div>

		 
		<?php
		include_once 'db_connect.php';
		$query="SELECT * FROM dsinfo  WHERE DATE(datetime) = CURDATE() ORDER BY free_space ";
		$result=$conn->query($query);
		$i = 0;

		echo '<table border=1>';
			
		echo '<tr align="left">';
		echo '<th>'.'#'.'</th>';
		echo '<th>'.'datetime'.'</th>';
		echo '<th>'.'ds_name'.'</th>';
		echo '<th>'.'UUID'.'</th>';
		echo '<th>'.'vmfs_version'.'</th>';
		echo '<th>'.'is_local_vmfs'.'</th>';
		echo '<th>'.'SSD'.'</th>';
		echo '<th>'.'URL'.'</th>';
		echo '<th>'.'capacity'.'</th>';
		echo '<th>'.'uncommitted'.'</th>';
		echo '<th>'.'provisioned'.'</th>';
		echo '<th>'.'free_space'.'</th>';
		echo '<th>'.'hosts_quantity'.'</th>';
		echo '<th>'.'vm_quantity'.'</th>';
		echo '</tr>';
		 while ($row[$i]=$result->fetch_array(MYSQLI_ASSOC)) { 
		echo "<tr>";	
		echo "<td>".($i+1)."</td>\n";
		echo "<td>".$row[$i]['datetime']."</td>\n";
		echo "<td>".$row[$i]['ds_name']."</td>\n";
		echo "<td>".$row[$i]['UUID']."</td>\n";
		echo "<td>".$row[$i]['vmfs_version']."</td>\n";
		echo "<td>".$row[$i]['is_local_vmfs']."</td>\n";
		echo "<td>".$row[$i]['SSD']."</td>\n";
		echo "<td>".$row[$i]['URL']."</td>\n";
		echo "<td>".$row[$i]['capacity']."</td>\n";
		echo "<td>".$row[$i]['uncommitted']."</td>\n";
		echo "<td>".$row[$i]['provisioned']."</td>\n";
		echo "<td>".$row[$i]['free_space']."</td>\n";
		echo "<td>".$row[$i]['hosts_quantity']."</td>\n";
		echo "<td>".$row[$i]['vm_quantity']."</td>\n";
		echo "</tr>";	
		$i++;
		}
		echo "</table>";

		
	?>

</body>

</html>


