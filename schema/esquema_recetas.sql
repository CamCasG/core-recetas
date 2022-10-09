-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema esquema_recetas
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `esquema_recetas` ;

-- -----------------------------------------------------
-- Schema esquema_recetas
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `esquema_recetas` DEFAULT CHARACTER SET utf8 ;
USE `esquema_recetas` ;

-- -----------------------------------------------------
-- Table `esquema_recetas`.`usuarios`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_recetas`.`usuarios` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `apellido` VARCHAR(45) NULL,
  `email` VARCHAR(45) NULL,
  `password` VARCHAR(200) NULL,
  `nacimiento` DATE NULL,
  `genero` VARCHAR(45) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_recetas`.`recetas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_recetas`.`recetas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre` VARCHAR(45) NULL,
  `descripcion` VARCHAR(255) NULL,
  `instrucciones` TEXT NULL,
  `fecha` DATE NULL,
  `under30` VARCHAR(45) NULL,
  `usuario_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_recetas_usuarios_idx` (`usuario_id` ASC) VISIBLE,
  CONSTRAINT `fk_recetas_usuarios`
    FOREIGN KEY (`usuario_id`)
    REFERENCES `esquema_recetas`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `esquema_recetas`.`recetas_favoritas`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `esquema_recetas`.`recetas_favoritas` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `nombre_id` INT NOT NULL,
  `receta_id` INT NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_recetas_favoritas_usuarios1_idx` (`nombre_id` ASC) VISIBLE,
  INDEX `fk_recetas_favoritas_recetas1_idx` (`receta_id` ASC) VISIBLE,
  CONSTRAINT `fk_recetas_favoritas_usuarios1`
    FOREIGN KEY (`nombre_id`)
    REFERENCES `esquema_recetas`.`usuarios` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_recetas_favoritas_recetas1`
    FOREIGN KEY (`receta_id`)
    REFERENCES `esquema_recetas`.`recetas` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
