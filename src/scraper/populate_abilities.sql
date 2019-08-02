INSERT INTO Abilities (id, name, weather, modify_stat, multiplier, stat, value, target, type) VALUES
('deltastream','Delta Stream','Wind',null,null,null,null,null,'WeatherAbility'),
('desolateland','Desolate Land','desolateland',null,null,null,null,null,'WeatherAbility'),
('hugepower','Huge Power',null,'atk',2,null,null,'self','BuffUserAbility'),
('primordialsea','PrimordialSea','primordialsea',null,null,null,null,null,'WeatherAbility'),
('purepower','Pure Power',null,'atk',2,null,null,null,'BuffUserAbility'),
('drizzle','Drizzle','raindance',null,null,null,null,null,'WeatherAbility'),
('drought','Drought','sunnyday',null,null,null,null,null,'WeatherAbility'),
('intimidate','Intimidate',null,null,null,'atk',-1,'enemy','DebuffEnemyAbility');
