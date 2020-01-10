CREATE TABLE `%dbname%` (
  `idKey` varchar(15) COLLATE utf8_bin NOT NULL,
  `championId` int(11) NOT NULL,
  `tier` varchar(10) COLLATE utf8_bin NOT NULL,
  `ban` bigint(20) NOT NULL,
  PRIMARY KEY (`idKey`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;
