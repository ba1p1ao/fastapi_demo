from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `clas` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '班级名称'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `student` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '学生id',
    `name` VARCHAR(32) NOT NULL COMMENT '姓名',
    `pwd` VARCHAR(32) NOT NULL COMMENT '密码',
    `sno` INT NOT NULL COMMENT '学号',
    `clas_id` INT NOT NULL,
    CONSTRAINT `fk_student_clas_4be9b492` FOREIGN KEY (`clas_id`) REFERENCES `clas` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `teacher` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT COMMENT '教师id',
    `name` VARCHAR(32) NOT NULL COMMENT '姓名',
    `pwd` VARCHAR(32) NOT NULL COMMENT '密码',
    `tno` INT NOT NULL COMMENT '教师编号'
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `course` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(255) NOT NULL COMMENT '课程名称',
    `teacher_id` INT NOT NULL,
    CONSTRAINT `fk_course_teacher_2de38fe7` FOREIGN KEY (`teacher_id`) REFERENCES `teacher` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;
CREATE TABLE IF NOT EXISTS `student_course` (
    `student_id` INT NOT NULL,
    `course_id` INT NOT NULL,
    FOREIGN KEY (`student_id`) REFERENCES `student` (`id`) ON DELETE CASCADE,
    FOREIGN KEY (`course_id`) REFERENCES `course` (`id`) ON DELETE CASCADE,
    UNIQUE KEY `uidx_student_cou_student_0d222b` (`student_id`, `course_id`)
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztWV1P2zAU/SsoT0xiU79Cy95KNzTGAAnYNAlQ5CZOGjW1i+MMKpT/Pn8kdZImWdpCCV"
    "NeSrm+du49vr7n1HnWZtiCnv9p5AFf+7z3rCEwg+xLyn6wp4H5XFm5gYKxJxzN2GPsUwJM"
    "ymw28HzITBb0TeLOqYsRs6LA87gRm8zRRY4yBch9CKBBsQPpBBI2cHvPzC6y4BP043/nU8"
    "N2oWelwnQt/mxhN+hiLmyniJ4IR/60sWFiL5gh5Txf0AlGS28XUW51IIIEUMiXpyTg4fPo"
    "oizjjGSkykWGmJhjQRsEHk2kWxEDEyOOH4tG7oPDn/Kx0+71e4PuYW/AXEQkS0s/lOmp3O"
    "VEgcDFjRaKcUCB9BAwKtzE3xXkRhNA8qGL/TPgsZCz4MVQlaEXGxR8qmRK8dPugn4XWuwT"
    "gv5doPda/PuR3dKqoToDT4YHkUMnHEpdL8Hw1/Bq9G14tc+8PvDVMStuWfEX0VBHjoUhr0"
    "57msCZG8bAnD4CYhmpEbUDPg0syONa2YXjaObJ2RX0gMh8FfnofF7LVXa6CZWLOIyrKLZG"
    "50QAhju4CLHVoVlnlrUABBwRNX82f1LcsXBAfJjby+RIeTdTPk0/a/rZDvrZYGxD1sNAa1"
    "ybfnaQKEgKgclq2FirMNOT/l2g9WhXL1GjK1SwguQqjCeYQNdBZ3Ah0DxlQQFk5pVn1Mhu"
    "1Er1Q7Go6TMzAY/LlpepEZYkSw1SeWyH16Phl69aWMyjWzJIFRo+B2hxg/lnxW3Zgotfu/"
    "2WbIoI3shQZSIVwjUItJYekiElXpgItKdwkYAy2tHlXkSjcl40SCcEB84kOUsxb24tMLuR"
    "5bSwVAjEOeQogUR6xVLATzg1WqASl+njw0PGX3rbluE0umBzXaAfWV2pCDbRAt1OBSnQ7R"
    "QqAT6UFgLzx5xyLAYycq8BjmOT1+Sg1a4Hjj7CaxzryPuNJdTyaOtdu7/Lg61g49dM64nQ"
    "xIxGgaau6raUn/GdYP3wq6o9E6XxZsIzqaO2053qXuO9y06VSVZ1pmR6WnamhGVWdaY16f"
    "ayU0BYrjvjX2c5ujPxw61YdyZ+Jza6sxo5Her6ESMn2Bo0urPRnTXBsWa6k66lO2lddKc6"
    "2gxMu71zDbrRu51Cbl/n1c7mtP6fvtkZQuKakzxejUZKaRUon4ZVX7AUXptJ/0DiR+ekKg"
    "ckprwxD1RH8fXf5PCjsQaIkfv7BLDdalUAkHkVAijGMlcQGNHoQjgN4vfry4uCOwg1JQPk"
    "T8QSvLVckx7sea5P7+sJawmKPGse9Mz3H7wkePvnw99ZXEc/Lo8FCtinDhGriAWO16PYl6"
    "eX8C9HNNxg"
)
