"""Single-CSS staging fix; preserve all application and business data."""
import shlex
import subprocess
from pathlib import Path
import apply_client_media_staging as t

BASE = '823832db53d4b88acd2978cfcb229294b851247a'
CSS = t.THEME + 'assets/css/app.css'

def main():
    sha = t.release_sha()
    paths = subprocess.check_output(['git', 'diff', '--name-only', BASE, '--', t.THEME, t.PLUGIN], cwd=t.ROOT, text=True).splitlines()
    if paths != [CSS]:
        raise ValueError('Only storefront CSS may change')
    script = f'''
[[ -z "$(git -C "$PROJECT_ROOT" status --porcelain)" ]]
[[ "$(git -C "$PROJECT_ROOT" rev-parse HEAD)" == {BASE} ]]
grep -qx 'release={BASE}' "$HOME/.rollsbar-client-nov05-release"
grep -qx 'phase=browser_verified' "$HOME/.rollsbar-client-nov05-release"
{t.code_hash_guard(sha, before=True, changed=[CSS], base=BASE)}
business_before="$(wp_cmd eval {shlex.quote(t.BUSINESS_PHP)})"
git -C "$PROJECT_ROOT" fetch --depth=1 origin {sha}
git -C "$PROJECT_ROOT" checkout --detach {sha}
export WP_PATH PROJECT_ROOT
source "$PROJECT_ROOT/wordpress/deploy/prepare-s1-r2-backup.sh"
[[ "$ROLLSBAR_FRESH_BACKUP_VERIFIED" == YES ]]
snapshot="$HOME/rollsbar-backups/staging/$ROLLSBAR_FRESH_BACKUP_SNAPSHOT"
cp -p "$WP_PATH/wp-content/themes/rollsbar-theme/assets/css/app.css" "$snapshot/promo-title-before.css"
sha256sum "$snapshot/promo-title-before.css" > "$snapshot/promo-title-before.sha256"
sha256sum -c "$snapshot/promo-title-before.sha256"
install -m 0644 "$PROJECT_ROOT/{CSS}" "$WP_PATH/wp-content/themes/rollsbar-theme/assets/css/app.css.promo-new"
mv -f "$WP_PATH/wp-content/themes/rollsbar-theme/assets/css/app.css.promo-new" "$WP_PATH/wp-content/themes/rollsbar-theme/assets/css/app.css"
{t.code_hash_guard(sha, changed=[CSS], base=BASE)}
[[ "$(wp_cmd eval {shlex.quote(t.BUSINESS_PHP)})" == "$business_before" ]]
printf '%s\n' 'release={sha}' "backup=$ROLLSBAR_FRESH_BACKUP_SNAPSHOT" 'phase=backend_verified' > "$HOME/.rollsbar-promo-title-release"
cat "$HOME/.rollsbar-promo-title-release"
echo PROMO_TITLE_CSS_ONLY_PASS
'''
    output = t.execute(script)
    out = Path('qa/visual-results/promo-title')
    out.mkdir(parents=True, exist_ok=True)
    (out / 'apply.log').write_text(output, encoding='utf-8')

if __name__ == '__main__':
    main()
