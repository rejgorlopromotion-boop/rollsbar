<?php
define('ABSPATH',__DIR__);class WP_Error{public function __construct(...$args){}}
function is_wp_error($v){return $v instanceof WP_Error;}function absint($v){return abs((int)$v);}function sanitize_text_field($v){return trim(strip_tags((string)$v));}function sanitize_textarea_field($v){return trim(strip_tags((string)$v));}function current_time($f){return $f==='Y-m-d'?'2026-11-05':'2026-11-05 12:00:00';}function get_posts($args){return [(object)['ID'=>42]];}function get_post_meta(...$args){return 'Симферополь';}function get_the_title($p){return 'Кечкеметская улица, 1';}
require __DIR__.'/../../wordpress/wp-content/plugins/rollsbar-core/includes/class-rollsbar-vacancy-page.php';
$input=['location'=>42,'city'=>'Симферополь','name'=>'Иван','phone'=>'89781234567','position'=>'kitchen','consent'=>'1'];$data=RollsBar_Vacancy_Page::validate($input);
if(is_wp_error($data)||$data['phone']!=='+79781234567'||$data['address']!=='Кечкеметская улица, 1'||$data['birthday']!=='')throw new RuntimeException('Valid canonical application');
$cases=[['name'=>''],['phone'=>'00000000000'],['phone'=>'7123'],['phone'=>['bad']],['consent'=>''],['location'=>99999],['city'=>'Москва'],['position'=>'invented'],['birthday'=>'2030-01-01'],['birthday'=>'2000-02-30'],['comment'=>str_repeat('а',3001)]];
foreach($cases as $case)if(!is_wp_error(RollsBar_Vacancy_Page::validate(array_merge($input,$case))))throw new RuntimeException('Invalid input accepted');
echo "CAREER_VALIDATION_PASS positive=1 negative=11\n";
