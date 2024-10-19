<?php

/*

This script processes updates to the https://github.com/ai-robots-txt/ai.robots.txt repository.

It generates:

  - robots.txt
  - table-of-bot-metrics.md

*/

$robots = json_decode(file_get_contents('robots.json'), 1);
var_dump($robots);


$robots_txt = null;
$robots_table = '| Name | Operator | Respects `robots.txt` | Data use | Visit regularity | Description |'."\n";
$robots_table .= '|-----|----------|-----------------------|----------|------------------|-------------|'."\n";

foreach($robots as $robot => $details) {
  $robots_txt .= 'User-agent: '.$robot."\n";
  $robots_table .= '| '.$robot.' | '.$details['operator'].' | '.$details['respect'].' | '.$details['function'].' | '.$details['frequency'].' | '.$details['description'].' | '."\n";
}

$robots_txt .= 'Disallow: /';

var_dump($robots_txt);
var_dump($robots_table);

file_put_contents('robots.txt', $robots_txt);
file_put_contents('table-of-bot-metrics.md', $robots_table);
