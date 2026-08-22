"""rename table products to goods

Revision ID: 964ee737ed17
Revises: 24780ec7f9ff
Create Date: 2026-08-15 08:06:36.129884

"""

from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "964ee737ed17"
down_revision: str | Sequence[str] | None = "24780ec7f9ff"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.rename_table("products", "goods")

    op.execute("ALTER INDEX products_pkey RENAME TO goods_pkey")

    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_sku_id_fkey TO goods_sku_id_fkey")

    op.execute("ALTER INDEX ix_products_sku_id RENAME TO ix_goods_sku_id")

    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_created_at_not_null TO goods_created_at_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_id_not_null TO goods_id_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_reserved_state_not_null TO goods_reserved_state_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_sku_id_not_null TO goods_sku_id_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_stock_not_null TO goods_stock_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT products_updated_at_not_null TO goods_updated_at_not_null")

    op.alter_column(
        "tasks",
        "product_id",
        new_column_name="good_id",
    )

    op.execute("ALTER TABLE tasks RENAME CONSTRAINT tasks_product_id_fkey TO tasks_good_id_fkey")

    op.execute("ALTER INDEX ix_tasks_product_id RENAME TO ix_tasks_good_id")


def downgrade() -> None:
    """Downgrade schema."""
    op.execute("ALTER INDEX ix_tasks_good_id RENAME TO ix_tasks_product_id")

    op.execute("ALTER TABLE tasks RENAME CONSTRAINT tasks_good_id_fkey TO tasks_product_id_fkey")

    op.alter_column(
        "tasks",
        "good_id",
        new_column_name="product_id",
    )

    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_updated_at_not_null TO products_updated_at_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_stock_not_null TO products_stock_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_sku_id_not_null TO products_sku_id_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_reserved_state_not_null TO products_reserved_state_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_id_not_null TO products_id_not_null")
    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_created_at_not_null TO products_created_at_not_null")

    op.execute("ALTER INDEX ix_goods_sku_id RENAME TO ix_products_sku_id")

    op.execute("ALTER TABLE goods RENAME CONSTRAINT goods_sku_id_fkey TO products_sku_id_fkey")

    op.execute("ALTER INDEX goods_pkey RENAME TO products_pkey")

    op.rename_table("goods", "products")
