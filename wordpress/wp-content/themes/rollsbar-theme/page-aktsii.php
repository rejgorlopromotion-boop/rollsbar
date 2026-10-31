<?php
/** Published owner offers; informational only, no cart/discount mutation. */
if ( ! defined( 'ABSPATH' ) ) { exit; }
get_header();
$today = current_datetime()->format( 'Y-m-d' );
$birthday_active = $today >= '2026-02-17' && $today <= '2027-02-17';
?>
<style>
.rb-offers{padding:32px 0 72px}.rb-offers__back{display:inline-flex;align-items:center;min-height:44px;margin-bottom:16px;font-weight:700}.rb-offers h1{font-size:clamp(32px,5vw,48px);line-height:1.1;margin:0 0 24px;letter-spacing:-.04em}.rb-offer{display:grid;grid-template-columns:minmax(180px,.65fr) minmax(0,1.35fr);border:1px solid var(--rb-line);border-radius:26px;overflow:hidden;background:#fff;box-shadow:0 14px 36px rgba(0,0,0,.055)}.rb-offer__amount{display:flex;flex-direction:column;align-items:center;justify-content:center;gap:12px;background:var(--rb-red);color:#fff;padding:36px 24px}.rb-offer__amount strong{font-size:clamp(64px,9vw,108px);line-height:1;letter-spacing:-.06em}.rb-offer__amount span{font-weight:700;font-size:18px}.rb-offer__body{padding:32px}.rb-offer h2{font-size:clamp(24px,3vw,32px);line-height:1.15;margin:0 0 20px;letter-spacing:-.03em}.rb-offer p,.rb-offer li,.rb-offers__source{font-size:16px;line-height:1.6}.rb-offer ul{padding-left:22px;margin:0 0 20px}.rb-offer li+li{margin-top:8px}.rb-offer__dates{color:#555}.rb-offer__note{padding:16px;border-radius:14px;background:var(--rb-soft)}.rb-offer__actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:24px}.rb-offer__actions a{display:inline-flex;align-items:center;justify-content:center;min-height:48px;padding:12px 20px;border-radius:14px;font-weight:800;text-decoration:none;background:var(--rb-soft)}.rb-offer__actions a:first-child{background:var(--rb-red);color:#fff}.rb-offers__source{margin-top:24px;color:#555}.rb-offers a:focus-visible{outline:3px solid #222;outline-offset:4px}.rb-offers__empty{padding:24px;border:1px solid var(--rb-line);border-radius:20px;font-size:16px}
@media(max-width:700px){.rb-offers{padding-top:24px}.rb-offer{grid-template-columns:1fr;border-radius:20px}.rb-offer__amount{padding:28px 20px}.rb-offer__body{padding:24px 20px}.rb-offer__actions{flex-direction:column}.rb-offer__actions a{width:100%}}
</style>
<section class="rb-offers rollsbar-shell" aria-labelledby="rb-offers-title">
 <a class="rb-offers__back" href="<?php echo esc_url( home_url( '/' ) ); ?>">← Вернуться в меню</a>
 <h1 id="rb-offers-title">Акции Rolls Bar</h1>
 <?php if ( $birthday_active ) : ?>
 <article class="rb-offer" aria-labelledby="rb-birthday-title">
  <div class="rb-offer__amount"><strong>−10%</strong><span>Ко дню рождения</span></div>
  <div class="rb-offer__body">
   <h2 id="rb-birthday-title">Скидка 10% именинникам</h2>
   <ul><li>В день рождения и ещё два дня после него.</li><li>На всё меню, кроме сетов.</li></ul>
   <p class="rb-offer__dates">Срок акции: с 17 февраля 2026 по 17 февраля 2027 года.</p>
   <p class="rb-offer__note">Скидка не применяется автоматически в корзине. Чтобы воспользоваться предложением, свяжитесь с нами при оформлении заказа.</p>
   <div class="rb-offer__actions"><a href="tel:+79786882288">Позвонить: +7 978 688-22-88</a><a href="<?php echo esc_url( home_url( '/#rolls' ) ); ?>">Выбрать блюда</a></div>
  </div>
 </article>
 <?php else : ?>
 <p class="rb-offers__empty">Сейчас опубликованных действующих акций нет. Следите за новыми предложениями Rolls Bar.</p>
 <?php endif; ?>
 <p class="rb-offers__source">Наши предложения также опубликованы в <a href="https://yandex.ru/maps/org/rolls_bar/229692973623/" target="_blank" rel="noopener">Яндекс Картах</a>.</p>
</section>
<?php get_footer(); ?>
