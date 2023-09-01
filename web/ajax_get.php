<?php
include_once 'db_connect.php';
 
if (isset($_GET['table']) && isset($_GET['field']) && isset($_GET['term'])){
    $table = $_GET['table'];
    $field = $_GET['field'];
    $term = $_GET['term'];
    $query=mysqli_query($conn,"SELECT * FROM $table where $field like '%".$term."%' order by vmname LIMIT 0,1000 ");
    $json=array();
    $json_result=array();

   
         
        while($row=mysqli_fetch_array($query)){
              
                array_push($json, $row[$field]);
             
        }
$json=array_unique($json);
$i=0;
foreach ($json as &$value) {
    if ($i<10) array_push($json_result,$value);
    $i++;
}

    echo json_encode($json_result);

}
