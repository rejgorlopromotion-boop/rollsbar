<?php
if(wp_get_environment_type()!=='staging'||home_url()!=='https://staging.rollsbar.ru')throw new RuntimeException('Staging only');
function nov05_assert($valid,$message){if(!$valid)throw new RuntimeException($message);}
$locations=RollsBar_Vacancy_Page::locations();$id=array_key_first($locations);
$valid=['location'=>$id,'city'=>$locations[$id]['city'],'name'=>'QA TEMP — не кандидат','phone'=>'+79781234567','position'=>'kitchen','consent'=>'1'];
$phones=['+79781234567','+44 20 7946 0958','+380501234567','+1 (202) 555-0123','+995555123456'];
foreach($phones as $phone){$data=RollsBar_Vacancy_Page::validate(array_replace($valid,['phone'=>$phone]));nov05_assert(!is_wp_error($data)&&$data['phone']===$phone,'Career international phone changed');nov05_assert(WC_Validation::is_phone($phone,'RU'),'Native Woo international phone rejected');}
foreach(['+7','abc1234567890','++442079460958',str_repeat('1',16),['array']] as $phone)nov05_assert(is_wp_error(RollsBar_Vacancy_Page::validate(array_replace($valid,['phone'=>$phone]))),'Invalid career phone accepted');
// Exercise canonical private persistence without queuing or calling email.
$fixture=0;$application=0;
try{
 $fixture=wp_insert_post(['post_type'=>'rb_job_location','post_status'=>'draft','post_title'=>'QA TEMP — адрес для проверки']);update_post_meta($fixture,'_rollsbar_job_city','Тестгород');
 nov05_assert(!isset(RollsBar_Vacancy_Page::locations()[$fixture]),'Draft location public');wp_update_post(['ID'=>$fixture,'post_status'=>'publish']);nov05_assert(isset(RollsBar_Vacancy_Page::locations()[$fixture]),'Published location missing');
 $data=RollsBar_Vacancy_Page::validate(array_replace($valid,['city'=>'Тестгород','location'=>$fixture,'phone'=>$phones[1]]));nov05_assert(!is_wp_error($data),'New city/address invalid');
 $application=wp_insert_post(['post_type'=>'rb_job_application','post_status'=>'private','post_title'=>'QA TEMP — не кандидат','meta_input'=>['_rollsbar_application'=>$data]]);
 nov05_assert(get_post_meta($application,'_rollsbar_application',true)===$data,'Private phone/location persistence failed');
 nov05_assert(is_wp_error(RollsBar_Vacancy_Page::validate(array_replace($valid,['city'=>'Wrong','location'=>$fixture]))),'Wrong city accepted');
}finally{if($application)wp_delete_post($application,true);if($fixture)wp_delete_post($fixture,true);}
echo "CLIENT_NOV05_BACKEND_PASS international=5 invalid=5 editable_location=yes private_persistence=yes email_calls=0 orders=0\n";
