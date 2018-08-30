<?PHP
   $data = file_get_contents('php://input');
   //echo $data;
	print_r($_GET);
   if (!(file_put_contents($_GET['fileName'],$data) === FALSE)) echo "File xfer completed."; // file could be empty, though
   else echo "File xfer failed.";
?>
