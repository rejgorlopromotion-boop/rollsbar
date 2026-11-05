"""Client checklist presentation/phone release. Email readiness stays deferred."""
import argparse,hashlib,json,os,shlex,subprocess
from pathlib import Path
import apply_client_media_staging as t
from apply_storefront_ux_staging import verify
ROOT=Path(__file__).resolve().parents[2]
BASE='0705edbd44001177fd2d315b716bc7e066d27610'
DEPLOY_BASE='d47cff79ec6dd3d83a659145f51d279e22273916'
CHANGED=[t.THEME+p for p in ['front-page.php','assets/js/app.js','assets/css/app.css']]+[t.PLUGIN+p for p in ['assets/js/checkout.js','includes/class-rollsbar-vacancy-page.php','includes/class-rollsbar-checkout.php']]
RECEIPT='$HOME/.rollsbar-client-nov05-release'
OUT=ROOT/'qa/visual-results/client-nov05'
# Only native product menu_order and its modification timestamp may change.
BUSINESS=t.BUSINESS_PHP.replace("unset($d['image_id'],$d['date_modified'],$d['date_created']);","unset($d['menu_order'],$d['date_modified']);")
def scope():
 paths=subprocess.check_output(['git','diff','--name-only',BASE,'--',t.THEME,t.PLUGIN],cwd=ROOT,text=True).splitlines()
 if sorted(paths)!=sorted(CHANGED):raise ValueError('Unexpected application scope')
def inspect(sha):
 return f'''echo CLIENT_NOV05_INSPECT_BEGIN
git -C "$PROJECT_ROOT" rev-parse HEAD
git -C "$PROJECT_ROOT" status --porcelain
cat "$HOME/.rollsbar-staging-deployed-sha"
cat "{RECEIPT}" 2>/dev/null || true
wp_cmd core version
{t.code_hash_guard(sha,before=True,changed=CHANGED,base=DEPLOY_BASE)}
{verify()}
[[ ! -e "$HOME/rollsbar-backups/staging/.backup-staging.lock" ]]
echo CLIENT_NOV05_CURRENT_BYTES_PASS
'''
def apply(sha):
 copy=''
 for path in CHANGED:
  live='$WP_PATH/'+path.removeprefix('wordpress/')
  copy+=f'install -m 0644 "$PROJECT_ROOT/{path}" "{live}.nov05-new"\nmv -f "{live}.nov05-new" "{live}"\n'
 return inspect(sha)+f'''
[[ -z "$(git -C "$PROJECT_ROOT" status --porcelain)" ]]
[[ "$(git -C "$PROJECT_ROOT" rev-parse HEAD)" == {DEPLOY_BASE} ]]
grep -qx 'release={DEPLOY_BASE}' "{RECEIPT}"
grep -qx 'phase=backend_verified' "{RECEIPT}"
business_before="$(wp_cmd eval {shlex.quote(BUSINESS)})"
git -C "$PROJECT_ROOT" fetch --depth=1 origin {sha}
git -C "$PROJECT_ROOT" checkout --detach {sha}
export WP_PATH PROJECT_ROOT
source "$PROJECT_ROOT/wordpress/deploy/prepare-s1-r2-backup.sh"
[[ "$ROLLSBAR_FRESH_BACKUP_VERIFIED" == YES ]]
snapshot="$HOME/rollsbar-backups/staging/$ROLLSBAR_FRESH_BACKUP_SNAPSHOT"
tar -czf "$snapshot/client-nov05-code.tar.gz" -C "$WP_PATH" {' '.join(shlex.quote(p.removeprefix('wordpress/')) for p in CHANGED)}
tar -tzf "$snapshot/client-nov05-code.tar.gz" >/dev/null
sha256sum "$snapshot/client-nov05-code.tar.gz" > "$snapshot/client-nov05-code.sha256"
sha256sum -c "$snapshot/client-nov05-code.sha256"
printf '%s\n' 'actual_application_before={DEPLOY_BASE}' > "$snapshot/client-nov05-actual-code.txt"
wp_cmd eval-file "$PROJECT_ROOT/wordpress/deploy/apply-client-nov05.php" inspect > "$snapshot/client-nov05-content-before.json"
chmod 600 "$snapshot"/client-nov05-*
printf '%s\n' 'release={sha}' "backup=$ROLLSBAR_FRESH_BACKUP_SNAPSHOT" 'phase=applying' > "{RECEIPT}"
{copy}
{t.code_hash_guard(sha,changed=CHANGED,base=BASE)}
wp_cmd eval-file "$PROJECT_ROOT/wordpress/deploy/apply-client-nov05.php" apply
wp_cmd eval-file "$PROJECT_ROOT/wordpress/deploy/apply-client-nov05.php" verify
wp_cmd eval-file "$PROJECT_ROOT/wordpress/deploy/verify-client-nov05.php"
[[ "$(wp_cmd eval {shlex.quote(BUSINESS)})" == "$business_before" ]]
echo "preserved_product_business_sha256=$business_before"
{verify()}
printf '%s\n' 'release={sha}' "backup=$ROLLSBAR_FRESH_BACKUP_SNAPSHOT" 'phase=backend_verified' 'email_scope=deferred' > "{RECEIPT}"
cat "{RECEIPT}"
echo CLIENT_NOV05_APPLY_PASS
'''
def manifest():
 files=sorted(OUT.glob('*.png'))
 if not files:raise ValueError('No screenshots')
 return hashlib.sha256('\n'.join(p.name+':'+hashlib.sha256(p.read_bytes()).hexdigest() for p in files).encode()).hexdigest()
