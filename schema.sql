DROP TABLE if EXISTS games;

CREATE TABLE games (
  name text,
  consoles text,
  category text,
  logourl text,
  leaderboardurl text,
  exactParticipants integer,
  uptoParticipants integer
);
