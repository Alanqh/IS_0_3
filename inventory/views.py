from django.core.checks import messages
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from register.models import Message
from .models import ProductList, InventoryProducts, PurchaseOrder, InventoryChange
from .forms import PurchaseForm


def inventory_home(request):
    return render(request, 'inventory_home.html')


def purchase_product(request):
    if request.method == 'POST':
        form = PurchaseForm(request.POST)
        if form.is_valid():
            product = form.cleaned_data['product']
            quantity = form.cleaned_data['quantity']
            if quantity <= 0:
                messages.error(request, '购买数量必须大于0')
                return redirect('purchase')

            # 创建新的采购订单
            purchase_order = PurchaseOrder.objects.create(
                product=product,
                quantity=quantity
            )

            # 更新库存产品表中对应产品的数量
            inventory_product, created = InventoryProducts.objects.get_or_create(
                product=product
            )
            inventory_product.quantity += quantity
            inventory_product.save()

            # 更新库存变化表
            inventory_change = InventoryChange.objects.create(
                product=product,
                change_amount=quantity,
                description=f"采购了 {quantity} 件 {product.name}"
            )

            messages.success(request, '采购成功')
            return redirect('purchase_success')
    else:
        form = PurchaseForm()

    products = ProductList.objects.all()
    context = {'form': form, 'products': products}
    return render(request, 'purchase_product.html', context)


def purchase_success(request):
    return render(request, 'purchase_success.html')


def inventory_list(request):
    categories = {'engine': '发动机', 'battery': '电池', 'tire': '轮胎', 'charging pile': '充电桩',
                  'parts': '其他小配件'}
    inventory_by_category = {}

    for category_en, category_cn in categories.items():
        products = InventoryProducts.objects.filter(product__category=category_en)
        product_list = ProductList.objects.filter(category=category_en)

        inventory_by_category[category_cn] = {
            'products': products,
            'other_info': product_list
        }

    return render(request, 'inventory_list.html', {'inventory_by_category': inventory_by_category})


def inventory_change_list(request):
    inventory_changes = InventoryChange.objects.all().order_by('-timestamp')
    return render(request, 'inventory_change_list.html', {'inventory_changes': inventory_changes})


def in_view_messages(request):
    user = request.user
    unread_messages = user.received_messages.filter(is_read=0, recipient=user).order_by('-timestamp')
    return render(request, 'in_view_messages.html',
                  {'unread_messages': unread_messages})


def in_mark_as_read(request, message_id):
    user = request.user
    message = get_object_or_404(Message, id=message_id, recipient=user)
    message.mark_as_read()
    return redirect('in_view_messages')