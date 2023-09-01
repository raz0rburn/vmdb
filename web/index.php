<?php 
include_once("db_connect.php");

include("header.php"); 
?>
<title>KITOOLS</title>

<script type="text/javascript">
$(function() {
  $('#datep').datepicker({ dateFormat: 'yy-mm-dd' });

});
$(function() {
  $('#nic_datep').datepicker({ dateFormat: 'yy-mm-dd' });

});
</script>   
<script type="text/javascript">


$(document).ready(function(){

	if (document.getElementById('datep').value == '')
	{
		let now = new Date();
		document.getElementById('datep').value =now.toISOString().split('T')[0];
	}	
		if (document.getElementById('nic_datep').value == '')
	{
		let now = new Date();
		document.getElementById('nic_datep').value =now.toISOString().split('T')[0];
	}	

    $("#vmname").autocomplete({
        source:'ajax_get.php?table=vminfo&field=vmname',
		select: function(event, ui) {
		event.preventDefault();
		$(this).val(ui.item.label);
		$("#vmname_hid").val(ui.item.value);
		},
						
		change: function( event, ui ) {
			if  ((this).value=='')
			$( "#vmname_hid" ).val( '0' );
		},			
        minLength:1
    }); 

    $("#folder").autocomplete({
        source:'ajax_get.php?table=vminfo&field=folder&',
		select: function(event, ui) {
			event.preventDefault();
			$(this).val(ui.item.label);
			$("#folder_hid").val(ui.item.value);
		},
					
		change: function( event, ui ) {
			if  ((this).value=='')
			$( "#folder_hid" ).val( '0' );
		},
						
        minLength:1
    });  

    $("#nic_vmname").autocomplete({
        source:'ajax_get.php?table=nicinfo&field=vmname&',
		select: function(event, ui) {
			event.preventDefault();
			$(this).val(ui.item.label);
			$("#nic_vmname_hid").val(ui.item.value);
		},
					
		change: function( event, ui ) {
			if  ((this).value=='')
			$( "#nic_vmname_hid" ).val( '0' );
		},
						
        minLength:1
    }); 

    $("#nic_mac").autocomplete({
        source:'ajax_get.php?table=nicinfo&field=mac&',
		select: function(event, ui) {
			event.preventDefault();
			$(this).val(ui.item.label);
			$("#nic_mac_hid").val(ui.item.value);
		},
					
		change: function( event, ui ) {
			if  ((this).value=='')
			$( "#nic_mac_hid" ).val( '0' );
		},
						
        minLength:1
    }); 

    $("#nic_netlabel").autocomplete({
        source:'ajax_get.php?table=nicinfo&field=netlabel&',
		select: function(event, ui) {
			event.preventDefault();
			$(this).val(ui.item.label);
			$("#nic_netlabel_hid").val(ui.item.value);
		},
					
		change: function( event, ui ) {
			if  ((this).value=='')
			$( "#nic_netlabel_hid" ).val( '0' );
		},
						
        minLength:1
    }); 
        $("#nic_ip").autocomplete({
        source:'ajax_get.php?table=nicinfo&field=ipv4&',
		select: function(event, ui) {
			event.preventDefault();
			$(this).val(ui.item.label);
			$("#nic_ip_hid").val(ui.item.value);
		},
					
		change: function( event, ui ) {
			if  ((this).value=='')
			$( "#nic_ip_hid" ).val( '0' );
		},
						
        minLength:1
    }); 

});			


</script> 	

<script type="text/javascript">
	let url;
