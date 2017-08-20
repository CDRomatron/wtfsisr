DROP TABLE if EXISTS games;
DROP TABLE if EXISTS consoles;

CREATE TABLE games (
  name text,
  consoles text,
  category text,
  logourl text,
  leaderboardurl text,
  exactParticipants integer,
  uptoParticipants integer
);

CREATE TABLE consoles (
  name text,
  id text
);
