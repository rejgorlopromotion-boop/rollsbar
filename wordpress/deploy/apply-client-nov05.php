<?php
// Invoked only after a fresh verified DB/uploads/code backup by the staging runner.
if (wp_get_environment_type()!=='staging'||home_url()!=='https://staging.rollsbar.ru')throw new RuntimeException('Staging only');
$mode=$args[0]??'inspect';$root=getenv('PROJECT_ROOT');$file=$root.'/wordpress/data/client-2026-11-05/catalog-order.json';
$plan=json_decode(file_get_contents($file),true,512,JSON_THROW_ON_ERROR);
$products=[];
foreach(wc_get_products(['status'=>'publish','limit'=>-1]) as $product){$source=$product->get_meta('_rollsbar_source_id',true);if(isset($plan['menu_order'][$source]))$products[$source]=$product;}
if(count($products)!==118)throw new RuntimeException('Canonical 118 identities required');
$promos=[];foreach(get_posts(['post_type'=>'rb_promo','post_status'=>'publish','numberposts'=>-1]) as $post){$variant=get_post_meta($post->ID,'_rollsbar_promo_variant',true);if(in_array($variant,['promo','delivery','work','reviews'],true)){if(isset($promos[$variant]))throw new RuntimeException('Duplicate promo variant');$promos[$variant]=$post;}}
if($mode==='inspect'){
 echo wp_json_encode(['products'=>count($products),'orders'=>array_map(static fn($p)=>$p->get_menu_order(),$products),'promos'=>array_map(static fn($p)=>['id'=>$p->ID,'title'=>$p->post_title,'excerpt'=>$p->post_excerpt,'menu_order'=>$p->menu_order,'url'=>get_post_meta($p->ID,'_rollsbar_promo_url',true),'image'=>get_post_thumbnail_id($p->ID)],$promos)],JSON_UNESCAPED_UNICODE)."\n";return;
}
if(!in_array($mode,['apply','verify'],true))throw new RuntimeException('Unknown mode');
if($mode==='apply'){
 require_once ABSPATH.'wp-admin/includes/image.php';require_once ABSPATH.'wp-admin/includes/file.php';require_once ABSPATH.'wp-admin/includes/media.php';
 $titles=['promo'=>'Акции','delivery'=>'Доставка','work'=>'Работа в Rolls Bar','reviews'=>'Отзывы'];$urls=['promo'=>'/aktsii/','delivery'=>'/#delivery','work'=>'/rabota-v-rolls-bar/','reviews'=>'/otzyvy/'];
 foreach($titles as $variant=>$title){
  $post=['post_type'=>'rb_promo','post_status'=>'publish','post_title'=>$title,'menu_order'=>array_search($variant,array_keys($titles),true),'post_excerpt'=>''];
  if(isset($promos[$variant]))$post['ID']=$promos[$variant]->ID;
  $id=wp_insert_post($post,true);if(is_wp_error($id))throw new RuntimeException('Promo update failed');
  update_post_meta($id,'_rollsbar_promo_variant',$variant);update_post_meta($id,'_rollsbar_promo_url',home_url($urls[$variant]));
  $path=$root.'/wordpress/data/client-2026-11-05/'.$variant.'.png';$hash=hash_file('sha256',$path);
  $existing=get_posts(['post_type'=>'attachment','post_status'=>'inherit','numberposts'=>1,'meta_key'=>'_rollsbar_nov05_sha256','meta_value'=>$hash]);
  if($existing)$image=$existing[0]->ID;
  else{$tmp=wp_tempnam($variant.'.png');if(!copy($path,$tmp))throw new RuntimeException('Media temp failed');$image=media_handle_sideload(['name'=>'rollsbar-'.$variant.'-2026-11-05.png','tmp_name'=>$tmp],0,$title);if(is_wp_error($image))throw new RuntimeException('Media import failed');update_post_meta($image,'_rollsbar_nov05_sha256',$hash);}
  if(!set_post_thumbnail($id,$image)&&get_post_thumbnail_id($id)!=$image)throw new RuntimeException('Thumbnail failed');
 }
 foreach($products as $source=>$product){$order=$plan['menu_order'][$source];if($product->get_menu_order()!==$order){$product->set_menu_order($order);$product->save();}}
}
foreach($products as $source=>$product){$fresh=wc_get_product($product->get_id());if($fresh->get_menu_order()!==$plan['menu_order'][$source])throw new RuntimeException('Order readback failed');}
foreach(['promo','delivery','work','reviews'] as $variant){$posts=get_posts(['post_type'=>'rb_promo','post_status'=>'publish','numberposts'=>-1,'meta_key'=>'_rollsbar_promo_variant','meta_value'=>$variant]);if(count($posts)!==1)throw new RuntimeException('Promo readback failed');$image=get_post_thumbnail_id($posts[0]->ID);if(hash_file('sha256',get_attached_file($image))!==hash_file('sha256',$root.'/wordpress/data/client-2026-11-05/'.$variant.'.png'))throw new RuntimeException('Media byte mismatch');}
echo "CLIENT_NOV05_CONTENT_PASS products=118 promos=4 originals=byte_verified\n";
