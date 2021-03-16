from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib import messages
from .apiviews import send_sms

import string, json, random

from .models import *
from Xpos.models import Item as XPOSItem
from ModuleTask.views import UserCustomNav

#from product.models import Item as XPOSItem

def randomStringGenerator():
	name = "I"
	name = name + str(random.randint(100, 999))
	letters = string.ascii_uppercase
	name = name + ''.join(random.choice(letters) for i in range(2))
	name = name + str(random.randint(10, 99))
	name = name + ''.join(random.choice(letters) for i in range(2))
	name = name + str(random.randint(100, 999))
	name = name + "."
	return name

def ChangeFileName(filename):
	extension = filename.split(".")[1]
	changed_file_name = randomStringGenerator()
	return "%s%s" % (changed_file_name, extension)

# Create your views here.
def ItemManagement(request):
	# send_sms('01828127309', 'see message')
	itemq = request.GET.get('item')
	if itemq:
		ecomitems = eComItem.objects.filter(display_name__icontains=itemq)
	else:
		ecomitems = eComItem.objects.all().order_by('id')
	
	paginator = Paginator(ecomitems, 10)
	page = request.GET.get('page')
	pag_item = paginator.get_page(page)
	context = {
		'items': pag_item,
		'cnav': UserCustomNav(request)
		#'privilege': DetailPermissions(request, 'Supplier Management')
	}
	return render(request, 'ECommerce/eComItemManagement.html', context)

@login_required
def ItemCreate(request):
	if request.method == 'POST':

		# form-body, so request.POST.get is applicable
		r = request.POST
		print(r)
		display_name = r.get('display_name')
		# thumbnail = r.get('thumbnail')
		base_price = r.get('base_price')
		offer_id = r.get('offer_id')
		offer_price = float(r.get('offer_price'))
		offer_stock = (r.get('offer_stock'))
		category_id = int(r.get('cateogory_id'))
		xpos_item_id = int(r.get('xpos_item_id'))

		short_description = r.get('short_description')
		long_description = r.get('long_description')
		safety_stock = int(r.get('safety_stock'))
		re_order_stock = int(r.get('re_order_stock'))
		max_sale_stock = int(r.get('max_sale_stock'))
		brand_id = r.get('brand_id')
		thumbnail = ''
		
		if offer_id != '':
			offer = Offer.objects.get(id=int(offer_id))
			offer_start_date = offer.start_date
			offer_end_date = offer.end_date
			offer_stock = int(offer_stock)
		else:
			offer = None
			offer_start_date = None
			offer_end_date = None
			offer_stock = 0
			offer_price = 0

		if display_name == "" or base_price == "" :
			messages.warning(request, f'Please fill up all required fields')
			return redirect('ECom-ItemCreate')
		elif eComItem.objects.filter(display_name__iexact=display_name).exists() :
			messages.warning(request, f'Another Item already has the same name: {display_name}')
			return redirect('ECom-ItemCreate')
		elif eComItem.objects.filter(item_id=xpos_item_id).exists():
			messages.warning(request, f'Item already exists.')
			return redirect('ECom-ItemCreate')
		
		try:
			ecomitem = eComItem(display_name=display_name, thumbnail=thumbnail, \
			base_price=base_price, offer_price=offer_price, offer_start_date=offer_start_date,\
			offer_end_date=offer_end_date, offer_stock=offer_stock, category_id=category_id,
			item_id=xpos_item_id, offer=offer)

			print(ecomitem)

			if brand_id != '':
				brand_id = int(brand_id)
			else:
				brand_id = None
			
			#ecomitem.save()
			print(ecomitem.id)

			ecomitemmeta = eComItemMeta(item_id=ecomitem.id, brand_id=brand_id, safety_stock=safety_stock,\
			re_order_stock=re_order_stock, max_sale_stock=max_sale_stock, \
			short_description=short_description, long_description=long_description)

			print(ecomitemmeta)
			
			#ecomitemmeta.save()
			file_url = []
			for filename, file in request.FILES.items():
				myfile = request.FILES[filename]
				
				if filename == 'thumbnail': # html form get name
					fs = FileSystemStorage(
						location = settings.FS_ECOM_ITEM_THUMBNAIL_UPLOADS,
						base_url= settings.FS_ECOM_ITEM_THUMBNAIL_URL
					)
					myfile.name = ChangeFileName(myfile.name)
					filename=fs.save(myfile.name, file)
					thumbnail=fs.url(filename)
				else:
					fs = FileSystemStorage(
						location = settings.FS_ECOM_ITEM_IMAGE_UPLOADS,
						base_url= settings.FS_ECOM_ITEM_IMAGE_URL
					)
					myfile.name = ChangeFileName(myfile.name)
					filename=fs.save(myfile.name, file)
					file_url.append(fs.url(filename))
			
			if thumbnail != '':
				ecomitem.thumbnail = thumbnail
				#ecomitem.save()

			for fileurl in file_url:
				ecomimg = eComItemImage(item=ecomitem, image=fileurl)
				#ecomimg.save()

			messages.success(request, f'Item added successfully')
		except:
			print("except")
		return redirect('ECom-ItemManagement')
	else:
		context = {
			'categories': eComCategory.objects.all(),
			'xpos_items': XPOSItem.objects.all(),
			'offers': Offer.objects.all(),
			'cnav': UserCustomNav(request),
			'brands': Brand.objects.all()
		}
		return render(request, 'ECommerce/eComItemCreate.html', context)


