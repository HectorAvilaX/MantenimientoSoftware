create database bdalmacen;
use bdalmacen;

create table categoria 
(
	idCategoria		integer not null auto_increment primary key,
	nombre			text not null
);

create table marca
(
	idMarca		integer not null auto_increment primary key,
    nombre		text not null
);

create table producto
(
	idProducto	integer not null auto_increment primary key,
    nombre		text not null,
    precio		real not null,
    descripcion	text not null,
    idMarca		integer,
    idCategoria integer,
    foreign key(idMarca) references marca(idMarca),
    foreign key(idCategoria) references categoria(idCategoria)
);

create table vale_cabecera
(
	idVale_cabecera		integer not null auto_increment primary key,
    fecha				date not null,
    tipo				int not null,
	nombre				text not null,
    observacion			text not null,
    total				real not null
);

create table vale_detalle
(
	idVale_detalle		integer not null auto_increment primary key,
    cantidad			int not null,
    unidadMedida		text not null,
    idVale_cabecera		integer,
    foreign key(idVale_cabecera) references vale_cabecera(idVale_cabecera)
);