function startAjax(){
	
	

	date = document.getElementById('datep').value;
	

	cluster=$('select[name="cluster"]').val();

	host=$('select[name="host"]').val();

	vmname=document.getElementById('vmname').value;
	vmname=$("#vmname").val();
	if(vmname == ''  )
		vmname = "0";
	
	folder=document.getElementById('folder').value;
	folder=$("#folder").val();
	if(folder == ''  )
		folder = "0";
   
	vmstate = $('select[name="vmstate"]').val();
	vmwtools = $('select[name="vmwtools"]').val();

		ip_primary = "0";
	annotation = document.getElementById('annotation').value;
	if(annotation  == ''  )
		annotation = "0";
	sortby = document.getElementById('sortby').value;
	if(sortby  == ''  )
		sortby = "0";
	
	var radioOrder = document.getElementsByName('order');
	if (radioOrder[0].checked) 
		order = 1;
	else order = 0;

	
	url="print.php?date="+date+"&cluster="+cluster+"&host="+host+"&vmstate="+vmstate+"&vmname="+vmname+"&folder="+folder+"&ip_primary="+ip_primary+"&annotation="+annotation+"&vmwtools="+vmwtools+"&sortby="+sortby+"&order="+order;
	
    
	var request; 
	
    if(window.XMLHttpRequest){ 
        request = new XMLHttpRequest(); 
    } else if(window.ActiveXObject){ 
        request = new ActiveXObject("Microsoft.XMLHTTP");  
    } else { 
        return;
    } 
    request.onreadystatechange = function(){
        if (request.readyState==4) {
            if(request.status==200){
                document.getElementById("result").innerHTML = request.responseText;
            }else if(request.status==404){
                alert("Ошибка: запрашиваемый скрипт не найден!");
            }
            else alert("Ошибка: сервер вернул статус: "+ request.status);
        }       
    } 
    request.open ('GET', url, true);
    request.send (''); 
}

		
function startAjaxNic(){
	date = document.getElementById('nic_datep').value;

	connected=$('select[name="nic_connected"]').val();

	vmname = document.getElementById('nic_vmname').value;
	vmname = $("#nic_vmname").val();
	if(vmname == ''  )
		vmname = "0";

	mac = document.getElementById('nic_mac').value;
	mac = $("#nic_mac").val();
	if(mac == ''  )
		mac = "0";

	netlabel = document.getElementById('nic_netlabel').value;
	netlabel = $("#nic_netlabel").val();
	if(netlabel == ''  )
		netlabel = "0";

	ipv4 = document.getElementById('nic_ip').value;
	ipv4 = $("#nic_ip").val();
	if(ipv4 == ''  )
		ipv4 = "0";
	sortby_nic = document.getElementById('sortby_nic').value;
	if(sortby_nic  == ''  )
		sortby_nic = "0";
	var radioOrderNic = document.getElementsByName('order_nic');
	if (radioOrderNic[0].checked) 
		order_nic = 1;
	else order_nic = 0;
	
	url="print_nic.php?date="+date+"&vmstate="+vmstate+"&vmname="+vmname+"&mac="+mac+"&connected="+connected+"&netlabel="+netlabel+"&ipv4="+ipv4+"&sortby_nic="+sortby_nic+"&order_nic="+order_nic;
	    var request; 
	
    if(window.XMLHttpRequest){ 
        request = new XMLHttpRequest(); 
    } else if(window.ActiveXObject){ 
        request = new ActiveXObject("Microsoft.XMLHTTP");  
    } else { 
        return;
    } 
    request.onreadystatechange = function(){
        if (request.readyState==4) {
            if(request.status==200){
                document.getElementById("result").innerHTML = request.responseText;
            }else if(request.status==404){
                alert("Ошибка: запрашиваемый скрипт не найден!");
            }
            else alert("Ошибка: сервер вернул статус: "+ request.status);
        }       
    } 
    request.open ('GET', url, true);
    request.send (''); 

}
function exportCsv(){

	

        urlExport = url + "&export=1";


	$.ajax({
	    type: 'GET',              // Задаем метод передачи
	    url: urlExport,
	    //data      : postData, //Forms name
	    success: function(data){
		window.location = urlExport;
        document.getElementById("result").innerHTML = request.responseText;
    }
});

}	

			
</script>




</head>




