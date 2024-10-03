use fastcoupon;

CREATE TABLE coupon_type(
	id VARCHAR(256) DEFAULT(uuid()) NOT NULL,
    description VARCHAR(256),
    type VARCHAR(256),
    PRIMARY KEY (id)
);

CREATE TABLE coupon (
	id VARCHAR(256) DEFAULT(uuid()) NOT NULL,
	code VARCHAR(256) NOT NULL,
    id_type VARCHAR(256) NOT NULL,
	PRIMARY KEY (id),
    FOREIGN KEY (id_type) REFERENCES coupon_type(id)
);

CREATE TABLE product_category(
	id VARCHAR(256) DEFAULT(uuid()) NOT NULL,
    description VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE product (
	id VARCHAR(256) DEFAULT(uuid()) NOT NULL,
    description VARCHAR(256) NOT NULL,
    price DOUBLE(10,2) NOT NULL,
    id_category VARCHAR(256) NOT NULL,
    image_url VARCHAR(256) DEFAULT('404') NOT NULL,
    PRIMARY KEY (id),
	FOREIGN KEY (id_category) REFERENCES product_category(id)
);

CREATE TABLE user(
	id VARCHAR(256) DEFAULT(uuid()) NOT NULL,
    email VARCHAR(256) NOT NULL,
    password VARCHAR(256) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE coupon_reedem(
	id_operation VARCHAR(256) DEFAULT(uuid()) NOT NULL,
    id_user VARCHAR(256) NOT NULL,
    id_coupon  VARCHAR(256) NOT NULL,
    PRIMARY KEY (id_operation),
    FOREIGN KEY (id_user) REFERENCES user(id),
    FOREIGN KEY (id_coupon) REFERENCES coupon(id)
);

CREATE TABLE coupon_settings(
	id VARCHAR(256) DEFAULT(uuid()) NOT NULL,
	field VARCHAR(256) UNIQUE NOT NULL,
    value VARCHAR(256) NOT NULL,
	PRIMARY KEY (id)
);

CREATE TABLE coupon_details(
	id_coupon VARCHAR(256) NOT NULL,
    percentage int,
    value int,
    id_category_to_apply VARCHAR(256),
    id_user VARCHAR(256),
    id_product VARCHAR(256),
    quantity int,
    date_expiration DATE,
    min_price_to_apply DOUBLE(10,2),
    FOREIGN KEY (id_product) REFERENCES product(id),
    FOREIGN KEY (id_coupon) REFERENCES coupon(id),
    FOREIGN KEY (id_user) REFERENCES user(id),
    FOREIGN KEY (id_category_to_apply) REFERENCES product_category(id)
);


INSERT INTO `fastcoupon`.`product_category`
(
`description`)
VALUES
("Electrónica");

INSERT INTO `fastcoupon`.`product_category`
(
`description`)
VALUES
("Muebles");


INSERT INTO `fastcoupon`.`product`
(
`description`,
`price`,
`id_category`,
`image_url`)
VALUES
("iPhone 16 Pro Max",
20000.50,
"f9cf67ee-8145-11ef-918b-183eeff5001b",
"https://resources.sears.com.mx/medios-plazavip/fotos/productos_sears1/original/4504865.jpg");


INSERT INTO `fastcoupon`.`product`
(
`description`,
`price`,
`id_category`,
`image_url`)
VALUES
("Sala Modular",
15000.25,
"14228dc4-8146-11ef-918b-183eeff5001b",
"https://www.kessamuebles.com/cdn/shop/products/catania_2-2E_chocolate_636x.png?v=1631556954");

INSERT INTO `fastcoupon`.`coupon_type`
(`description`,
`type`)
VALUES
("Cupon autogenerado para el usuario",
"GIFT_CARD");

## ceb7fac0-8146-11ef-918b-183eeff5001b

INSERT INTO `fastcoupon`.`coupon_type`
(`description`,
`type`)
VALUES
("Cupon genérico que otorga un porcentage al total sin minimo de compra",
"COUPON_PERCENTAGE");

## f92e7ffe-8146-11ef-918b-183eeff5001b


INSERT INTO `fastcoupon`.`coupon`
(`code`,
`id_type`)
VALUES
("wildfork",
"f92e7ffe-8146-11ef-918b-183eeff5001b");

## 3c725e52-8147-11ef-918b-183eeff5001b

INSERT INTO `fastcoupon`.`coupon`
(`code`,
`id_type`)
VALUES
("wildfork20",
"f92e7ffe-8146-11ef-918b-183eeff5001b");

## 465bef3c-8147-11ef-918b-183eeff5001b

INSERT INTO `fastcoupon`.`coupon_details`
(`id_coupon`,
`percentage`,
`quantity`)
VALUES
("3c725e52-8147-11ef-918b-183eeff5001b",
10,
10);

INSERT INTO `fastcoupon`.`coupon_details`
(`id_coupon`,
`percentage`,
`quantity`)
VALUES
("465bef3c-8147-11ef-918b-183eeff5001b",
20,
5);

INSERT INTO `fastcoupon`.`coupon_settings`
(
`field`,
`value`)
VALUES
(
"MAX_PER_USER",
"1");

INSERT INTO `fastcoupon`.`user`
(
`email`,
`password`)
VALUES
(
"oscarmiguelf@gmail.com",
"password");

## a8af392c-8148-11ef-918b-183eeff5001b


SELECT count(*) AS total FROM coupon_reedem where id_coupon = "3c725e52-8147-11ef-918b-183eeff5001b"


