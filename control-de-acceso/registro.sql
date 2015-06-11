use registro;

create table if not exists alumnos
	(
		nControl int(8) zerofill not null,
		nombre varchar(40) not null,
		pApellido varchar(30),
		mApellido varchar(30),
		carrera varchar(50) not null,

		primary key (nControl)
	);
create table if not exists entrada
	(
		id_entrada int(7) auto_increment not null,
		nControl int(8) zerofill not null,
		nMaquina int(3) not null,
		fentrada date not null,
		hentrada time not null,

		foreign key (nControl) references alumnos(nControl),
		primary key (id_entrada)
	);

create table if not exists salida
	(
		id_entrada int not null,
		nControl int(8) zerofill not null,
		fSalida date not null,
		hSalida time not null,

		foreign key (id_entrada) references entrada(id_entrada),
		foreign key (nControl) references alumnos(nControl),
		primary key(id_entrada)
	);
