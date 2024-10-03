# fast-coupon

* Fast Coupon is a backend created using fastAPI and Python

### Solution

* In order to comply with the requirements were created three endpoint using fast api, Python and MYSQL

### Considerations

* We have two types of coupons but ```coupon_details``` table allows to have other types of coupons but it's necessary create the logic in the backend service, for example we can create a coupon for a specific category
* A Gift Card is created when user pay any order
* When apply coupon is called the system checks if the coupon is valid, the coupon book have coupons to redeem, if not a error response is returned
* A Gift Card can only be redeemed by the owner user
* We have a table for coupon settings, for example I put MAX_USER_COUPONS_PER_USER, and the discount percentage for gift cards
* In this solution I don't create a transaction_purchase table, but I use the coupon_redeem instead
* It's possible create new coupon types, new products and products catgories but we need create the CRUD endpoints but this is not part of the challenge
* The tables need date fields in order to know when a field was created, deleted, updated but this is not part of the challenge
* It's possible to improve the solution by separating into individual files
* The backend use .env in order to don't expose the sensible information

MYSQL Dump

```
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
);```
