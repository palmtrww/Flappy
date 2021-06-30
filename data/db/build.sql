/* Builds the database tables for usage */

CREATE TABLE IF NOT EXISTS Guilds(
    GuildID INTEGER NOT NULL,
    Prefix TEXT DEFAULT "f!"
)