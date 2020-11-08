<?php
	if (isset($_GET['hub_challenge'])) {
	    echo $_GET['hub_challenge'];
	    exit();
	}
	else {
		$req_dump = "";
		foreach ($_SERVER as $key => $value) {
			if (strpos($key, 'HTTP_') === 0) {
				$chunks = explode('_', $key);
				$header = '';
				for ($i = 1; $y = sizeof($chunks) - 1, $i < $y; $i++) {
					$header .= ucfirst(strtolower($chunks[$i])).'-';
				}
				$header .= ucfirst(strtolower($chunks[$i])).': '.$value;
				#echo $header."\n";
				$req_dump .= $header."\n";
			}
		}
		$body = file_get_contents('php://input');
		if ($body != '') {
		  $req_dump .= "\n$body\n\n";
		}
		ob_start();
		$req_dump .= var_export($_GET)."\n\n---------------";
		$req_dump .= var_export($_POST)."\n\n---------------";
		$result = ob_get_clean();
		$req_dump .= $result;
		$fp = file_put_contents('request.log', $req_dump, FILE_APPEND);
		ob_end_clean();

		$out = shell_exec("nohup python3 pwn.py > /dev/null 2>&1 &");
	}
?>