<body>
<h3 align="center">Найти ВМ</h3>
<a href="dashboard.php">Приборная панель</a>
<table  align="center" >
<tr>
<td>
<form>
    <div class="select-sort">
    	Дата:<br />
        <label for="datep"> </label><input id="datep"/>
    </div>
</td>
<td>
	Кластер:<br />		
	<div class="select-sort">
		<?php
		include_once 'db_connect.php';


		$query="SELECT cluster FROM vminfo GROUP BY cluster";
		$result=$conn->query($query);
		?>
		<select name="cluster" id="cluster">
		<option value="0">- выберите кластер -</option>
		<?php while ($row=$result->fetch_array(MYSQLI_ASSOC)) { ?>
		<option value=<?php echo $row['cluster']?>><?php echo $row['cluster']?></option>
		<?php } ?>
		</select>
</td>

<td>
	Хост:<br />		
	<div class="select-sort">
		<?php
		include_once 'db_connect.php';


		$query="SELECT host FROM vminfo GROUP BY host";
		$result=$conn->query($query);

		?>
		<select name="host" id="host">
		<option value="0">- выберите хост -</option>
		<?php while ($row=$result->fetch_array(MYSQLI_ASSOC)) { ?>
		<option value=<?php echo $row['host']?>><?php echo $row['host']?></option>
		<?php } ?>
		</select>

</td>
<td>
	</div>
	VM State:<br />
	<div class="select-sort">
			
		<select name="vmstate" id="vmstate">
			<option value="0">- выберите сост. -</option>
			<option value="poweredOn">poweredOn</option>
			<option value="poweredOff">poweredOff</option>
		</select>
</td>
<td>		
    </div>
	VMwareTools:<br />
	<div class="select-sort">
			
		<select name="vmwtools" id="vmwtools">
			<option value="0">- выберите сост. -</option>
			<option value="toolsOld">toolsOld</option>
			<option value="toolsNotRunning">toolsNotRunning</option>
			<option value="toolsNotInstalled">toolsNotInstalled</option>
			<option value="toolsOk">toolsOk</option>
		</select>
	</div>
</td>
<td>		 
    <div class="select-sort">
		<form method="post" action="">
            vmname : <br /> <input type="text" id="vmname" name="vmname"/>
			<input type='hidden' id='vmname_hid' value='' />
      	</form>
    </div>
</td>

<td> 
	 <div class="select-sort">
		<form method="post" action="">
        	Папка :  <br /> <input type="text" id="folder" name="folder" />
        	<input type='hidden' id='folder_hid' value='' />
    	</form>
    </div>
</td>
<td>	
	<div class="select-sort">
		<form method="post" action="">
			Annotation : <br /> <input type="text" id="annotation" name="annotation"/>
			<input type='hidden' id='annotation_hid' value='' />
		</form>
	</div>
</td>
<td>
	<label for="order">Сортировка: </label>
	<input type="radio" name="order" value="0" checked="checked">Возр.</input>
	<input type="radio" name="order" value="1">Убыв.</input>	
	<br/>
	<div class="select-sort">
		<select name="sortby" id="sortby">
			<option value="0">- Сортировка по: -</option>
			<option value="vmname">vmname</option>
			<option value="cluster">cluster</option>
			<option value="host">host</option>
			<option value="folder">folder</option>
			<option value="ip_primary">ip_primary</option>
			<option value="provisioned_space">provisioned_space</option>
			<option value="guest_disk_usage">guest_disk_usage</option>
			<option value="usage_storage">usage_storage</option>
			<option value="memory_overhead">memory_overhead</option>
			<option value="max_cpu_usage">max_cpu_usage</option>
			<option value="max_memory_usage">max_memory_usage</option>
			<option value="path">path</option>
			<option value="mem">mem</option>
			<option value="cpu">cpu</option>
			<option value="sockets">sockets</option>
			<option value="ostype">ostype</option>
			<option value="state">state</option>
			<option value="annotation">annotation</option>
			<option value="boottime">boottime</option>
		</select>
    </div>
