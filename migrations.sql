/*

    DRONES

*/
CREATE TABLE "drones" (
    "id" INTEGER PRIMARY KEY,
    "serial_number" VARCHAR(100) UNIQUE,
    "model" VARCHAR(20),
    "weight" INTEGER,
    "battery_capacity" INTEGER,
    "state" VARCHAR(15)
);
INSERT INTO "drones" VALUES (NULL, "QWOIEJO1202115", "Lightweight", "250", "80", "IDLE");
