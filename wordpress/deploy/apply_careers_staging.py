"""Career form, private applications and footer contrast; staging only."""
import argparse,hashlib,json,os,shlex,subprocess
from pathlib import Path
import apply_client_media_staging as transport
from apply_storefront_ux_staging import verify
ROOT=Path(__file__).resolve().parents[2]
BASE='ee7dcd5fa90a646419bda611f6ff0cd2d8582f5a'
CHANGED=[transport.PLUGIN+'includes/class-rollsbar-vacancy-page.php']+[transport.THEME+p for p in ['page-rabota-v-rolls-bar.php','footer.php','assets/css/app.css','assets/js/app.js','assets/images/footer-logo.svg']]
OUT=ROOT/'qa/visual-results';RECEIPT='$HOME/.rollsbar-careers-release'
CHECK=r"""$p=get_page_by_path('rabota-v-rolls-bar',OBJECT,'page');if(!$p||$p->post_status!=='publish'||!RollsBar_Vacancy_Page::locations())throw new RuntimeException('Career page contract failed');echo "CAREERS_NATIVE_PAGE_PASS\n";"""

def scope():
 paths=subprocess.check_output(['git','diff','--name-only',BASE,'--',transport.PLUGIN,transport.THEME],cwd=ROOT,text=True).splitlines()
 if sorted(paths)!=sorted(CHANGED):raise ValueError('Only six approved application files permitted')

def manifest():
 files=sorted(p for name in ['careers','storefront-ux-staging','address-complete','mobile-feedback','promotions'] for p in (OUT/name).rglob('*.png'))
 if len(list((OUT/'careers').glob('*.png')))!=16:raise ValueError('Five form/consent/footer views and received capture required')
 return hashlib.sha256('\n'.join(p.relative_to(OUT).as_posix()+':'+hashlib.sha256(p.read_bytes()).hexdigest() for p in files).encode()).hexdigest()

def apply(sha):
 copy=''
 for path in CHANGED:
  live='$WP_PATH/'+path.removeprefix('wordpress/')
  copy+=f'install -m 0644 "$PROJECT_ROOT/{path}" "{live}.careers-new"\nmv -f "{live}.careers-new" "{live}"\n'
 return f'''[[ -z "$(git -C "$PROJECT_ROOT" status --porcelain)" ]]
{transport.code_hash_guard(sha,before=True,changed=CHANGED,base=BASE)}
{verify()}
business_before="$(wp_cmd eval {shlex.quote(transport.BUSINESS_PHP)})"
git -C "$PROJECT_ROOT" fetch --depth=1 origin {sha}
git -C "$PROJECT_ROOT" checkout --detach {sha}
export WP_PATH PROJECT_ROOT
source "$PROJECT_ROOT/wordpress/deploy/prepare-s1-r2-backup.sh"
[[ "$ROLLSBAR_FRESH_BACKUP_VERIFIED" == YES ]]
umask 077
printf '%s\n' 'release={sha}' "backup=$ROLLSBAR_FRESH_BACKUP_SNAPSHOT" 'phase=applying' > "{RECEIPT}"
{copy}
{transport.code_hash_guard(sha,changed=CHANGED,base=BASE)}
[[ "$(wp_cmd eval {shlex.quote(transport.BUSINESS_PHP)})" == "$business_before" ]]
wp_cmd eval {shlex.quote(CHECK)}
wp_cmd eval-file "$PROJECT_ROOT/wordpress/deploy/verify-careers.php"
{verify()}
printf '%s\n' 'release={sha}' "backup=$ROLLSBAR_FRESH_BACKUP_SNAPSHOT" 'phase=backend_verified' > "{RECEIPT}"
cat "{RECEIPT}"
echo CAREERS_BACKEND_PASS
'''

def finalize(sha):
 for name,n in [('careers/evidence.json',5),('address-complete/evidence.json',5),('mobile-feedback/evidence.json',5),('promotions/evidence.json',5),('storefront-ux-staging/original-browser.json',5),('storefront-ux-staging/browser.json',5),('storefront-ux-staging/interaction/browser.json',6)]:
  d=json.loads((OUT/name).read_text(encoding='utf8'))
  if d.get('status')!='PASS' or d.get('release_sha')!=sha or len(d.get('checks',[]))!=n:raise ValueError('Exact live proof required: '+name)
 mail=json.loads((OUT/'careers/mail.json').read_text(encoding='utf8'))
 if mail.get('status')!='PASS' or mail.get('release_sha')!=sha or mail.get('smtp_accepted') is not True:raise ValueError('Native email proof required')
 if os.environ.get('ROLLSBAR_REVIEWED_MANIFEST')!=manifest():raise ValueError('Screenshots must be reviewed')
 return f'''[[ "$(git -C "$PROJECT_ROOT" rev-parse HEAD)" == {sha} ]]
{transport.code_hash_guard(sha,changed=CHANGED,base=BASE)}
grep -qx 'release={sha}' "{RECEIPT}"
grep -qx 'phase=backend_verified' "{RECEIPT}"
wp_cmd eval {shlex.quote(CHECK)}
{verify()}
printf '%s\n' '{sha}' > "$HOME/.rollsbar-staging-deployed-sha.careers-new"
chmod 600 "$HOME/.rollsbar-staging-deployed-sha.careers-new"
mv -f "$HOME/.rollsbar-staging-deployed-sha.careers-new" "$HOME/.rollsbar-staging-deployed-sha"
sed -i 's/phase=backend_verified/phase=browser_verified/' "{RECEIPT}"
cat "{RECEIPT}"
echo CAREERS_STAGING_PASS
'''

def main():
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['apply','finalize','inspect','manifest'],required=True);args=p.parse_args()
 if args.phase=='manifest':print(manifest());return
 sha=transport.release_sha();scope();(OUT/'careers').mkdir(parents=True,exist_ok=True)
 script=apply(sha) if args.phase=='apply' else finalize(sha) if args.phase=='finalize' else f'cat "{RECEIPT}" 2>/dev/null || true\ncat "$HOME/.rollsbar-staging-deployed-sha"\ngit -C "$PROJECT_ROOT" rev-parse HEAD\n'
 output=transport.execute(script);(OUT/'careers'/(args.phase+'.log')).write_text(output,encoding='utf8')
 if args.phase=='apply':
  if 'CAREERS_BACKEND_PASS' not in output:raise RuntimeError('Missing receipt')
  target=OUT/'storefront-ux-staging';target.mkdir(parents=True,exist_ok=True)
  (target/'media.json').write_text(output.split('UX_MEDIA_BEGIN\n')[-1].split('\nUX_MEDIA_END')[0].strip(),encoding='utf8')
if __name__=='__main__':main()