</td>	
<td>
</form>
<div align="center" id="selectBoxInfo"></div>
<center><input type=button id="btn_find_vm" value="Найти ВМ" onclick="startAjax();">
<br/>
</tr>
</table>

<body><h3 align="center">Вычислить по IP (При наличии VmWareTools)</h3>
<table  align="center" >

<tr>
<td>
<form>
    <div class="select-sort">
    	Дата:<br />		
        <label for="nic_datep"> </label><input id="nic_datep"/>
    </div>
</td>
<td>
	Подключено:<br />		
	<div class="select-sort">
		<select name="nic_connected" id="nic_connected">
			<option value="2">- выберите состояние -</option>
			<option value="1">connected</option>
			<option value="0">not connected</option>
		</select>
	</div>
</td>
<td>
	
	<div class="select-sort">
		<form method="post" action="">
                 vmname : <br /> <input type="text" id="nic_vmname" name="nic_vmname"/>
			 	  <input type='hidden' id='nic_vmname_hid' value='' />
      	</form>
    </div>
</td>
<td>
	<div class="select-sort">
		<form method="post" action="">
                 MAC : <br /> <input type="text" id="nic_mac" name="nic_mac"/>
			 	  <input type='hidden' id='nic_mac_hid' value='' />
    	</form>
    </div>
</td>
<td>
	
	<div class="select-sort">
		<form method="post" action="">
                 Netlabel (VLAN): <br /> <input type="text" id="nic_netlabel" name="nic_netlabel"/>
			 	  <input type='hidden' id='nic_netlabel_hid' value='' />
		</form>
	</div>
</td>
<td>
	 


	<div class="select-sort">
	<form method="post" action="">
			IP-address : <br /> <input type="text" id="nic_ip" name="nic_ip"/>
			<input type='hidden' id='nic_ip_hid' value='' />
	</form>
	</div>
</td>
<td>
	<label for="order_nic">Сортировка: </label>
	<input type="radio" name="order_nic" value="0" checked="checked">Возр.</input>
	<input type="radio" name="order_nic" value="1">Убыв.</input>	
	<br/>
	<div class="select-sort">
		<select name="sortby_nic" id="sortby_nic">
			<option value="0">- Сортировка по: -</option>
			<option value="host">host</option>
			<option value="vmname">vmname</option>
			<option value="mac">mac</option>
			<option value="connected">connected</option>
			<option value="netlabel">netlabel</option>
			<option value="prefix">prefix</option>
			<option value="ipv4">ipv4</option>

		</select>
    </div>
</td>	
<td>
	</div>
		</form>
		<div align="center" id="selectBoxInfo"></div>
			<center><input type=button value="Найти NIC" onclick="startAjaxNic();">
		</div>
		</form>
		<br/>
		
</tr>
</table>


<center><input type=button  value="Экспорт в CSV" id="btn_export" onclick="exportCsv();">
<div id=result>Тут появится результат</div>


<style type="text/css">
.select-sort {
	margin-bottom: 20px;
}
.select-sort select {
	box-sizing: border-box;
	background-color: #fff;
	border: 2px solid #cb11ab;
	border-radius: 3px;
	color: #001a34;
	padding: 5px 10px;
}

table {

	width: 100%;

	margin-bottom: 20px;

	border-collapse: collapse; 

}

table th {

	font-weight: bold;

	padding: 5px;

	background: #efefef;

	border: 1px solid #dddddd;

}

table td {

	border: 1px solid #dddddd;

	padding: 5px;

	font-size: 85%;

}

table tr td:first-child, .table tr th:first-child {

	border-left: none;

}

table tr td:last-child, .table tr th:last-child {

	border-right: none;

}
table tbody tr:nth-child(odd) td {
	background: #f4f4f4;
}
</style>


</body>
</html>
