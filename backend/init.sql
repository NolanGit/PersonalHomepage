create table app
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	url varchar(255) not null,
	user_id int not null,
	expect_price int not null,
	`order` int not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table app_price
(
	id int auto_increment
		primary key,
	app_id int not null,
	price varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table bookmarks
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	url varchar(255) not null,
	icon varchar(255) not null,
	`order` int not null,
	user_id int not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table cloud_drive
(
	id int auto_increment
		primary key,
	file_id int not null,
	user_id int not null,
	share_token varchar(255) null,
	share_link varchar(255) null,
	share_expire_time datetime null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table console
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	`order` int not null,
	icon varchar(255) null,
	component_name varchar(255) null,
	is_valid int null,
	update_time datetime null
)
charset=utf8;

create table fund
(
	id int auto_increment
		primary key,
	code varchar(255) not null,
	name varchar(255) not null
)
charset=utf8;

create table fund_belong
(
	id int auto_increment
		primary key,
	fund_id int not null,
	user_id int not null,
	push int not null,
	push_threshold varchar(255) not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table fund_price
(
	id int auto_increment
		primary key,
	fund_id int not null,
	price float not null,
	`range` float null,
	update_time datetime not null
)
charset=utf8;

create table gold_price
(
	id int auto_increment
		primary key,
	price varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table gold_price_push_option
(
	id int auto_increment
		primary key,
	user_id int not null,
	is_valid int not null,
	push_threshold varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table icon
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	category int not null
)
charset=utf8;

create table icon_category
(
	id int auto_increment
		primary key,
	name varchar(255) not null
)
charset=utf8;

create table image_hosting
(
	id int auto_increment
		primary key,
	file_name varchar(255) not null,
	file_path varchar(255) not null,
	token varchar(255) not null,
	shorted_link varchar(255) not null,
	user_id int not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table ip_location
(
	id int auto_increment
		primary key,
	ip varchar(255) not null,
	location varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table news
(
	id int auto_increment
		primary key,
	website text charset utf8 not null,
	category text charset utf8 not null,
	content text charset utf8 not null,
	create_time datetime not null
);

create table notes
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	token varchar(255) null,
	content varchar(255) not null,
	user_id int not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table privilege
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	mark varchar(255) not null,
	remark varchar(255) null,
	is_valid int not null,
	update_time datetime null
)
charset=utf8;

create table privilege_role
(
	id int auto_increment
		primary key,
	privilege_id int not null,
	role_id int not null,
	is_valid int not null
)
charset=utf8;

create table push
(
	id int auto_increment
		primary key,
	user_id int not null,
	widget_id int not null,
	is_valid int not null,
	notify int not null,
	notify_method int not null,
	notify_interval_raw int not null,
	notify_interval_unit int not null,
	notify_interval int not null,
	notify_trigger_time datetime not null,
	update_time datetime not null
)
charset=utf8;

create table push_queue
(
	id int auto_increment
		primary key,
	user_id int not null,
	method int not null,
	address varchar(255) not null,
	title varchar(255) not null,
	content varchar(255) not null,
	status int not null,
	trigger_time datetime not null,
	log varchar(255) not null,
	create_time datetime not null,
	update_time datetime not null
)
charset=utf8;

create table role
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	remark varchar(255) null,
	is_valid int not null,
	update_time datetime null
)
charset=utf8;

create table script
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	sub_system_id int null,
	start_folder text null,
	start_script text null,
	type int null,
	runs int not null,
	is_valid int null,
	version int not null,
	user text not null,
	update_time datetime null
)
charset=utf8;

create table script_detail
(
	id int auto_increment
		primary key,
	script_id int null,
	type text null,
	label text null,
	value text null,
	place_holder text null,
	options text null,
	createable int not null,
	disabled int null,
	extra_button int null,
	extra_button_label text null,
	extra_button_script text null,
	remark text null,
	is_important int not null,
	is_valid int not null,
	visible int not null,
	version int not null,
	user text null,
	update_time datetime null
)
charset=utf8;

create table script_log
(
	id int auto_increment
		primary key,
	script_id int null,
	command text null,
	detail text null,
	output text null,
	version int null,
	user_id int null,
	user text null,
	start_time datetime null,
	end_time datetime null
)
charset=utf8;

create table script_schedule
(
	id int auto_increment
		primary key,
	script_id int null,
	command text null,
	detail text null,
	version int null,
	user_id int not null,
	is_valid int not null,
	is_automatic int not null,
	`interval` int not null,
	interval_raw int not null,
	interval_unit int not null,
	trigger_time datetime null,
	update_time datetime null
)
charset=utf8;

create table script_sub_system
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	user_id int not null,
	is_valid int null,
	update_time datetime null
)
charset=utf8;

create table search_engines
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	main_url varchar(255) not null,
	suggest_url varchar(255) not null,
	suggest_func varchar(255) null,
	icon varchar(255) not null
)
charset=utf8;

