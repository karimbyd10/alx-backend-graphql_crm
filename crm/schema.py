import graphene
from graphene_django import DjangoObjectType
from crm.models import Product

# GraphQL type for Product
class ProductType(DjangoObjectType):
    class Meta:
        model = Product
        fields = ("id", "name", "stock")


class UpdateLowStockProducts(graphene.Mutation):
    class Arguments:
        # no arguments needed
        pass

    updated_products = graphene.List(ProductType)
    success_message = graphene.String()

    def mutate(self, info):
        low_stock_products = Product.objects.filter(stock__lt=10)
        updated_list = []

        for product in low_stock_products:
            product.stock += 10  # simulate restocking
            product.save()
            updated_list.append(product)

        message = f"{len(updated_list)} products updated successfully."
        return UpdateLowStockProducts(updated_products=updated_list, success_message=message)


class Mutation(graphene.ObjectType):
    update_low_stock_products = UpdateLowStockProducts.Field()