def ItemView(request, id):
	ecomitem = get_object_or_404(eComItem, id=id)
	#print(ecomitem.thumbnail)#.url
	print("----/////////")
	
	images = [img.image for img in ecomitem.ecomitemimage_set.get_queryset()]
	print(images)
	context = {
		'eComItem': ecomitem,
		'item_images': images
		#'cnav': UserCustomNav(request)
	}
	print(settings.MEDIA_ROOT+"----------------------------")
	return render(request, 'ECommerce/eComItemView.html', context)
	# return HttpResponse('<h1>ItemView works!</h1>')


def ItemEdit(request, id):
	if request.method == 'POST':
		r = request.POST
		print(r)
		display_name = r.get('display_name')
		# thumbnail = r.get('thumbnail')
		base_price = r.get('base_price')
		offer_id = r.get('offer_id')
		offer_price = float(r.get('offer_price'))
		offer_stock = (r.get('offer_stock'))
		category_id = int(r.get('cateogory_id'))

		short_description = r.get('short_description')
		long_description = r.get('long_description')
		safety_stock = r.get('safety_stock')
		re_order_stock = r.get('re_order_stock')
		max_sale_stock = r.get('max_sale_stock')
		brand_id = r.get('brand_id')
		thumbnail = ''
		
		if safety_stock == '':
			safety_stock == 0
		if re_order_stock == '':
			re_order_stock == 0
		if max_sale_stock == '':
			max_sale_stock == 0
		if offer_id != '':
			offer = Offer.objects.get(id=int(offer_id))
			offer_start_date = offer.start_date
			offer_end_date = offer.end_date
			offer_stock = int(offer_stock)
		else:
			offer = None
			offer_start_date = None
			offer_end_date = None
			offer_stock = 0
			offer_price = 0

		if display_name == "" or base_price == "" :
			messages.warning(request, f'Please fill up all required fields')
			return redirect('ECom-ItemEdit')
		
		try:
			# ecomitem = eComItem(display_name=display_name, thumbnail=thumbnail, \
			# base_price=base_price, offer_price=offer_price, offer_start_date=offer_start_date,\
			# offer_end_date=offer_end_date, offer_stock=offer_stock, category_id=category_id,
			# item_id=xpos_item_id, offer=offer)

			ecomitem = eComItem.objects.get(id=id)
			ecomitem.display_name = display_name
			ecomitem.base_price = base_price
			ecomitem.offer_price = offer_price
			ecomitem.offer_start_date = offer_start_date
			ecomitem.offer_end_date = offer_end_date
			ecomitem.offer_stock = offer_stock
			ecomitem.category_id = category_id
			ecomitem.offer = offer

			print(ecomitem)
			ecomitem.save()
			print(ecomitem)

			if brand_id != '':
				brand_id = int(brand_id)
			else:
				brand_id = None
			
			#ecomitem.save()
			print(ecomitem.id)

			# ecomitemmeta = eComItemMeta(item_id=ecomitem.id, brand_id=brand_id, safety_stock=safety_stock,\
			# re_order_stock=re_order_stock, max_sale_stock=max_sale_stock, \
			# short_description=short_description, long_description=long_description)

			if eComItemMeta.objects.filter(item_id = ecomitem.id).exists():
				ecomitemmeta = ecomitem.ecomitemmeta
			else:
				ecomitemmeta = eComItemMeta(item_id = ecomitem.id)

			ecomitemmeta.brand_id = brand_id
			ecomitemmeta.safety_stock = safety_stock
			ecomitemmeta.re_order_stock = re_order_stock
			ecomitemmeta.max_sale_stock = max_sale_stock
			ecomitemmeta.short_description = short_description
			ecomitemmeta.long_description = long_description

			ecomitemmeta.save()

			# print(ecomitemmeta)
			
			file_url = []
			for filename, file in request.FILES.items():
				myfile = request.FILES[filename]
				
				if filename == 'thumbnail': # html form get name
					fs = FileSystemStorage(
						location = settings.FS_ECOM_ITEM_THUMBNAIL_UPLOADS,
						base_url= settings.FS_ECOM_ITEM_THUMBNAIL_URL
					)
					myfile.name = ChangeFileName(myfile.name)
					filename=fs.save(myfile.name, file)
					thumbnail=fs.url(filename)
				else:
					fs = FileSystemStorage(
						location = settings.FS_ECOM_ITEM_IMAGE_UPLOADS,
						base_url= settings.FS_ECOM_ITEM_IMAGE_URL
					)
					myfile.name = ChangeFileName(myfile.name)
					filename=fs.save(myfile.name, file)
					file_url.append(fs.url(filename))
			
			if thumbnail != '':
				ecomitem.thumbnail = thumbnail
				ecomitem.save()

			for fileurl in file_url:
				ecomimg = eComItemImage(item=ecomitem, image=fileurl)
				ecomimg.save()

			messages.success(request, f'Item edited successfully')
		except:
			print("except")
		return redirect('ECom-ItemManagement')
	else:
		item = get_object_or_404(eComItem, id=id)
		print(item.display_name)
		context = {
			'categories': eComCategory.objects.all(),
			'eComItem': item,
			'cnav': UserCustomNav(request),
			'images': list(eComItemImage.objects.filter(item_id=id)),
			'offers': Offer.objects.all(),
			'brands': Brand.objects.all()
		}
		return render(request, 'ECommerce/eComItemEdit.html', context)

