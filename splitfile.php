<?php
set_time_limit(600);
ini_set("auto_detect_line_endings", true);
ini_set('memory_limit', '1024M');
/* Number of 'insert' statements per file */
$max_lines_per_split = 50;
$dump_file = "G:\\Backup Studienarbeits DB\\backup_zuege2_090218.sql";
$split_file = "dump-split-%d.sql";
$dump_directory = "G:\\Backup Studienarbeits DB\\sql-dump\\";
$line_count = 0;
$file_count = 1;
$total_lines = 0; 
$handle = fopen($dump_file, "r");
$buffer = "";
if ($handle) {
 while(($line = fgets($handle)) !== false) {
  $total_lines++;
  if($total_lines > 50000000 || $file_count > 200) {
   break;
  }
  if(preg_match("/insert into/i", $line)) {
   /* Copy buffer to the split file */
   if($line_count >= $max_lines_per_split) {
    $file_name = $dump_directory . sprintf($split_file, $file_count);
    $out_write = @fopen($file_name, "w+");
    fputs($out_write, $buffer);
    fclose($out_write);
    $buffer = '';
    $line_count = 0;
    $file_count++;
   }
   $line_count++;
  }
  $buffer .= $line;
 } 
 if($buffer && strlen($buffer) < 200)  {
  /* Write out the remaining buffer */
  $file_name = $dump_directory . sprintf($split_file, $file_count);
  $out_write = @fopen($file_name, "w+");
  fputs($out_write, $buffer);
  fclose($out_write);
 } elseif ($buffer) {
  echo 'Warning please check last file if complete';
 }
 fclose($handle);
 echo "Split done.";
} else {
 echo 'No Handle obtained.';
}