create table search_engines_log
(
	id int auto_increment
		primary key,
	user_id int not null,
	user varchar(255) not null,
	engine_id int not null,
	search_text varchar(255) not null,
	ip varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table short_content
(
	id int auto_increment
		primary key,
	code varchar(255) not null,
	content varchar(255) not null,
	type int not null,
	is_valid int not null,
	expire_time datetime not null,
	update_time datetime not null
)
charset=utf8;

create table stock
(
	id int auto_increment
		primary key,
	code varchar(255) not null,
	name varchar(255) not null,
	market int not null
)
charset=utf8;

create table stock_belong
(
	id int auto_increment
		primary key,
	stock_id int not null,
	user_id int not null,
	push int null,
	push_threshold varchar(255) null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table stock_price
(
	id int auto_increment
		primary key,
	stock_id int not null,
	price float not null,
	`range` float null,
	update_time datetime not null
)
charset=utf8;

create table upload
(
	id int auto_increment
		primary key,
	file_name varchar(255) not null,
	file_path varchar(255) not null,
	size varchar(255) null,
	user_id int not null,
	update_time datetime not null
)
charset=utf8;

create table user
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	login_name varchar(255) not null,
	password varchar(255) not null,
	stable_salt varchar(255) not null,
	salt varchar(255) not null,
	salt_expire_time datetime not null,
	role_id int not null,
	email varchar(255) not null,
	wechat_key varchar(255) not null,
	is_valid int not null,
	create_time datetime not null,
	update_time datetime not null
)
charset=utf8;

create table wallpapers
(
	id int auto_increment
		primary key,
	date varchar(255) not null,
	url varchar(255) not null,
	size varchar(255) not null,
	copyright varchar(255) not null,
	copyrightlink varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table weather_data
(
	id int auto_increment
		primary key,
	location_id int not null,
	aqi int not null,
	cond_code_d int not null,
	cond_code_n int not null,
	cond_txt_d varchar(255) not null,
	cond_txt_n varchar(255) not null,
	fl int not null,
	tmp int not null,
	tmp_max int not null,
	tmp_min int not null,
	tomorrow_cond_code_d int not null,
	tomorrow_cond_txt_d varchar(255) not null,
	tomorrow_tmp_max int not null,
	tomorrow_tmp_min int not null,
	wind varchar(255) not null,
	update_time datetime not null
)
charset=utf8;

create table weather_location
(
	id int auto_increment
		primary key,
	location varchar(255) not null,
	user_id int not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table weather_notify
(
	id int auto_increment
		primary key,
	location varchar(255) not null,
	user_id int not null,
	notify_type varchar(255) not null,
	notify_method int not null,
	is_valid int not null,
	update_time datetime not null
)
charset=utf8;

create table widget
(
	id int auto_increment
		primary key,
	name varchar(255) not null,
	name_zh varchar(255) null,
	is_valid int not null,
	span int not null,
	buttons varchar(255) null,
	auto_update int null,
	update_time datetime not null
)
charset=utf8;

create table widget_suite
(
	id int auto_increment
		primary key,
	name varchar(255) null,
	user_id int not null,
	`order` int not null,
	is_valid int not null,
	detail varchar(255) not null,
	update_time datetime not null
)
charset=utf8;


TRUNCATE TABLE `search_engines`;
INSERT INTO `search_engines` (`id`, `name`, `main_url`, `suggest_url`, `suggest_func`, `icon`) VALUES ('1', '百度', 'https://www.baidu.com/s?word=%word%', 'https://suggestion.baidu.com/su?wd=%word%&cb=window.baidu.sug', 'window.baidu={sug:function(json){cb(json.s.map(function(x){return{\'value\':x}}))}}', 'iconfont icon-baidu-line');
INSERT INTO `search_engines` (`id`, `name`, `main_url`, `suggest_url`, `suggest_func`, `icon`) VALUES ('2', 'Google', 'https://www.google.com/search?q=%word%&oq=1&sourceid=chrome&ie=UTF-8', 'https://suggestqueries.google.com/complete/search?client=youtube&q=%word%&jsonp=window.google.ac.h', 'window.google={ac:{h:function(json){cb(json[1].map(function(x){return{\'value\':x[0]}}))}}}', 'iconfont icon-google-line');
INSERT INTO `search_engines` (`id`, `name`, `main_url`, `suggest_url`, `suggest_func`, `icon`) VALUES ('3', 'Bing', 'https://cn.bing.com/search?q=%word%', 'https://api.bing.com/qsonhs.aspx?type=cb&q=%word%&cb=window.bing.sug', 'window.bing={sug:function(json){let sugList=\"\";if(json.AS.Results !== undefined && json.AS.Results[0].Suggests !== undefined){sugList = json.AS.Results[0].Suggests};cb(sugList.map(function(x){return{\'value\':x.Txt}}))}}', '');
INSERT INTO `search_engines` (`id`, `name`, `main_url`, `suggest_url`, `suggest_func`, `icon`) VALUES ('4', '360搜索', 'https://www.so.com/s?ie=utf-8&fr=hao_360so&src=home_hao_360so&q=%word%', 'https://sug.so.360.cn/suggest?encodein=utf-8&encodeout=utf-8&format=json&word=%word%&callback=window.so.sug', 'window.so={sug:function(json){cb(json.result.map(function(x){return{\'value\':x.word}}))}}', '');
INSERT INTO `search_engines` (`id`, `name`, `main_url`, `suggest_url`, `suggest_func`, `icon`) VALUES ('5', '搜狗', 'https://www.sogou.com/web?query=%word%', 'https://www.sogou.com/suggnew/ajajjson?type=web&key=%word%', 'window.sogou={sug:function(json){cb(json[1].map(function(x){return{\'value\':x}}))}}', '');
TRUNCATE TABLE `bookmarks`;
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (1, 'GitHub', 'https://www.github.com', 'iconfont icon-github', 1, 0, 1, '2019-10-28 11:35:37.428601');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (2, '知乎', 'https://www.zhihu.com', 'iconfont icon-ai-book', 1, 0, 1, '2019-10-28 11:35:37.428601');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (3, '地图', 'https://map.baidu.com/', 'iconfont icon-ditu', 1, 0, 1, '2019-10-30 15:54:32.744137');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (4, '淘宝', 'http://taobao.com', 'iconfont icon-taobao-line', 1, 0, 1, '2019-10-30 15:54:32.744137');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (5, 'JSON', 'http://json.cn', 'iconfont icon-ai-code', 1, 0, 1, '2019-10-30 15:54:32.744137');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (6, 'weibo', 'http://weibo.com', 'iconfont icon-weibo-fill', 1, 0, 1, '2019-10-30 15:54:32.744137');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (7, '微信', 'http://wx.qq.com', 'iconfont icon-wechat-line', 1, 0, 1, '2019-10-30 15:54:32.744137');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (8, 'icloud', 'http://icloud.com', 'iconfont icon-apple-fill', 1, 0, 1, '2019-10-30 15:54:32.744137');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (9, 'GitHub', 'https://www.github.com', 'iconfont icon-github', 1, 1, 0, '2019-12-30 10:49:32.586422');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (10, '知乎', 'https://www.zhihu.com', 'iconfont icon-ai-book', 1, 1, 0, '2019-12-30 10:49:32.586422');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (11, '地图', 'https://map.baidu.com/', 'iconfont icon-ditu', 1, 1, 0, '2019-12-30 10:49:32.586422');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (12, '京东', 'https://jd.com', 'iconfont icon-31gouwuchexuanzhong', 2, 1, 0, '2019-12-30 10:49:32.586422');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (13, 'JSON', 'https://www.json.cn/', 'iconfont icon-ai-code', 3, 1, 0, '2019-12-30 10:49:32.586422');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (14, 'iCloud', 'https://www.icloud.com/', 'iconfont icon-apple-fill', 4, 1, 0, '2019-12-30 10:49:32.586422');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (15, 'GitHub', 'https://www.github.com', 'iconfont icon-github', 1, 1, 1, '2019-12-30 10:49:32.651957');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (16, 'JSON', 'https://www.json.cn/', 'iconfont icon-ai-code', 2, 1, 1, '2019-12-30 10:49:32.754595');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (17, 'iCloud', 'https://www.icloud.com/', 'iconfont icon-apple-fill', 3, 1, 1, '2019-12-30 10:49:32.813966');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (18, '知乎', 'https://www.zhihu.com', 'iconfont icon-ai-book', 4, 1, 1, '2019-12-30 10:49:32.869960');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (19, '地图', 'https://map.baidu.com/', 'iconfont icon-ditu', 5, 1, 1, '2019-12-30 10:49:32.927004');
INSERT INTO `bookmarks` (`id`, `name`, `url`, `icon`, `order`, `user_id`, `is_valid`, `update_time`) VALUES (20, '京东', 'https://jd.com', 'iconfont icon-31gouwuchexuanzhong', 6, 1, 1, '2019-12-30 10:49:32.982482');
TRUNCATE TABLE `console`;
INSERT INTO `console` (`id`, `name`, `order`, `icon`, `component_name`, `is_valid`, `update_time`) VALUES ('1', '修改主页组件', '1', 'iconfont icon-ai-edit', 'widgetEdit', '1', '2019-10-28 11:35:37');
INSERT INTO `console` (`id`, `name`, `order`, `icon`, `component_name`, `is_valid`, `update_time`) VALUES ('2', '账户和权限', '2', 'iconfont icon-ai-user', 'Privilege', '1', '2019-10-28 11:35:37');
INSERT INTO `console` (`id`, `name`, `order`, `icon`, `component_name`, `is_valid`, `update_time`) VALUES ('3', '运行脚本', '3', 'iconfont icon-ai-code', 'Script', '1', '2019-10-28 11:35:37');
TRUNCATE TABLE `icon`;
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('1', 'iconfont icon-bug-report', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('2', 'iconfont icon-card-giftcard', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('3', 'iconfont icon-explore', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('4', 'iconfont icon-flight-takeoff', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('5', 'iconfont icon-g-translate', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('6', 'iconfont icon-http', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('7', 'iconfont icon-language', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('8', 'iconfont icon-room', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('9', 'iconfont icon-shopping-basket', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('10', 'iconfont icon-store', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('11', 'iconfont icon-today', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('12', 'iconfont icon-translate', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('13', 'iconfont icon-trending-up', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('14', 'iconfont icon-verified-user', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('15', 'iconfont icon-album', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('16', 'iconfont icon-radio', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('17', 'iconfont icon-airplanemode-active', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('18', 'iconfont icon-headset', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('19', 'iconfont icon-keyboard', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('20', 'iconfont icon-laptop', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('21', 'iconfont icon-mouse', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('22', 'iconfont icon-phone-iphone', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('23', 'iconfont icon-security', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('24', 'iconfont icon-speaker', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('25', 'iconfont icon-tv', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('26', 'iconfont icon-toys', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('27', 'iconfont icon-videogame-asset', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('28', 'iconfont icon-watch', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('29', 'iconfont icon-brush', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('30', 'iconfont icon-collections', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('31', 'iconfont icon-color-lens', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('32', 'iconfont icon-musnote', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('33', 'iconfont icon-local-activity', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('34', 'iconfont icon-local-atm', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('35', 'iconfont icon-local-bar', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('36', 'iconfont icon-local-cafe', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('37', 'iconfont icon-local-florist', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('38', 'iconfont icon-local-taxi', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('39', 'iconfont icon-restaurant-menu', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('40', 'iconfont icon-restaurant', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('41', 'iconfont icon-terrain', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('42', 'iconfont icon-subway', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('43', 'iconfont icon-train', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('44', 'iconfont icon-time-to-leave', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('45', 'iconfont icon-airport-shuttle', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('46', 'iconfont icon-beach-access', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('47', 'iconfont icon-golf-course', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('48', 'iconfont icon-spa', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('49', 'iconfont icon-cake', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('50', 'iconfont icon-publpx', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('51', 'iconfont icon-school', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('52', 'iconfont icon-whatshot', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('53', 'iconfont icon-ditu', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('54', 'iconfont icon-qing', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('55', 'iconfont icon-shachenbao', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('56', 'iconfont icon-shachen', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('57', 'iconfont icon-qiangshachenbao', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('58', 'iconfont icon-yangsha', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('59', 'iconfont icon-mai', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('60', 'iconfont icon-dayu', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('61', 'iconfont icon-duoyun', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('62', 'iconfont icon-duoyunzhuanyin', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('63', 'iconfont icon-xiaoyu', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('64', 'iconfont icon-zhongyu', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('65', 'iconfont icon-baoyu', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('66', 'iconfont icon-wu', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('67', 'iconfont icon-leizhenyu', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('68', 'iconfont icon-wumai', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('69', 'iconfont icon-xiaoxue', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('70', 'iconfont icon-baoxue', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('71', 'iconfont icon-bingbao', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('72', 'iconfont icon-daxue', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('73', 'iconfont icon-leizhenxue', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('74', 'iconfont icon-yujiaxue', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('75', 'iconfont icon-zhongxue', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('76', 'iconfont icon-feng', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('77', 'iconfont icon-shachen1', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('78', 'iconfont icon-shachengbao', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('79', 'iconfont icon-taifeng', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('80', 'iconfont icon-PM', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('81', 'iconfont icon-app_icons--', '4');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('82', 'iconfont icon-cart', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('83', 'iconfont icon-cart-fill', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('84', 'iconfont icon-ai-module', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('85', 'iconfont icon-ai-article', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('86', 'iconfont icon-ai-code', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('87', 'iconfont icon-ai-edit', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('88', 'iconfont icon-ai-copy', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('89', 'iconfont icon-ai-set', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('90', 'iconfont icon-ai-user', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('91', 'iconfont icon-ai-home', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('92', 'iconfont icon-ai-img-list', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('93', 'iconfont icon-work-copy', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('94', 'iconfont icon-huodong-copy', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('95', 'iconfont icon-ai-hot', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('96', 'iconfont icon-ai-link', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('97', 'iconfont icon-ai-resume', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('98', 'iconfont icon-ai-briefcase', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('99', 'iconfont icon-ai-calendar', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('100', 'iconfont icon-ai-calculator', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('101', 'iconfont icon-jiageprice1-copy', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('102', 'iconfont icon-yuedureading19-copy', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('103', 'iconfont icon-ai-book', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('104', 'iconfont icon-ai-cart', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('105', 'iconfont icon-ai-new', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('106', 'iconfont icon-ai-search', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('107', 'iconfont icon-dianpu-copy', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('108', 'iconfont icon-ai-mark', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('109', 'iconfont icon-ai-tel', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('110', 'iconfont icon-ai-eye', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('111', 'iconfont icon-ai-video', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('112', 'iconfont icon-ai-camera', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('113', 'iconfont icon-ai-i', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('114', 'iconfont icon-ai-keyboard', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('115', 'iconfont icon-ai-wallet', '2');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('116', 'iconfont icon-ai-profit', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('117', 'iconfont icon-instagram', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('118', 'iconfont icon-raspberrypi', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('119', 'iconfont icon-ie-line', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('120', 'iconfont icon-instagram-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('121', 'iconfont icon-github-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('122', 'iconfont icon-linkedin-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('123', 'iconfont icon-linkedin-box-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('124', 'iconfont icon-linkedin-box-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('125', 'iconfont icon-linkedin-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('126', 'iconfont icon-mastercard-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('127', 'iconfont icon-google-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('128', 'iconfont icon-evernote-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('129', 'iconfont icon-firefox-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('130', 'iconfont icon-mastercard-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('131', 'iconfont icon-opera-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('132', 'iconfont icon-netflix-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('133', 'iconfont icon-google-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('134', 'iconfont icon-paypal-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('135', 'iconfont icon-playstation-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('136', 'iconfont icon-qq-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('137', 'iconfont icon-reactjs-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('138', 'iconfont icon-safari-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('139', 'iconfont icon-reactjs-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('140', 'iconfont icon-safari-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('141', 'iconfont icon-skype-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('142', 'iconfont icon-spotify-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('143', 'iconfont icon-stack-overflow-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('144', 'iconfont icon-spotify-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('145', 'iconfont icon-reddit-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('146', 'iconfont icon-telegram-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('147', 'iconfont icon-stack-overflow-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('148', 'iconfont icon-taobao-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('149', 'iconfont icon-tumblr-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('150', 'iconfont icon-tumblr-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('151', 'iconfont icon-taobao-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('152', 'iconfont icon-twitter-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('153', 'iconfont icon-twitch-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('154', 'iconfont icon-switch-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('155', 'iconfont icon-ubuntu-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('156', 'iconfont icon-vuejs-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('157', 'iconfont icon-ubuntu-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('158', 'iconfont icon-twitter-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('159', 'iconfont icon-wechat--fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('160', 'iconfont icon-wechat--line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('161', 'iconfont icon-windows-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('162', 'iconfont icon-wechat-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('163', 'iconfont icon-weibo-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('164', 'iconfont icon-switch-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('165', 'iconfont icon-wechat-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('166', 'iconfont icon-weibo-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('167', 'iconfont icon-whatsapp-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('168', 'iconfont icon-whatsapp-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('169', 'iconfont icon-xbox-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('170', 'iconfont icon-xbox-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('171', 'iconfont icon-youtube-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('172', 'iconfont icon-zhihu-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('173', 'iconfont icon-zhihu-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('174', 'iconfont icon-vuejs-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('175', 'iconfont icon-wechat-pay-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('176', 'iconfont icon-alipay-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('177', 'iconfont icon-alipay-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('178', 'iconfont icon-angularjs-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('179', 'iconfont icon-android-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('180', 'iconfont icon-angularjs-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('181', 'iconfont icon-apple-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('182', 'iconfont icon-amazon-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('183', 'iconfont icon-amazon-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('184', 'iconfont icon-chrome-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('185', 'iconfont icon-apple-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('186', 'iconfont icon-baidu-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('187', 'iconfont icon-bilibili-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('188', 'iconfont icon-bilibili-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('189', 'iconfont icon-baidu-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('190', 'iconfont icon-dingding-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('191', 'iconfont icon-douban-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('192', 'iconfont icon-edge-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('193', 'iconfont icon-dropbox-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('194', 'iconfont icon-edge-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('195', 'iconfont icon-evernote-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('196', 'iconfont icon-dingding-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('197', 'iconfont icon-douban-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('198', 'iconfont icon-dropbox-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('199', 'iconfont icon-github-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('200', 'iconfont icon-gitlab-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('201', 'iconfont icon-chrome-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('202', 'iconfont icon-gitlab-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('203', 'iconfont icon-firefox-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('204', 'iconfont icon-ie-fill', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('205', 'iconfont icon-viber', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('206', 'iconfont icon-adobeaftereffects', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('207', 'iconfont icon-adobeindesign', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('208', 'iconfont icon-playerme', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('209', 'iconfont icon-dribbble', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('210', 'iconfont icon-gitter', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('211', 'iconfont icon-justgiving', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('212', 'iconfont icon-microsoftonenote', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('213', 'iconfont icon-graphql', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('214', 'iconfont icon-podcasts', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('215', 'iconfont icon-angular', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('216', 'iconfont icon-foursquare', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('217', 'iconfont icon-macys', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('218', 'iconfont icon-mastercard', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('219', 'iconfont icon-nintendoswitch', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('220', 'iconfont icon-pinterest', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('221', 'iconfont icon-twilio', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('222', 'iconfont icon-sinaweibo', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('223', 'iconfont icon-microsoftaccess', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('224', 'iconfont icon-netflix', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('225', 'iconfont icon-airbnb', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('226', 'iconfont icon-ebay', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('227', 'iconfont icon-npm', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('228', 'iconfont icon-tinder', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('229', 'iconfont icon-youtube', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('230', 'iconfont icon-tesla', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('231', 'iconfont icon-flipboard', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('232', 'iconfont icon-ted', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('233', 'iconfont icon-jenkins', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('234', 'iconfont icon-redis', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('235', 'iconfont icon-git', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('236', 'iconfont icon-gitlab', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('237', 'iconfont icon-adobeacrobatreader', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('238', 'iconfont icon-gmail', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('239', 'iconfont icon-swift', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('240', 'iconfont icon-ubuntu', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('241', 'iconfont icon-html', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('242', 'iconfont icon-stackoverflow', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('243', 'iconfont icon-sogou', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('244', 'iconfont icon-sparkpost', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('245', 'iconfont icon-rss', '5');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('246', 'iconfont icon-mozillafirefox', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('247', 'iconfont icon-amazon', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('248', 'iconfont icon-xbox', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('249', 'iconfont icon-empirekred', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('250', 'iconfont icon-wechat', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('251', 'iconfont icon-javascript', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('252', 'iconfont icon-spreaker', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('253', 'iconfont icon-linux', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('254', 'iconfont icon-vim', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('255', 'iconfont icon-nginx', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('256', 'iconfont icon-hulu', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('257', 'iconfont icon-line', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('258', 'iconfont icon-nodejs', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('259', 'iconfont icon-bing', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('260', 'iconfont icon-mongodb', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('261', 'iconfont icon-tripadvisor', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('262', 'iconfont icon-vuejs', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('263', 'iconfont icon-googlehangouts', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('264', 'iconfont icon-slack', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('265', 'iconfont icon-kickstarter', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('266', 'iconfont icon-spotify', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('267', 'iconfont icon-wordpress', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('268', 'iconfont icon-tencentqq', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('269', 'iconfont icon-skype', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('270', 'iconfont icon-vimeo', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('271', 'iconfont icon-react', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('272', 'iconfont icon-visualstudiocode', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('273', 'iconfont icon-microsoftoutlook', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('274', 'iconfont icon-twitter', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('275', 'iconfont icon-docker', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('276', 'iconfont icon-googleplay', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('277', 'iconfont icon-webpack', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('278', 'iconfont icon-px', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('279', 'iconfont icon-telegram', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('280', 'iconfont icon-python', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('281', 'iconfont icon-jsfiddle', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('282', 'iconfont icon-ifixit', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('283', 'iconfont icon-buffer', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('284', 'iconfont icon-paypal', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('285', 'iconfont icon-windows', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('286', 'iconfont icon-intel', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('287', 'iconfont icon-readthedocs', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('288', 'iconfont icon-baidu', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('289', 'iconfont icon-php', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('290', 'iconfont icon-visa', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('291', 'iconfont icon-google', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('292', 'iconfont icon-googledrive', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('293', 'iconfont icon-onedrive', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('294', 'iconfont icon-playstation', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('295', 'iconfont icon-jira', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('296', 'iconfont icon-dropbox', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('297', 'iconfont icon-xcode', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('298', 'iconfont icon-microsoftword', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('299', 'iconfont icon-github', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('300', 'iconfont icon-instapaper', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('301', 'iconfont icon-django', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('302', 'iconfont icon-sublimetext', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('303', 'iconfont icon-microsoft', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('304', 'iconfont icon-apple', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('305', 'iconfont icon-yahoo', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('306', 'iconfont icon-bootstrap', '3');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('307', 'iconfont icon-mozilla', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('308', 'iconfont icon-steam', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('309', 'iconfont icon-wikipedia', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('310', 'iconfont icon-vsco', '1');
INSERT INTO `icon` (`id`, `name`, `category`) VALUES ('311', 'iconfont icon-applemusic', '1');
TRUNCATE TABLE `icon_category`;
INSERT INTO `icon_category` (`id`, `name`) VALUES ('1', '公司');
INSERT INTO `icon_category` (`id`, `name`) VALUES ('2', '物品');
INSERT INTO `icon_category` (`id`, `name`) VALUES ('3', '技术');
INSERT INTO `icon_category` (`id`, `name`) VALUES ('4', '天气');
INSERT INTO `icon_category` (`id`, `name`) VALUES ('5', '其他');
TRUNCATE TABLE `privilege`;
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('1', '用户信息', '/userInfo', '返回用户自定义的内容，如城市、书签等', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('2', '控制台', '/console/get', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('3', '控制台-账户和权限-用户列表获取', '/privilege/userGet', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('4', '控制台-账户和权限-用户禁用', '/privilege/userDisable', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('5', '控制台-账户和权限-用户启用', '/privilege/userEnable', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('6', '控制台-账户和权限-用户信息修改', '/privilege/userRoleChange', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('7', '控制台-账户和权限-用户删除', '/privilege/userDelete', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('8', '控制台-账户和权限-角色列表获取', '/privilege/roleGet', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('9', '控制台-账户和权限-角色具有的权限列表获取', '/privilege/rolePrivilegeGet', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('10', '控制台-账户和权限-用户对应权限修改', '/privilege/rolePrivilegeEdit', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('11', '控制台-账户和权限-角色新增和修改', '/privilege/roleEdit', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('12', '控制台-账户和权限-角色禁用', '/privilege/roleDisable', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('13', '控制台-账户和权限-角色启用', '/privilege/roleEnable', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('14', '控制台-账户和权限-角色删除', '/privilege/roleDelete', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('15', '控制台-账户和权限-权限列表获取', '/privilege/privilegeGet', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('16', '控制台-账户和权限-权限新增和修改', '/privilege/privilegeEdit', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('17', '控制台-账户和权限-权限禁用', '/privilege/privilegeDisable', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('18', '控制台-账户和权限-权限启用', '/privilege/privilegeEnable', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('19', '控制台-账户和权限-权限删除', '/privilege/privilegeDelete', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('20', '控制台-脚本运行平台-子系统列表', '/script/subSystem', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('21', '控制台-脚本运行平台-子系统脚本', '/script/subSystemScript', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('22', '控制台-脚本运行平台-脚本运行', '/script/run', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('23', '控制台-脚本运行平台-脚本终止运行', '/script/terminate', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('24', '控制台-脚本运行平台-脚本运行输出获取', '/script/runOutput', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('25', '控制台-脚本运行平台-脚本编辑', '/script/edit', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('26', '控制台-脚本运行平台-脚本删除', '/script/delete', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('27', '控制台-脚本运行平台-脚本运行输出保存', '/script/saveOutput', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('28', '控制台-脚本运行平台-脚本运行记录获取', '/script/getLogs', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('29', '控制台-脚本运行平台-脚本额外按钮脚本运行', '/script/extraButtonScriptRun', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('30', '控制台-脚本运行平台-定时任务查看', '/script/schedule', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('31', '控制台-脚本运行平台-定时任务编辑', '/script/scheduleEdit', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('32', '控制台-脚本运行平台-定时任务删除', '/script/scheduleDelete', '', '1', '2019-10-28 11:35:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('33', '控制台-脚本运行平台-新增栏目', '/script/subSystemAdd', '', '1', '2020-06-11 15:32:10');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('34', '控制台-脚本运行平台-删除栏目', '/script/subSystemDelete', '', '1', '2020-06-11 15:32:10');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('35', 'APP-获取', '/app/get', '', '1', '2020-06-11 15:31:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('36', 'APP-新增', '/app/add', '', '1', '2020-06-11 15:31:51');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('37', 'APP-编辑', '/app/edit', '', '1', '2020-06-11 15:32:10');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('38', '推送-获取', '/push/get', '', '0', '2020-06-22 23:06:06');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('39', '推送-新增', '/push/add', '', '1', '2020-06-22 23:10:45');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('40', '推送-编辑', '/push/edit', '', '1', '2020-06-22 23:11:32');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('41', '书签-新增', '/bookmarks/bookmarksAdd', '', '1', '2020-06-25 23:41:13');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('42', '书签-编辑', '/bookmarks/bookmarksEdit', '', '1', '2020-06-25 23:41:29');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('43', '天气-增加位置', '/weather/weatherLocationCreate', '', '1', '2020-06-25 23:42:17');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('44', '天气-编辑', '/weather/weatherLocationListEdit', '', '1', '2020-06-25 23:42:33');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('45', '文件-上传', '/upload', '', '1', '2020-07-11 15:41:10');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('46', '文件-下载', '/download', '', '1', '2020-07-11 15:41:26');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('47', '网盘-获取列表', '/cloudDrive/get', '', '1', '2020-07-11 17:38:16');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('48', '网盘-保存', '/cloudDrive/save', '', '1', '2020-07-11 17:38:48');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('49', '网盘-删除', '/cloudDrive/delete', '', '1', '2020-07-11 17:39:03');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('50', '控制台-脚本运行平台-全部脚本获取', '/script/scriptAll', '', '1', '2020-07-23 15:54:53');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('51', '便签-获取', '/notes/get', '', '1', '2020-07-31 10:28:37');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('52', '便签-保存', '/notes/save', '', '1', '2020-07-31 10:29:14');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('53', '便签-推送', '/notes/notify', '', '1', '2020-07-31 10:29:47');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('54', '便签-回滚', '/notes/revert', '', '1', '2020-07-31 18:06:57');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('55', '控制台-编辑组件-组件集获取', '/widget/suite/detail', '', '1', '2020-08-09 14:37:27');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('56', '控制台-编辑组件-组件获取全部', '/widget/get_all', '', '1', '2020-08-09 14:37:50');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('57', '控制台-编辑组件-保存', '/widget/suite/save', '', '1', '2020-08-09 23:30:58');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('58', '网盘-分享', '/cloudDrive/share/set', '', '1', '2020-08-12 15:55:54');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('59', '网盘-取消分享', '/cloudDrive/share/cancel', '', '1', '2020-08-12 17:01:26');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('60', '黄金价格-编辑阈值', '/gold/edit', '', '1', '2020-08-17 19:20:27');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('61', '图床-获取', '/imageHosting/get', '', '1', '2020-08-28 23:10:02');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('62', '图床-文件改名', '/imageHosting/changeName', '', '1', '2020-08-28 23:13:58');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('63', '网盘-文件改名', '/cloudDrive/changeName', '', '1', '2020-08-28 23:14:27');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('64', '图床-删除', '/imageHosting/delete', '', '1', '2020-08-28 23:30:15');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('65', '图床-保存', '/imageHosting/save', '', '1', '2020-08-29 21:48:47');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('66', '翻译-翻译文本', '/translator/translate', '', '1', '2020-09-04 17:44:33');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('67', '天气-获取推送', '/weather/notifyGet', '', '1', '2020-09-16 11:25:46');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('68', '天气-编辑推送', '/weather/notifySet', '', '1', '2020-09-16 11:26:40');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('69', '天气-校验地理位置', '/weather/check', '', '1', '2020-09-16 17:56:39');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('70', '股票-新增', '/stock/add', '', '1', '2020-10-13 21:21:41');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('71', '股票-校验', '/stock/check', '', '1', '2020-10-14 10:54:16');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('72', '股票-编辑', '/stock/edit', '', '1', '2020-10-14 10:54:40');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('73', '基金-新增', '/fund/add', '', '1', '2020-10-13 21:21:41');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('74', '基金-校验', '/fund/check', '', '1', '2020-10-14 10:54:16');
INSERT INTO `privilege` (`id`, `name`, `mark`, `remark`, `is_valid`, `update_time`) VALUES ('75', '基金-编辑', '/fund/edit', '', '1', '2020-10-14 10:54:40');
TRUNCATE TABLE `privilege_role`;
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('1', '1', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('2', '2', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('3', '3', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('4', '4', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('5', '5', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('6', '6', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('7', '7', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('8', '8', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('9', '9', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('10', '10', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('11', '11', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('12', '12', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('13', '13', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('14', '14', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('15', '15', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('16', '16', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('17', '17', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('18', '18', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('19', '19', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('20', '20', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('21', '21', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('22', '22', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('23', '23', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('24', '24', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('25', '25', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('26', '26', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('27', '27', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('28', '28', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('29', '29', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('30', '30', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('31', '31', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('32', '32', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('33', '33', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('34', '34', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('35', '35', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('36', '36', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('37', '37', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('38', '38', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('39', '39', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('40', '40', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('41', '41', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('42', '42', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('43', '43', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('44', '44', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('45', '45', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('46', '46', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('47', '47', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('48', '48', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('49', '49', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('50', '50', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('51', '51', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('52', '52', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('53', '53', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('54', '54', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('55', '55', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('56', '56', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('57', '57', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('58', '58', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('59', '59', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('60', '60', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('61', '61', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('62', '62', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('63', '63', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('64', '64', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('65', '65', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('66', '66', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('67', '67', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('68', '68', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('69', '69', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('70', '70', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('71', '71', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('72', '72', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('73', '73', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('74', '74', '1', '1');
INSERT INTO `privilege_role` (`id`, `privilege_id`, `role_id`, `is_valid`) VALUES ('75', '75', '1', '1');
TRUNCATE TABLE `wallpapers`;
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('1', '2020-09-23', 'https://www.bing.com//th?id=OHR.Almabtrieb_ZH-CN8639425400_1920x1080.jpg', '0.34MB', '为牛下山节（即把牛从高山牧场赶回）装饰的牛，奥地利坦海姆塔尔 (© Hans Lippert/Alamy)', 'https://www.bing.com/search?q=%E5%A5%A5%E5%9C%B0%E5%88%A9%E5%9D%A6%E6%B5%B7%E5%A7%86%E5%A1%94%E5%B0%94&form=hpcapt&mkt=zh-cn', '2020-09-24 15:08:29');
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('2', '2020-09-24', 'https://www.bing.com/th?id=OHR.LoarreCastle_ZH-CN1136982025_1920x1080.jpg', '0.34MB', '洛阿雷城堡，西班牙韦斯卡 (© Sebastian Wasek/Alamy)', 'https://www.bing.com/search?q=%E6%B4%9B%E9%98%BF%E9%9B%B7%E5%9F%8E%E5%A0%A1&form=hpcapt&mkt=zh-cn', '2020-09-25 18:57:06');
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('3', '2020-09-25', 'https://www.bing.com/th?id=OHR.WatkinsGlen_ZH-CN1271268069_1920x1080.jpg', '0.34MB', '沃特金斯格伦州立公园的彩虹瀑布，纽约州北部芬格湖群 (© Kenneth Keifer/Alamy)', 'https://www.bing.com/search?q=%E6%B2%83%E7%89%B9%E9%87%91%E6%96%AF%E6%A0%BC%E4%BC%A6%E5%B7%9E%E7%AB%8B%E5%85%AC%E5%9B%AD&form=hpcapt&mkt=zh-cn', '2020-09-26 03:00:04');
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('4', '2020-09-26', 'https://www.bing.com/th?id=OHR.FraserRiver_ZH-CN1625992097_1920x1080.jpg', '0.34MB', '温哥华东部的弗雷泽河和金耳朵山脉，加拿大不列颠哥伦比亚省 (© LeonU/Getty Images)', 'https://www.bing.com/search?q=%E5%BC%97%E9%9B%B7%E6%B3%BD%E6%B2%B3&form=hpcapt&mkt=zh-cn', '2020-09-27 03:00:04');
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('5', '2020-09-27', 'https://www.bing.com/th?id=OHR.GreatBlueShark_ZH-CN1757082635_1920x1080.jpg', '0.12MB', '北大西洋亚速尔群岛附近的大青鲨 (© Nuno Sa/Minden Pictures)', 'https://www.bing.com/search?q=%E9%9D%92%E9%B2%A8&form=hpcapt&mkt=zh-cn', '2020-09-28 03:00:04');
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('6', '2020-09-28', 'https://www.bing.com/th?id=OHR.Lavaux_ZH-CN1891785892_1920x1080.jpg', '0.34MB', '日内瓦湖岸上陡峭的拉沃葡萄园梯田，瑞士 (© Yves Marcoux/plainpicture)', 'https://www.bing.com/search?q=%E6%8B%89%E6%B2%83%E8%91%A1%E8%90%84%E5%9B%AD&form=hpcapt&mkt=zh-cn', '2020-09-29 03:00:05');
INSERT INTO `wallpapers` (`id`, `date`, `url`, `size`, `copyright`, `copyrightlink`, `update_time`) VALUES ('7', '2020-09-29', 'https://www.bing.com/th?id=OHR.LaragangaMoth_ZH-CN2013788793_1920x1080.jpg', '0.34MB', '莫尔国家公园中的天蚕蛾，加纳拉拉班加 (© Robert Thompson/Minden Pictures)', 'https://www.bing.com/search?q=%E5%A4%A9%E8%9A%95%E8%9B%BE&form=hpcapt&mkt=zh-cn', '2020-09-30 03:00:05');
TRUNCATE TABLE `stock`;
INSERT INTO `stock` (`id`, `code`, `name`, `market`) VALUES ('1', '000001', '上证指数', '1');
INSERT INTO `stock` (`id`, `code`, `name`, `market`) VALUES ('2', '601360', '三六零', '1');
TRUNCATE TABLE `stock_belong`;
INSERT INTO `stock_belong` (`id`, `stock_id`, `user_id`, `push`, `push_threshold`, `is_valid`, `update_time`) VALUES ('1', '1', '1', '1', '[1000.0, 2000.0]', '0', '2020-10-14 19:28:52');
INSERT INTO `stock_belong` (`id`, `stock_id`, `user_id`, `push`, `push_threshold`, `is_valid`, `update_time`) VALUES ('2', '2', '1', '1', '[1000.0, 2000.0]', '0', '2020-10-14 19:28:52');
INSERT INTO `stock_belong` (`id`, `stock_id`, `user_id`, `push`, `push_threshold`, `is_valid`, `update_time`) VALUES ('3', '1', '0', '1', '[0.0, 0.0]', '1', '2020-10-14 19:28:52');
TRUNCATE TABLE `stock_price`;
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('1', '1', '3408.17', '-0.36', '2020-12-22 09:44:06');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('2', '1', '3408.53', '-0.35', '2020-12-22 09:45:06');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('3', '1', '3410.18', '-0.3', '2020-12-22 09:46:07');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('4', '1', '3410.53', '-0.29', '2020-12-22 09:47:05');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('5', '1', '3410.53', '-0.29', '2020-12-22 09:50:05');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('6', '2', '16.18', '-1.16', '2020-12-22 09:41:06');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('7', '2', '16.21', '-0.98', '2020-12-22 09:42:06');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('8', '2', '16.2', '-1.04', '2020-12-22 09:43:06');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('9', '2', '16.12', '-1.53', '2020-12-22 09:45:06');
INSERT INTO `stock_price` (`id`, `stock_id`, `price`, `range`, `update_time`) VALUES ('10', '2', '16.08', '-1.77', '2020-12-22 09:46:07');
TRUNCATE TABLE `fund`;
INSERT INTO `fund` (`id`, `code`, `name`) VALUES ('1', '005911', '广发双擎');
TRUNCATE TABLE `fund_price`;
INSERT INTO `fund_price` (`id`, `fund_id`, `price`, `range`, `update_time`) VALUES ('1', '1', '3.1172', '0.55', '2020-10-29 14:39:13');
INSERT INTO `fund_price` (`id`, `fund_id`, `price`, `range`, `update_time`) VALUES ('2', '1', '3.1251', '0', '2020-10-29 14:49:13');
INSERT INTO `fund_price` (`id`, `fund_id`, `price`, `range`, `update_time`) VALUES ('3', '1', '3.1172', '0.55', '2020-10-29 15:25:18');
INSERT INTO `fund_price` (`id`, `fund_id`, `price`, `range`, `update_time`) VALUES ('4', '1', '3.1253', '0.34', '2020-10-30 10:18:46');
INSERT INTO `fund_price` (`id`, `fund_id`, `price`, `range`, `update_time`) VALUES ('5', '1', '3.1211', '0.2', '2020-10-30 10:30:08');
TRUNCATE TABLE `fund_belong`;
INSERT INTO `fund_belong` (`id`, `fund_id`, `user_id`, `push`, `push_threshold`, `is_valid`, `update_time`) VALUES ('1', '1', '1', '1', '[]', '1', '2020-10-29 20:14:39');
TRUNCATE TABLE `notes`;
INSERT INTO `notes` (`id`, `name`, `token`, `content`, `user_id`, `is_valid`, `update_time`) VALUES ('1', '7.31', '2', '美好的一天！', '1', '1', '2020-08-01 14:38:23');
TRUNCATE TABLE `user`;
INSERT INTO `user` (`id`, `name`, `login_name`, `password`, `stable_salt`, `salt`, `salt_expire_time`, `role_id`, `email`, `wechat_key`, `is_valid`, `create_time`, `update_time`) VALUES (1, '管理员', 'admin', '71f11204b9cbf6ef09e83e43dda7399e', 'fndTb5mWFA6JYtdW1AKJvQSzZ3ERpVt0YupukTjI', 'SX2JQywwb13zhlt7uPPXh8Bne6V40JL2RwD3L6Wh', '2019-10-28 11:35:37', 1, 'my_email@my_email.cn', 'my_wechat_key', 1, '2019-08-21 16:46:21.981898', '2019-08-21 16:46:21.981898');
TRUNCATE TABLE `role`;
INSERT INTO `role` (`id`, `name`, `is_valid`, `update_time`) VALUES ('1', '管理员', '1', '2019-10-28 11:35:37');
TRUNCATE TABLE `widget`;
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('1', 'weather', '天气', '1', '8', '[\'add\', \'sort\', \'notify\']', '1800000', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('2', 'bookmarks', '书签', '1', '8', '[\'add\', \'sort\']', '0', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('3', 'app', 'AppStore监控', '1', '8', '[\'add\', \'sort\', \'notify\']', '1800000', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('4', 'gold', '黄金价格', '1', '8', '[\'setting\', \'notify\']', '1800000', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('5', 'notes', '便签', '1', '8', '[\'add\',\'revert\']', '180000', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('6', 'translator', '翻译', '1', '8', '[]', '0', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('7', 'wallpapers', '必应壁纸', '1', '8', '[]', '0', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('8', 'stock', '股票', '1', '8', '[\'add\', \'sort\', \'notify\']', '1800000', '2019-10-28 11:35:37');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('9', 'fund', '基金', '1', '8', '[\'add\', \'sort\', \'notify\']', '1800000', '2020-10-29 14:49:04');
INSERT INTO `widget` (`id`, `name`, `name_zh`, `is_valid`, `span`, `buttons`, `auto_update`, `update_time`) VALUES ('10', 'news', '新闻', '1', '24', '[]', '1800000', '2020-11-02 17:12:34');
TRUNCATE TABLE `widget_suite`;
INSERT INTO `widget_suite` (`id`, `name`, `user_id`, `order`, `is_valid`, `detail`, `update_time`) VALUES ('1', '基本组件', '0', '1', '1', '[1,2,7,4,8,10]', '2019-10-28 11:35:37');
INSERT INTO `widget_suite` (`id`, `name`, `user_id`, `order`, `is_valid`, `detail`, `update_time`) VALUES ('2', '常用', '1', '0', '1', '[1, 2, 6]', '2020-12-10 18:07:06');
INSERT INTO `widget_suite` (`id`, `name`, `user_id`, `order`, `is_valid`, `detail`, `update_time`) VALUES ('3', '金融', '1', '1', '1', '[4, 8, 9]', '2020-12-10 18:07:06');
INSERT INTO `widget_suite` (`id`, `name`, `user_id`, `order`, `is_valid`, `detail`, `update_time`) VALUES ('4', '新闻', '1', '2', '1', '[10]', '2020-12-10 18:07:06');
INSERT INTO `widget_suite` (`id`, `name`, `user_id`, `order`, `is_valid`, `detail`, `update_time`) VALUES ('5', '其他', '1', '3', '1', '[7, 3, 5]', '2020-12-10 18:07:06');
TRUNCATE TABLE `script_sub_system`;
INSERT INTO `script_sub_system` (`id`, `name`, `user_id`, `is_valid`, `update_time`) VALUES ('1', '定时任务', '1', '1', '2020-06-17 11:44:00');
INSERT INTO `script_sub_system` (`id`, `name`, `user_id`, `is_valid`, `update_time`) VALUES ('2', '小工具', '1', '1', '2020-07-21 23:30:49');
TRUNCATE TABLE `script`;
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('1', '推送', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.push.push_function', '1', '1', '1', '1', '管理员', '2020-06-17 16:27:03');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('2', 'App价格获取', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.app_price_monitor.app_price_spider', '1', '1', '1', '1', '管理员', '2020-06-17 16:28:25');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('3', '黄金价格获取', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.gold_price_monitor.gold_price_spider', '1', '1', '1', '1', '管理员', '2020-07-01 16:58:23');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('4', '生成短链接', '2', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.short_url.function %原始内容% %类型%', '2', '1', '1', '1', '管理员', '2020-08-17 18:03:27');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('5', '必应壁纸每日爬取', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.wallpapers.function', '2', '1', '1', '1', '管理员', '2020-09-24 15:10:34');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('6', '异常天气推送', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.weather.weather_function', '1', '1', '1', '1', '管理员', '2020-09-15 19:47:40');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('7', '股票价格获取', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.stock.stock_funtion', '1', '1', '1', '1', '管理员', '2020-10-12 16:37:41');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('8', '基金价格获取', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.fund.fund_function', '1', '1', '1', '1', '管理员', '2020-10-29 14:43:16');
INSERT INTO `script` (`id`, `name`, `sub_system_id`, `start_folder`, `start_script`, `type`, `runs`, `is_valid`, `version`, `user`, `update_time`) VALUES ('9', '新闻获取', '1', '/home/pi/Documents/Github/PersonalHomepage/backend', 'python3 -m app.news.get_news', '1', '1', '1', '1', '管理员', '2020-11-04 15:34:21');
TRUNCATE TABLE `script_detail`;
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('1', '1', 'input', '无需参数', '直接运行', '', '', '0', '1', '0', '', '', '', '0', '1', '1', '1', '管理员', '2020-06-17 16:27:03');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('2', '2', 'input', '无需参数', '直接运行', '', '', '0', '1', '0', '', '', '', '0', '1', '1', '1', '管理员', '2020-06-17 16:28:25');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('3', '3', 'input', '无需参数', '直接运行', '', '', '0', '1', '0', '', '', '', '0', '1', '1', '1', '管理员', '2020-07-01 16:58:23');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('4', '4', 'input', '无需参数', '直接运行', '', '{}', '0', '1', '0', '', '', '', '0', '1', '1', '10', '管理员', '2020-09-24 15:10:34');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('5', '5', 'input', '原始内容', 'https://baidu.com', '', '[]', '0', '0', '0', '', '', '', '1', '1', '1', '11', '管理员', '2020-10-08 21:30:02');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('6', '5', 'select', '类型', '1', '', '[{\'label\': \'URL\', \'value\': \'1\'}]', '0', '0', '0', '', '', '当前仅支持缩短URL', '1', '1', '1', '11', '管理员', '2020-10-08 21:30:02');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('7', '6', 'input', '无需参数', '直接运行', '', '[]', '0', '1', '0', 'test', '/usr/bin/python3 push_function.py', '', '1', '1', '1', '2', '管理员', '2020-09-15 19:47:40');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('8', '7', 'input', '无需参数', '直接运行', '', '[]', '0', '1', '0', '', '', '', '0', '1', '1', '1', '管理员', '2020-10-12 16:37:41');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('9', '9', 'input', '无需参数', '直接运行', '', '[]', '0', '1', '0', '', '', '', '0', '1', '1', '1', '管理员', '2020-11-04 15:34:21');
INSERT INTO `script_detail` (`id`, `script_id`, `type`, `label`, `value`, `place_holder`, `options`, `createable`, `disabled`, `extra_button`, `extra_button_label`, `extra_button_script`, `remark`, `is_important`, `is_valid`, `visible`, `version`, `user`, `update_time`) VALUES ('10', '8', 'input', '无需参数', '直接运行', '', '[]', '0', '1', '0', '', '', '', '0', '1', '1', '1', '管理员', '2020-10-29 14:43:17');
TRUNCATE TABLE `script_schedule`;
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('1', '1', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.push.push_function 直接运行', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '11', '1', '1', '1', '5', '5', '0', '2020-06-20 00:00:00', '2020-08-04 17:43:43');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('2', '2', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.app_price_monitor.app_price_spider 直接运行', '{\'无需参数\': \'直接运行\'}', '1', '1', '1', '1', '180', '3', '1', '2020-06-20 00:15:00', '2020-08-04 14:46:27');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('3', '3', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.gold_price_monitor.gold_price_spider 直接运行', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '1', '1', '1', '1', '120', '2', '1', '2020-06-20 00:15:00', '2020-08-17 18:18:30');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('4', '4', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.wallpapers.function', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '10', '1', '1', '1', '1440', '1', '2', '2020-06-20 03:00:00', '2020-09-25 18:57:27');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('5', '6', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.weather.weather_function 直接运行', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '2', '1', '1', '1', '1440', '1', '2', '2020-06-20 17:00:00', '2020-09-15 19:48:24');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('6', '7', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.stock.stock_funtion 直接运行', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '1', '1', '1', '1', '15', '15', '0', '2020-06-20 00:15:00', '2020-10-12 16:38:24');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('7', '8', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.fund.fund_function 直接运行', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '1', '1', '1', '1', '15', '15', '0', '2020-06-20 23:30:00', '2020-10-30 10:18:31');
INSERT INTO `script_schedule` (`id`, `script_id`, `command`, `detail`, `version`, `user_id`, `is_valid`, `is_automatic`, `interval`, `interval_raw`, `interval_unit`, `trigger_time`, `update_time`) VALUES ('8', '9', 'cd /home/pi/Documents/Github/PersonalHomepage/backend && python3 app.news.get_news 直接运行', '[{\'type\': \'input\', \'label\': \'无需参数\', \'value\': \'直接运行\'}]', '1', '1', '1', '1', '60', '1', '1', '2020-06-20 00:00:00', '2020-11-04 16:29:42');
TRUNCATE TABLE `weather_location`;
INSERT INTO `weather_location` (`id`, `location`, `user_id`, `is_valid`, `update_time`) VALUES ('1', '长春', '1', '1', '2019-10-28 11:35:37');
TRUNCATE TABLE `app`;
INSERT INTO `app` (`id`, `name`, `url`, `user_id`, `expect_price`, `order`, `is_valid`, `update_time`) VALUES ('1', 'gorogoa', 'https://apps.apple.com/cn/app/gorogoa/id1269225754?ign-mpt=uo%3D4', '1', '0', '1', '1', '2020-07-22 15:20:46');
TRUNCATE TABLE `app_price`;
INSERT INTO `app_price` (`id`, `app_id`, `price`, `update_time`) VALUES ('1', '1', '3.0', '2020-12-22 16:36:04');
TRUNCATE TABLE `gold_price`;
INSERT INTO `gold_price` (`id`, `price`, `update_time`) VALUES ('1', '400.7', '2020-07-01 16:51:51');
INSERT INTO `gold_price` (`id`, `price`, `update_time`) VALUES ('2', '400.7', '2020-07-01 16:58:29');
INSERT INTO `gold_price` (`id`, `price`, `update_time`) VALUES ('3', '400.7', '2020-07-01 19:00:05');
INSERT INTO `gold_price` (`id`, `price`, `update_time`) VALUES ('4', '399.37', '2020-07-01 21:00:05');
INSERT INTO `gold_price` (`id`, `price`, `update_time`) VALUES ('5', '396.6', '2020-07-01 23:00:06');
TRUNCATE TABLE `weather_notify`;
INSERT INTO `weather_notify` (`id`, `location`, `user_id`, `notify_type`, `notify_method`, `is_valid`, `update_time`) VALUES ('1', '北京', '1', '[\'rain\', \'air\', \'temperature\']', '1', '1', '2020-09-17 11:18:24');
INSERT INTO `weather_notify` (`id`, `location`, `user_id`, `notify_type`, `notify_method`, `is_valid`, `update_time`) VALUES ('2', '深圳', '1', '[\'rain\', \'air\', \'temperature\']', '1', '1', '2020-09-17 11:18:24');
