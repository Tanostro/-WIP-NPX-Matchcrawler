CREATE TABLE `%dbname%` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `tag` varchar(20) COLLATE utf8_bin NOT NULL,
  `region` varchar(4) COLLATE utf8_bin NOT NULL,
  `matchId` bigint(12) NOT NULL,
  `summonerId` varchar(63) COLLATE utf8_bin NOT NULL,
  `timestmp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `matchdata` json NOT NULL,
  UNIQUE KEY `id` (`id`),
  FULLTEXT KEY `tag` (`tag`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
