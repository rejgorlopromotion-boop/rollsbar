<?php
/**
 * Template for /rabota-v-rolls-bar/.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

get_header();

$vacancies = get_posts(
	array(
		'post_type'      => 'rb_vacancy',
		'post_status'    => 'publish',
		'posts_per_page' => -1,
		'orderby'        => array( 'menu_order' => 'ASC', 'date' => 'DESC' ),
	)
);

$phone_display = function_exists( 'rollsbar_setting' ) ? rollsbar_setting( 'phone_display', '+7 978 688-22-88' ) : '+7 978 688-22-88';
$phone_href    = function_exists( 'rollsbar_setting' ) ? rollsbar_setting( 'phone_href', '+79786882288' ) : '+79786882288';
$telegram_url  = function_exists( 'rollsbar_setting' ) ? rollsbar_setting( 'telegram_url', 'https://telegram.me/rollsbar82' ) : 'https://telegram.me/rollsbar82';
$vk_url        = function_exists( 'rollsbar_setting' ) ? rollsbar_setting( 'vk_url', 'https://vk.ru/rollsbar82' ) : 'https://vk.ru/rollsbar82';
$locations = RollsBar_Vacancy_Page::locations();
$cities = array_unique( array_column( $locations, 'city' ) );
$status = isset( $_GET['application'] ) ? sanitize_key( wp_unslash( $_GET['application'] ) ) : '';
$messages = array( 'received' => 'Спасибо! Анкета получена. Мы свяжемся с вами по указанному телефону.', 'invalid' => 'Проверьте обязательные поля: город, адрес заведения, направление, имя, телефон и согласие.', 'expired' => 'Обновите страницу и отправьте анкету ещё раз: время заполнения формы истекло.', 'rate' => 'Вы уже отправили несколько анкет. Попробуйте позже или позвоните нам.', 'error' => 'Не удалось сохранить анкету. Попробуйте ещё раз или позвоните нам.' );
?>

<section class="rb-career-hero">
	<div class="rollsbar-shell rb-career-hero__inner">
		<h1>Присоединяйся<br>к команде Rolls Bar</h1>
		<p>Выбери направление и заполни анкету — обсудим работу в команде Rolls Bar.</p>

		<div class="rb-career-art" aria-hidden="true">
			<div class="rb-career-arc">и всё закрутится</div>
			<div class="rb-career-circle"><span>ROLLS BAR</span></div>
		</div>
	</div>

	<div class="rb-career-tabs" data-rb-vacancy-tabs>
		<button class="active" type="button" data-area="all">Все</button>
		<button type="button" data-area="kitchen">Кухня и касса</button>
		<button type="button" data-area="delivery">Доставка</button>
	</div>
</section>

<section class="rollsbar-shell rb-career-section" id="vacancies">
	<h2>Актуальные вакансии</h2>

	<div class="rb-vacancy-list">
		<?php if ( $vacancies ) : ?>
			<?php foreach ( $vacancies as $vacancy ) : ?>
				<?php
				$area = (string) get_post_meta( $vacancy->ID, '_rollsbar_vacancy_area', true );
				if ( ! in_array( $area, array( 'kitchen', 'delivery', 'other' ), true ) ) {
					$area = 'other';
				}
				$summary = has_excerpt( $vacancy )
					? get_the_excerpt( $vacancy )
					: wp_trim_words( wp_strip_all_tags( $vacancy->post_content ), 28 );
				?>
				<article class="rb-vacancy-card" data-vacancy-area="<?php echo esc_attr( $area ); ?>">
					<h3><?php echo esc_html( get_the_title( $vacancy ) ); ?></h3>
					<?php if ( $summary ) : ?>
						<p><?php echo esc_html( $summary ); ?></p>
					<?php endif; ?>
					<?php if ( trim( (string) $vacancy->post_content ) ) : ?>
						<details>
							<summary>Подробнее</summary>
							<div class="rb-vacancy-card__details"><?php echo wp_kses_post( wpautop( $vacancy->post_content ) ); ?></div>
						</details>
					<?php endif; ?>
				</article>
			<?php endforeach; ?>
		<?php else : ?>
			<article class="rb-vacancy-card rb-vacancy-card--empty">
				<h3>Сейчас активных вакансий нет</h3>
				<p>Оставь анкету — мы сможем связаться с тобой и обсудить подходящие вакансии.</p>
			</article>
		<?php endif; ?>
	</div>
</section>

<section class="rollsbar-shell rb-career-section rb-career-form-section" id="vacancy-form" aria-labelledby="rb-career-form-title">
 <div class="rb-questionnaire">
  <h2 id="rb-career-form-title">Заполни небольшую анкету</h2>
  <p>Оставь свои контакты — мы свяжемся с тобой и обсудим детали.</p>
  <?php if ( isset( $messages[ $status ] ) ) : ?><div class="rb-career-status" role="<?php echo 'received' === $status ? 'status' : 'alert'; ?>" tabindex="-1" data-career-status><?php echo esc_html( $messages[ $status ] ); ?></div><?php endif; ?>
  <?php if ( $locations ) : ?>
  <form class="rb-career-form" method="post" action="<?php echo esc_url( admin_url( 'admin-post.php' ) ); ?>" data-career-form>
   <input type="hidden" name="action" value="rollsbar_career_apply">
   <?php wp_nonce_field( 'rollsbar_career_apply', 'career_nonce', false ); ?>
   <input type="hidden" name="application_token" value="<?php echo esc_attr( wp_generate_uuid4() ); ?>">
   <label class="rb-career-field rb-career-wide">Город <select name="city" autocomplete="address-level2" required data-career-city><?php foreach ( $cities as $city ) : ?><option value="<?php echo esc_attr( $city ); ?>"><?php echo esc_html( $city ); ?></option><?php endforeach; ?></select></label>
   <label class="rb-career-field rb-career-wide">Адрес заведения <select name="location" required data-career-location><option value="">Выберите адрес заведения</option><?php foreach ( $locations as $id => $location ) : ?><option value="<?php echo esc_attr( $id ); ?>" data-city="<?php echo esc_attr( $location['city'] ); ?>"><?php echo esc_html( $location['address'] ); ?></option><?php endforeach; ?></select></label>
   <label class="rb-career-field rb-career-wide">Направление <select name="position" required><option value="">Выберите направление</option><option value="kitchen">Кухня и касса</option><option value="delivery">Доставка</option><option value="other">Другое / уточнить</option></select></label>
   <label class="rb-career-field rb-career-wide">Номер телефона <input name="phone" type="tel" autocomplete="tel" inputmode="tel" placeholder="+7 978 123-45-67" maxlength="24" required data-career-phone></label>
   <label class="rb-career-field">Имя <input name="name" type="text" autocomplete="given-name" maxlength="80" required></label>
   <label class="rb-career-field">Фамилия <span class="rb-career-optional">— по желанию</span><input name="surname" type="text" autocomplete="family-name" maxlength="100"></label>
   <label class="rb-career-field rb-career-wide">Дата рождения <span class="rb-career-optional">— по желанию</span><input name="birthday" type="date" autocomplete="bday" min="1900-01-01" max="<?php echo esc_attr( current_time( 'Y-m-d' ) ); ?>"></label>
   <label class="rb-career-field rb-career-wide">Комментарий <span class="rb-career-optional">— по желанию</span><textarea name="comment" rows="3" maxlength="3000"></textarea></label>
   <label class="rb-career-consent rb-career-wide"><input name="consent" type="checkbox" value="1" required><span>Даю согласие на <a href="<?php echo esc_url( home_url( '/politika-konfidencialnosti/' ) ); ?>" target="_blank" rel="noopener">обработку персональных данных</a> для рассмотрения анкеты и связи по вопросам трудоустройства.</span></label>
   <label class="rb-career-honeypot" aria-hidden="true">Ваш сайт <input name="website" type="text" tabindex="-1" autocomplete="off"></label>
   <button class="rb-career-submit rb-career-wide" type="submit">Отправить анкету</button>
  </form>
  <?php else : ?><p>Чтобы оставить анкету, позвони нам: <a href="tel:<?php echo esc_attr( $phone_href ); ?>"><?php echo esc_html( $phone_display ); ?></a>.</p><?php endif; ?>
 </div>
</section>

<nav class="rb-career-actions" aria-label="Связаться по вакансии">
	<a class="rb-career-actions__apply" href="#vacancy-form" data-career-apply>Заполнить анкету</a>
	<button class="rb-career-actions__round" type="button" data-rb-career-chat aria-label="Написать">💬</button>
	<a class="rb-career-actions__round" href="tel:<?php echo esc_attr( $phone_href ); ?>" aria-label="Позвонить">☎</a>
</nav>

<div class="rb-career-chat" data-rb-career-chat-modal aria-hidden="true">
	<button class="rb-career-chat__backdrop" type="button" data-rb-career-chat-close aria-label="Закрыть"></button>
	<section class="rb-career-chat__panel" role="dialog" aria-modal="true" aria-label="Связаться с Rolls Bar">
		<h3>Связаться с Rolls Bar</h3>
		<p>Напиши нам или позвони, чтобы узнать о работе в команде.</p>
		<div class="rb-career-chat__links">
			<?php if ( $telegram_url ) : ?><a href="<?php echo esc_url( $telegram_url ); ?>" target="_blank" rel="noopener">Telegram</a><?php endif; ?>
			<?php if ( $vk_url ) : ?><a href="<?php echo esc_url( $vk_url ); ?>" target="_blank" rel="noopener">VK</a><?php endif; ?>
			<a href="tel:<?php echo esc_attr( $phone_href ); ?>"><?php echo esc_html( $phone_display ); ?></a>
		</div>
		<button type="button" class="rb-career-chat__close" data-rb-career-chat-close>Закрыть</button>
	</section>
</div>

<?php
get_footer();
