CREATE TABLE IF NOT EXISTS images (
    id SERIAL PRIMARY KEY,
    image_name VARCHAR(255) NOT NULL,
    bucket VARCHAR(255) NOT NULL,
    height INTEGER NOT NULL,
    width INTEGER NOT NULL,
    size_bytes BIGINT NOT NULL,
    format VARCHAR(50) NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    s3_link VARCHAR(512) NOT NULL,
    UNIQUE(bucket, image_name)
);

CREATE INDEX idx_images_bucket ON images(bucket);
CREATE INDEX idx_images_upload_date ON images(upload_date);
