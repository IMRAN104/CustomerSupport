from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from django.core import serializers
from django.contrib import messages

from .models import eComItem, eComCategory
#from product.models import Item as XPOSItem

@login_required
@view_permission_required
def eComItemManagement(request):
    ecomitems = eComItem.objects.all().order_by('-id')
    # supq = request.GET.get('sup')
    # cnoq = request.GET.get('cno')
    # if supq:
    #     suppliers = suppliers.filter(name__icontains=supq)
    # if cnoq:
    #     suppliers = suppliers.filter(mobile_no__contains=cnoq)
    #paginator = Paginator(suppliers, 10)
    #page = request.GET.get('page')
    #pag_sup = paginator.get_page(page)
    context = {
        'suppliers': pag_sup,
        'cnav': UserCustomNav(request),
        'privilege': DetailPermissions(request, 'Supplier Management')
    }
    return render(request, 'Supplier/SupplierManagement.html', context)

@login_required
#@view_permission_required
def eComItemView(request, id):
    ecomitem = get_object_or_404(eComItem, id=id)
    
    context = {
        'eComItem': ecomitem
    }
    return render(request, 'ecom/eComItemView.html', context)


@login_required
def eComItemCreate(request):
    if request.method == 'POST':
        r = request.POST
        display_name = r.get('display_name')
        thumbnail = r.get('thumbnail')
        base_price = r.get('base_price')
        offer_price = r.get('offer_price')
        offer_start_date = r.get('offer_start_date')
        offer_end_date = r.get('offer_end_date')
        offer_stock = r.get('offer_stock')
        category_id = int(r.get('cateogory_id'))
        xpos_item_id = int(r.get('xpos_item_id'))

        print(display_name == "as")
        print(thumbnail == "")
        print(offer_price == "0")
        print(offer_start_date == "")
        print(offer_stock == "")
        print(category_id)

        # if display_name == "" or city == "" or base_price == "" or country == "" or sup_mobile == "" :
        #     messages.warning(request, f'Please fill up all required fields')
        #     return redirect('SupplierCreate')
        # if eComItem.objects.filter(name__iexact=display_name).exists() :
        #     messages.warning(request, f'Item Display Name {display_name} already exists.')
        #     return redirect('SupplierCreate')
        # if Item.objects.filter(id=xpos_item_id).exists():
        #     messages.warning(request, f'Item {xpos_item_id} already exists.')
        #     return redirect('SupplierCreate')
        # if sup_email != '':
        #     if (eComCategory.objects.filter(id=category_id).exists()) == False:
        #         messages.warning(request, f'Category {category_id} does not exist.')
        #         return redirect('SupplierCreate')
        
        #supplier = Supplier(name=sup_name, apartment=aprtmnt, street_address=street, city=city, state=state,
        #                    postal_code=pcode, country=country, mobile_no=sup_mobile, email_address=sup_email, customer=customer.id)
        #supplier.save()

        # ecomitem = eComItem(display_name=display_name, thumbnail=thumbnail, \
        # base_price=base_price, offer_price=offer_price, offer_start_date=offer_start_date,\
        # offer_end_date=offer_end_date, offer_stock=offer_stock, category=cat,
        # item=xpositem)

        ecomitem = eComItem(display_name=display_name, \
        base_price=float(base_price),  category_id=category_id,
        item_id=xpos_item_id)

        ecomitem.save()
        
    #     return render(request, 'ecom/eComItemView.html', {
    #     'eComItem': ecomitem
    # })
        return render(request, 'ecom/eComItemCreate.html')
    else:
        return render(request, 'ecom/eComItemCreate.html')
