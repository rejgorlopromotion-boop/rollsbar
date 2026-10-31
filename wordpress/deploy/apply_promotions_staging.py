"""Three presentation files and one create-only WordPress page; staging only."""
import argparse,hashlib,json,os,shlex,subprocess
from pathlib import Path
import apply_client_media_staging as transport
from apply_storefront_ux_staging import verify
ROOT=Path(__file__).resolve().parents[2]
BASE='3edb1726673ab1761d1094589f95e99f8fb2f866'
CHANGED=[transport.THEME+p for p in ['front-page.php','page-aktsii.php','template-parts/site-menu.php']]
OUT=ROOT/'qa/visual-results';RECEIPT='$HOME/.rollsbar-promotions-release'
PAGE=r'''$p=get_page_by_path('aktsii',OBJECT,'page');if($p){if($p->post_status!=='publish'||trim($p->post_content)!=='')throw new RuntimeException('Existing promotions content requires review');}else{$id=wp_insert_post(['post_type'=>'page','post_status'=>'publish','post_title'=>'Акции','post_name'=>'aktsii','post_content'=>''],true);if(is_wp_error($id))throw new RuntimeException($id->get_error_message());}echo "PROMOTIONS_PAGE_READY\n";'''
CHECK=r'''$p=get_page_by_path('aktsii',OBJECT,'page');if(!$p||$p->post_status!=='publish'||get_page_template_slug($p->ID))throw new RuntimeException('Native promotions page contract failed');echo "PROMOTIONS_NATIVE_PAGE_PASS\n";'''

def scope():
 paths=subprocess.check_output(['git','diff','--name-only',BASE,'--',transport.PLUGIN,transport.THEME],cwd=ROOT,text=True).splitlines()
 if sorted(paths)!=sorted(CHANGED):raise ValueError('Only three presentation files permitted')

def manifest():
 files=sorted((OUT/'promotions').glob('*.png'))+sorted((OUT/'storefront-ux-staging').rglob('*.png'))
 if len(list((OUT/'promotions').glob('*.png')))!=7:raise ValueError('Five offer views and two homepage captures required')
 return hashlib.sha256('\n'.join(p.relative_to(OUT).as_posix()+':'+hashlib.sha256(p.read_bytes()).hexdigest() for p in files).encode()).hexdigest()

def apply(sha):
 copy=''
 for path in CHANGED:
  live='$WP_PATH/'+path.removeprefix('wordpress/')
  copy+=f'install -m 0644 "$PROJECT_ROOT/{path}" "{live}.offers-new"\nmv -f "{live}.offers-new" "{live}"\n'
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
wp_cmd eval {shlex.quote(PAGE)}
{copy}
{transport.code_hash_guard(sha,changed=CHANGED,base=BASE)}
[[ "$(wp_cmd eval {shlex.quote(transport.BUSINESS_PHP)})" == "$business_before" ]]
wp_cmd eval {shlex.quote(CHECK)}
{verify()}
printf '%s\n' 'release={sha}' "backup=$ROLLSBAR_FRESH_BACKUP_SNAPSHOT" 'phase=backend_verified' > "{RECEIPT}"
cat "{RECEIPT}"
echo PROMOTIONS_BACKEND_PASS
'''

def finalize(sha):
 for name,n in [('promotions/evidence.json',5),('storefront-ux-staging/original-browser.json',5),('storefront-ux-staging/browser.json',5),('storefront-ux-staging/interaction/browser.json',6)]:
  d=json.loads((OUT/name).read_text(encoding='utf8'))
  if d.get('status')!='PASS' or d.get('release_sha')!=sha or len(d.get('checks',[]))!=n:raise ValueError('Exact live proof required: '+name)
 if os.environ.get('ROLLSBAR_REVIEWED_MANIFEST')!=manifest():raise ValueError('Screenshots must be reviewed')
 return f'''[[ "$(git -C "$PROJECT_ROOT" rev-parse HEAD)" == {sha} ]]
{transport.code_hash_guard(sha,changed=CHANGED,base=BASE)}
grep -qx 'release={sha}' "{RECEIPT}"
grep -qx 'phase=backend_verified' "{RECEIPT}"
wp_cmd eval {shlex.quote(CHECK)}
{verify()}
printf '%s\n' '{sha}' > "$HOME/.rollsbar-staging-deployed-sha.offers-new"
chmod 600 "$HOME/.rollsbar-staging-deployed-sha.offers-new"
mv -f "$HOME/.rollsbar-staging-deployed-sha.offers-new" "$HOME/.rollsbar-staging-deployed-sha"
sed -i 's/phase=backend_verified/phase=browser_verified/' "{RECEIPT}"
cat "{RECEIPT}"
echo PROMOTIONS_STAGING_PASS
'''

def main():
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['apply','finalize','inspect','manifest'],required=True);args=p.parse_args()
 if args.phase=='manifest':print(manifest());return
 sha=transport.release_sha();scope();(OUT/'promotions').mkdir(parents=True,exist_ok=True)
 script=apply(sha) if args.phase=='apply' else finalize(sha) if args.phase=='finalize' else f'cat "{RECEIPT}" 2>/dev/null || true\ncat "$HOME/.rollsbar-staging-deployed-sha"\ngit -C "$PROJECT_ROOT" rev-parse HEAD\n'
 output=transport.execute(script);(OUT/'promotions'/(args.phase+'.log')).write_text(output,encoding='utf8')
 if args.phase=='apply':
  if 'PROMOTIONS_BACKEND_PASS' not in output:raise RuntimeError('Missing receipt')
  target=OUT/'storefront-ux-staging';target.mkdir(parents=True,exist_ok=True)
  (target/'media.json').write_text(output.split('UX_MEDIA_BEGIN\n')[-1].split('\nUX_MEDIA_END')[0].strip(),encoding='utf8')
if __name__=='__main__':main()