def ItemDelete(request):
	return HttpResponse('<h1>ItemDelete works!</h1>')

@login_required
def HomeGroupCreate(request):
	if request.method == 'POST':

		# form-body, so request.POST.get is applicable
		r = request.POST
		print(r)
		name = r.get('name')
		ordering = r.get('ordering')

		if HomeGroup.objects.filter(group_order=ordering).exists():
			messages.warning(request, f'Another Home Group exists at {ordering} already.')
			return redirect('ECom-HomeGroupCreate')
		if HomeGroup.objects.filter(group_name=name).exists():
			messages.warning(request, f'Home Group {name} exists.')
			return redirect('ECom-HomeGroupCreate')

		homegroup = HomeGroup(group_name=name, group_order=ordering)
		homegroup.save()

		messages.success(request, f'Home Group added successfully')
		return redirect('ECom-HomeGroupManagement')
	else:
		context = {
			'cnav': UserCustomNav(request)
		}
		return render(request, 'ECommerce/HomeGroupCreate.html', context)

def HomeItemManagement(request):
	
	homeitem = request.GET.get('home_item')
	if homeitem:
		homeitems = HomeItem.objects.filter(item_display_name__icontains=homeitem)
	else:
		homeitems = HomeItem.objects.all()#.order_by('group_id')
	
	paginator = Paginator(homeitems, 10)
	page = request.GET.get('page')
	pag_item = paginator.get_page(page)
	context = {
		'items': pag_item,
		'cnav': UserCustomNav(request)
		#'privilege': DetailPermissions(request, 'Supplier Management')
	}
	return render(request, 'ECommerce/HomeItemManagement.html', context)

@login_required
def HomeItemCreate(request):
	if request.method == 'POST':

		# form-body, so request.POST.get is applicable
		r = request.POST
		print(r)
		ecom_item_id = r.get('item_id')
		home_group_id = r.get('home_group_id')

		if HomeItem.objects.filter(item_id=ecom_item_id, group_id=home_group_id).exists():
			messages.warning(request, f'Another Home Item with same name exists already in same group.')
			return redirect('ECom-HomeItemCreate')
		
		homeitem = HomeItem(item_id=ecom_item_id, group_id=home_group_id)
		homeitem.save()

		messages.success(request, f'Home Item added successfully')
		return redirect('ECom-HomeItemManagement')
	else:
		context = {
			'cnav': UserCustomNav(request),
			'items': eComItem.objects.all(),
			'homegroups': HomeGroup.objects.all()
		}
		return render(request, 'ECommerce/HomeItemCreate.html', context)

def HomeItemEdit(request, id):
	if request.method == 'POST':
		r = request.POST
		print(r)
		ecom_item_id = r.get('item_id')
		home_group_id = r.get('home_group_id')
		is_archived = r.get('show')
		if is_archived == "show":
			is_archived = False
		else:
			is_archived = True
		

		# if HomeItem.objects.filter(item_id=ecom_item_id, group_id=home_group_id).exists():
		# 	messages.warning(request, f'Another Home Item with same name exists already in same group.')
		# 	return redirect('ECom-HomeItemCreate')
		
		homeitem = HomeItem.objects.get(id=id)
		homeitem.item_id = ecom_item_id
		homeitem.is_archived = is_archived
		homeitem.group_id = home_group_id
		homeitem.save()

		messages.success(request, f'Home Item edited successfully')
		return redirect('ECom-HomeItemManagement')
	elif request.method == 'GET':
		homeitem = get_object_or_404(HomeItem, id=id)
		context = {
			'ecomitems': eComItem.objects.all(),
			'cnav': UserCustomNav(request),
			'homegroups': HomeGroup.objects.all(),
			'homeitem': homeitem
		}
		return render(request, 'ECommerce/HomeItemEdit.html', context)