def finalize(sha):
 d=json.loads((OUT/'browser.json').read_text(encoding='utf8'))
 if d.get('status')!='PASS' or d.get('release_sha')!=sha or len(d.get('checks',[]))!=24:raise ValueError('Exact 3-engine/8-width proof required')
 for path,count in [('client-nov05/checkout-phone.json',3),('storefront-ux-staging/original-browser.json',5),('storefront-ux-staging/browser.json',5),('storefront-ux-staging/interaction/browser.json',6),('address-complete/evidence.json',5),('mobile-feedback/evidence.json',5),('promotions/evidence.json',5)]:
  proof=json.loads((OUT.parent/path).read_text(encoding='utf8'))
  if proof.get('status')!='PASS' or proof.get('release_sha')!=sha or len(proof.get('checks',[]))!=count:raise ValueError('Missing regression: '+path)
 if os.environ.get('ROLLSBAR_REVIEWED_MANIFEST')!=manifest():raise ValueError('Screenshot review required')
 return f'''[[ "$(git -C "$PROJECT_ROOT" rev-parse HEAD)" == {sha} ]]
{t.code_hash_guard(sha,changed=CHANGED,base=BASE)}
grep -qx 'release={sha}' "{RECEIPT}"
grep -qx 'phase=backend_verified' "{RECEIPT}"
wp_cmd eval-file "$PROJECT_ROOT/wordpress/deploy/apply-client-nov05.php" verify
{verify()}
sed -i 's/phase=backend_verified/phase=browser_verified/' "{RECEIPT}"
cat "{RECEIPT}"
echo CLIENT_NOV05_SCOPED_RELEASE_PASS_EMAIL_REMAINS_DEFERRED
'''
def main():
 p=argparse.ArgumentParser();p.add_argument('--phase',choices=['inspect','apply','manifest','finalize'],required=True);a=p.parse_args();OUT.mkdir(parents=True,exist_ok=True)
 if a.phase=='manifest':print(manifest());return
 sha=t.release_sha();scope();output=t.execute(inspect(sha) if a.phase=='inspect' else apply(sha) if a.phase=='apply' else finalize(sha))
 (OUT/(a.phase+'.log')).write_text(output,encoding='utf8')
 if a.phase=='apply':
  target=OUT.parent/'storefront-ux-staging';target.mkdir(exist_ok=True)
  (target/'media.json').write_text(output.split('UX_MEDIA_BEGIN\n')[-1].split('\nUX_MEDIA_END')[0].strip(),encoding='utf8')
if __name__=='__main__':main()
