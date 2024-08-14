#!/bin/bash
set -e

# Загрузить переменные окружения из .env файла
export $(grep -v '^#' .env | xargs)

echo "POSTGRES_USER: $POSTGRES_USER"
echo "POSTGRES_DB: $POSTGRES_DB"

docker exec -i containers_db_1 psql -U "$POSTGRES_USER" -d "$POSTGRES_DB" <<-EOSQL
    DROP TABLE IF EXISTS user_regions;
    CREATE TABLE user_regions (
        user_id BIGINT PRIMARY KEY,
        region VARCHAR(255) NOT NULL
    );

    DROP TABLE IF EXISTS vk_groups;
    CREATE TABLE vk_groups (
        id SERIAL PRIMARY KEY,
        group_id BIGINT NOT NULL,
        region VARCHAR(255),
        area VARCHAR(255),
        last_post_date TIMESTAMP,
        group_link TEXT,
        group_name VARCHAR(255),
        include_reposts BOOLEAN
    );

    DROP TABLE IF EXISTS vk_posts;
    CREATE TABLE vk_posts (
        id SERIAL PRIMARY KEY,
        post_id BIGINT NOT NULL,
        group_id BIGINT NOT NULL,
        date TIMESTAMP NOT NULL,
        post_link TEXT NOT NULL,
        features JSONB,
        region VARCHAR(255),
        area VARCHAR(255),
        district VARCHAR(255)
    );

    -- Индексы для vk_groups
    CREATE INDEX idx_vk_groups_group_id ON vk_groups(group_id);
    CREATE INDEX idx_vk_groups_region ON vk_groups(region);
    CREATE INDEX idx_vk_groups_area ON vk_groups(area);
    CREATE INDEX idx_vk_groups_city ON vk_groups(city);
    CREATE INDEX idx_vk_groups_group_name ON vk_groups(group_name);
    CREATE INDEX idx_vk_groups_group_link ON vk_groups(group_link);
    CREATE INDEX idx_vk_groups_include_reposts ON vk_groups(include_reposts);

    -- Индексы для vk_posts
    CREATE INDEX idx_vk_posts_post_id ON vk_posts(post_id);
    CREATE INDEX idx_vk_posts_group_id ON vk_posts(group_id);
    CREATE INDEX idx_vk_posts_date ON vk_posts(date);
    CREATE INDEX idx_vk_posts_post_link ON vk_posts(post_link);
    CREATE INDEX idx_vk_posts_features ON vk_posts USING gin(features);
    CREATE INDEX idx_vk_posts_region ON vk_posts(region);
    CREATE INDEX idx_vk_posts_area ON vk_posts(area);
    CREATE INDEX idx_vk_posts_district ON vk_posts(district);

EOSQL


