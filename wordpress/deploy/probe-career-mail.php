<?php
// Read-only SMTP connection/authentication probe: no message, order or application.
if(wp_get_environment_type()!=='staging'||home_url()!=='https://staging.rollsbar.ru')throw new RuntimeException('Staging only');
$result=['configured'=>RollsBar_SMTP::is_configured(),'messages_sent'=>0,'application_id'=>392,'status'=>get_post_meta(392,'_rollsbar_mail_status',true),'attempts'=>get_post_meta(392,'_rollsbar_mail_attempts',true)];
foreach(['Exception','SMTP','PHPMailer'] as $class)require_once ABSPATH.WPINC.'/PHPMailer/'.$class.'.php';
$m=new \PHPMailer\PHPMailer\PHPMailer(true);do_action('phpmailer_init',$m);$trace=[];$m->SMTPDebug=2;$m->Debugoutput=static function($line,$level)use(&$trace){if(str_starts_with($line,'SERVER -> CLIENT:'))$trace[]=trim($line);};$m->Timeout=12;$m->getSMTPInstance()->Timelimit=12;
$result['transport']=$m->Mailer;
if($result['configured']){try{$result['smtp_authenticated']=$m->smtpConnect();}catch(\Throwable $e){$result['smtp_authenticated']=false;$result['exception']=$e->getMessage();}finally{$error=$m->getSMTPInstance()->getError();$result['smtp_error_code']=$error['smtp_code']??'';$result['smtp_error']=$error['error']??'';$result['mailer_error']=$m->ErrorInfo;$m->smtpClose();$result['server_replies']=$trace;}}
echo 'CAREER_MAIL_PROBE '.wp_json_encode($result)."\n";
