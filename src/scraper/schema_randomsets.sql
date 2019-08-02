CREATE DATABASE showdown_db;

USE showdown_db;

CREATE TABLE  Randomsets(
	pokemon VARCHAR(30) NOT NULL,
	battle_type VARCHAR(10) NOT NULL,
	move VARCHAR(30) NOT NULL,
	CONSTRAINT pokemon_battleType_move PRIMARY KEY (pokemon, battle_type, move)
);
