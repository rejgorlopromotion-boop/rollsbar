"""Read-only confirmation of the single explicitly requested staging application email."""
import os,re,shlex,time,json
from pathlib import Path
from apply_client_media_staging import execute
run=os.environ.get('GITHUB_RUN_ID','')
if not re.fullmatch(r'\d+',run):raise ValueError('Exact browser run required')
php=r'''$matches=[];foreach(get_posts(['post_type'=>'rb_job_application','post_status'=>'private','numberposts'=>20])as $p){if($p->post_title==='ТЕСТ — НЕ ЗВОНИТЬ RUN')$matches[]=$p->ID;}if(count($matches)!==1)throw new RuntimeException('Expected exactly one marked application');$id=$matches[0];$d=get_post_meta($id,'_rollsbar_application',true);if(!str_contains($d['comment'],'QA RUN'))throw new RuntimeException('Wrong test application');echo wp_json_encode(['application_id'=>$id,'status'=>get_post_meta($id,'_rollsbar_mail_status',true),'attempts'=>(int)get_post_meta($id,'_rollsbar_mail_attempts',true),'recipient'=>RollsBar_Vacancy_Page::RECIPIENT,'sent_at'=>get_post_meta($id,'_rollsbar_mail_sent_at',true)]);'''.replace('RUN',run)
for attempt in range(7):
 output=execute('wp_cmd eval '+shlex.quote(php));data=json.loads(output.strip())
 if data['status']=='sent':break
 if attempt==6:raise RuntimeError('Application saved, SMTP acceptance not yet proven: '+data['status'])
 time.sleep(10)
data.update(status='PASS',smtp_accepted=True,inbox_delivery='not asserted',release_sha=os.environ['GITHUB_SHA'])
Path('qa/visual-results/careers/mail.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
