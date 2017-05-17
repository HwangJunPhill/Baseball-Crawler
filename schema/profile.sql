CREATE TABLE `profile` (
	`No` INT(11) NOT NULL AUTO_INCREMENT,
	`Name` VARCHAR(50) NULL DEFAULT NULL,
	`Number` VARCHAR(50) NOT NULL DEFAULT '0',
	`Debut` VARCHAR(50) NULL DEFAULT NULL,
	`Born` VARCHAR(50) NULL DEFAULT NULL,
	`Position` VARCHAR(50) NULL DEFAULT NULL,
	`Body` VARCHAR(50) NULL DEFAULT NULL,
	PRIMARY KEY (`No`)
)
COMMENT='나성범의 프로필'
COLLATE='utf8_general_ci'
ENGINE=InnoDB
AUTO_INCREMENT=6
;
