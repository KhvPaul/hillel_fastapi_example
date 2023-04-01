from sqladmin import ModelView

from db.models.models_base import Category, Customer, Manufacturer, Order, Product, Seller


class CustomerAdminView(ModelView, model=Customer):
    column_list = (
        Customer.sub,
        Customer.email,
        Customer.first_name,
        Customer.last_name,
        Customer.birthday,
        Customer.phone_number,
    )


class SellerAdminView(ModelView, model=Seller):
    column_list = (Seller.sub, Seller.email, Seller.first_name, Seller.last_name, Seller.birthday, Seller.phone_number)


class ManufacturerAdminView(ModelView, model=Manufacturer):
    column_list = (
        Manufacturer.pk,
        Manufacturer.email,
        Manufacturer.name,
        Manufacturer.country,
        Manufacturer.phone_number,
        Manufacturer.mailing_address,
    )


class ProductAdminView(ModelView, model=Product):
    column_list = (Product.pk, Product.name, Product.price, Product.available_count, Product.categories)


class CategoryAdminView(ModelView, model=Category):
    name_plural = "Categories"
    column_list = (Category.pk, Category.name)


class OrderAdminView(ModelView, model=Order):
    column_list = (Order.pk, Order.customer_sub, Order.total_price, Order.created_at)


export_views = (
    CustomerAdminView,
    SellerAdminView,
    ManufacturerAdminView,
    ProductAdminView,
    CategoryAdminView,
    OrderAdminView,
)
