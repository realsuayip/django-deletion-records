# ruff: noqa: E501, RUF012
from django.db import migrations


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(
            """
            CREATE TABLE django_deletion_record
            (
                id         bigint                   NOT NULL PRIMARY KEY GENERATED BY DEFAULT AS IDENTITY,
                object_id  bigint                   NOT NULL,
                table_name varchar(128)             NOT NULL,
                data       jsonb                    NOT NULL,
                deleted_at timestamp with time zone NOT NULL DEFAULT current_timestamp
            );
            """,
            reverse_sql="DROP TABLE IF EXISTS django_deletion_record;",
        ),
        migrations.RunSQL(
            """
            CREATE INDEX deletion_obj_idx ON django_deletion_record (object_id, table_name);
            """,
            reverse_sql="DROP INDEX IF EXISTS deletion_obj_idx;",
        ),
        migrations.RunSQL(
            """
            CREATE FUNCTION deletion_record_insert() RETURNS trigger
                LANGUAGE plpgsql
            AS
            $$
            BEGIN
                EXECUTE 'INSERT INTO django_deletion_record (object_id, table_name, data) VALUES ($1, $2, $3)'
                    USING OLD.id, TG_TABLE_NAME, to_jsonb(OLD.*);
                RETURN OLD;
            END;
            $$;
            """,
            reverse_sql="DROP FUNCTION IF EXISTS deletion_record_insert CASCADE;",
        ),
    ]