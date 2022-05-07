create table team
(
    team_id integer generated always as identity
        primary key,
    team    text not null
        unique
);

alter table team
    owner to nica_timingv1;

create unique index team_pkey
    on team (team_id);

create unique index team_team_key
    on team (team);

create table racer
(
    nica_id    integer not null
        primary key,
    first_name text,
    last_name  text,
    team_id    integer
);

alter table racer
    owner to nica_timingv1;

create unique index racer_pkey
    on racer (nica_id);

create table category
(
    category_id integer generated always as identity
        primary key,
    category    text not null
        unique,
    lap_num     integer
);

alter table category
    owner to nica_timingv1;

create unique index category_pkey
    on category (category_id);

create unique index category_category_key
    on category (category);

create table race
(
    race_id        integer generated always as identity
        primary key,
    race_result_id integer not null
        unique,
    race_name      text    not null
);

alter table race
    owner to nica_timingv1;

create unique index race_pkey
    on race (race_id);

create unique index race_race_result_id_key
    on race (race_result_id);

create table racer_id
(
    race_id     integer not null,
    bib_id      integer not null,
    nica_id     integer not null,
    category_id integer not null
);

alter table racer_id
    owner to nica_timingv1;

create table racer_info
(
    bib_id     integer                  not null,
    race_id    integer                  not null,
    start_race boolean default false    not null,
    timestamp  timestamp with time zone not null,
    lap1       time,
    lap2       time,
    lap3       time,
    lap4       time,
    lap5       time,
    primary key (bib_id, race_id)
);

alter table racer_info
    owner to nica_timingv1;

create unique index racer_info_pkey
    on racer_info (bib_id, race_id);

