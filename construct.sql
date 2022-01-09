drop table if exists wardrobe_user;
drop table if exists invites;
drop table if exists wardrobe_look;
drop table if exists look_clothes;
drop table if exists look;
drop table if exists clothes;
drop table if exists wardrobe;
drop table if exists user;
drop table if exists image;
drop table if exists api_keys;

PRAGMA foreign_keys = ON;

CREATE TABLE image (
    image_id INTEGER PRIMARY KEY AUTOINCREMENT,
    data BLOB
);

CREATE TABLE user (
    user_login VARCHAR(100) PRIMARY KEY NOT NULL,
    user_name VARCHAR(100),
    password VARCHAR(100),
    image_id INTEGER,
    FOREIGN KEY (image_id) REFERENCES image(image_id)
);

CREATE TABLE wardrobe (
    wardrobe_id INTEGER PRIMARY KEY,
    wardrobe_description varchar(500),
    wardrobe_name varchar(100) NOT NULL,
    wardrobe_image_id INT,
    wardrobe_owner VARCHAR(100) NOT NULL,
    FOREIGN KEY (wardrobe_owner) REFERENCES user(user_login)
);

CREATE TABLE look (
    look_id INTEGER PRIMARY KEY,
    look_image_id INTEGER,
    look_name varchar(100),
    FOREIGN KEY (look_image_id) REFERENCES image(image_id)
);

CREATE TABLE clothes (
    clothes_id INTEGER PRIMARY KEY NOT NULL,
    clothes_name varchar(100),
    type varchar(100),
    image_id INTEGER,
    owner_login TEXT NOT NULL,
    FOREIGN KEY (image_id) REFERENCES image(image_id),
    FOREIGN KEY (owner_login) REFERENCES user(user_login)
);

create table wardrobe_user (
    wardrobe_id INTEGER,
    user_login VARCHAR(100),
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobe(wardrobe_id),
    FOREIGN KEY (user_login) REFERENCES user(user_login)
);

create table wardrobe_look (
    wardrobe_id INTEGER,
    look_id INTEGER,
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobe(wardrobe_id),
    FOREIGN KEY (look_id) REFERENCES look(look_id)
);

create table look_clothes (
    look_id INTEGER,
    clothes_id INTEGER,
    FOREIGN KEY (clothes_id) REFERENCES clothes(clothes_id),
    FOREIGN KEY (look_id) REFERENCES look(look_id)
);

CREATE TABLE api_keys (
    api_key TEXT
);

create table invites (
    invite_id INTEGER PRIMARY KEY,
    login_that_invites VARCHAR(100) NOT NULL,
    login_whom_invites VARCHAR(100) NOT NULL,
    wardrobe_id INTEGER NOT NULL,
    FOREIGN KEY (login_that_invites) REFERENCES user(user_login),
    FOREIGN KEY (login_whom_invites) REFERENCES user(user_login),
    FOREIGN KEY (wardrobe_id) REFERENCES wardrobe(wardrobe_id),
    UNIQUE(login_that_invites, login_whom_invites, wardrobe_id)
);

