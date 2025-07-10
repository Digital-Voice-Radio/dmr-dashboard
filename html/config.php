<?php
    $configFile = getenv('MONITOR_CONFIG') ?: '/config/mon.cfg';
    $config = parse_ini_file($configFile, true);
?>
