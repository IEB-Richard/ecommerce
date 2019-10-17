from django.http import Http404
from django.views.generic import ListView, DetailView
from django.shortcuts import render, get_object_or_404

from .models import Product
# Create your views here.


class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductListView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context


def product_list_view(request):
    queryset = Product.objects.all()
    context = {
        'object_list': queryset
    }
    return render(request, "products/list.html", context)


class ProductDetailView(DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(
            *args, **kwargs)
        print(context)
        return context


def product_detail_view(request, pk=None):
    # Solution 01: get directly, if it cannot find record, then it will be an system fault.
    # instance = Product.objects.get(pk=pk)

    # Solution 02:
    # instance = get_object_or_404(Product, id=pk)

    # Solution 03: with a try catch block
    # try:
    #     instance = Product.objects.get(pk=pk)
    # except Product.DoesNotExist:
    #     print('no product here')
    #     raise Http404('Product does not exist')    
    # except:
    #     print('huh?')

    # Solution 04: with filter and return the value
    qs = Product.objects.filter(pk=pk)
    print(qs)
    if qs.exists() and qs.count() == 1:
        instance = qs.first()
    else:
        raise Http404("Product doesn't exist")

    context = {
        'object': instance
    }
    return render(request, "products/detail.html", context)
